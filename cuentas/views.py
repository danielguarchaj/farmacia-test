from django.views.generic import TemplateView


from rest_framework import generics
from rest_framework import permissions

from .models import User
from .serializers import UserSerializer

class CurrentUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#     permission_classes = (permissions.AllowAny,)