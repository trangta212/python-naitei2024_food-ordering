from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "app"

urlpatterns = [
    path('', views.index, name='index'),
    
    path("sign-up/", views.register_view, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
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
]
