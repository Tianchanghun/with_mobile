from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import company_info
from .models import company_send
import json
import time
import datetime
import uuid
import hmac
import hashlib
import requests

class information_company_info(admin.ModelAdmin):
    list_display = ['id', 'use', 'company_class', 'company_name','person_in_charge','cell_address','area_1', 'created_date']
    list_display_links =['id', 'use', 'company_class', 'company_name','person_in_charge','cell_address','area_1', 'created_date']
    ordering = ['-created_date', '-published_date', 'id', 'use', 'company_class', 'company_name','person_in_charge', 'cell_address']
    list_filter = ['id', 'use', 'company_class', 'company_name','person_in_charge','cell_address','created_date', 'published_date']
    search_fields = ['company_class', 'company_name', 'person_in_charge','cell_address','created_date','certification', 'item_of_acquisition', 'note', 'creditworthiness']
admin.site.register(company_info,information_company_info)



apiKey = 'NCSQTCSYYSYMYHEA'
apiSecret = '5MRXIRBD3KXWXR1JTJPQDDIR7WFIPWQF'

# 아래 값은 필요시 수정
protocol = 'https'
domain = 'api.solapi.com'
prefix = ''

def unique_id():
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(apiKey, apiSecret):
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    return {
        'Authorization': 'HMAC-SHA256 ApiKey=' + apiKey + ', Date=' + date + ', salt=' + salt + ', signature=' +
                         get_signature(apiSecret, data),
        'Content-Type': 'application/json; charset=utf-8'
    }


def getUrl(path):
    url = '%s://%s' % (protocol, domain)
    if prefix != '':
        url = url + prefix
    url = url + path
    return url


def sendMany(data):
    return requests.post(getUrl('/messages/v4/send-many'), headers=get_headers(apiKey, apiSecret), json=data)


