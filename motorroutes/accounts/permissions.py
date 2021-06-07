from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    """
    If the user is not owner, read and write only allowed
    """
    pass