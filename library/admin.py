from django.contrib import admin
from .models import Author, Publisher, Book, Review, Reviewer
# Register your models here.

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Reviewer)
