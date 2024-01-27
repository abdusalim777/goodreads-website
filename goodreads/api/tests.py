from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPIViewTestCase(APITestCase):
    def setUp(self):
        # DRY don't repeat yourself
        self.user = CustomUser.objects.create(username='abdusalimjon', first_name='abdusalimbe')
        self.user.set_password('1234')
        self.user.save()
        self.client.login(username='abdusalimjon', password='1234')

    def test_book_review_detail(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='1212325')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice')

        response = self.client.get(reverse('api:review_detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)

        self.assertEqual(response.data['comment'], 'nice')
        # self.assertEqual(response.data['book']['id'], br.book.id)
        # self.assertEqual(response.data['book']['title'], 'Book1')
        # self.assertEqual(response.data['book']['description'], 'description1')
        # self.assertEqual(response.data['book']['isbn'], '1212325')

    def test_delete_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='1212325')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice')

        response = self.client.delete(reverse('api:review_detail', kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='1212325')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice')

        response = self.client.patch(reverse('api:review_detail', kwargs={"id": br.id}), data={'stars_given': 3})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 3)

    def test_put_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='1212325')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice')

        response = self.client.patch(
            reverse('api:review_detail', kwargs={"id": br.id}),
            data={'stars_given': 4, 'comment': 'nice book new', 'user_id': self.user.id, 'book_id': book.id})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book new')


    def test_create_review(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='1212325')

        data = {
            'stars_given': 2,
            'comment': 'bad book',
            'user_id': self.user.id,
            'book_id': book.id
        }

        response = self.client.post(reverse('api:review_list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 2)
        self.assertEqual(br.comment, 'bad book')



    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='abdusalim', first_name='abdusalim')
        book = Book.objects.create(title='Book1', description='description1', isbn='1212325')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='nice')
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=5, comment='not good')

        response = self.client.get(reverse('api:review_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
