from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include

app_name = "app"

urlpatterns = [
    path('', views.index, name='index'),
    
    path("accounts/sign-up/", views.register_view, name="sign-up"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('send_otp', views.send_otp, name='send_otp'),
    path('enter_otp', views.enter_otp, name='enter_otp'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('menu', views.menu_view, name='menu'),
    path(
        'dish/<int:item_id>/',
        views.DishDetail.as_view(),
        name='dish_detail'
    ),
    path('dishfilter/<int:category_id>/',
         views.DishFilter.as_view(),
         name='dish_filter'),
    path('search', views.search_view, name='search'),
    path('add-review/<int:item_id>/', views.add_review, name='add-review'),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('order/<int:order_id>/', views.OrderView.as_view(), name='order'),
    path('create-order/', views.create_order, name='create_order'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('orderhistory/', views.order_history, name='order_history'),
    path('res/order', views.ResOrderView.as_view(), name='res_order'),
]
