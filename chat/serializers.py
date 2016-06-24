from swampdragon.serializers.model_serializer import ModelSerializer
from core.models import Admin


class AdminSerializer(ModelSerializer):

    class Meta:
        model = Admin
        publish_fields = ('id', 'login')
        update_fields = ('login', 'address', )


class ChatSerializer(ModelSerializer):
    user = AdminSerializer

    class Meta:
        model = 'Chat'
        publish_fields = ['admin', 'message']
        update_fields = ('message', )
