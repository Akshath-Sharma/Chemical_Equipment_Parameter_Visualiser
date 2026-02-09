from .models import EquipmentHistory
from .serializers import EquipmentHistorySerializer
from .utils import process_equipment_file, generate_pdf_report
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.contrib.auth.models import User


class Register(APIView):
    # AllowAny to let any new user to register.
    permission_classes = [AllowAny] 

    # Method to handle incoming HTTP requests and send responses
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists!'}, status=400)

        User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully!'}, status=201)
 

class EquipmentUpload(APIView):
    # For logged-in users
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        try:
            history = EquipmentHistory.objects.filter(user=request.user)[:5]
            # Allowing the serializer to access request context for pdf url generation
            serializer = EquipmentHistorySerializer(history, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            print(f"Error in GET /equipment/: {e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

    # Method to handle file upload, processing, saving, and enforcing Last 5 only history rule
    def post(self, request, *args, **kwargs):
        try:
            file_object = request.FILES['file']
            print(f"DEBUG: Processing file {file_object.name}")
            results = process_equipment_file(file_object)
            print(f"DEBUG: File processed, saving to history")
            EquipmentHistory.objects.create(
                user=request.user,
                filename=file_object.name,
                summary_data=results,
                file=file_object
            )
            user_files = EquipmentHistory.objects.filter(user=request.user)
            if user_files.count() > 5:
                # Delete the oldest file
                oldest = user_files.last()
                oldest.delete()
            print(f"DEBUG: File upload complete")
            # Return the results to the frontend 
            return Response(results, status=201)
        except Exception as e:
            print(f"Error in POST /equipment/: {e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class PDFDownload(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            print(f"DEBUG: PDF download request for pk={pk}")
            user_history = EquipmentHistory.objects.get(pk=pk, user=request.user)
            print(f"DEBUG: Found history record, generating PDF")
            pdf_buffer = generate_pdf_report(user_history)
            print(f"DEBUG: PDF generated, returning to client")

            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{user_history.filename}.pdf"'
            return response
        except EquipmentHistory.DoesNotExist:
            print(f"DEBUG: History record not found pk={pk}")
            return Response({"error": "File not found or access denied."}, status=404)
        except Exception as e:
            print(f"Error in GET /report/{pk}/: {e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class CSVDownload(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            print(f"DEBUG: CSV download request for id={id}")
            history = EquipmentHistory.objects.get(id=id, user=request.user)
            print(f"DEBUG: Found CSV file {history.filename}")
            
            csv_file = history.file
            csv_file.seek(0)
            file_content = csv_file.read()
            
            response = HttpResponse(file_content, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{history.filename}"'
            return response
        except EquipmentHistory.DoesNotExist:
            print(f"DEBUG: CSV file not found id={id}")
            return Response({"error": "File not found or access denied."}, status=404)
        except Exception as e:
            print(f"Error in GET /csv/{id}/: {e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)