class information_company_send(admin.ModelAdmin):
    #물품등록
    def KAKAO_mulpumdeunglog(modeladmin, request, queryset):
        selected = queryset.values_list()

        for send in selected:
            #등급 추출
            company_value=send[2]
            #메세지 추출
            company_message=send[4]
            #작성일 추출
            date=send[6]
            message_date=datetime.datetime.strftime(date,'%Y년%m월%d')
            company_info_data=company_info.objects.filter(company_class=company_value).order_by('-created_date')

            for Company_info_data in company_info_data:
                print(company_value)
                data = {
                    'messages': [
                        # 알림톡 발송
                        {
                            'to': Company_info_data.cell_address,
                            'from': '01073395062',
                            'text': '#{'+Company_info_data.person_in_charge+'}님 #{'+message_date+'} 입찰 정보를 전달 합니다.#{'+company_message+'}',
                            'kakaoOptions': {
                                'pfId': 'KA01PF210324021522934r8Z3O4HcDyr',
                                'templateId': 'KA01TP210324044418025IKNOZCxWiy3',
                                'buttons': [
                                    {
                                        'buttonType': 'MD',  # 상담요청하기 (상담요청하기 버튼을 누르면 메시지 내용이 상담원에게 그대로 전달됩니다.)
                                        'buttonName': '상담요청하기'
                                    }
                                ]
                            }
                        }
                        # ...
                        # 1만건까지 추가 가능
                    ]
                }
                #print(data)
                res = sendMany(data)
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    def KAKAO_Attachments(modeladmin, request, queryset):
        selected = queryset.values_list()

        for send in selected:
            #등급 추출
            company_value=send[2]
            #메세지 추출
            company_message=send[4]
            #작성일 추출
            date=send[6]
            #첨부파일 추출
            company_Attachments = send[5]
            #print(send)
            message_date=datetime.datetime.strftime(date,'%Y년%m월%d')
            company_info_data=company_info.objects.filter(company_class=company_value).order_by('-created_date')

            for Company_info_data in company_info_data:
                #print(company_value)
                data = {
                    'messages': [
                        # 알림톡 발송
                        {
                            'to': Company_info_data.cell_address,
                            'from': '01073395062',
                            'text': '#{'+Company_info_data.person_in_charge+'}님 #{'+message_date+'} 입찰 정보를 전달 합니다.#{'+company_message+'}',
                            'kakaoOptions': {
                                'pfId': 'KA01PF210324021522934r8Z3O4HcDyr',
                                'templateId': 'KA01TP210325015516541kvz5CGeWkvI',
                                'buttons': [
                                    {
                                         'buttonType': 'WL',
                                         'buttonName': '첨부파일',
                                         'linkMo': 'https://info.ipchalmoa.co.kr/'+company_Attachments,
                                         'linkPc': 'https://info.ipchalmoa.co.kr/'+company_Attachments
                                    },
                                    {
                                        'buttonType': 'MD',  # 상담요청하기 (상담요청하기 버튼을 누르면 메시지 내용이 상담원에게 그대로 전달됩니다.)
                                        'buttonName': '상담요청하기'
                                    }
                                ]
                            }
                        }
                        # ...
                        # 1만건까지 추가 가능
                    ]
                }
                #print(data)
                res = sendMany(data)
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    def KAKAO_cancel(modeladmin, request, queryset):
        selected = queryset.values_list()

        for send in selected:
            #등급 추출
            company_value=send[2]
            #메세지 추출
            company_message=send[4]
            #작성일 추출
            date=send[6]
            message_date=datetime.datetime.strftime(date,'%Y년%m월%d')
            company_info_data=company_info.objects.filter(company_class=company_value).order_by('-created_date')

            for Company_info_data in company_info_data:
                print(company_value)
                data = {
                    'messages': [
                        # 알림톡 발송
                        {
                            'to': Company_info_data.cell_address,
                            'from': '01073395062',
                            'text': '#{'+Company_info_data.person_in_charge+'}님 #{'+message_date+'} 투찰 취소 요청 드립니다 죄송합니다.#{'+company_message+'}',
                            'kakaoOptions': {
                                'pfId': 'KA01PF210324021522934r8Z3O4HcDyr',
                                'templateId': 'KA01TP2103250212005445SPKyR9fx27',
                                'buttons': [
                                    {
                                        'buttonType': 'MD',  # 상담요청하기 (상담요청하기 버튼을 누르면 메시지 내용이 상담원에게 그대로 전달됩니다.)
                                        'buttonName': '상담요청하기'
                                    }
                                ]
                            }
                        }
                        # ...
                        # 1만건까지 추가 가능
                    ]
                }
                #print(data)
                res = sendMany(data)
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    def KAKAO_Emergency(modeladmin, request, queryset):
        selected = queryset.values_list()

        for send in selected:
            #등급 추출
            company_value=send[2]
            #메세지 추출
            company_message=send[4]
            #작성일 추출
            date=send[6]
            message_date=datetime.datetime.strftime(date,'%Y년%m월%d')
            company_info_data=company_info.objects.filter(company_class=company_value).order_by('-created_date')

            for Company_info_data in company_info_data:
                print(company_value)
                data = {
                    'messages': [
                        # 알림톡 발송
                        {
                            'to': Company_info_data.cell_address,
                            'from': '01073395062',
                            'text': '#{'+Company_info_data.person_in_charge+'}님 #{'+message_date+'} 긴급 참가신청 및 투찰 요청드립니다 #{'+company_message+'}',
                            'kakaoOptions': {
                                'pfId': 'KA01PF210324021522934r8Z3O4HcDyr',
                                'templateId': 'KA01TP210325021613947ABXyQdN7iAu',
                                'buttons': [
                                    {
                                        'buttonType': 'MD',  # 상담요청하기 (상담요청하기 버튼을 누르면 메시지 내용이 상담원에게 그대로 전달됩니다.)
                                        'buttonName': '상담요청하기'
                                    }
                                ]
                            }
                        }
                        # ...
                        # 1만건까지 추가 가능
                    ]
                }
                #print(data)
                res = sendMany(data)
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    def KAKAO_attend(modeladmin, request, queryset):
        selected = queryset.values_list()

        for send in selected:
            #등급 추출
            company_value=send[2]
            #메세지 추출
            company_message=send[4]
            #작성일 추출
            date=send[6]
            message_date=datetime.datetime.strftime(date,'%Y년%m월%d')
            company_info_data=company_info.objects.filter(company_class=company_value).order_by('-created_date')

            for Company_info_data in company_info_data:
                print(company_value)
                data = {
                    'messages': [
                        # 알림톡 발송
                        {
                            'to': Company_info_data.cell_address,
                            'from': '01073395062',
                            'text': '#{'+Company_info_data.person_in_charge+'}님 #{'+message_date+'} 일단 참가신청만 요청 드립니다. 투찰여부는 추후 말씀드리겠습니다.#{'+company_message+'}',
                            'kakaoOptions': {
                                'pfId': 'KA01PF210324021522934r8Z3O4HcDyr',
                                'templateId': 'KA01TP210325021836504OMw2zbyIVTV',
                                'buttons': [
                                    {
                                        'buttonType': 'MD',  # 상담요청하기 (상담요청하기 버튼을 누르면 메시지 내용이 상담원에게 그대로 전달됩니다.)
                                        'buttonName': '상담요청하기'
                                    }
                                ]
                            }
                        }
                        # ...
                        # 1만건까지 추가 가능
                    ]
                }
                #print(data)
                res = sendMany(data)
                print(json.dumps(res.json(), indent=2, ensure_ascii=False))


    list_display = ['id', 'use', 'company_class','content_size', 'area_1','created_date','published_date']
    list_display_links =['id', 'use', 'company_class', 'content_size', 'area_1', 'created_date', 'published_date']
    ordering = ['-created_date', '-published_date', 'id', 'use', 'company_class', 'area_1']
    list_filter = ['id', 'use', 'company_class', 'area_1', 'created_date', 'published_date']
    search_fields = ['id', 'use', 'company_class', 'area_1', 'bid_info']
    actions = ['KAKAO_mulpumdeunglog', 'KAKAO_Attachments', 'KAKAO_cancel', 'KAKAO_Emergency', 'KAKAO_attend']


    def content_size(self, company_send):
        return mark_safe('<u>{}</u>글자'.format(len(company_send.bid_info)))

    content_size.short_description = '글자수'
    KAKAO_mulpumdeunglog.short_description = '카카오톡 - 물품등록' #KA01TP210324044418025IKNOZCxWiy3
    KAKAO_Attachments.short_description = '카카오톡 - 파일첨부'  # KA01TP210325015516541kvz5CGeWkvI
    KAKAO_cancel.short_description = '카카오톡 - 취소'  # KA01TP2103250212005445SPKyR9fx27
    KAKAO_Emergency.short_description='카카오톡 - 긴급' #KA01TP210325021613947ABXyQdN7iAu
    KAKAO_attend.short_description='카카오톡 - 참가신청' #KA01TP210325021836504OMw2zbyIVTV


admin.site.register(company_send,information_company_send)


# Register your models here.
