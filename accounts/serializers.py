from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)

    class Meta:
        model = User
        fields = ['email','name', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def create(self,validated_data):
        # Extract validated data
        email = validated_data["email"]
        name = validated_data["name"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        # Check if the passwords match
        if password != password2:
            raise serializers.ValidationError({'password':"passwords do not match"})
        
        # Create and save the user
        user = User(email=email,name=name)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','phone']