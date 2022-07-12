import asyncio
import graphene
from .decorators import login_required_sub

from .types import NotificationType
from .models import Notifications
from channels.db import database_sync_to_async

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


import json
from django.core import serializers


@database_sync_to_async
def get_notifications(user):
    try:
        print('hello world')
        notification =Notifications.objects.filter(user =user, sent = False)
        # notification = len(Notifications.objects.all())
        return notification
    except Exception as e:
            print('other error 2', e)




class Subscription(graphene.ObjectType):
    notifications = graphene.Field(NotificationType, required = True)
    brodcast_notification = graphene.Field(NotificationType, required = True)


    @login_required_sub
    async def resolve_notifications(self, info):
        # channel_layer = get_channel_layer()
        user = info.context['user']
        try:
            channel_name = await channel_layer.new_channel()
            await channel_layer.group_add(str(user.email), channel_name)
            # ch_group_list = channel_layer.pubsub_channels('Broadcast Notifications')
            # print(ch_group_list)
            try:
                while True:
                    message = await channel_layer.receive(channel_name)
                    yield await database_sync_to_async(lambda: Notifications.objects.get(id=message['id']))()
            except Exception as e:
                print(e)
            finally:
                await channel_layer.group_discard("new_message", channel_name)

        except Exception as e:
            print(e)

    @login_required_sub
    async def resolve_brodcast_notification(self, info):
        user = info.context['user']
        channel_name = await channel_layer.new_channel()
        await channel_layer.group_add('Broadcast Notifications', channel_name)
        try:
            while True:
                message = await channel_layer.receive(channel_name)
                yield await database_sync_to_async(lambda: Notifications.objects.get(id=message['id']))()
        except Exception as e:
            print('Subscriptions Error' ,e)
        finally:
            await channel_layer.group_discard("new_message", channel_name)

