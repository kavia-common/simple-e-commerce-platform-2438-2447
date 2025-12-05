from django.db import models
from django.contrib.auth.models import AbstractUser

# PUBLIC_INTERFACE
class CustomUser(AbstractUser):
    """Custom user model to allow customization for customer info."""
    email = models.EmailField(unique=True)
    # Add other custom user attributes here if needed

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# PUBLIC_INTERFACE
class Product(models.Model):
    """Product available for purchase."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# PUBLIC_INTERFACE
class Cart(models.Model):
    """Shopping cart, one per user."""
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name='cart')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s Cart"

# PUBLIC_INTERFACE
class CartItem(models.Model):
    """An item in a shopping cart."""
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# PUBLIC_INTERFACE
class Order(models.Model):
    """Order placed by a user."""
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # Extend in real app

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"

# PUBLIC_INTERFACE
class OrderItem(models.Model):
    """Each item in an Order."""
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at order time

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
