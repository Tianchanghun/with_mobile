import json
import time
import datetime
import uuid
import hmac
import hashlib
import requests

from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField



class company_info(models.Model):
    company_class_type={('1', '1'), ('2','2'), ('3','3')}
    classify_option_type = {('헤드', '헤드'), ('매입처', '매입처'), ('매출처', '매출처')}
    area_1_type = {('강원', '강원'), ('경기', '경기'), ('경북', '경북'), ('경남', '경남'), ('광주', '광주'), ('대구', '대구'), ('대전', '대전'), ('부산', '부산'), ('서울', '서울'), ('세종', '세종'), ('울산', '울산'), ('인천', '인천'), ('전남', '전남'), ('전북', '전북'), ('제주', '제주'), ('충남', '충남'), ('충북', '충북')}

    use = models.BooleanField(default=False,verbose_name="사용여부") # 사용여부
    company_class= models.CharField(max_length=30, choices=company_class_type,verbose_name="업체등급") #업체등급
    classify_option= models.CharField(max_length=30, choices=classify_option_type,verbose_name="분류선택") #분류선택
    company_head=models.CharField(max_length=80,blank=True, null=True,verbose_name="헤드") #헤드
    company_name=models.CharField(max_length=80,verbose_name="업체명") #업체명
    representative=models.CharField(max_length=80,verbose_name="대표자") #대표자
    company_no=models.CharField(max_length=80,verbose_name="사업자번호") #사업자 번호
    business_license=models.FileField(blank=True, null=True,upload_to='business_license/%Y%M%d',verbose_name="사업자 등록증") #사업자 등록증
    address=models.CharField(max_length=80,blank=True, null=True,verbose_name="주소") #주소
    person_in_charge=models.CharField(max_length=20,verbose_name="담당자") #담당자
    contact_phone=models.CharField(max_length=80,blank=True, null=True,verbose_name="연락처") #연락처
    cell_address=models.CharField(max_length=80,verbose_name="핸드폰") #핸드폰
    mail=models.EmailField(max_length=80,blank=True, null=True,verbose_name="이메일") #이메일
    home_page=models.URLField(max_length=80,blank=True, null=True,verbose_name="홈페이지") #홈페이지
    area_1= models.CharField(max_length=30, choices=area_1_type,verbose_name="지역") #지역
    area_2=models.CharField(max_length=80,blank=True, null=True,verbose_name="지역2") #지역2
    area_3=models.CharField(max_length=80,blank=True, null=True,verbose_name="지역3") #지역3
    credit_evaluation= models.BooleanField(default=True,verbose_name="신용평가") #신용평가 유무
    credit_evaluation_end=models.DateField(blank=True, null=True,verbose_name="신용평가만료일") #신용평가 만료일
    certificate_end=models.DateField(blank=True, null=True,verbose_name="공인인증서 만료일") #공인인증서만료일
    creditworthiness=models.CharField(max_length=80,blank=True, null=True,verbose_name="신인도") #신인도
    sort_company=models.CharField(max_length=80,blank=True, null=True,verbose_name="기업분류") #기업분류
    certification=models.CharField(max_length=80,blank=True, null=True,verbose_name="각종인증") #각종인증
    item_of_acquisition=models.CharField(max_length=80,blank=True, null=True,verbose_name="주요취급품목") #주요취급품목
    note=RichTextUploadingField(blank=True, null=True,verbose_name="비고") #비고

    created_date = models.DateTimeField(default=timezone.now,verbose_name="작성일")
    published_date = models.DateTimeField(blank=True, null=True,verbose_name="수정일")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class company_send(models.Model):
    company_class_type={('1', '1'), ('2', '2'), ('3', '3')}
    area_1_type = {('전국', '전국'), ('경기', '경기'), ('경북', '경북'), ('경남', '경남'), ('광주', '광주'), ('대구', '대구'), ('대전', '대전'), ('부산', '부산'), ('서울', '서울'), ('세종', '세종'), ('울산', '울산'), ('인천', '인천'), ('전남', '전남'), ('전북', '전북'), ('제주', '제주'), ('충남', '충남'), ('충북', '충북')}

    use = models.BooleanField(default=False,verbose_name="사용여부") # 사용여부
    company_class= models.CharField(max_length=30, choices=company_class_type,verbose_name="발송등급") #업체등급
    area_1 = models.CharField(max_length=30, choices=area_1_type,verbose_name="지역")  # 지역
    bid_info=models.TextField(max_length=1000,blank=True, null=True,verbose_name="발송자료")
    bid_info_file = models.FileField(blank=True, null=True, upload_to='bid_info_file/%Y%M%d')  # 사업자 등록증

    created_date = models.DateTimeField(default=timezone.now,verbose_name="작성일")
    published_date = models.DateTimeField(blank=True, null=True,verbose_name="수정일")

    def publish(self):
        self.published_date = timezone.now()
        self.save()
