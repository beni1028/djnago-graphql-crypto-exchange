from celery import shared_task
from celery.contrib.abortable import AbortableTask
from backend.models import OTP, Wallet, AllTransactionHistory, DigitalWallet
from web3 import Web3

import time
import requests

from pycoingecko import CoinGeckoAPI

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.core import serializers

cg = CoinGeckoAPI()



@shared_task(bind=True)
def check_for_deposite(wallet_id, tx_id):
    wallet = Wallet.objects.get(id=wallet_id)
    tx = AllTransactionHistory.objects.filter(id=tx_id)
    if wallet.network == "eth":
        URL = f'https://api.etherscan.io/api?module=account&action=txlist&address={wallet.wallet_address}&startblock={wallet.latest_block}&endblock=99999999&page=1&offset=10&sort=desc&apikey=NCDR3WPT9ZV7DQXMEYZ3ZKE8IIRXXWUB81'
        network='ethereum'
        # price_usd = cg.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']

    elif wallet.network == "bnb":
        URL = f"https://api.bscscan.com/api?module=account&action=txlist&address={wallet.wallet_address}&startblock={wallet.latest_block}&endblock=99999999&page=1&offset=10&sort=desc&apikey=DYY8F2H5Q1Q3V84PJMRI5FNJI2WXMWDNED"
        network = 'binancecoin'
        # price_usd = cg.get_price(ids='binancecoin', vs_currencies='usd')['binancecoin']['usd']
    else:
        return f'Wrong network'
    t_end = time.time() + 1 * 10 # minutes X seconds
    print(URL)
    while time.time() < t_end:
        r = requests.get(url = URL)
        data = r.json()
        # print(data)
        x= data['result']
        if x == []:
            print("No Data Yet")
        # if tx[0].status == 'Cancelled':
        #     print('Cancelled')
        elif x != [] and x!="E":
            x=x[0]
            if int(x['blockNumber']) > int(wallet.latest_block):
                value = Web3.fromWei(float(x['value']), 'ether')
                price_usd = cg.get_price(ids='ethereum', vs_currencies='usd')[network]['usd']
                usd_value = float(price_usd) * float(value)
                
                if x['txreceipt_status']=="1":
                    status = 'Successful'
                elif x['isError']=="1":
                    status = 'Failed'
                else:
                    status = "Incomplete"
                tx_input ={"value" : value, "from_wallet" : x['from'], "to" : x['to'], "hash" : x['hash'], "blockNumber" : x['blockNumber'], "txreceipt_status" : x['txreceipt_status'], "status":status, "usd": usd_value}
                tx.update(**tx_input)
                wallet.balance = wallet.balance + value
                wallet.latest_block = x['blockNumber']
                wallet.save()
                # tx.save()
                dw = DigitalWallet.objects.get(user=wallet.user)
                dw.balance = float(dw.balance) + float(usd_value)
                dw.total_deposite = float(dw.total_deposite) + float(usd_value)
                dw.save()
                break
    tx_input ={"value": 0, "from_wallet" : "", "to" :"", "hash" : "", "blockNumber" : "", "txreceipt_status" : "-1", "status":"Incomplete","to":wallet.wallet_address, "status":"Incomplete" }
    tx.update(**tx_input)
    # tx.value=560
    # tx.save()


