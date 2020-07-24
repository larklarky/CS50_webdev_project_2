from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length = 255, blank = False)
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'children', on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}'

class Listing(models.Model):
    STATUS = [
        ('ACTIVE', 'Active'),
        ('FINISHED', 'Finished')
    ]

    title = models.CharField(max_length = 255, blank = False)
    price = models.DecimalField( blank=False, decimal_places=2, max_digits = 25)
    description = models.TextField()
    image = models.ImageField(upload_to = 'listings')
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    valid_until = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete = models.CASCADE, related_name = 'listings')
    status = models.CharField(max_length = 10, choices = STATUS, default = 'ACTIVE')
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'listings')



class Bid(models.Model):
    bid = models.DecimalField(blank = False, decimal_places=2, max_digits = 25)
    date_created = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'bids')
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE, related_name = 'bids')


class Comment(models.Model):
    comment = models.CharField(max_length = 1000, blank = False)
    date_created = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'comments')
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE, related_name = 'comments')


class Wishlist(models.Model):
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE, related_name = 'wishlist')
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'wishlist')