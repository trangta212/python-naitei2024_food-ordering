from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Restaurant


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')
    readonly_fields = ('user_id', 'role')  

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return User.objects.none()

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('name', 'email', 'phone_number', 'address', 'profile_type')
    search_fields = ('name', 'email', 'phone_number', 'address', 'profile_type')
    readonly_fields = ('profile_id', 'user')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return Profile.objects.none()

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class RestaurantAdmin(admin.ModelAdmin):
    model = Restaurant
    list_display = ('restaurant_id', 'profile', 'image_url', 'opening_hours')
    search_fields = ('profile__name', 'image_url')
    readonly_fields = ('restaurant_id', 'profile')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        return Restaurant.objects.none()

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
