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