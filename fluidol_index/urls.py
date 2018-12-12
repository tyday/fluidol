from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    
]
#Add Django site authentication urls ( for login, logout, password management)
urlpatterns += [ path('accounts/', include('django.contrib.auth.urls')),]