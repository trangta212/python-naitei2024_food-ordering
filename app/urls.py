from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu_view, name='menu'),
    path(
        'dish/<int:item_id>/',
        views.DishDetail.as_view(),
        name='dish_detail'
    ),
    path('dishfilter/<int:category_id>/',
         views.DishFilter.as_view(),
         name='dish_filter'),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
]
