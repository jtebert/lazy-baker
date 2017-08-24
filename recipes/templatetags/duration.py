from django import template

register = template.Library()

@register.filter(is_safe=True, name='duration')
def duration(td):
    """
    Format the duration into a string for display in templates
    :param td: DurationField
    :return: Formatted string of duration
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    out_str = ''
    if hours == 1:
        out_str += '1 hour '
    elif hours > 1:
        out_str += '{} hours '.format(hours)
    if minutes == 1:
        out_str += '1 minute'
    elif minutes > 1:
        out_str += '{} minutes'.format(minutes)

    return out_str