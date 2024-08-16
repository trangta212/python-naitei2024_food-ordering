import json
from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
from .models import Category, MenuItem, Cart, User, CartItem
from .constants import TOP_RATED_ITEMS_LENGTH, CART_VIEW_PAGINATE


def index(request):
    """View function for home page of site."""

    top_rated_items = MenuItem.objects.order_by("-rate_avg")[
        :TOP_RATED_ITEMS_LENGTH
    ]

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
                {"status": "failed", "message": _("Item sold out")}, status=400
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item, defaults={"quantity": 1}
        )

        if not created:
            cart_item.quantity += 1

        cart_item.save()

        return JsonResponse({"status": _("success")})
    return JsonResponse({"status": _("failed")}, status=400)


@csrf_exempt
def update_cart(request):
    try:
        data = json.loads(request.body)
        user = User.objects.first()
        cart, created = Cart.objects.get_or_create(user=user)

        if request.method == "POST":
            for item in data:
                item_id = item["id"]
                quantity = item["quantity"]

                try:
                    cart_item = CartItem.objects.get(
                        cart=cart, item_id=item_id
                    )
                    menu_item = MenuItem.objects.get(item_id=item_id)
                    if int(quantity) < menu_item.quantity:
                        cart_item.quantity = quantity
                        if int(quantity) == 0:
                            cart_item.delete()
                        else:
                            cart_item.save()
                except CartItem.DoesNotExist:
                    menu_item = MenuItem.objects.get(id=item_id)
                    CartItem.objects.create(
                        cart=cart, item=menu_item, quantity=quantity
                    )

            return JsonResponse(
                {"success": True, "message": _("Cart updated successfully.")}
            )

        elif request.method == "DELETE":
            data = json.loads(request.body)
            item_id = data["id"]

            try:
                cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
                cart_item.delete()
                return JsonResponse(
                    {
                        "success": True,
                        "message": _("Item deleted successfully."),
                    }
                )
            except CartItem.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": _("Item not found.")}
                )

    except Exception as e:
        original_message = str(e)
        translated_message = _(original_message)

        return JsonResponse({"success": False, "message": translated_message})


class CartView(generic.ListView):
    """View function for home page of site."""

    paginate_by = CART_VIEW_PAGINATE
    context_object_name = "cart_items"

    def get_queryset(self):
        first_user = User.objects.first()
        if first_user:
            return CartItem.objects.filter(cart__user=first_user)
        else:
            return CartItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.get_queryset()
        total_item = items.count()
        total_quantity = items.aggregate(Sum("quantity"))["quantity__sum"] or 0
        total_price = (
            items.aggregate(total_price=Sum(F("quantity") * F("item__price")))[
                "total_price"
            ]
            or 0
        )

        context["total_price"] = total_price
        context["total_price_include_shipping"] = total_price + 5
        context["total_item"] = total_item
        context["total_quantity"] = total_quantity
        return context
    
class DishFilter(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        menu_items = MenuItem.objects.filter(categories=category)

        # Tạo context với category và menu_items
        context = {
            'category': category,
            'menu_items': menu_items
        }
        # Trả về context trong render
        return render(request, 'dishes/filter.html', context)
