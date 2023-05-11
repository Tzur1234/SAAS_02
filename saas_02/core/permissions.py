from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


# The methods should return True if the request should be granted access, and False otherwise.

class IsMember(permissions.BasePermission):
    '''
    This permission check if the user send the request is:
    1. Authenticated
    2. Member or in free trial
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_member or request.user.on_free_trial:
                return True
            else:
                raise PermissionDenied(code="The user must be a member / on free trial")
                
        raise PermissionDenied(code="User must be authenticted first!")


