from datetime import datetime


get_time = lambda x: f"{x.seconds // 3600} ч., {(x.seconds // 60) % 60} м."


def get_empl_dict(employees: list[dict]) -> dict:
    return {empl["uuid"]: empl for empl in employees}


def exam_handler(exam_list: list[dict], employee_dict: dict) -> dict:
    res = {}
    for exam in exam_list:
        if exam["employee_uuid"] not in res:
            res[exam["employee_uuid"]] = {
                "number": exam["employee_uuid"],
                "name": "Не найдено",
                "type_1": False,
                "date_type_1": None,
                "type_2": False,
                "date_type_2": None,
                "duration": "0 ч., 0 м.",
            }
        if exam["type"] == 1:
            res[exam["employee_uuid"]]["type_1"] = True
            res[exam["employee_uuid"]]["date_type_1"] = datetime.fromtimestamp(exam["date"])
        if exam["type"] == 2:
            res[exam["employee_uuid"]]["type_2"] = True
            res[exam["employee_uuid"]]["date_type_2"] = datetime.fromtimestamp(exam["date"])
        if res[exam["employee_uuid"]]["type_1"] and res[exam["employee_uuid"]]["type_2"]:
            diff = res[exam["employee_uuid"]]["date_type_2"] - res[exam["employee_uuid"]]["date_type_1"]
            res[exam["employee_uuid"]]["duration"] = get_time(diff)
    for uuid, val in res.items():
        res[uuid]["name"] = employee_dict.get(uuid, {}).get("full_name", "Не найдено")
    return res