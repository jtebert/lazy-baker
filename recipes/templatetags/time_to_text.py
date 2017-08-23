from django import template
import math

register = template.Library()

@register.filter(is_safe=True, name='time_to_text')
def time_to_text(value):
    '''
    Convert an integer number of minutes to a string of hours/minutes
    :param value: Number of minutes
    :return: String of hours/mins
    '''
    if value >= 60:
        hours = int(math.floor(value/60))
    else:
        hours = 0
    mins = value - hours * 60
    if hours > 0:
        txt = '{} hour {} minutes'.format(hours, mins)
    else:
        txt = '{} minutes'.format(mins)
    return txt