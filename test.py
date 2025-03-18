from datetime import datetime


start_of_day = datetime.strptime("08:00", "%H:%M").time()
start_of_lunch = datetime.strptime("12:00", "%H:%M").time()
end_of_lunch = datetime.strptime("13:00", "%H:%M").time()
end_of_day = datetime.strptime("17:00", "%H:%M").time()


def is_working_time(time: datetime) -> bool:
    t = time.time()
    if t >= start_of_day and t < start_of_lunch:
        return True
    if t>= end_of_lunch and t < end_of_day:
        return True
    return False


t1 = datetime(2025,3,18, 11,0,0)
if not is_working_time(t1):
    print("fora do expediente")