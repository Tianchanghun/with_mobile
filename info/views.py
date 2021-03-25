from API.models import api_list
from board.models import board
from banner.models import Mainbanner,subbanner
from django.shortcuts import render,redirect
import json, sys, requests

import os.path
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
from django.http.response import HttpResponseRedirect

def oauth(request):
    check=False
    context = {'check': check}
    if request.session.get('client_id'):
        code=request.GET['code']
        client_id=request.session.get('client_id')
        redirect_uri=request.session.get('redirect_uri')
        api = api_list.objects.filter(api_name='kakao_login').order_by('-created_date')[:1]
        for api_ in api:
            api_api_1_key = api_.api_1_key
            api_api_2_key = api_.api_2_key

        access_token_request_uri=api_api_1_key
        access_token_request_uri +="client_id=" + client_id
        access_token_request_uri +="&redirect_uri=" + redirect_uri
        access_token_request_uri +="&code=" + code

        access_token_request_uri_data=requests.get(access_token_request_uri)
        json_data=access_token_request_uri_data.json()
        access_token=json_data['access_token']
        request.session['access_token'] =access_token
        context['check'] = True

        user_profile_info_uri = api_api_2_key
        user_profile_info_uri += str(access_token)

        user_profile_info_uri_data = requests.get(user_profile_info_uri)
        user_json_data = user_profile_info_uri_data.json()
        nickName = user_json_data['nickName']

        request.session['nickName']=nickName
        profileImageURL = user_json_data['profileImageURL']
        thumbnailURL = user_json_data['thumbnailURL']

        request.session['nickName'] = nickName
        request.session['thumbnailURL']=thumbnailURL
        request.session['check']=check

        mainbanner = Mainbanner.objects.order_by('-created_date')[:1]
        Subbanner = subbanner.objects.filter(subbanner_part='info').order_by('-created_date')[:1]
        Notice = board.objects.filter(board_use=True, board_part='notice').order_by('-created_date')[:3]
        news = board.objects.filter(board_use=True, board_part='news').order_by('-created_date')[:3]

        context = {'mainbanner':mainbanner,'Subbanner':Subbanner,'Notice':Notice,'News':news,'access_token': access_token}

    return render(request, 'info/main.html', context)


def info(request):
    api=api_list.objects.filter(api_name='kakao_login').order_by('-created_date')[:1]
    for api_ in api:
        api_site_address = api_.api_site_address
        api_code = api_.api_code
        api_site_url = api_.api_site_url

    login_request_uri = api_site_address
    client_id = api_code
    redirect_uri = api_site_url

    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'
    request.session['client_id']=client_id
    request.session['redirect_uri']=redirect_uri
    return redirect(login_request_uri)


def logout(request):
    mainbanner = Mainbanner.objects.order_by('-created_date')[:1]
    Subbanner = subbanner.objects.filter(subbanner_part='info').order_by('-created_date')[:1]
    Notice = board.objects.filter(board_use=True, board_part='notice').order_by('-created_date')[:3]
    news = board.objects.filter(board_use=True, board_part='news').order_by('-created_date')[:3]

    if request.session.get('client_id'):
        if request.session.get('access_token'):
            api = api_list.objects.filter(api_name='kakao_login').order_by('-created_date')[:1]
            for api_ in api:
                api_api_3_key = api_.api_3_key
            access_token=request.session['access_token']
            logout_request_uri=api_api_3_key
            logout_header={'Authorization': f'bearer {access_token}'}

            logout_res=requests.post(logout_request_uri, headers=logout_header)
            logout_result=logout_res.json()

            check=True

            context={'mainbanner':mainbanner,'Subbanner':Subbanner,'Notice':Notice,'News':news}
            if logout_result.get('id'):
                context['check'] = True
                del request.session['client_id']
                del request.session['redirect_uri']

                del request.session['nickName']
                del request.session['thumbnailURL']
                request.session['check']=True
                return render(request, 'info/main.html', context)
            else:
                check = True
                context['check'] = True
                del request.session['nickName']
                del request.session['thumbnailURL']
                request.session['check']=True
                #del request.session['access_token']

                del request.session['client_id']
                del request.session['redirect_uri']
                context={'mainbanner':mainbanner,'Subbanner':Subbanner,'Notice':Notice,'News':news}
                return render(request, 'info/main.html', context)
        else:
            check = False
            context={'mainbanner':mainbanner,'Subbanner':Subbanner,'Notice':Notice,'News':news}
            return render(request, 'info/main.html', context)
    else:
        return info(request)

def main(request):
    mainbanner=Mainbanner.objects.order_by('-created_date')[:1]
    Subbanner = subbanner.objects.filter(subbanner_part='info').order_by('-created_date')[:1]
    Notice = board.objects.filter(board_use=True, board_part='notice').order_by('-created_date')[:3]
    news = board.objects.filter(board_use=True, board_part='news').order_by('-created_date')[:3]

    if request.session.get('check'):
        request.session['check'] = False
    else:
        request.session['check'] = True

    context={'mainbanner':mainbanner,'Subbanner':Subbanner, 'Notice':Notice, 'News':news}
    return render(request, 'info/main.html',context)


