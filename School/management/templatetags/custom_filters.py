from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value from the dictionary for the given key."""
    return dictionary.get(key)

@register.filter
def to_float(value):
    """Converts a value to a float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return value

@register.filter
def add(value, arg):
    """Adds two integers."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value
