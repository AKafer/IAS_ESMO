from datetime import datetime

import httpx
from django.http import HttpRequest, HttpResponse
from django.views import View
import logging

from externals.esmo import gest_client

logger = logging.getLogger("esmo")


URL = 'https://profaudit.kvzrm.ru/api/v1/exchange/examsessions/?per_page=100'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkwMGIyMTE0NWEzZjVjMDE0Nzg1MjdiZGQxN2RlOWIzZDNjOWZjOGEyODQ1OTk0NTI4ZGUzMjNjMmMzMjM4ZGRlM2M3ZTVmZmM3NTY3NWZjIn0.eyJhdWQiOiIxIiwianRpIjoiOTAwYjIxMTQ1YTNmNWMwMTQ3ODUyN2JkZDE3ZGU5YjNkM2M5ZmM4YTI4NDU5OTQ1MjhkZTMyM2MyYzMyMzhkZGUzYzdlNWZmYzc1Njc1ZmMiLCJpYXQiOjE3MTEyNzc5MjUsIm5iZiI6MTcxMTI3NzkyNSwiZXhwIjoxNzQyODEzOTI1LCJzdWIiOiIxNDAiLCJzY29wZXMiOltdfQ.LW3rw5VXrTsmYWKquAtkK_8UgOeifiji7t2N5Qf8LYx33JZN77-pDBH60zT_XFj0TXWQEwrg7eujFASZuYSybr7iBGhvnJF4fM5yiVvxDXRTBMBv6EY9jw-nFdyD9Qp-zUZRuQ1mfQkUWtEYOP0tuvV_VA3bUY2XAiJF61JagqlmRtpfbry-VPcbWFuZmtOmLq4IZe6x5mlgwLAme15ESTHs_Mq6IQrsF9nmSCXoCzORaKo6Eh_EnN21sSu_0cOmlR7yxQwUUlODs0i2KTVTQPDlesSZweqPUXGpR1pQyuUoG7u8rCNtOd2XZOAZt6zaUmjmeQyODCx5hyTKSdnliZtzc3qLVr2ZWgBm1pvI9hQm9E8JuerYAv--ls6xVIGLn3xS5YgeUIWgPAzCmH_vlukOh7pZ9YYd2TR8v8WyfNI4ISvZRkUOnF6EgFHfGJ7LIbtq69-MzXQnBoOZL2RbNUSFQeO0cCx4cehsePFBzf5o_dTEPqtO5UJmmJOMIvs7ElCUR1wtl6a-v62HbDQCqLuZv3rZO-Dyg1O2z2081fvKWH9LxpySyZFXtOMQTufqI2iysMGXTeiykw8IwQVh4jNF95TVE-3JlAbOkJoztN7CPpdYJNF0-UkU-8eYsZ7Ey7pdmwu7bJQCPu0rzH7lK0OANt5PO5Up7DNRmxIIJOM'

HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }


class IndexView(View):
    async def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse("Welcome to Esmo Proxy app")


class ApiView(View):
    async def get(self, request: HttpRequest):
        # async with httpx.AsyncClient(verify=False) as client:
        #     response = await client.request(
        #         method='GET',
        #         url=URL,
        #         headers=HEADERS,
        #     )
        #     print('1')
        #     # pars_response = await _deserialize_response(response)
        from_date = datetime(2024, 3, 18)
        to_date = datetime(2024, 3, 19)
        result = await gest_client.get_examsessions(from_date, to_date)

        print(f"LEN: {len(result)}")
        return HttpResponse(f"LEN: {len(result)}")
