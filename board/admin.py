from django.contrib import admin
from .models import board

# Register your models here.
class information_board(admin.ModelAdmin):
    list_display = ['id', 'board_title', 'board_part', 'board_use','created_date','published_date']
    list_display_links =['id', 'board_title', 'board_part', 'board_use','created_date','published_date']
    ordering = ['-created_date', '-published_date', 'id', 'board_title', 'board_part', 'board_picture','board_text','board_file_1','board_file_2','board_file_3','board_use']
    list_filter = ['id', 'board_title', 'board_part', 'board_picture','board_text','board_file_1','board_file_2','board_file_3','board_use','created_date','published_date']
    search_fields = ['id', 'board_title', 'board_part', 'board_picture','board_text','board_file_1','board_file_2','board_file_3','board_use','created_date','published_date']

admin.site.register(board,information_board)