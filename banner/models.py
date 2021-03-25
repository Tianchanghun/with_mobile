from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField

class Mainbanner(models.Model):
    first_label=models.CharField(blank=True, null=True, max_length=50,verbose_name="#1레이블")
    first_copy=models.CharField(blank=True, null=True, max_length=50,verbose_name="#1카피")
    image_1=models.ImageField(upload_to='main_banner/%Y%M%d',verbose_name="#1이미지")
    image_thumbnail_1=ImageSpecField(source='image_1', processors=[ResizeToFill(1903, 400)],format='JPEG')

    second_label=models.CharField(blank=True, null=True, max_length=50,verbose_name="#2레이블")
    second_copy=models.CharField(blank=True, null=True, max_length=50,verbose_name="#2카피")
    image_2 = models.ImageField(upload_to='main_banner/%Y%M%d',verbose_name="#2이미지")
    image_thumbnail_2 = ImageSpecField(source='image_2', processors=[ResizeToFill(1903, 400)], format='JPEG')

    Third_label=models.CharField(blank=True, null=True, max_length=50,verbose_name="#3레이블")
    third_copy=models.CharField(blank=True, null=True, max_length=50,verbose_name="#3카피")
    image_3 = models.ImageField(upload_to='main_banner/%Y%M%d',verbose_name="#3이미지")
    image_thumbnail_3 = ImageSpecField(source='image_3', processors=[ResizeToFill(1903, 400)], format='JPEG')

    created_date = models.DateTimeField(default=timezone.now,verbose_name="작성일")
    published_date = models.DateTimeField(blank=True, null=True,verbose_name="수정일")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class subbanner(models.Model):
    subbanner_select = {('info', 'info'), ('map', 'map'), ('introduction','introduction'),('request','request'),('board','board')}

    subbanner_part = models.CharField(max_length=30, choices=subbanner_select,verbose_name="노출영역")

    label=models.CharField(blank=True, null=True, max_length=50,verbose_name="레이블")
    copy=models.CharField(blank=True, null=True, max_length=50,verbose_name="카피")
    image=models.ImageField(upload_to='sub_banner/%Y%M%d',verbose_name="첨부파일")
    image_thumbnail=ImageSpecField(source='image', processors=[ResizeToFill(1294, 289)],format='JPEG')

    created_date = models.DateTimeField(default=timezone.now,verbose_name="작성일")
    published_date = models.DateTimeField(blank=True, null=True,verbose_name="수정일")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

# Create your models here.
