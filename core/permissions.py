from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)


class CustomPermission(BasePermission):
    """
    Customize the permission logic for the view.
    Based on the request type, we can determine
    if the user is allowed to access the view.
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.request.method == "GET":
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
