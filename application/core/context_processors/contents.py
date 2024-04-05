import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils import timezone

from application.settings import (
    PPEJ_5,
    PPEJC_1,
    PPELSLE_2,
    PPELTWT_3,
    PPEWATWT_4,
    TODAY,
)

NAME_FILE = {
    PPEJC_1: "Комплектация",
    PPELSLE_2: "Срок службы истек",
    PPELTWT_3: "Испытаны не вовремя",
    PPEWATWT_4: "Осмотрены не вовремя",
    PPEJ_5: "Журнал СИЗ",
}


def year(request):
    """Выводим год в футер."""

    return {"year": timezone.now()}


@login_required
def download_journals(request, file):
    """Выгрузка Журналов СИЗ."""

    file_path = os.path.join(settings.MEDIA_ROOT, f"journals/{TODAY}/{file}")
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response[
                "Content-Disposition"
            ] = f"inline; filename={os.path.basename(file_path)}"
            os.remove(file_path)
            return response
    return HttpResponse(f"Файла нет! {file_path}, {file}")


def content(request):
    """Вывод формы выгрузки журналов."""

    form_material = ""
    return {"list_journals": form_material}
