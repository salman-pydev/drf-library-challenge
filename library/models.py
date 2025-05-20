from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField()

    def __str__(self):
        return self.name


class Reviewer(models.Model):
    name = models.CharField(max_length=100, unique=True)



class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    favorite_reviewers = models.ManyToManyField(Reviewer, blank=True)

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None

    @property
    def is_poorly_rated(self):
        avg = self.average_rating
        return avg is not None and avg < 2

    def __str__(self):
        return self.title



class Review(models.Model):
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.rating == 5:
            reviewer, _ = Reviewer.objects.get_or_create(name=self.reviewer_name)
            self.book.favorite_reviewers.add(reviewer)
