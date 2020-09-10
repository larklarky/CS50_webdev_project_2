from django.contrib import admin

# Register your models here.
from .models import User, Listing, Category, Comment, Bid, Wishlist


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'valid_until' )

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'bid')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Wishlist, WishlistAdmin)