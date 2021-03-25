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

# Create your views here.
def notice(request):
    mainbanner = Mainbanner.objects.order_by('-created_date')[:1]
    Subbanner = subbanner.objects.filter(subbanner_part='board').order_by('-created_date')[:1]

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    #board_list = board.objects.order_by('-create_date')
    Board = board.objects.filter(board_use=True,board_part='notice').order_by('-created_date')
    if kw:
        Board = Board.filter(
            Q(board_title__icontains=kw) |  # 제목검색
            Q(board_text__icontains=kw)   # 내용검색
        ).distinct()
    paginator = Paginator(Board, 10)
    page_obj = paginator.get_page(page)
    access_token = request.session['access_token']
    if request.session.get('check'):
        check = request.session.get('check')
    else:
        check = True

    nickName = request.session.get('nickName')
    thumbnailURL = request.session.get('thumbnailURL')

    context={'mainbanner':mainbanner,'Subbanner':Subbanner,'Board':page_obj,'page': page, 'kw': kw,'nickName':nickName,'thumbnailURL':thumbnailURL,'check':check,'access_token':access_token}
    return render(request, 'board/notice.html', context)


def news(request):
    mainbanner = Mainbanner.objects.order_by('-created_date')[:1]
    Subbanner = subbanner.objects.filter(subbanner_part='board').order_by('-created_date')[:1]

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    #board_list = board.objects.order_by('-create_date')
    Board = board.objects.filter(board_use=True,board_part='news').order_by('-created_date')
    if kw:
        Board = Board.filter(
            Q(board_title__icontains=kw) |  # 제목검색
            Q(board_text__icontains=kw)   # 내용검색
        ).distinct()
    paginator = Paginator(Board, 10)
    page_obj = paginator.get_page(page)


    access_token = request.session['access_token']
    if request.session.get('check'):
        check = request.session.get('check')
    else:
        check=True

    nickName=request.session.get('nickName')
    thumbnailURL = request.session.get('thumbnailURL')

    context={'mainbanner':mainbanner,'Subbanner':Subbanner,'Board':page_obj,'page': page, 'kw': kw,'nickName':nickName,'thumbnailURL':thumbnailURL,'check':check,'access_token':access_token}
    return render(request, 'board/news.html', context)





