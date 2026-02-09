from rest_framework import serializers
from .models import EquipmentHistory
#
# Serializer for EquipmentHistory model
class EquipmentHistorySerializer(serializers.ModelSerializer):
    pdf_download_url = serializers.SerializerMethodField()
    class Meta:
        model = EquipmentHistory
        fields = ['id', 'filename', 'upload_date', 'summary_data', 'pdf_download_url']
    def get_pdf_download_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(f'/api/report/{obj.id}/')