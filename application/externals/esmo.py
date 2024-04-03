from datetime import datetime, timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from lazy_object_proxy import Proxy

from services.exams_handler import exam_handler, get_empl_dict, get_div_dict
from externals.base import BaseApiClient


class EsmoApiClient(BaseApiClient):
    base_url = 'https://profaudit.kvzrm.ru/api/v1/'
    HEADERS = {
        'Authorization': f'Bearer {settings.TOKEN}',
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

    async def get_divisions(self):
        cache_key = f"divisions"
        divisions_dict = cache.get(cache_key)
        if not divisions_dict:
            endpoint = f"/exchange/divisions/?per_page={settings.ROWS_PER_PAGE}"
            result = await self._fetch_paginated(endpoint, 1)
            divisions_dict = get_div_dict(result)
            cache.set(cache_key, divisions_dict, settings.EMPL_TTL)
        return divisions_dict

    def _get_date_range(self, date: str):
        from_date_str = date + ' 00:00:00'
        to_date_str = date + ' 23:59:59'
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d %H:%M:%S')
        return from_date, to_date

    async def get_examsessions(self, date: str, time: str, interval: str):
        print('ESMO')
        cache_key = "dct_exams_{date}-{time}-{interval}".format(
            date=date, time=time, interval=interval
        ).replace(":", "-")
        result = cache.get(cache_key)
        print('CACHE')
        if not result:
            from_date = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
            to_date = from_date + timedelta(hours=int(interval))
            endpoint = (
                f"exchange/examsessions/"
                f"?from={int(from_date.timestamp())}"
                f"&to={int(to_date.timestamp())}"
                f"&per_page={settings.ROWS_PER_PAGE}"
            )
            result = await self._fetch_paginated(endpoint, 1)
            cache.set(cache_key, result, settings.EXAM_TTL)

        employee_dict = await self.get_employees()
        divisions_dict = await self.get_divisions()
        response_lst = exam_handler(result, employee_dict, divisions_dict)
        return response_lst


esmo_client: EsmoApiClient = Proxy(EsmoApiClient)
