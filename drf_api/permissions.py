"""
File used to create custom permissions
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Overrides the base permissions through the use of has_object_permission function
    see: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

    """
    def has_object_permission(self, request, view, obj):
        """ 
        Checks if the method being called in the request is in the SAFE_METHODS tuple
        which includes GET, HEAD and OPTIONS. If it is then True returned allowing the request to 
        go ahead as no changes to the data are being made. 
        If not then the request can only go ahead (return True) if the owner of the object is the user
        making the request.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user