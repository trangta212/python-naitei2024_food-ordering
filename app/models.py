from django.db import models
from django.contrib.auth.models import AbstractUser
from . import constants


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=constants.ROLE_LENGTH)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=constants.NAME_LENGTH)
    email = models.EmailField()
    phone_number = models.CharField(max_length=constants.PHONE_LENGTH)
    address = models.CharField(max_length=constants.ADDRESS_LENGTH)
    profile_type = models.CharField(max_length=constants.PROFILE_TYPE_LENGTH)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_url = models.URLField(
        max_length=constants.URL_LENGTH, null=True, blank=True
    )
    opening_hours = models.JSONField(
        null=True,
        blank=True,
    )


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=constants.CATEGORY_NAME_LENGTH)
    description = models.CharField(
        max_length=constants.DESCROPTION_LENGTH, null=True, blank=True
    )

    def __str__(self):
        return self.category_name


class MenuItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=constants.NAME_LENGTH)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=constants.PRICE_MAX_DIGITS,
        decimal_places=constants.PRICE_DECIMAL_PLACES,
    )
    categories = models.ManyToManyField(Category)
    image_url = models.URLField(
        max_length=constants.URL_LENGTH, null=True, blank=True
    )
    rate_avg = models.DecimalField(
        max_digits=constants.RATE_AVG_MAX_DIGITS,
        decimal_places=constants.RATE_AVG_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_id = models.CharField(
        max_length=constants.PAYMENT_ID_LENGTH, primary_key=True
    )
    payment_date = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=constants.AMOUNT_MAX_DIGITS,
        decimal_places=constants.AMOUNT_DECIMAL_PLACES,
    )
    method = models.CharField(max_length=constants.METHOD_LENGTH)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_price = models.DecimalField(
        max_digits=constants.PRICE_MAX_DIGITS,
        decimal_places=constants.PRICE_DECIMAL_PLACES,
    )
    status = models.CharField(max_length=constants.STATUS_LENGTH)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=constants.PRICE_MAX_DIGITS,
        decimal_places=constants.PRICE_DECIMAL_PLACES,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "item"], name="unique_order_item"
            )
        ]


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE
    )
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ("cart", "item")


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
