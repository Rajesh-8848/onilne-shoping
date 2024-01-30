from .models import *
import json
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Cat, Products
from .models import cart  # Import the cart model

def home(request):
    cat = Cat.objects.all()
    pro = Products.objects.all()

    # Get the cart items count for the logged-in user
    cart_items_count = 0  # Default value
    if request.user.is_authenticated:
        cart_items_count = cart.objects.filter(user=request.user).count()

    context = {
        'pro': pro,
        'cat': cat,
        'cart_items_count': cart_items_count,
    }

    return render(request, 'index.html', context)

def category_details(request):
    Products = get_object_or_404(Cat, slug=category_slug)

    # Number of products per page

    return render(request, 'all.html', {'products': products,})


def products_by_category(request, category_slug=None):
    # Get all products
    products = Products.objects.all()

    # Initialize selected_category variable
    selected_category = 'All'

    # Filter products by category if category_slug is provided
    if category_slug and category_slug != 'All':
        category = get_object_or_404(Cat, slug=category_slug)
        products = products.filter(category=category)
        selected_category = category.name

    # Convert to list and sort by the primary key (you can use another field)
    products = list(products)
    products = sorted(products, key=lambda x: x.id)

    # Pagination
    items_per_page = 6
    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page', 1)

    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    # Pass the paginated products and selected_category to the context
    context = {'products': products_paginated, 'categories': Cat.objects.all(), 'selected_category': selected_category}

    return render(request, 'All.html', context)

class ProductDetailView(DetailView):
    model = Products
    template_name = 'one_product.html'
    context_object_name = 'i'
    slug_url_kwarg = 'product_slug'


def searching(request):
    prod = None
    query = None
    no_results_message = ""
    no_results_button = ""

    if 'q' in request.GET:
        query = request.GET.get('q').strip()

        if not query:
            no_results_button = "Please enter a valid search query."
        else:
            prod = Products.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
            if not prod:
                no_results_message = "No matching products found."

    # Check if prod is not None before trying to paginate
    if prod is not None:
        # Pagination
        paginator = Paginator(prod, 10)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None

    context = {
        'qr': query,
        'pr': page_obj,
        'no_results_message': no_results_message,
        'no_results_button': no_results_button,
    }

    return render(request, 'search.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomLoginForm

from django.contrib.auth import authenticate, login


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
# your_app/views.py

def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = RegistrationForm()

    return render(request, 'Register.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_str = request.POST.get('quantity', '1')  # Default to '1' if not provided
        quantity = int(quantity_str)

        # Assuming 'Products' is your product model
        product = Products.objects.get(id=product_id)

        # Calculate total_price based on product price and quantity
        total_price = product.price * quantity

        # Create or update the cart item
        cart_item, created = cart.objects.get_or_create(
            user=request.user,  # Assuming you have a user associated with the cart
            name=product,
            defaults={'quantity': quantity, 'price': product.price, 'total_price': total_price, 'image': product.img}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.total_price = product.price * cart_item.quantity  # Update total_price
            cart_item.save()

        messages.success(request, f'{product.name} added to cart.')
        return redirect('home')  # Replace 'home' with the actual view name

    # Handle other cases or return an appropriate response
    return render(request, 'cart.html')
from django.shortcuts import render
from .models import cart

def view_cart(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to view your cart.')
        return redirect('login')  # Replace 'login' with your actual login URL name
    cart_items = cart.objects.filter(user=request.user).select_related('name')
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)

@login_required
def update_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        action = request.POST.get('action')

        try:
            # Ensure that the CartItem belongs to the current user
            item = cart.objects.get(id=item_id, user=request.user)
        except cart.DoesNotExist:
            messages.error(request, "Item not found in the cart.")
            return redirect('viewcart')

        item.quantity = quantity
        item.total_price = item.price * quantity
        item.save()
        messages.success(request, "Cart updated successfully.")
        print("Cart updated successfully")

        return redirect('viewcart')

    else:
        messages.error(request, "Invalid request.")
        return redirect('viewcart')

@login_required
def delete_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        # Ensure that the CartItem belongs to the current user
        cart_item = get_object_or_404(cart, id=item_id, user=request.user)

        # Delete the cart item
        cart_item.delete()

        messages.success(request, "Item deleted successfully.")
        return redirect('viewcart')
    else:
        messages.error(request, "Invalid request.")
        return redirect('viewcart')