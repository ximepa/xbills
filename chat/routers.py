from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter
from .serializers import ChatSerializer, AdminSerializer
from .models import Chat
from core.models import Admin


class ChatRouter(BaseRouter):
    route_name = 'chat-route'
    serializer_class = ChatSerializer
    model = Chat
    include_related = [AdminSerializer, ]
    valid_verbs = ['chat', 'subscribe']

    def get_initial(self, verb, **kwargs):
        admin = Admin.objects.get(pk=kwargs['user_id'])
        return {'admin': admin}

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

    def get_subscription_channels(self, **kwargs):
        return ['chatroom']

    def chat(self, *args, **kwargs):
        print kwargs
        errors = {}
        if 'name' not in kwargs or len(kwargs['name']) is 0:
            errors['name'] = 'Specify a name'

        if 'message' not in kwargs or len(kwargs['message']) is 0:
            errors['message'] = 'Enter a chat message'

        if errors:
            self.send_error(errors)
        else:
            self.send({'status': 'ok'})
            self.publish(self.get_subscription_channels(), kwargs)


route_handler.register(ChatRouter)


