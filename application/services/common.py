from django.core.cache import cache

from externals.esmo import esmo_client, USER_LAST_EXAM_CACHE_KEY
from transliterate import translit

from services.exceptions import QueryParamsNotProvidedError


def extract_query_params(request):
    date = request.GET.get('date', '')
    time = request.GET.get('time', '')
    interval = request.GET.get('interval', '')
    div = request.GET.get('div', '')
    if not date or not time or not interval:
        raise QueryParamsNotProvidedError('Time params is not provided')
    return date, time, interval, div


def extract_query_params_from_cache_key(username: str) -> tuple:
    last_cache_key = cache.get(USER_LAST_EXAM_CACHE_KEY.format(username=username))
    params = last_cache_key.split('<>')[1].split('_')
    date = params[0].split('=')[1]
    time = params[1].split('=')[1]
    interval = params[2].split('=')[1]
    div = params[3].split('=')[1]
    return date, time, interval, div


async def get_div_name(div_id: str) -> str:
    divs = await esmo_client.get_divisions()
    div = divs.get(int(div_id), {}).get("name", "Не найдено") if div_id != "all" else div_id
    return translit(div, 'ru', reversed=True)
