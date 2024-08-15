from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views import View
from .models import Category, MenuItem


def index(request):
    """View function for home page of site."""
    context = {}
    return render(request, "index.html", context=context)


def menu_view(request):
    """View function for menu."""

    category_names = ["breakfast", "launch", "dinner"]
    menu_items_by_category = {}
    for category_name in category_names:
        category = Category.objects.filter(category_name=category_name).first()
        if category:
            menu_items_by_category[category_name] = MenuItem.objects.filter(
                categories=category
            )
        else:
            menu_items_by_category[category_name] = []
    context = {
        "breakfast_item": menu_items_by_category["breakfast"],
        "launch_item": menu_items_by_category["launch"],
        "dinner_item": menu_items_by_category["dinner"],
    }
    return render(request, "menu/menu.html", context=context)


class DishDetail(View):
    def get(self, request, item_id):
        menu_item = get_object_or_404(MenuItem, item_id=item_id)
        name = menu_item.name
        description = menu_item.description
        price = menu_item.price
        image_url = menu_item.image_url
        context = {
            'name': name,
            'description': description,
            'price': price,
            'image_url': image_url
        }
        return render(request, 'dishes/detail.html', context)
