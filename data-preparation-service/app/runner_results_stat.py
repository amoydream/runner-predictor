from datetime import timedelta, date
from string import Template


class RunnerResultsStat:
    def __init__(self, results):
        self.results = results

    def best_time(self, distance, race_type):
        best_time = string_to_timedelta(self.results[0]["result_of_the_race"])
        for result in self.results:
            same_race_type = result["race_type"] == race_type
            same_disntance = float(result["distance"]) == float(distance)
            if same_race_type and same_disntance:
                res_time = string_to_timedelta(result["result_of_the_race"])
                if best_time > res_time:
                    best_time = res_time
        return_dict = {
            "time": strfdelta(best_time, "%H:%M:%S"),
            "decimal": convert_time_to_hours_decimal(str(best_time)),
        }
        return return_dict


def convert_time_to_hours_decimal(string_time):
    delta_time = string_to_timedelta(string_time)
    seconds = delta_time.seconds
    minutes = seconds / 60
    hours = minutes / 60
    return round(hours, 3)


def string_to_timedelta(delta_string):
    """Change string format 00:00:00 to timedelta instance"""
    ti = delta_string.split(":")
    try:
        hour = int(ti[0])
        minute = int(ti[1])
        second = int(ti[2])
    except ValueError:
        time_delta = None
    except IndexError:
        time_delta = None
    else:
        time_delta = timedelta(hours=hour, minutes=minute, seconds=second)
    return time_delta


class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = "{:02d}".format(hours)
    d["M"] = "{:02d}".format(minutes)
    d["S"] = "{:02d}".format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)
