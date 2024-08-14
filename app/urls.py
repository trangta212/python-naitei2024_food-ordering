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
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
