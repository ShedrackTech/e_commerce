from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Link to logged-in user if authenticated
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        # Pre-fill form from user profile if logged in
        initial = {}
        if request.user.is_authenticated:
            u = request.user
            initial = {
                'first_name': u.first_name,
                'last_name':  u.last_name,
                'email':      u.email,
                'address':    u.address,
                'postal_code': u.postal_code,
                'city':       u.city,
            }
        form = OrderCreateForm(initial=initial)
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/detail.html', {'order': order})