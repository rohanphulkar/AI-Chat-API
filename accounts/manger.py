from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email,name, password=None):
        if not email:
            raise ValueError("Email is required")
        if not name:
            raise ValueError("Name is required")
        if not password:
            raise ValueError("Password is required")
        
        user = self.model(
            email = self.normalize_email(email),
            name=name
        )

        user.set_password(password)

        user.save()

        return user
    
    def create_superuser(self, email,name, password=None):

        if not email:
            raise ValueError("Email is required")
        if not name:
            raise ValueError("Name is required")
        if not password:
            raise ValueError("Password is required")
        
        user = self.create_user(email=email, password=password,name=name)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user