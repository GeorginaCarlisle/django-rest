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
        #print(response.data)
        #print(len(response.data))

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
        #print(response.data)
        #print(count)

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
        #print(response.data)
        #print(count)


class PostDetailViewTests(APITestCase):
    """
    Class to contain all the tests associated with the PostDetail view
    """
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        james = User.objects.create_user(username='James', password='word')
        Post.objects.create(
            owner=adam, title='Adams title', content='Adams content')
        Post.objects.create(
            owner=james, title='James title', content='James content')

    def test_can_retrieve_valid_post(self):
        """
        Context: As set-up
        When: HTTP get request to access post with id 1, which is Adams post
        Then: Adams post return in response along with status code 200
        """
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['owner'], 'adam')
        self.assertEqual(response.data['title'], 'Adams title')
        self.assertEqual(response.data['content'], 'Adams content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
    
    def test_invalid_post_request_handled(self):
        """
        Context: As set-up
        When: HTTP get request to access post with id 3, which doesn't exist
        Then: response status code 404
        """
        response = self.client.get('/posts/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        #print(response.data)
    
    def test_user_update_their_post(self):
        """
        context: Adam logged in
        When: HTTP put request to update post id 1, which is Adams post
        Then: Changes saved to DB and respose status 200
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'Title changed'})
        adamsPost = Post.objects.filter(pk=1).first()
        self.assertEqual(adamsPost.title, 'Title changed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_user_denied_update_others_post(self):
        """
        context: James logged in
        When: HTTP put request to update post id 1, which is Adams post
        Then: Error status code 403
        """
        self.client.login(username='james', password='word')
        response = self.client.put('/posts/1/', {'title': 'Title changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #print(response.status_code)
    
    def test_user_delete_their_post(self):
        """
        context: Adam logged in
        When: HTTP delete request to update post id 1, which is Adams post
        Then: Changes saved to DB and respose status 200
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/posts/1/')
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_user_denied_delete_others_post(self):
        """
        context: James logged in
        When: HTTP delete request to update post id 1, which is Adams post
        Then: No posts deleted. Error respose status 403
        """
        self.client.login(username='james', password='word')
        response = self.client.delete('/posts/1/')
        count = Post.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    