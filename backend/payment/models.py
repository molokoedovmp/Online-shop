from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from shop.models import Product

User = get_user_model()


class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"
        ordering = ['-id']

    def __str__(self):
        """
        Returns a string representation of the shipping address.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            str: A string containing "Shipping Address" followed by a hyphen and the full name.
        """
        return "Shipping Address" + " - " + self.full_name

    def get_absolute_url(self):
        """Returns the absolute URL for the shipping payment page.
        
        Args:
            self: The instance of the class containing this method.
"""Creates a default shipping address for a user.

Args:
    user (User): The user object for whom the default shipping address is being created.

Returns:
    ShippingAddress: A new ShippingAddress object with default values.
"""        
        Returns:
            str: A string representing the absolute URL path for the shipping payment page.
        """
        return f"/payment/shipping"

    @classmethod
    def create_default_shipping_address(cls, user):
        default_shipping_address = {"user": user, "full_name": "Noname", "email": "email@example.com",
                                    "street_address": "fill address", "apartment_address": "fill address", "country": ""}
        shipping_address = cls(**default_shipping_address)
        shipping_address.save()
        return shipping_address


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                amount__gte=0), name='amount_gte_0'),
        ]

    def __str__(self):
        """Return a string representation of the Order object.
        
        Args:
            self: The Order instance.
        
        Returns:
            str: A string in the format "Order<id>" where <id> is the order's unique identifier.
        """
        return "Order" + str(self.id)

    def get_absolute_url(self):
        """
        Get the absolute URL for the order detail page.
        
        Args:
            self: Order instance
        
        Returns:
            str: The absolute URL for the order detail page
        """
        return reverse("payment:order_detail", kwargs={"pk": self.pk})

    def get_total_cost_before_discount(self):
        """Calculate the total cost of all items before applying any discount.
        
        Args:
            self: The instance of the class containing this method.
"""
Calculates the discount amount based on the total cost and discount percentage.

Args:
    self: The instance of the class containing this method.

Returns:
    Decimal: The calculated discount amount. Returns 0 if there's no total cost or no discount set.
"""
        
        Returns:
            float: The sum of the costs of all items in the order.
        """
        return sum(item.get_cost() for item in self.items.all())

    @property
    def get_discount(self):
        if (total_cost := self.get_total_cost_before_discount()) and self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        ```
        """Calculate the total cost after applying the discount.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            float: The final total cost after subtracting the discount from the initial total cost.
        """
        ```        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    """
    Returns a string representation of the OrderItem object.
    
    Args:
        self: The instance of the OrderItem class.
    
    Returns:
        str: A string in the format "OrderItem<id>" where <id> is the OrderItem's id.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(check=models.Q(
                quantity__gt=0), name='quantity_gte_0'),
        ]

    def __str__(self):
        return "OrderItem" + str(self.id)

    def get_cost(self):
        """Calculate the total cost of the item.
        
        Args:
            self: The instance of the class containing price and quantity attributes.
        
        Returns:
            float: The total cost, calculated by multiplying price and quantity.
        """
        return self.price * self.quantity

    @property
    def total_cost(self):
        """Calculate the total cost of the item.
        
        Args:
            self: The instance of the class containing price and quantity attributes.
        
        Returns:
            float: The total cost, calculated by multiplying price and quantity.
        """
        return self.price * self.quantity

    @classmethod
    def get_total_quantity_for_product(cls, product):
        """
        Get the total quantity for a specific product.
        
        Args:
            product (Product): The product object for which to calculate the total quantity.
        
        Returns:
            int: The total quantity of the product across all records, or 0 if no records are found.
        """        return cls.objects.filter(product=product).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    @staticmethod
    def get_average_price():
        ```
        """Calculates the average price of all order items.
        
        Args:
            None
        
        Returns:
            float: The average price of all order items in the database.
        """
        
        ```        return OrderItem.objects.aggregate(average_price=models.Avg('price'))['average_price']
