from django.contrib import admin

# Register your models here.
from .models import User, Listing, Category, Comment, Bid, Wishlist


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Wishlist)