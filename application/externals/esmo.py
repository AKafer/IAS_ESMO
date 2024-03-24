from urllib.parse import urljoin

from lazy_object_proxy import Proxy

from externals.base import BaseApiClient

TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkwMGIyMTE0NWEzZjVjMDE0Nzg1MjdiZGQxN2RlOWIzZDNjOWZjOGEyODQ1OTk0NTI4ZGUzMjNjMmMzMjM4ZGRlM2M3ZTVmZmM3NTY3NWZjIn0.eyJhdWQiOiIxIiwianRpIjoiOTAwYjIxMTQ1YTNmNWMwMTQ3ODUyN2JkZDE3ZGU5YjNkM2M5ZmM4YTI4NDU5OTQ1MjhkZTMyM2MyYzMyMzhkZGUzYzdlNWZmYzc1Njc1ZmMiLCJpYXQiOjE3MTEyNzc5MjUsIm5iZiI6MTcxMTI3NzkyNSwiZXhwIjoxNzQyODEzOTI1LCJzdWIiOiIxNDAiLCJzY29wZXMiOltdfQ.LW3rw5VXrTsmYWKquAtkK_8UgOeifiji7t2N5Qf8LYx33JZN77-pDBH60zT_XFj0TXWQEwrg7eujFASZuYSybr7iBGhvnJF4fM5yiVvxDXRTBMBv6EY9jw-nFdyD9Qp-zUZRuQ1mfQkUWtEYOP0tuvV_VA3bUY2XAiJF61JagqlmRtpfbry-VPcbWFuZmtOmLq4IZe6x5mlgwLAme15ESTHs_Mq6IQrsF9nmSCXoCzORaKo6Eh_EnN21sSu_0cOmlR7yxQwUUlODs0i2KTVTQPDlesSZweqPUXGpR1pQyuUoG7u8rCNtOd2XZOAZt6zaUmjmeQyODCx5hyTKSdnliZtzc3qLVr2ZWgBm1pvI9hQm9E8JuerYAv--ls6xVIGLn3xS5YgeUIWgPAzCmH_vlukOh7pZ9YYd2TR8v8WyfNI4ISvZRkUOnF6EgFHfGJ7LIbtq69-MzXQnBoOZL2RbNUSFQeO0cCx4cehsePFBzf5o_dTEPqtO5UJmmJOMIvs7ElCUR1wtl6a-v62HbDQCqLuZv3rZO-Dyg1O2z2081fvKWH9LxpySyZFXtOMQTufqI2iysMGXTeiykw8IwQVh4jNF95TVE-3JlAbOkJoztN7CPpdYJNF0-UkU-8eYsZ7Ey7pdmwu7bJQCPu0rzH7lK0OANt5PO5Up7DNRmxIIJOM'


class EsmoApiClient(BaseApiClient):
    base_url = 'https://profaudit.kvzrm.ru/api/v1/'
    HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async def _fetch_paginated(self, url: str, page, from_date, to_date) -> list:
        print(f"URL: {url}")
        response = await self.get(url, headers=self.HEADERS)
        results = response.get("data", [])

        if response.get("next_page_url"):
            page += 1
            endpoint = (
                f"exchange/examsessions/"
                f"?page={page}"
                f"&from={int(from_date.timestamp())}"
                f"&to={int(to_date.timestamp())}"
                f"&per_page=200"
            )
            url = urljoin(self.base_url, endpoint.lstrip("/"))
            next_results = await self._fetch_paginated(
                url, page, from_date, to_date
            )
            results.extend(next_results)
        return results

    async def get_examsessions(self, from_date=None, to_date=None):
        endpoint = (
            f"exchange/examsessions/"
            f"?from={int(from_date.timestamp())}"
            f"&to={int(to_date.timestamp())}"
            f"&per_page=200"
        )
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        return await self._fetch_paginated(url, 1, from_date, to_date)


gest_client: EsmoApiClient = Proxy(EsmoApiClient)
