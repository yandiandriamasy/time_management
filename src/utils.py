from datetime import datetime
import pytz


def convert_utc_to_paris_time(utc_time: str) -> str:
    """
    Convert UTC time to Paris time
    :param utc_time: UTC time
    :return: Paris time
    """
    utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f%z")
    tz = pytz.timezone("Europe/Paris")
    return utc_time.astimezone(tz).strftime("%d/%m/%Y, %H:%M:%S")
