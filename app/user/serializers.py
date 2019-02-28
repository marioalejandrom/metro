from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """Public serializer for the users object.
    May be used in other model serializers"""

    class Meta:
        model = User
        fields = ('id', 'username',)


class UserRegisterSerializer(serializers.ModelSerializer):
    """Registration serializer for the users object"""

    class Meta:
        model = User
        fields = ('email',
                  'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Profile serializer for user management activities"""

    class Meta:
        model = User
        fields = ('email',
                  'password',
                  'username',
                  'first_name',
                  'last_name',)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
