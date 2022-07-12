from graphql.error.base import GraphQLError
from requests.api import request
from worker import tasks
import graphene
from graphene_django import DjangoListField
from graphql_auth.schema import UserQuery, MeQuery
from .types import UserProfileType, AllTransactionHistoryType, WalletType, StakingType,DigitalWalletType,OTPType
from .models import AllTransactionHistory, DigitalWallet, Staking, UserProfile, Wallet,OTP
from graphql_jwt.decorators import login_required
from django.core import serializers

from graphene_django.filter import DjangoFilterConnectionField

#QUERIES
class Query(UserQuery, MeQuery, graphene.ObjectType):

    update_referral =graphene.Field(UserProfileType,referral_code=graphene.String())
    userprofile = graphene.Field(UserProfileType)
    # txs = graphene.Field(AllTransactionHistoryType,userPK=graphene.Int())
    get_wallets = graphene.Field(WalletType,network=graphene.String())
    refresh_deposite = graphene.Field(AllTransactionHistoryType)
    get_all_deposites = DjangoListField(AllTransactionHistoryType)
    get_all_withdraws = DjangoListField(AllTransactionHistoryType)
    get_all_txs= DjangoListField(AllTransactionHistoryType)
    get_all_stakes = DjangoListField(StakingType)
    get_digital_wallet_balance=graphene.Field(DigitalWalletType)
    request_withdraw_otp = graphene.String()
    # verify_withdraw_otp = graphene.String()


    @login_required
    def resolve_userprofile(parent, info):
        return UserProfile.objects.get(user=info.context.user)


    @login_required
    def resolve_refresh_deposite(parent, info):
        tx = AllTransactionHistory.objects.filter(user=info.context.user, status = "Incomplete").latest('date')

        # TODO
        # check if transactions has hit the server
        tasks.refresh_deposite(tx.id)
        return tx

    # @login_required
    # def resolve_refresh_deposite(parent, info):
    #     tx = WalletType.objects.filter(user=info.context.user, status = "Incomplete").latest('date')

    @login_required
    def resolve_get_all_tx(parent, info):
        print(info.context.user.username)
        print('hererer')
        tx = AllTransactionHistory.objects.filter(user=info.context.user).order_by('-date')
        # tx = AllTransactionHistory.objects.filter(status='cv')
        return tx

    @login_required
    def resolve_get_all_deposites(parent, info):
        tx = AllTransactionHistory.objects.filter(user=info.context.user, t_type = "Deposite").order_by('-date')
        # tx = AllTransactionHistory.objects.filter(status='cv')
        return tx

    @login_required
    def resolve_get_all_withdraws(parent, info):
        tx = AllTransactionHistory.objects.filter(user=info.context.user, t_type = "Withdraw").order_by('-date')
        # tx = AllTransactionHistory.objects.filter(status='cv')
        return tx


    @login_required
    def resolve_get_wallets(parent, info, network):
        if Wallet.objects.filter(user__id=info.context.user.id, network = network).exists():
            print(34)
            return Wallet.objects.get(user__id=info.context.user.id, network = network)
        else:
            print(37)
            tasks.create_wallet(info.context.user.id, network)
            return Wallet.objects.get(user__id=info.context.user.id, network = network)


    @login_required
    def resolve_all_stakes(parent, info):
        stakes = Staking.objects.filter(user=info.context.user)
        return stakes 

    @login_required
    def resolve_get_digital_wallet_balance(parent, info):
        digitalwallet = DigitalWallet.objects.get(user=info.context.user)
        return digitalwallet


    @login_required
    def resolve_request_withdraw_otp(parent, info):
        # otp = OTP.objects.create(user=info.context.user).create_slug()
        # user_id = serializers.serialize("json", [info.context.user.id])
        # send_mail_now.delay(email_type='OTP',instance=user_data)
        if DigitalWallet.objects.get(user= info.context.user).balance >=50:
            print(95)
            tasks.emails(info.context.user.id,'otp')
            return f"email sent"
        else:
            raise GraphQLError('You do not have sufficient balance to make a withdraw. The minimum withdrawable amount is $50.')
        
    # @login_required
    # def resolve_verify_withdraw_otp(parent,info):
