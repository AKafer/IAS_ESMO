from datetime import datetime, timedelta


def get_time(diff: timedelta) -> str:
    h = diff.seconds // 3600
    if h < 10:
        h = f"0{h}"
    h = f"{h} ч.,"
    m = diff.seconds // 60 % 60
    if m < 10:
        m = f"0{m}"
    m = f" {m} м."
    return h + m


def get_empl_dict(employees: list[dict]) -> dict:
    return {empl["uuid"]: empl for empl in employees}


def exam_handler(exam_list: list[dict], employee_dict: dict) -> list[dict]:
    res = {}
    for exam in exam_list:
        if exam["employee_uuid"] and exam["model"] == 1:
            if exam["employee_uuid"] not in res:
                res[exam["employee_uuid"]] = {
                    "number": exam["employee_uuid"],
                    "name": "Не найдено",
                    "division_id": "Не найдено",
                    "type_1": [],
                    "type_2": [],
                    "duration": "00 ч., 00 м.",
                    "marks": "0-0"
                }
            if exam["type"] == 1:
                res[exam["employee_uuid"]]["type_1"].append(datetime.fromtimestamp(exam["date"]))
            if exam["type"] == 2:
                res[exam["employee_uuid"]]["type_2"].append(datetime.fromtimestamp(exam["date"]))

    for uuid, val in res.items():
        type_1 = sorted(val["type_1"])
        type_2 = sorted(val["type_2"])
        res[uuid]["marks"] = f"{len(type_1)}-{len(type_2)}"
        val["type_1"] = type_1
        val["type_2"] = type_2
    for uuid, val in res.items():
        res[uuid]["name"] = employee_dict.get(uuid, {}).get("full_name", "Не найдено")
        res[uuid]["division_id"] = employee_dict.get(uuid, {}).get("division_id", "Не найдено")
    res_list = list(res.values())
    return res_list
