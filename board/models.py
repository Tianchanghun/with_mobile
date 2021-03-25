from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class board(models.Model):
    part_select={('notice', '공지사항'), ('news','입찰뉴스')}
    board_title = models.CharField(max_length=100,verbose_name="제목")
    board_part = models.CharField(max_length=30, choices=part_select,verbose_name="게시분류")
    board_picture = models.ImageField(blank=True, null=True,upload_to='board/%Y%M%d',verbose_name="첨부이미지")
    board_picture_thumbnail = ImageSpecField(source='board_picture', processors=[ResizeToFill(1920, 400)], format='JPEG')
    board_text = RichTextUploadingField(blank=True, null=True,verbose_name="내용")
    board_file_1 = models.FileField(blank=True, null=True,upload_to='board/%Y%M%d',verbose_name="첨부파일#1")
    board_file_2 = models.FileField(blank=True, null=True,upload_to='board/%Y%M%d',verbose_name="첨부파일#2")
    board_file_3 = models.FileField(blank=True, null=True,upload_to='board/%Y%M%d',verbose_name="첨부등급3")
    board_use = models.BooleanField(default=False,verbose_name="사용여부")

    created_date = models.DateTimeField(default=timezone.now,verbose_name="작성일")
    published_date = models.DateTimeField(blank=True, null=True,verbose_name="수정일")

    def publish(self):
        self.published_date = timezone.now()
        self.save()