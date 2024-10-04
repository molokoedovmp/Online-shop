from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from shop.models import ProductProxy

from .cart import Cart


def cart_view(request):
    cart = Cart(request)

    context = {
        'cart': cart
    }

    return render(request, 'cart/cart-view.html', context)


def cart_add(request):
    """Add a product to the shopping cart.
    
    Args:
        request (HttpRequest): The HTTP request object containing POST data.
    
    Returns:
        JsonResponse: A JSON response containing the updated cart quantity and added product title.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(ProductProxy, id=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, "product":product.title})

        return response

def cart_delete(request):
    """Handles the deletion of a product from the shopping cart.
    
    Args:
        request (HttpRequest): The HTTP request object containing POST data.
    
    Returns:
        JsonResponse: A JSON response containing updated cart quantity and total price.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)
        
        cart_qty = cart.__len__()
        
        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})

        return response

def cart_update(request):
    """Updates the shopping cart based on the provided request.
    
    Args:
        request (HttpRequest): The HTTP request object containing POST data.
    
    Returns:
        JsonResponse: A JSON response containing updated cart quantity and total price.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})

        return response