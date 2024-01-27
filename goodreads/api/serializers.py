from rest_framework import serializers

from books.models import Book, BookReview
from users.models import CustomUser


# class BookSerializer(serializers.Serializer):
#     itle = serializers.CharField(max_length=200)
#     description = serializers.CharField()
#     isbn = serializers.CharField(max_length=17)
#     cover_picture = serializers.ImageField(default='default_cover_pic.jpg')


# class UserSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=200)
#     last_name = serializers.CharField(max_length=200)
#     username = serializers.CharField(max_length=200)
#     email = serializers.CharField(max_length=255)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'user', 'book', 'user_id', 'book_id')
