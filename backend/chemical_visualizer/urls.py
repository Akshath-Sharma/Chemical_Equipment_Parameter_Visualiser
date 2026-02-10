from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import EquipmentUpload, PDFDownload, Register, CSVDownload

urlpatterns = [
    # Standard Admin Interface provided by Django
    path('admin/', admin.site.urls),
    # Endpoint for User Registration
    path('register/', Register.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint for uploading the equipment data (CSV files)
    path('equipment/', EquipmentUpload.as_view(), name='equipment-upload'),
    path('report/<int:pk>/', PDFDownload.as_view(), name='pdf-download'),
    path('csv/<int:id>/', CSVDownload.as_view(), name='csv-download'),    
]