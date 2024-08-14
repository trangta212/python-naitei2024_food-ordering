from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, MenuItem, Cart, User, CartItem


def index(request):
    """View function for home page of site."""

    top_rated_items = MenuItem.objects.order_by("-rate_avg")[:20]

    context = {
        "popular_items": top_rated_items,
    }
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
            "name": name,
            "description": description,
            "price": price,
            "image_url": image_url,
        }
        return render(request, "dishes/detail.html", context)


def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        user = User.objects.first()

        cart, created = Cart.objects.get_or_create(user=user)

        item = get_object_or_404(MenuItem, item_id=item_id)

        if item.quantity == 0:
            return JsonResponse(
                {"status": "failed", "message": "Item sold out"}, status=400
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item, defaults={"quantity": 1}
        )

        if not created:
            cart_item.quantity += 1

        cart_item.save()

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)
