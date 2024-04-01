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
        if exam["employee_uuid"] not in res:
            res[exam["employee_uuid"]] = {
                "number": exam["employee_uuid"],
                "name": "Не найдено",
                "type_1": '',
                "date_type_1": None,
                "type_2": '',
                "date_type_2": None,
                "duration": "00 ч., 00 м.",
            }
        if exam["type"] == 1:
            res[exam["employee_uuid"]]["type_1"] = 'X'
            res[exam["employee_uuid"]]["date_type_1"] = datetime.fromtimestamp(exam["date"])
        if exam["type"] == 2:
            res[exam["employee_uuid"]]["type_2"] = 'X'
            res[exam["employee_uuid"]]["date_type_2"] = datetime.fromtimestamp(exam["date"])
        if (
            res[exam["employee_uuid"]]["type_1"]
            and res[exam["employee_uuid"]]["type_2"]
            and res[exam["employee_uuid"]]["date_type_1"] < res[exam["employee_uuid"]]["date_type_2"]
        ):
            diff = res[exam["employee_uuid"]]["date_type_2"] - res[exam["employee_uuid"]]["date_type_1"]
            res[exam["employee_uuid"]]["duration"] = get_time(diff)
    for uuid, val in res.items():
        res[uuid]["name"] = employee_dict.get(uuid, {}).get("full_name", "Не найдено")
    res_list = list(res.values())
    return res_list
