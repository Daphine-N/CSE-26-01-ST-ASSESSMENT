from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def landing(request):
    """Landing page"""
    return render(request, 'landing.html')

def dashboard(request):
    """Main dashboard with form and product table"""
    products = Product.objects.all()
    
    # Dummy statistics exactly as in your image
    stats = {
        'sales': 'UGX 50,000,000',
        'orders': 'UGX 15,000,000',
        'in_stock': 'UGX 42,000,000',
        'out_of_stock': '5',
    }
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f' Product "{product.name}" saved successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, ' Please fix the errors below.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'products': products,
        'stats': stats,
    }
    
    return render(request, 'dashboard.html', context)

