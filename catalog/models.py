from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', null=True)
    stock = models.PositiveIntegerField(default=10)  # اضافه شد
    available = models.BooleanField(default=True)  # اضافه شد
    created = models.DateTimeField(auto_now_add=True)  # اضافه شد
    updated = models.DateTimeField(auto_now=True)  # اضافه شد
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='books/', blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    # ... بقیه فیلدها

    def get_absolute_url(self):
        return reverse('catalog:book_detail', args=[self.id, self.slug])
