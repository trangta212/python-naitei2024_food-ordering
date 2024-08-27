import json
import uuid
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from django.views import View, generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
import random
from .tokens import account_activation_token 
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode



from app.forms import SignUpForm, LogInForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F
from django.db import transaction, models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import (
    Category,
    MenuItem,
    Cart,
    Order, OrderItem, Profile, User,
    CartItem,
    OrderItem,
    Profile,
    Order,
    Payment,
)
from .constants import (
    TOP_RATED_ITEMS_LENGTH,
    CART_VIEW_PAGINATE,
    SHIPPING,
    HIGHLIGHT_DISH,
    HIGHLIGHT_DISH_IMG,
)


def index(request):
    """View function for home page of site."""

    top_rated_items = MenuItem.objects.order_by("-rate_avg")[
        :TOP_RATED_ITEMS_LENGTH
    ]

    highlight_categories = Category.objects.filter(
        category_name__in=HIGHLIGHT_DISH
    )
    category_ids = {
        category.category_name: category.category_id
        for category in highlight_categories
    }
    category_img = dict(zip(HIGHLIGHT_DISH, HIGHLIGHT_DISH_IMG))
    categories_info = {
        name: {
            "id": category_ids.get(name, None),
            "img": category_img.get(name, None),
        }
        for name in HIGHLIGHT_DISH
    }
    context = {
        "popular_items": top_rated_items,
        "categories_info": categories_info,
    }
    return render(request, "index.html", context=context)


