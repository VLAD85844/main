from django import template
from django.urls import resolve, Resolver404
from tree_menu.models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    try:
        menu = Menu.objects.prefetch_related('items__children').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_tree': []}
    menu_items = list(menu.items.all())
    menu_tree = build_menu_tree(menu_items, None, current_url)

    return {
        'menu_tree': menu_tree,
        'current_url': current_url,
    }


def build_menu_tree(items, parent_id, current_url):
    tree = []

    for item in items:
        if item.parent_id == parent_id:
            is_active = is_menu_item_active(item, current_url)
            children = build_menu_tree(items, item.id, current_url)
            is_expanded = is_active or any(child.get('is_expanded', False) for child in children)
            tree.append({
                'item': item,
                'children': children,
                'is_active': is_active,
                'is_expanded': is_expanded,
                'has_active_child': any(
                    child.get('is_active', False) or child.get('has_active_child', False) for child in children),
            })
    return tree


def is_menu_item_active(menu_item, current_url):
    try:
        item_url = menu_item.get_url()

        if item_url == current_url:
            return True

        if menu_item.named_url:
            try:
                resolved_current = resolve(current_url)
                resolved_item = resolve(item_url)
                if (resolved_current.url_name == resolved_item.url_name and
                        resolved_current.namespace == resolved_item.namespace):
                    return True
            except Resolver404:
                pass

    except Exception:
        pass

    return False