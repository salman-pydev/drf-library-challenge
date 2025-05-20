from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import AuthorViewSet, PublisherViewSet, BookViewSet, ReviewViewSet

# Base router
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

# Nested router for book reviews
books_router = NestedDefaultRouter(router, r'books', lookup='book')
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
]
