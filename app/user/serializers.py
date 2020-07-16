from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {
            'write_only': True,
            'min_length': 8,
            'style': {'input_type': 'password'}, }}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly, return it"""
        # instance is model instance from serializer, user object
        # validated data is the fields that have been through validation

        # remove password from validated data
        # none is because users can optionally not leave a password
        password = validated_data.pop('password', None)

        # super allows us to call the default update function
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        # anytime you override the validate function, must return values
        # once the validation is successful
        return attrs
