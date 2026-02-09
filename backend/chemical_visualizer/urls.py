from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import EquipmentUpload, PDFDownload, Register, CSVDownload

urlpatterns = [
    # Standard Admin Interface provided by Django
    path('admin/', admin.site.urls),
    # Endpoint for User Registration
    path('api/register/', Register.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint for uploading the equipment data (CSV files)
    path('api/equipment/', EquipmentUpload.as_view(), name='equipment-upload'),
    path('api/report/<int:pk>/', PDFDownload.as_view(), name='pdf-download'),
    path('api/csv/<int:id>/', CSVDownload.as_view(), name='csv-download'),
    # Endpoint for fetching the user upload history and the processed data:
    
]