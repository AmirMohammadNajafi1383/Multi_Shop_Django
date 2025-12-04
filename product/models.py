from django.db import models

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs',blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category,blank=True,null=True)
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.SmallIntegerField()
    image = models.ImageField(upload_to='products')
    color = models.ManyToManyField(Color,blank=True,related_name='products')
    size = models.ManyToManyField(Size,related_name='products')

    def __str__(self):
        return self.title


# Create your models here.
class Information(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE,related_name='informations')

    def __str__(self):
        return self.text[:30]