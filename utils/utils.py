import datetime


def time_to_unix(s):
    date, time_ = s.split(" ")
    arr_date = date.split("-")
    arr_time = time_.split(":")
    drt = datetime.datetime(int(arr_date[0]), int(arr_date[1]), int(arr_date[2]), int(arr_time[0]), int(arr_time[1]))
    return datetime.datetime.timestamp(drt)


def unix_to_time(s: int):
    value = datetime.datetime.fromtimestamp(int(s))
    return value.strftime('%Y-%m-%d %H:%M')


def campus_coordinates(campus_name):
    if campus_name == 'MSK':
        return 55.79711190250842, 37.57968578011329
    if campus_name == 'KAZ':
        return 55.78197203199345, 49.12511843556399
    if campus_name == 'NSK':
        return 54.980136150869086, 82.89756155471028


def check_coordinates(point, check_point):
    k = 111200
    l = 200
    x = (abs(point[0] - check_point[0]) * k < l)
    y =  (abs(point[1] - check_point[1]) * k < l)
    return x and y


def get_deeplink(payload: str):
    return f"https://t.me/weeklython_school21_checkin_bot?start={payload}"
    # return f"https://t.me/my_memkek_bot?start={payload}"