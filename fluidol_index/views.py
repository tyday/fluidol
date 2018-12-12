from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import Product
# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

class ProductListView(generic.ListView):
    model = Product
class ProductDetailView(generic.DetailView):
    model=Product
# def product_detail_view(request, primary_key):
#     try:
#         product = Product.objects.get(pk=primary_key)
#     except Product.DoesNotExist:
#         raise Http404('Product does not exist')
    
#     return render(request, 'catalog/product_detail.html', context={'product':product})