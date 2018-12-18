from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'nombres',
            'apellidos',
            'tipo'
        )


# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'password',
#             'first_name',
#             'last_name',
#             'gender',
#             'address',
#             'phone',
#             'birth_date',
#             'groups',
#         )

#     def create(self, validated_data):
#         user = super(UserCreateSerializer, self).create(validated_data)
#         user.set_password(validated_data.get('password'))
#         user.save()
#         return user
