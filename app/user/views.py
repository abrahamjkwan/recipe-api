from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """"Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # set the renderer so we can view the endpoint in the browser
    # with the browsable api
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # we are overriding the get_object, typically with an API view
    # you would link to model retrieve database items
    def get_object(self):
        """Retrieve and return authenticated user"""
        # with authentication_class, user is assigned to request
        return self.request.user