def refresh_deposite(tx_id):
    tx = AllTransactionHistory.objects.filter(id=tx_id)
    wallet = Wallet.objects.get(user=tx.user, network =tx.network )
    if wallet.network == "eth":
        URL = f'https://api.etherscan.io/api?module=account&action=txlist&address={wallet.wallet_address}&startblock={wallet.latest_block}&endblock=99999999&page=1&offset=10&sort=desc&apikey=NCDR3WPT9ZV7DQXMEYZ3ZKE8IIRXXWUB81'
        network='ethereum'        
    elif wallet.network == "bsc":
        URL = f"https://api.bscscan.com/api?module=account&action=txlist&address={wallet.wallet_address}&startblock={wallet.latest_block} 1&endblock=99999999&page=1&offset=10&sort=desc&apikey=DYY8F2H5Q1Q3V84PJMRI5FNJI2WXMWDNED"
        network = 'binancecoin'
    r = requests.get(url = URL)
    data = r.json()
        # print(data)
    x= data['result']
    if x == []:
        print("No Data Yet")
        # if tx[0].status == 'Cancelled':
        #     print('Cancelled')
    elif x != [] and x!="E":
        print(type(x),len(x))
        print(x)
        x=x[2]
        if int(x['blockNumber']) > int(wallet.latest_block):
            value = Web3.fromWei(float(x['value']), 'ether')
            price_usd = cg.get_price(ids='ethereum', vs_currencies='usd')[network]['usd']
            usd_value = float(price_usd) * float(value)
            if x['txreceipt_status']=="1":
                status = 'Successful'
            elif x['isError']=="1":
                status = 'Failed'
            else:
                status = "Incomplete"
            tx_input ={"value" : value, "from_wallet" : x['from'], "to" : x['to'], "hash" : x['hash'], "blockNumber" : x['blockNumber'], "txreceipt_status" : x['txreceipt_status'], "status":status, "usd": usd_value}
            tx.update(**tx_input)
            wallet.balance = wallet.balance + value
            wallet.latest_block = x['blockNumber']
            wallet.save()
            # tx.save()
            dw = DigitalWallet.objects.get(user=wallet.user)
            dw.balance = float(dw.balance) + float(usd_value)
            dw.total_deposite = float(dw.total_deposite) + float(usd_value)
            dw.save()
    tx_input ={"value": 0, "from_wallet" : "", "to" :"", "hash" : "", "blockNumber" : "", "txreceipt_status" : "-1", "status":"Incomplete","to":wallet.wallet_address, "status":"Incomplete" }
    tx.update(**tx_input)




def generate_wallet(user_id,network):
    if network == "eth":
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
        web3.isConnected()
    elif network == "bnb":
        web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
        web3.isConnected()
    else:
        return f'Wrong network'
    account = web3.eth.account.create()
    address_key = [account._address,account._private_key.hex()]
    Wallet.objects.create(user_id=user_id,network=network)
    Wallet.objects.filter(user_id=user_id,network=network).update(wallet_address=account._address,private_key=account._private_key.hex())
    return Wallet



def deposite(user,network):
    print("120")
    if Wallet.objects.filter(user=user,network=network).exists():
        wallet  = Wallet.objects.get(user=user, network=network)
    elif not Wallet.objects.filter(user=user,network=network).exists():
        wallet = generate_wallet(user.id, network)
    atx = AllTransactionHistory.objects.create(user=user,network=network,status= "Pending",value = 0, t_type = "Deposite", to= wallet.wallet_address)
    print("120")
    check_for_deposite.delay(wallet.id, atx.id)
    print("124")
    return atx.id, wallet.wallet_address

@shared_task
def test():
    print('testing')
    return f'testing new successful'


@shared_task
def emails(user_id, email_type):
    from_email = 'dev.metatest@gmail.com'
    if email_type=="otp":
        if OTP.objects.filter(user_id=user_id, verified=False, expired = False).exists():
            otp= OTP.objects.filter(user_id=user_id, verified=False, expired = False).latest("created_at")
        else:
            otp = OTP.objects.create(user_id=user_id)
        print(183)
        otp.create_slug()
        # for obj in serializers.deserialize("json", user_instance):
        #     user  = obj.object
        # otp = OTP.objects.get(user_id=user_id)
        to_email = otp.user.email
        subject = 'Verify Your Cryptodot.io Account'
        # plain_message = strip_tags(html_message)
        context = {
            'email_otp': otp.otp,

        }        
        html_message = render_to_string('emails/otp.html', context=context)
    
    plain_message = strip_tags(html_message)
    result = send_mail(subject, plain_message, from_email,[to_email], html_message=html_message)

# def withdraw()
