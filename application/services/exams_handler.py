from datetime import datetime, timedelta
import pytz


def get_time(diff: timedelta) -> str:
    d = diff.days
    h = diff.seconds // 3600 + d * 24
    if h < 10:
        h = f"0{h}"
    h = f"{h} ч."
    m = diff.seconds // 60 % 60
    if m < 10:
        m = f"0{m}"
    m = f" {m} м."
    return h + m


def get_empl_dict(employees: list[dict]) -> dict:
    return {empl["uuid"]: empl for empl in employees if empl.get("uuid")}


def get_div_dict(divisions: list[dict]) -> dict:
    return {div["id"]: div for div in divisions}


def exam_handler(
    exam_list: list[dict],
    employee_dict: dict,
    divisions_dict: dict
) -> list[dict]:
    res = {}
    for exam in exam_list:
        if exam["employee_uuid"] and exam["model"] == 1:
            if exam["employee_uuid"] not in res:
                res[exam["employee_uuid"]] = {
                    "number": exam["employee_uuid"],
                    "name": "Не найдено",
                    "division": "Не найдено",
                    "type_1": [],
                    "type_2": [],
                    "duration": [],
                    "marks": "0-0"
                }
            if exam["type"] == 1:
                res[exam["employee_uuid"]]["type_1"].append(datetime.fromtimestamp(exam["date"], pytz.timezone("Europe/Moscow")))
            if exam["type"] == 2:
                res[exam["employee_uuid"]]["type_2"].append(datetime.fromtimestamp(exam["date"], pytz.timezone("Europe/Moscow")))

    for uuid, val in res.items():
        type_1 = sorted(val["type_1"])
        type_2 = sorted(val["type_2"])
        res[uuid]["marks"] = f"{len(type_1)}-{len(type_2)}"
        val["type_1"] = type_1.copy()
        val["type_2"] = type_2.copy()

        if len(type_1) <= len(type_2):
            for x in type_1:
                for y in type_2:
                    if x < y:
                        diff = y - x
                        res[uuid]["duration"].append(get_time(diff))
                        type_2.remove(y)
                        break
        else:
            type_1 = type_1[::-1]
            type_2 = type_2[::-1]
            for y in type_2:
                for x in type_1:
                    if x < y:
                        diff = y - x
                        res[uuid]["duration"].insert(0, get_time(diff))
                        type_1.remove(x)
                        break

    for uuid, val in res.items():
        res[uuid]["name"] = employee_dict.get(uuid, {}).get("full_name", "Не найдено")
        div_id = employee_dict.get(uuid, {}).get("division_id")
        if div_id:
            res[uuid]["division"] = divisions_dict.get(div_id, {}).get("name", "Не найдено")
    res_list = list(res.values())
    return res_list
