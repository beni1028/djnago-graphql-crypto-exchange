#TYPES
from graphene_django import DjangoObjectType
from .models import OTP, DigitalWallet, UserProfile,Wallet, AllTransactionHistory, Staking, Notifications


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ('__all__')

class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet
        fields = ('network','wallet_address','balance')


class AllTransactionHistoryType(DjangoObjectType):
    class Meta:
        model = AllTransactionHistory
        fields = ('__all__')


class StakingType(DjangoObjectType):
    class Meta:
        model = Staking
        fields = ('__all__')



class DigitalWalletType(DjangoObjectType):
    class Meta:
        model = DigitalWallet
        fields = ('__all__')

class OTPType(DjangoObjectType):
    class Meta:
        model = OTP
        fields = ('__all__')

class NotificationType(DjangoObjectType):
    class Meta:
        model = Notifications
        fields = ('__all__')