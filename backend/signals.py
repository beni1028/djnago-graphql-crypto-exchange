
from django.db.models.signals import post_save
import asyncio
import json
import redis
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Wallet,DigitalWallet,Staking, Notifications
from channels.layers import get_channel_layer
from django.core import serializers


@receiver(post_save, sender=User) 
def update_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance).create_slug()
        DigitalWallet.objects.create(user=instance)


@receiver(post_save, sender=Staking) 
def update_staking_table(sender, instance, created, **kwargs):
    if created:
        instance.update_unlock_date()




@receiver(post_save, sender=Notifications) 
def send_notifications(sender, instance, created, **kwargs):
    # try:
        if created:
            group_name = instance.user.email if not instance.brodcast_message else 'Broadcast Notifications'
            print(group_name)
            print(instance.message,'signals')
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # serialized_qs = serializers.serialize('json', instance)

            # print(serialized_qs)
            loop.run_until_complete(channel_layer.group_send(group_name,
            {
                'type':'send_notification',
                'id': instance.id,
            }))
        else:
            return False
    # except Exception as e:
    #     print(e)
        # red_layer = RedisPubSubLoopLayer()
        # red_layer._get_group_channel_name()
        # redis_client = redis.StrictRedis( port=6379,)
        # try:
        #     redis_client.publish("asgispecific.6f196d03c4f44ffabb0df92fb0082e38", json.dumps(instance.message))
        #     print('done')
        # except Exception as e:
        #     print(e)
        # print('hello signals.py ')