from rest_framework import serializers
from .models import Account, Follow
from django_countries.fields import CountryField
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=25, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=25, write_only=True)
    location = CountryField()

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'bio', 'phone_number',
                  'avatar', 'location', 'password', 'password2', 'created_date', 'modified_date')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password does not same, Try again!')
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=25, required=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        username = obj.get('username')
        tokens = Account.objects.get(username=username).tokens
        return tokens

    class Meta:
        model = Account
        fields = ('username', 'password', 'tokens')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                "message": "Username or password not correct"
            })
        if not user.is_active:
            raise AuthenticationFailed({
                "message": "Account disabled"
            })
        return attrs


class ProfilesSerializer(serializers.ModelSerializer):
    location = CountryField()
    avatar = serializers.FileField()
    first_name = serializers.CharField(max_length=200),
    last_name = serializers.CharField(max_length=200)
    # following_count = FollowingSerializer(read_only=True)
    # follower_count = FollowerSerializer(read_only=True)


    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'gender', 'location', 'phone_number', 'following_count', 'follower_count', 'created_date')


class FollowingListSerializer(serializers.ModelSerializer):
    users_name = serializers.SerializerMethodField()
    following_back = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'following', 'users_name', 'following_back')

    def get_users_name(self, obj):
        return {
            'id': obj.followers.id,
            'name': obj.followers.username
        }

    def get_following_back(self, obj):
        return Follow.objects.filter(following=obj.followers, followers=obj.following).exists()


class FollowCreateSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):
    #     following_user = attrs.get('following_user')
    #     users_id = attrs.get('users_id')
    #     if users_id in following_user:
    #         raise ()

    class Meta:
        model = Follow
        fields = ('id', 'following', 'followers')


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username')


class FollowerSerializer(serializers.ModelSerializer):
    user_name_following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'user_name_following', 'followers')

    def get_user_name_following(self, obj):
        return obj.following.username