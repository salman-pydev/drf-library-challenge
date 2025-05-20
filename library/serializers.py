
from rest_framework import serializers
from .models import Author, Publisher, Book, Review, Reviewer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    average_rating = serializers.FloatField(read_only=True)
    is_poorly_rated = serializers.BooleanField(read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'publication_date', 'publisher',
            'authors', 'average_rating', 'is_poorly_rated', 'reviews'
        ]

    def get_reviews(self, obj):
        request = self.context.get('request')
        if request and request.query_params.get('include_reviews') == 'true':
            queryset = obj.reviews.all()
            min_rating = request.query_params.get('rating_min')
            max_rating = request.query_params.get('rating_max')
            if min_rating:
                queryset = queryset.filter(rating__gte=int(min_rating))
            if max_rating:
                queryset = queryset.filter(rating__lte=int(max_rating))
            return ReviewSerializer(queryset, many=True).data
        return None
