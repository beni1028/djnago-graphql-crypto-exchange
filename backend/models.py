from django.db import models
from django.contrib.auth.models import User
import hashlib
from datetime import datetime, timedelta

from django.db.models.deletion import CASCADE

# from backend.mutations import Deposite
# import time
# from django.contrib.auth.models import AbstractUser
# Create your models here.



# class User(AbstractUser):
#     referred_by = models.CharField(max_length=20, blank= True, default='')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField( blank=True,null=True)
    gender = models.CharField(max_length=20, blank= True, default='') 
    contact_number = models.IntegerField(blank=True, null=True)
    referral_code = models.CharField(max_length=20, blank= True, default='',unique=True)
    referral_count =  models.IntegerField( blank=True,null=True)


    def create_slug(self):
        # referral = Referral.create( user=self.user, redirect_to=reverse("register_customer"))
        s=str(self.user.username)
        hash_is_not_unique = True
        while hash_is_not_unique:
            hash = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8
            hash_is_not_unique = UserProfile.objects.filter(referral_code=hash).exists()
        self.referral_code = hash
        self.save()
        return hash

    def __str__(self) :
        return str(self.user.username)




class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    expired = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    otp = models.IntegerField( blank=True,null=True, unique= True)

    def create_slug(self):
        # referral = Referral.create( user=self.user, redirect_to=reverse("register_customer"))
        s=str(self.user.username)+str(datetime.now())
        hash_is_not_unique = True
        while hash_is_not_unique:
            hash = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8
            hash_is_not_unique = OTP.objects.filter(otp=hash).exists()
            print(hash)
            print(hash_is_not_unique)
        self.otp = hash
        self.save()
        return hash

    def __str__(self) :
        return str(self.user.username)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.CharField(max_length=10) 
    wallet_address = models.CharField(max_length=200)
    private_key = models.CharField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    balance =  models.DecimalField(max_digits=24, decimal_places=12,  default = 0)
    latest_block = models.CharField(max_length=10,default=0)
    first_transaction = models.BooleanField(default=True)
    in_use = models.BooleanField(default=True)


    def __str__(self):
        return str(self.user.id)


class DigitalWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    balance =  models.DecimalField(max_digits=24, decimal_places=12,  default = 0)
    total_deposite =  models.DecimalField(max_digits=24, decimal_places=12,  default = 0)
    total_withdrawn =  models.DecimalField(max_digits=24, decimal_places=12,  default = 0)
    roi_earned =  models.DecimalField(max_digits=24, decimal_places=12,  default = 0)
    active = models.BooleanField(default=True)

    # latest_block = models.CharField(max_length=10,default=0)
    # first_transaction = models.BooleanField(default=True)


    def __str__(self):
        return str(self.user.username)



class AllTransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.CharField(max_length=10) 
    value = models.DecimalField(max_digits=15, decimal_places=4, default=0.00)
    date =models.DateTimeField(auto_now_add=True)
    txreceipt_status = models.CharField(max_length=5)
    from_wallet = models.CharField(max_length=200, blank = True)
    to = models.CharField(max_length=200, blank = True)
    hash = models.CharField(max_length=200, blank = True)
    blockNumber = models.CharField(max_length=10, blank = True)
    t_type = models.CharField(max_length=20)
    status = models.CharField(max_length=30)
    usd = models.DecimalField(max_digits=15, decimal_places=4, default =0.00)
    def __str__(self):
        return str(self.id)



class Staking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lock_date =models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=15, decimal_places=4)
    unlock_date =models.DateTimeField(blank=True, null =True)
    status = models.IntegerField( blank=True,null=True)
    comments =  models.CharField(max_length=200, blank = True)
    roi_generated = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    # roi_pending = models.DecimalField(max_digits=15, decimal_places=4)


    def update_unlock_date(self):
        self.unlock_date = self.lock_date+timedelta(days=30)
        self.save()
   
    def __str__(self):
        return str(self.id)

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class NetworkAPIS(SingletonModel):
    bsc = models.CharField(max_length=1000)
    eth = models.CharField(max_length=1000)


        
    def __str__(self):
        return str("NetwrokAPIS")

class Remitter(SingletonModel):
    balance =  models.DecimalField(max_digits=24, decimal_places=12,  default = 0)
    wallet_address = models.CharField(max_length=200)
    private_key = models.CharField(max_length=200) 

        
    def __str__(self):
        return str("Remitter")


class Notifications(models.Model):
    # class NotificationType(models.TextChoices):
    #     Deposite
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message =models.TextField()
    sent = models.BooleanField(default=True)
    read = models.BooleanField(default=False)
    brodcast_message = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user.username)