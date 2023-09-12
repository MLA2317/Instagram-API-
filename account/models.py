from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver



class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError('User should have a password')

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Location(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Account(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=221, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER = (
        ('None', 'None'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=20, choices=GENDER)
    email = models.EmailField()
    bio = models.TextField()
    phone_number = PhoneNumberField(verbose_name='Phone Number', null=True, blank=True)
    avatar = models.ImageField(upload_to='profile/', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='account_location', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def image_tag(self):
        if self.avatar:
            return mark_safe(f"<a href='{self.avatar.url}'><img src='{self.avatar.url}' style='height:43px;'/></a>")
        else:
            return 'Image not found'

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),  # bu - access token ni yangilab beradi
            'access': str(refresh.access_token)  # bu - saytga kirish un ruhsat
        }
        return data

    @property
    def following_count(self):
        return self.account_following.count()

    @property
    def follower_count(self):
        return self.followers.count()


class Follow(models.Model):
    following = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_following')
    followers = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return self.following.username
