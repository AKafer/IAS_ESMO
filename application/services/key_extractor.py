from externals.esmo import esmo_client
from transliterate import translit


async def extract_params_from_cache_key(cache_key: str) -> tuple:
    parts = cache_key.split('<>')[1].split('_')
    date = parts[0].split('=')[1]
    time = parts[1].split('=')[1]
    interval = parts[2].split('=')[1]
    div = parts[3].split('=')[1]
    divs = await esmo_client.get_divisions()
    if div != "all":
        div = divs.get(int(div), {}).get("name", "Не найдено")
    div = translit(div, 'ru', reversed=True)
    return date, time, interval, div
