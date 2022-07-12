from django.contrib import admin
from .models import UserProfile, Wallet, AllTransactionHistory, DigitalWallet, Staking,OTP, Notifications 
# from .models import CustomUser
from django.apps import apps
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Wallet)
admin.site.register(DigitalWallet)
admin.site.register(Staking)
admin.site.register(OTP)
admin.site.register(Notifications)


class AllTransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user','network','value', 'date','status','txreceipt_status','from_wallet','to')
    list_display_links=('user',)
    list_editable=('txreceipt_status','status',)

admin.site.register(AllTransactionHistory,AllTransactionHistoryAdmin )

app = apps.get_app_config('graphql_auth')
app2 = apps.get_app_config('graphql_jwt')
# app3 = apps.get_app_config('celery')

for model_name, model in app.models.items():
    admin.site.register(model)

for model_name, model in app2.models.items():
    print(model_name)
    admin.site.register(model)


# for model_name, model in app3.models.items():
#     print(model_name)
#     admin.site.register(model)