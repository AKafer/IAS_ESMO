from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from lazy_object_proxy import Proxy

from services.exams_handler import exam_handler, get_empl_dict
from externals.base import BaseApiClient

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkwMGIyMTE0NWEzZjVjMDE0Nzg1MjdiZGQxN2RlOWIzZDNjOWZjOGEyODQ1OTk0NTI4ZGUzMjNjMmMzMjM4ZGRlM2M3ZTVmZmM3NTY3NWZjIn0.eyJhdWQiOiIxIiwianRpIjoiOTAwYjIxMTQ1YTNmNWMwMTQ3ODUyN2JkZDE3ZGU5YjNkM2M5ZmM4YTI4NDU5OTQ1MjhkZTMyM2MyYzMyMzhkZGUzYzdlNWZmYzc1Njc1ZmMiLCJpYXQiOjE3MTEyNzc5MjUsIm5iZiI6MTcxMTI3NzkyNSwiZXhwIjoxNzQyODEzOTI1LCJzdWIiOiIxNDAiLCJzY29wZXMiOltdfQ.LW3rw5VXrTsmYWKquAtkK_8UgOeifiji7t2N5Qf8LYx33JZN77-pDBH60zT_XFj0TXWQEwrg7eujFASZuYSybr7iBGhvnJF4fM5yiVvxDXRTBMBv6EY9jw-nFdyD9Qp-zUZRuQ1mfQkUWtEYOP0tuvV_VA3bUY2XAiJF61JagqlmRtpfbry-VPcbWFuZmtOmLq4IZe6x5mlgwLAme15ESTHs_Mq6IQrsF9nmSCXoCzORaKo6Eh_EnN21sSu_0cOmlR7yxQwUUlODs0i2KTVTQPDlesSZweqPUXGpR1pQyuUoG7u8rCNtOd2XZOAZt6zaUmjmeQyODCx5hyTKSdnliZtzc3qLVr2ZWgBm1pvI9hQm9E8JuerYAv--ls6xVIGLn3xS5YgeUIWgPAzCmH_vlukOh7pZ9YYd2TR8v8WyfNI4ISvZRkUOnF6EgFHfGJ7LIbtq69-MzXQnBoOZL2RbNUSFQeO0cCx4cehsePFBzf5o_dTEPqtO5UJmmJOMIvs7ElCUR1wtl6a-v62HbDQCqLuZv3rZO-Dyg1O2z2081fvKWH9LxpySyZFXtOMQTufqI2iysMGXTeiykw8IwQVh4jNF95TVE-3JlAbOkJoztN7CPpdYJNF0-UkU-8eYsZ7Ey7pdmwu7bJQCPu0rzH7lK0OANt5PO5Up7DNRmxIIJOM'


class EsmoApiClient(BaseApiClient):
    base_url = 'https://profaudit.kvzrm.ru/api/v1/'
    HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async def _fetch_paginated(self, endpoint: str, page) -> list:
        url = urljoin(self.base_url, f"{endpoint}&page={page}".lstrip("/"))
        response = await self.get(url, headers=self.HEADERS)
        results = response.get("data", [])

        if response.get("next_page_url"):
            page += 1
            next_results = await self._fetch_paginated(endpoint, page)
            results.extend(next_results)
        return results

    async def get_employees(self):
        cache_key = f"employees"
        employee_dict = cache.get(cache_key)
        if not employee_dict:
            endpoint = f"/exchange/employees/?per_page={settings.ROWS_PER_PAGE}"
            result = await self._fetch_paginated(endpoint, 1)
            employee_dict = get_empl_dict(result)
            cache.set(cache_key, employee_dict, settings.EMPL_TTL)
        return employee_dict

    def _get_date_range(self, date: str):
        from_date_str = date + ' 00:00:00'
        to_date_str = date + ' 23:59:59'
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d %H:%M:%S')
        return from_date, to_date

    async def get_examsessions(self, date_from_str: str, date_to_str: str):
        cache_key = "dct_exams: {date_from_str}-{date_to_str}".format(
            date_from_str=date_from_str, date_to_str=date_to_str
        ).replace(":", "-")
        result = cache.get(cache_key)
        if not result:
            from_date = datetime.strptime(date_from_str, '%Y-%m-%d %H:%M:%S')
            to_date = datetime.strptime(date_to_str, '%Y-%m-%d %H:%M:%S')
            endpoint = (
                f"exchange/examsessions/"
                f"?from={int(from_date.timestamp())}"
                f"&to={int(to_date.timestamp())}"
                f"&per_page={settings.ROWS_PER_PAGE}"
            )
            result = await self._fetch_paginated(endpoint, 1)
            cache.set(cache_key, result, settings.EXAM_TTL)

        employee_dict = await self.get_employees()
        response_lst = exam_handler(result, employee_dict)
        return response_lst


esmo_client: EsmoApiClient = Proxy(EsmoApiClient)
