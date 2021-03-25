from django.contrib import admin
from .models import api_list
# Register your models here.

class information_api_list(admin.ModelAdmin):
    list_display = ['id', 'api_name', 'start_date', 'end_date']
    list_display_links = ['id', 'api_name', 'start_date', 'end_date']
    ordering = ['-created_date', '-published_date', 'id', 'api_name', 'api_site_name', 'api_code', 'api_site_address','api_site_url', 'api_1_key', 'api_2_key', 'api_3_key','api_4_key', 'api_5_key',  'start_date', 'end_date']
    list_filter = ['id', 'api_name', 'api_site_name', 'api_code', 'api_site_address', 'api_site_url', 'api_1_key','api_2_key', 'api_3_key','api_4_key', 'api_5_key',  'start_date', 'end_date', 'created_date', 'published_date']
    search_fields = ['id', 'api_name', 'api_site_name', 'api_code', 'api_site_address', 'api_site_url', 'api_1_key','api_2_key', 'api_3_key','api_4_key', 'api_5_key',  'start_date', 'end_date', 'created_date', 'published_date']

admin.site.register(api_list, information_api_list)

