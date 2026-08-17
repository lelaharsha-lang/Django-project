from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('app1.User', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='blog_pictures/', null=True, blank=True)
    published = models.BooleanField(default=False)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title 

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null = True,blank = True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey('nike.Author', on_delete=models.CASCADE)
    published_date = models.DateField()
    language = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class BookManager(models.Manager):
        def expensive(self):
            return self.filter(price__gt=350)

    objects = BookManager()