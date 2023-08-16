from rest_framework import serializers
from .models import Account, Follow, Location
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'title')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=25, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=25, write_only=True)

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

    class Meta:
        model = Account
        fields = ('username', 'password')

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
    location = LocationSerializer(read_only=True)
    # following_count = FollowingSerializer(read_only=True)
    # follower_count = FollowerSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'avatar', 'gender', 'location', 'phone_number', 'following_count', 'follower_count', 'created_date')


class AllAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'avatar', 'gender', 'location', 'phone_number', 'following_count', 'follower_count',
        'created_date')


class FollowingListSerializer(serializers.ModelSerializer):
    users_name = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'following', 'users_name')

    def get_users_name(self, obj):
        return [{'id': user.id, 'name': user.username} for user in obj.followers.all()]


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username')


class FollowerListSerializer(serializers.ModelSerializer):
    followers_id = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('followers_id',)

    def get_followers_id(self, obj):
        # Fetch related Follow instance using related_name
        try:
            follow_instance = obj.account_following.first()
            if follow_instance:
                return [follower.id for follower in follow_instance.followers.all()]
            return []
        except AttributeError:
            return []

    # class Meta:
    #     model = Account
    #     fields = ('followers',)
    #
    # def get_followers(self, obj):
    #     # Serialize each follower and return the list
    #     return AccountListSerializer(obj.followers.all()).data


class FollowCreateSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):
    #     following_user = attrs.get('following_user')
    #     users_id = attrs.get('users_id')
    #     if users_id in following_user:
    #         raise ()

    class Meta:
        model = Follow
        fields = ('id', 'following', 'followers')


# class FollowerSerializer(serializers.ModelSerializer):
#     users_name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Follower
#         fields = ('id', 'follower_user', 'users_name')
#
#     def get_users_name(self, obj):
#         return [user.username for user in obj.users_id.all()]
#
#     def validate(self, attrs):
#         follower_user = attrs.get('follower_user')
#         users = attrs.get('users_id', [])
#
#         # follower_user o'zini o'ziga yozuvchiga aylanmasligini taqiqlash:
#         if follower_user in users:
#             raise serializers.ValidationError({
#                 "users_id": "A user cannot follow themselves."
#             })
#
#         return attrs


#
    # def validate(self, attrs):
    #     following_user = attrs.get('following_user')
    #     users = attrs.get('users_id', [])
    #     print(users)
    #
    #     # following_user o'zini o'ziga yozuvchiga aylantirishini taqiqlash:
    #     if following_user in users:
    #         raise serializers.ValidationError({
    #             "users_id": "A user cannot follow themselves."
    #         })
    #
    #     # users_id maydonida biror foydalanuvchini ikki marta kiritishni taqiqlash:
    #     if len(users) != len(set(users)):
    #         raise serializers.ValidationError({
    #             "users_id": "Duplicated users are not allowed."
    #         })
    #     return attrs