User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            activateEmail(request, new_user, form.cleaned_data.get("email"))
            messages.success(request, _("Account created successfully! Please check your email to activate your account."))
            return redirect("app:index")
        else:
            for error in form.errors:
              messages.error(request, _(error))
    else:  
        form = SignUpForm()
    context = {
        "form": form,
    }
    return render(request, "registration/sign-up.html", context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  
        messages.success(request, _("Account activated successfully"))
        return redirect("app:index")  
    else:
        messages.error(request, _("Activation link is invalid!"))
        return redirect("app:index") 


def activateEmail(request, new_user, email):
    mail_subject = 'Activate your account'
    message = render_to_string("registration/acctivate_account.html", {
        "user": new_user.username,
        "domain": get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
        'token': account_activation_token.make_token(new_user),
        "protocol": "https" if request.is_secure() else "http",
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        messages.success(request, _("Dear {name}, your account has been created successfully. Please check your email to activate your account.").format(name=new_user.username))
    else:
        messages.error(request, _("Error sending email. Please try again."))


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except Exception:
            messages.warning(request, _(f"User with {email} does not exist"))

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _("Logged in"))
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect("app:index")
        else:
            messages.warning(request, _("User does not exist."))

    context = {}

    return render(request, "registration/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("app:login")


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
            "item_id": item_id,
        }
        return render(request, "dishes/detail.html", context)


def search_view(request):
    query = request.GET.get("q")  # Search by name
    category_id = request.GET.get("category")  # Filter by category
    price_order = request.GET.get("price_order")  # Sort by price

    items = MenuItem.objects.all()

    if query:
        items = MenuItem.objects.filter(
            name__icontains=query
        ) | MenuItem.objects.filter(description__icontains=query)
    categories = Category.objects.all()

    if category_id:
        items = items.filter(categories=category_id)

    if price_order:
        if price_order == "asc":
            items = items.order_by("price")
        elif price_order == "desc":
            items = items.order_by("-price")

    context = {
        "items": items,
        "query": query,
        "categories": categories,
    }
    return render(request, "search/search.html", context)


@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        user = request.user

        cart, created = Cart.objects.get_or_create(user=user)

        item = get_object_or_404(MenuItem, item_id=item_id)

        if item.quantity == 0:
            return JsonResponse(
                {"status": "failed", "message": _("Item sold out")}, status=400
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item, defaults={"quantity": 1}
        )

        if not created and cart_item.quantity < item.quantity:
            cart_item.quantity += 1

        cart_item.save()

        return JsonResponse({"status": _("success")})
    return JsonResponse({"status": _("failed")}, status=400)


@csrf_exempt
@login_required
def update_cart(request):
    try:
        data = json.loads(request.body)
        user = request.user
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


class CartView(LoginRequiredMixin, generic.ListView):
    """View function for home page of site."""

    paginate_by = CART_VIEW_PAGINATE
    context_object_name = "cart_items"

    def get_queryset(self):
        user = self.request.user
        if user:
            return CartItem.objects.filter(cart__user=user)
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
        context["total_price_include_shipping"] = total_price + SHIPPING
        context["total_item"] = total_item
        context["total_quantity"] = total_quantity
        return context


class DishFilter(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        menu_items = MenuItem.objects.filter(categories=category)

        # Tạo context với category và menu_items
        context = {"category": category, "menu_items": menu_items}
        # Trả về context trong render
        return render(request, "dishes/filter.html", context)


class OrderView(LoginRequiredMixin, generic.ListView):
    """View function for home page of site."""

    paginate_by = CART_VIEW_PAGINATE
    context_object_name = "order_items"

    def get_queryset(self):
        order_id = self.kwargs["order_id"]
        user = self.request.user

        if Order.objects.get(order_id=order_id).user.user != user:
            return JsonResponse(
                {
                    "error": _(
                        "You do not have permission to cancel this order."
                    )
                },
                status=403,
            )

        if user:
            return OrderItem.objects.filter(order__order_id=order_id)
        else:
            return OrderItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        order = Order.objects.filter(user=profile).first()

        context["order_id"] = self.kwargs["order_id"]
        context["user_name"] = profile.name

        context["total_price"] = order.total_price
        context["total_price_include_shipping"] = order.total_price + SHIPPING
        return context


@login_required
def create_order(request):
    if request.method == "POST":
        try:
            user = request.user
            cart = Cart.objects.filter(user=user).first()
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart or not cart_items:
                return JsonResponse(
                    {"error": _("Cart is not found")}, status=400
                )

            profile = Profile.objects.get(user=user)

            next_payment_id = str(uuid.uuid4())
            payment = Payment.objects.create(
                payment_id=next_payment_id,
                payment_date=timezone.now(),
                amount=0,
                method="Credit Card",
            )

            restaurant = cart_items.first().item.restaurant
            if not restaurant:
                return JsonResponse(
                    {"error": _("Restaurant not found")}, status=400
                )

            order = Order.objects.create(
                user=profile,
                restaurant=restaurant,
                total_price=0,
                status="Pending",
                payment=payment,
            )

            total_price = 0
            order_items = []

            for cart_item in cart_items:
                item_price = cart_item.item.price * cart_item.quantity
                total_price += item_price
                if cart_item.item.quantity < cart_item.quantity:
                    order.delete()
                    cart_item.quantity = cart_item.item.quantity
                    return JsonResponse(
                        {"error": _("Insufficient product quantity")},
                        status=500,
                    )

                order_item = OrderItem(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=item_price,
                )
                order_items.append(order_item)

                cart_item.item.quantity -= cart_item.quantity
                cart_item.item.save()

            with transaction.atomic():
                OrderItem.objects.bulk_create(order_items)
                order.total_price = total_price
                payment.amount = total_price
                payment.save()
                order.save()

                cart_items.all().delete()

            return JsonResponse(
                {
                    "order_id": order.order_id,
                    "status": _("Order created successfully"),
                },
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@login_required
def cancel_order(request):
    if request.method == "POST":
        try:
            user = request.user
            data = json.loads(request.body)
            order_id = data.get("order_id")
            order = Order.objects.get(order_id=order_id)
            items = OrderItem.objects.filter(order=order)

            if order.user.user != user:
                return JsonResponse(
                    {
                        "error": _(
                            "You do not have permission to cancel this order."
                        )
                    },
                    status=403,
                )

            if order.status == "Pending":
                for item in items:
                    menu_item = item.item
                    menu_item.quantity += item.quantity
                    menu_item.save()

                items.delete()
                order.delete()

                return JsonResponse(
                    {
                        "order_id": order_id,
                        "success": True,
                        "status": _("Order has been canceled successfully"),
                    },
                    status=200,
                )

            else:
                return JsonResponse(
                    {
                        "error": _(
                            "Order cannot be canceled as it is not in Pending status."
                        ),
                    },
                    status=400,
                )

        except Order.DoesNotExist:
            return JsonResponse({"error": _("Order not found")}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@login_required
def order_history(request):
    user_profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(user=user_profile).order_by('-order_id')
    order_items = OrderItem.objects.filter(order__in=orders)
    context = {
        'orders': orders,
        'order_items': order_items
    }
    return render(request, 'app/order_history.html', context)
def forgot_password(request):
    return render(request, 'registration/forgot_password.html')

def send_otp(request):
    error_message = None
    otp = random.randint(11111, 99999)
    email = request.POST.get('email')
    user_email = User.objects.filter(email=email)
    
    if user_email.exists():
        user = user_email.get()
        user.otp = otp
        user.save()
        request.session['email'] = email
        html_message = _("Your One Time Password is {otp}").format(otp=otp)
        subject = 'Welcome to Food Ordering'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email]
        message = EmailMessage(subject, html_message, email_from, email_to)
        message.send()
        messages.success(request, 'OTP has been sent to your email')
        return redirect('app:enter_otp')  
    else:
        error_message = 'Email does not exist'
        return render(request, 'registration/forgot_password.html', {'error': error_message})
    
def enter_otp(request):
    error_message = None
    if 'email' in request.session:
        email = request.session['email']
        user = User.objects.get(email=email)
        user_otp = user.otp
        
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if not otp:
                error_message = 'OTP is required'
            elif otp != str(user_otp):
                error_message = 'Invalid OTP'
            
            if not error_message:
                return redirect('app:password_reset')  
            
            return render(request, 'registration/enter_otp.html', {'error': error_message})
        
        return render(request, 'registration/enter_otp.html')
    
    return redirect('app:forgot_password')


User = get_user_model()
def password_reset(request):
    error_message = None
    if 'email' in request.session:
        email = request.session['email']
        user = get_object_or_404(User, email=email)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            
            if not new_password:
                error_message = 'Enter new password'
            elif not confirm_new_password:
                error_message = 'Enter Confirm New Password'
            elif new_password != confirm_new_password:
                error_message = 'Passwords do not match'
            elif user.check_password(new_password):  
                error_message = 'This password is already used'
            if not error_message:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful')
                
                user = authenticate(email=email, password=new_password)
                if user is not None:
                    login(request, user)
                    return redirect('app:index')  
                else:
                    messages.error(request, 'Unable to log in with new password')
        
        return render(request, 'registration/password_reset.html', {'error': error_message})
    
    return redirect('app:forgot_password')
