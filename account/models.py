from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.conf import settings
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save, post_save


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

    def follow(self, user):
        """Follows a user."""
        if user != self:
            following_instance, created = Follow.objects.get_or_create(following=self)
            following_instance.followers.add(user)

    def unfollow(self, user):
        """Unfollows a user."""
        if user != self:
            following_instance, created = Follow.objects.get_or_create(following=self)
            following_instance.followers.remove(user)

    @property
    def following_count(self):
        try:  # 1-usul
            following_instance = self.account_following.first()
            if following_instance:
                return following_instance.followers.count()
            return 0
        except AttributeError:
            return 0

        # try: # 2-usul
        #     return self.account_following.aggregate(count=models.Count('followers'))['count']
        # except AttributeError:
        #     return 0

    @property
    def follower_count(self):
        return self.followers.count()


class Follow(models.Model):
    following = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_following')
    followers = models.ManyToManyField(Account, related_name='followers')

    def __str__(self):
        return self.following.username


    # def get_following_count(self):
    #     return self.users_id.count()

    # def get_followers_count(self):
    #     return self.users_id.count()



    # def follow(self, user_to_follow):
    #     if not Following.objects.filter(following_user=self, followed_user=user_to_follow).exists():
    #         Following.objects.create(following_user=self, followed_user=user_to_follow)
    #
    # def unfollow(self, user_to_unfollow):
    #     try:
    #         follow_instance = Following.objects.get(following_user=self, followed_user=user_to_unfollow)
    #         follow_instance.delete()
    #     except Following.DoesNotExist:
    #         pass



    # @property
    # def following_count(self):
    #     following_instance = Following.objects.filter(following_user=self).first()
    #     if following_instance:
    #         return following_instance.users_id.count()
    #     return 0
    #
    #
    # @property
    # def follower_count(self):
    #     follower_instance = Follower.objects.filter(follower_user=self).first()
    #     if follower_instance:
    #         return follower_instance.users_id.count()
    #     return 0