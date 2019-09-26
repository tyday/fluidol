from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
class Product_benefits(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Product_features(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Product_applications(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
       
class Product(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, null=True)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    main_photo = models.ImageField(null=True,blank=True)
    main_photo_description = models.CharField(max_length=100, null=True,blank=True)
    optional_photo_one = models.ImageField(null=True,blank=True)
    optional_photo_one_description = models.CharField(max_length=100, null=True,blank=True)
    optional_photo_two = models.ImageField(null=True,blank=True)
    optional_photo_two_description = models.CharField(max_length=100, null=True,blank=True)
    Product_benefits = models.ManyToManyField(Product_benefits, blank=True)
    Product_features = models.ManyToManyField(Product_features, blank=True)
    Product_applications = models.ManyToManyField(Product_applications, blank=True)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])