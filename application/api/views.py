import json

from asgiref.sync import sync_to_async, async_to_sync
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
import logging

from django.views.decorators.csrf import csrf_exempt

from externals.esmo import esmo_client
from services.book_handler import get_book
from services.common import get_div_name, extract_query_params_from_cache_key


logger = logging.getLogger("esmo")


class IndexView(View):
    @sync_to_async
    @method_decorator(login_required)
    @csrf_exempt
    @async_to_sync
    async def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'esmo/index.html')


class DivsView(View):
    @csrf_exempt
    async def get(self, request: HttpRequest):
        result = await esmo_client.get_divisions()
        converted_result = json.dumps(list(result.values()), default=str)
        return HttpResponse(converted_result, content_type="application/json")


class ExamsTableView(View):
    @csrf_exempt
    async def get(self, request: HttpRequest):
        date = request.GET.get('date', '')
        time = request.GET.get('time', '')
        interval = request.GET.get('interval', '')
        div = request.GET.get('div', '')
        user = await sync_to_async(auth.get_user)(request)
        username = user.username
        result = await esmo_client.get_examsessions(username, date, time, interval, div)
        converted_result = json.dumps(result, default=str)
        return HttpResponse(converted_result, content_type="application/json")


class ExamsEmptyView(View):
    @csrf_exempt
    async def get(self, request: HttpRequest):
        example_result = []
        return HttpResponse(json.dumps(example_result), content_type="application/json")


class ExamsFileView(View):
    @csrf_exempt
    async def get(self, request: HttpRequest):
        user = await sync_to_async(auth.get_user)(request)
        username = user.username
        date, time, interval, div = extract_query_params_from_cache_key(username)
        result = await esmo_client.get_examsessions(username, date, time, interval, div)
        div_name = await get_div_name(div)
        wb = await get_book(result)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = (
            'attachment; filename="{div}_{date}_{time}_{interval}.xlsx"'
            .format(date=date, time=time, interval=interval, div=div_name)
        )
        wb.save(response)
        return response
