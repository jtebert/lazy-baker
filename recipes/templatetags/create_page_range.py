from django import template

register = template.Library()

@register.simple_tag(name='create_page_range')
def create_page_range(all_range, current_page):
    """Generate a range of up to 5 pages to show links to"""
    last_page = all_range[-1]
    if len(all_range) <= 5:
        return all_range
    elif current_page - 2 < 1:
        return range(1, 6)
    elif current_page + 2 > last_page:
        return range(last_page - 4, last_page + 1)
    else:
        return range(current_page - 2, current_page + 3)