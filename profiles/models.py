from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    """ 
    Model for User Profile data 
    Django's inbuilt User model used for base User data
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)#Set on creation only
    updated_at = models.DateTimeField(auto_now=True)#Updated every time the instance is saved
    name = models.CharField(max_length=225, blank=True)#blank=True allows this field to be optional
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_yzfpjq'
        )
    
    class Meta:
        """
        Model Meta is the inner class of the model. 
        It is used to change the behaviour of your model fields, for example:
        changing order options.
        It is completely optional.
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        A Dunder string method:
        This allows the object to be converted into a string representation.
        It is then called whenever you call str() on an object,
        which Django does in a number of places and so this is an important method to always include
        """
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Called by post_save after a user instance is saved.
    post_save.connect requires the arguments:
    sender model, it's instance, created (a boolean value of whether 
    the instance has just been created or not) and kwargs.
    """
    if created:
        Profile.objects.create(owner=instance)

post_save.connect(create_profile, sender=User)
"""
This uses the signal post_save running the given function when
the given sender is saved.
"""
