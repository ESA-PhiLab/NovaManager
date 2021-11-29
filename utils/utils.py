from datetime import datetime

from dateutil import relativedelta


def get_delta_to_now(date_str):
    return human_readable_delta(
        relativedelta.relativedelta(
            datetime.utcnow(), datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        )
    )


def get_hours_to_now(date_str):
    diff = datetime.utcnow() - datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return diff.days * 24 + diff.seconds // 3600


def human_readable_delta(delta):
    attrs = ["years", "months", "days", "hours", "minutes", "seconds"]
    return " ".join(
        [
            "%d %s"
            % (getattr(delta, attr), attr if getattr(delta, attr) > 1 else attr[:-1])
            for attr in attrs
            if getattr(delta, attr)
        ]
    )
