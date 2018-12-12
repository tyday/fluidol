from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    main_photo = models.ImageField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])