from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    """
    Class to contain all the tests associated with the PostList view
    """
    def setUp(self):
        """
        What information to we need stored in the database so that
        we can run the required tests.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        """
        This test first creates a post associated with the test user set-up in the DB (the context)
        It then sends a request to the DB, mimicking a real HTTP request (the when)
        It expects a specific response back (the then). If this line of code is true the test will pass.
        Finally it prints some key info to the console so that the developer can see exactly what has happend
        """
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assertEqual takes tow parameters the variable and what the variable should be equal too
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        """
        The context: DB user Adam is logged in
        The when: HTTP post request to create a new post
        The then: Response post.data, status=status.HTTP_201_CREATED
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
        print(count)

    def test_logged_out_user_can_not_create_post(self):
        """
        The context: No logged in user
        The when: HTTP post request to create a new post
        The then: Response errors, status=status.HTTP_400_BAD_REQUEST
        """
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(response.data)
        print(count)
