from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):

        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):

        fields = ['email', 'username', 'password', 'first_name', 'last_name']
