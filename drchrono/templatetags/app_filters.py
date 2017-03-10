import datetime
from django import template
import pytz
register = template.Library()


@register.filter(name='time_from_now')
def time_from_now(value):
    delta = datetime.datetime.now(pytz.utc) - value.astimezone(pytz.utc)
    seconds = delta.total_seconds()
    minutes = seconds / 60
    return int(minutes - 420)
