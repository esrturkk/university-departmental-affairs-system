from django import template
register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key, None)

@register.filter
def make_range(value):
    return range(1, int(value) + 1)

@register.filter
def get_seat(seating, seat_number):
    for seat in seating:
        if seat.seat_number == seat_number:
            return seat
    return None
