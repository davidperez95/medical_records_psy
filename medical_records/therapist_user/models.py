from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, id, email, first_name, last_name, phone, password, **other_fields):

        user = self.create_user(
            id,
            email,
            first_name,
            last_name, 
            phone,
            password=password, 
            **other_fields
        )
        
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        
        return user


    def create_user(self, id, email, first_name, last_name, phone, password, **other_fields):
        if not id:
            raise ValueError('You must provide your id')
        
        if not email:
            raise ValueError('You must provide and valid email')
        
        email = self.normalize_email(email)
        user = self.model(id=id, email=email, first_name=first_name, last_name=last_name, phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class Therapist(AbstractBaseUser, PermissionsMixin):
    """
    Custom model for the therapist user
    Inherits from AbstractBaseUser from Django that allows to
    customise the User Object
    """

    id = models.IntegerField(name='id', primary_key=True, unique=True)
    email = models.EmailField(name='email', max_length=50, unique=True)
    first_name = models.CharField(name='first_name', max_length=30)
    last_name = models.CharField(name='last_name', max_length=30)
    phone = models.CharField(name='phone', max_length=15)
    registration_date = models.DateTimeField(name='registration_date', auto_now_add=True)
    last_login = models.DateTimeField(name='last_login', auto_now=True)
    is_active = models.BooleanField(name='is_active', default=False)
    is_admin = models.BooleanField(name='is_admin', default=False)
    is_staff = models.BooleanField(name='is_staff', default=False)
    is_superuser = models.BooleanField(name='is_superuser', default=False)

    objects = CustomAccountManager()

    #Define the field to login with
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'first_name', 'last_name', 'phone']

    def __str__(self):
        """Return the string format for the Therapist objects"""
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
