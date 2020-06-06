from noshdapp.models import RestaurantPost, User, UserFollowing
from rest_framework import serializers
from django.db.models.functions import Cast
from django.contrib.auth.models import Group


class RestaurantPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = RestaurantPost
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = 'username', 'id', 'email', 'url', 'following', 'followers'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FollowingSerializer(serializers.ModelSerializer):
    following_user_id = serializers.IntegerField
    following_user_username = serializers.SerializerMethodField()
    user_id = serializers.IntegerField
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ("following_user_id", "following_user_username", "created", "user_id", "user_username", "id")

    def get_following_user_username(self, obj):
        return obj.following_user_id.username

    def get_user_username(self, obj):
        return obj.user_id.username


class FollowersSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ("user_id", "user_username", "created")

    def get_user_username(self, obj):
        return obj.user_id.username



