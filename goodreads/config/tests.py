from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Sport', description='description1', isbn='1212325')

        user = CustomUser.objects.create(
            username='abdusalimjon',
            first_name='abdusalimbe',
            last_name='shoirjonov',
            email='sayitqulov@gmail.com'
        )
        user.set_password('12345')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='nice book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment='nice!')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='useful book')

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)