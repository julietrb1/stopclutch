from datetime import timedelta

from django import template
from django.contrib.humanize.templatetags.humanize import ordinal
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def modelimage(image, classes, image_for):
    if not image:
        return ''
    else:
        return format_html('<img src="{}" alt="Image for {}" class="{}">', image.url, image_for, classes)


@register.filter()
def durationformat(race_duration: timedelta):
    milliseconds = int((race_duration.microseconds / 1000))
    seconds = int(race_duration.seconds % 60)
    minutes = int((race_duration.seconds / 60) % 60)

    if minutes:
        return "{:d}:{:02d}.{:03d}".format(minutes, seconds, milliseconds)
    else:
        return "{:2d}.{:03d}".format(seconds, milliseconds)


@register.simple_tag
def trophy(placement):
    ordinal_placement = ordinal(placement)

    icon_class = False

    if placement == 1:
        icon_class = 'chess-king'
    elif placement == 2:
        icon_class = 'chess-queen'
    elif placement == 3:
        icon_class = 'chess-knight'

    if icon_class:
        icon = mark_safe('<i class="fas fa-{}"></i>'.format(icon_class))
        return format_html('<span class="placement-{}"><b>{}</b> {}</span>', placement, ordinal_placement, icon)
    else:
        return ordinal_placement


@register.inclusion_tag('partials/racetime_table.html')
def racetimetable(racetimes, pagination=None, columns=None, highlighted_placements=(), fastest_time=None,
                  mobile_player_only=False):
    if not columns:
        columns = ('when', 'placement', 'player', 'vehicle', 'track', 'duration')
    return {
        'racetimes': racetimes,
        'columns': columns,
        'pagination': pagination,
        'highlighted_placements': highlighted_placements,
        'fastest_time': fastest_time,
        'mobile_player_only': mobile_player_only
    }


@register.simple_tag
def breadcrumb(label, path=None):
    if path:
        return format_html('<li class="breadcrumb-item"><a href="{}">{}</a></li>', reverse(path), label)
    else:
        return format_html('<li class="breadcrumb-item active" aria-current="page">{}</a>', label)


@register.simple_tag
def time_diff(o1, o2):
    return durationformat(o1 - o2).strip()


@register.inclusion_tag('partials/mobile_racetime.html')
def mobile_racetime(racetime, player_only=False, fastest_time=None):
    return {'racetime': racetime, 'player_only': player_only, 'fastest_time': fastest_time}


@register.inclusion_tag('partials/nav_item_simple.html', takes_context=True)
def nav_item_simple(context, path: str, display_name):
    return {
        'path_search': path.split(':')[0],
        'path': path,
        'display_name': display_name,
        'view_name': context['view_name']
    }


@register.inclusion_tag('partials/nav_item_list.html', takes_context=True)
def nav_item_list(context, paths: str, display_names, parent_name):
    paths_split = paths.split(',')
    display_names_split = display_names.split(',')
    view_name = context['view_name']

    nav_items = []
    active = False

    for index, path in enumerate(paths_split):
        initial_path = path.split(':')[0]
        if initial_path in view_name and not active:
            active = True

        nav_items.append({'path_search': initial_path, 'path': path, 'display_name': display_names_split[index]})

    return {
        'nav_items': nav_items,
        'view_name': view_name,
        'active': active,
        'parent_name': parent_name
    }
