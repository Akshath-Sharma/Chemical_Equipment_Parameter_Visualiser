from django.contrib import admin
from .models import EquipmentHistory
from django.contrib.auth.models import Group

# Unregistera the Group model from Admin since we dont exactly need it 
admin.site.unregister(Group)

@admin.register(EquipmentHistory)
class EquipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('filename', 'upload_date') 
    list_filter = ('upload_date',)
    search_fields = ('filename',)
    admin.site.site_header = "Chemical Visualizer Admin"
    admin.site.site_title = "FOSSEE Dashboard"
    admin.site.index_title = "Welcome to the Equipment Manager"