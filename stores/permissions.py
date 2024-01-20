from rest_framework.permissions import BasePermission
from profiles.models import Vendor

class IsVendorUser(BasePermission):
    """
    Custom permission to check if the user is a valid vendor.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            id = request.user.id
            try:
                vendor = Vendor.objects.filter(user_id=id)
                return True
            except:
                return False


