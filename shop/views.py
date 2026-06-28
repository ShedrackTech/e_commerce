from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddProductForm
from .models import Category, Product
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView
)
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .forms import SignUpForm, LoginForm, UserUpdateForm
from cart.cart import Cart
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage

@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')   # already logged in
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in right after registration
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,
                f'Welcome, {user.get_full_name()}! Your account is ready.')
            return redirect('shop:product_list')
    else:
        form = SignUpForm()
    return render(request, 'shop/register.html', {'form': form})

class ShopLoginView(LoginView):
    form_class        = LoginForm
    template_name     = 'shop/login.html'
    redirect_authenticated_user = True
    def form_valid(self, form):
        # Migrate anonymous cart to authenticated user
        response = super().form_valid(form)
        messages.success(self.request,f'Welcome back, {self.request.user.get_full_name()}!')
        return response
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)

class ShopLogoutView(LogoutView):
    next_page = 'shop:login'
    def dispatch(self, request, *args, **kwargs):
        # Clear the cart session on logout
        if settings.CART_SESSION_ID in request.session:
            del request.session[settings.CART_SESSION_ID]
        messages.info(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('shop:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    cart = Cart(request)
    return render(request, 'shop/profile.html', {
        'form': form,
        'cart': cart,
    })

class ShopPasswordChangeView(PasswordChangeView):
    template_name   = 'shop/password_change.html'
    success_url     = reverse_lazy('shop:password_change_done')
    def form_valid(self, form):
        messages.success(self.request,
            'Your password has been changed successfully.')
        return super().form_valid(form)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)

def about(request):
    return render(request, 'shop/about.html')

def privacy(request):
    return render(request, 'shop/privacy.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Persist to the database
            ContactMessage.objects.create(
                name    = form.cleaned_data['name'],
                email   = form.cleaned_data['email'],
                subject = form.cleaned_data['subject'],
                message = form.cleaned_data['message'],
            )

            # Optional: send a notification email to your team
            # from django.core.mail import send_mail
            # send_mail(
            #     subject  = f"[Contact] {form.cleaned_data['subject']}",
            #     message  = f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
            #                f"{form.cleaned_data['message']}",
            #     from_email = settings.DEFAULT_FROM_EMAIL,
            #     recipient_list = [settings.CONTACT_EMAIL],
            # )

            messages.success(request, "Message sent! We'll be in touch soon.")
            return redirect('shop:contact')
    else:
        # Pre-fill email if the user is logged in
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
        form = ContactForm(initial=initial)

    return render(request, 'shop/contact.html', {'form': form})