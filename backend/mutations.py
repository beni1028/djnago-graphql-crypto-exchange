
from datetime import date
# from typing_extensions import Required
import graphene
from .types import OTPType, UserProfileType, WalletType, AllTransactionHistoryType, StakingType
from graphql_auth import mutations
from graphene_django import DjangoObjectType
from .models import OTP, UserProfile, Wallet, AllTransactionHistory,DigitalWallet, Staking
from graphql_jwt.decorators import login_required, superuser_required
# from .decorators import login_required_sub
from worker import tasks
from graphql import GraphQLError
#TYPE
class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()





class UserProfileInput(graphene.InputObjectType):
    # id = graphene.ID(required=True)
    age = graphene.Int()
    contact_numeber = graphene.Int()
    gender = graphene.String()

class UpdateUserProfile(graphene.Mutation):
    class Arguments:
        input = UserProfileInput(required=True)

    userprofile = graphene.Field(UserProfileType)

    @login_required
    def mutate(parent, info, input=None):
        if input is None:
            return UpdateUserProfile(userprofile=None)
        _userprofile = UserProfile.objects.filter(user =info.context.user).update(**input)
        _userprofile = UserProfile.objects.get(user =info.context.user)
        tasks.create_and_or_receive.delay(info.context.user.id,input.age)

        return UpdateUserProfile(userprofile=_userprofile)
####################################################################################


# class DepositeInput(graphene.InputObjectType):
#     # id = graphene.ID(required=True)
#     network = graphene.String(required= True)
    

class Deposite(graphene.Mutation):
    class Arguments:
        network = graphene.String(required= True)


    TXDetails = graphene.Field(AllTransactionHistoryType)
    Wallet_address = graphene.String()
    @login_required
    def mutate(parent, info, network):
        print(network,dir(info.context))
        if network == 'eth' or network =="bnb":
            if AllTransactionHistory.objects.filter(user=info.context.user, status= 'Pending').exists():
                raise GraphQLError('You have a transaction pending. Either, cancel the existing transaction or please wait for the transaction to complete.')
            else:    
                txh,wallet_address = tasks.deposite(info.context.user,network)
                txh = AllTransactionHistory.objects.get(id = txh)
                return Deposite(TXDetails=txh,Wallet_address=wallet_address)
        else:
            raise GraphQLError('Accepted Newtorks ETH or BNB. Use "eth" or "bnb" .')



####################################################################################
# STAKING
class Stake(graphene.Mutation):
    class Arguments:
        amount = graphene.Float()
    Staking_Details = graphene.Field(StakingType)
    # Staking_Message= graphene.String()


    @login_required
    def mutate(parent, info, amount):
        if amount is None:
            raise GraphQLError( f'Please enter a valid amout')
        elif amount <50:
            raise GraphQLError( f'The minimum staking amount is $50. Please input a minimum of $50 and above')
        elif amount >=50:
            print('here 99')
            if int(DigitalWallet.objects.get(user=info.context.user).balance) >= int(50):
                print('here 101')
                print(type(amount))
                stake =Staking.objects.create(user=info.context.user,value = amount,status = 0)
                print('here_return 104')
                return Stake(Staking_Details =stake)
            else:
                raise GraphQLError(f'Your current wallet balance is {DigitalWallet.objects.get(user=info.context.user).balance}. You need to have atleast a minimum of $50 to stake.')
####################################################################################

class BgworkerTest(graphene.Mutation):
    testout = graphene.String()
    def mutate(parent, info, input=None):
        tasks.test.delay()
        _testout = f'sent123--to--321worker'
        return BgworkerTest(testout=_testout)

####################################################################################
class Withdraw(graphene.Mutation):
    class Arguments:
        otp = graphene.Int(required= True)
        amount = graphene.Float(required= True)
    Tx = graphene.Field(AllTransactionHistoryType)
    @login_required
    def mutate(parent, info, otp,amount):
        if OTP.objects.filter(user=info.context.user,otp=otp,verified =True, expired=False).exists():
            # tasks.withdraw.delay()
            tx = AllTransactionHistory.objects.filter(user=info.context.user, status = "Incomplete").latest('date')
            return Withdraw(Tx=tx)
        elif otp is None:
            raise GraphQLError( f'Please enter a valid OTP')
        elif OTP.objects.filter(user=info.context.user,otp=otp,verified =True, expired=True).exists():
            raise GraphQLError( f'This OTP has expired. Kindly request for a new OTP.')

####################################################################################
class Verify_OTP(graphene.Mutation):
    class Arguments:
        otp = graphene.Int(required = True)
    OTP_Status = graphene.String()
    # @login_required_sub
    def mutate(parent, info, otp):
        print(info.context.user)
        print(';here')
        if OTP.objects.filter(user=info.context.user,otp = otp, verified =False, expired= False).exists():
            otp = OTP.objects.filter(user=info.context.user,otp = otp, verified =False, expired= False)
            otp.update(verified=True)
            return Verify_OTP(OTP_Status ='Verified')
        else:
            raise GraphQLError(f"Doesn't Exists heheh")
####################################################################################


class Mutation(AuthMutation, graphene.ObjectType):
    updateuserprofile = UpdateUserProfile.Field()
    deposite = Deposite.Field()
    bgworkertest = BgworkerTest.Field()
    stake = Stake.Field()
    withdraw= Withdraw.Field()
    verify_otp = Verify_OTP.Field()