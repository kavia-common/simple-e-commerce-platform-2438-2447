from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer, UserSerializer, RegisterSerializer,
    CartSerializer, OrderSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(generics.CreateAPIView):
    """User Registration endpoint."""
    serializer_class = RegisterSerializer

    permission_classes = [permissions.AllowAny]


# PUBLIC_INTERFACE
class UserProfileView(generics.RetrieveAPIView):
    """Get profile of logged in user."""
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# PUBLIC_INTERFACE
class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for products (CRUD)."""
    queryset = Product.objects.all().order_by('-created')
    serializer_class = ProductSerializer

    permission_classes = [permissions.AllowAny]


# PUBLIC_INTERFACE
class CartView(APIView):
    """Retrieve and update cart of current user."""

    permission_classes = [permissions.IsAuthenticated]

    # PUBLIC_INTERFACE
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # PUBLIC_INTERFACE
    def post(self, request):
        # Add or update a cart item; expects {product_id, quantity}
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = quantity
        item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # PUBLIC_INTERFACE
    def delete(self, request):
        # Remove item from cart; expects {product_id}
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        CartItem.objects.filter(cart=cart, product=product).delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

# PUBLIC_INTERFACE
class OrderViewSet(viewsets.ModelViewSet):
    """Order creation/listing."""
    serializer_class = OrderSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        order = Order.objects.create(user=request.user)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.delete()  # Remove from cart after ordering
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
