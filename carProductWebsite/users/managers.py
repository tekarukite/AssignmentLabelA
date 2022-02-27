from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
            Creates and saves a user given an email and password
        """
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email) # Put in lowercase the email
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hash the password
        user.save() 

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            Creates and saves a SuperUser given an email and password
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser equal to True')

        return self.create_user(email, password, **extra_fields)

