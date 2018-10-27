import json
import requests
# import etherdelta

from app.celery import app

from .models import Coinsuper, Coinmarketcap, Idex, TokenJar


@app.task
def parse_data():
    ETH_USD = float(requests.get(
        'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD').json()['USD'])
    r = requests.get('https://api.coinmarketcap.com/v2/ticker/3067/')
    data = json.loads(r.text)['data']
    usd_price = data['quotes']['USD']['price']
    eth_price = float(usd_price) / ETH_USD
    volume_24h = data['quotes']['USD']['volume_24h']
    # Etherscan 
    obj_c = Coinmarketcap.objects.create(
        price_usd=usd_price,
        price_eth=eth_price,
        volume=volume_24h)
    print("Created coinmarketcap obj: " + str(obj_c.date))

    r = requests.get('https://api.coingecko.com/api/v3/coins/xtrade?localization=en')
    data = json.loads(r.text)['tickers']

    for tiker in data:
        if(tiker['market']['name'] == 'Coinsuper'):
            volume_c = tiker['volume']
            usd_price_c = tiker['converted_last']['usd']
            eth_price_c = tiker['converted_last']['eth']

            obj_c = Coinsuper.objects.create(
                price_usd=float(usd_price_c),
                price_eth=float(eth_price_c),
                volume=float(volume_c))
            print("Created Coinsuper obj: " + str(obj_c.date))

        if(tiker['market']['name'] == 'Idex'):
            volume_i = tiker['volume']
            usd_price_i = tiker['converted_last']['usd']
            eth_price_i = tiker['converted_last']['eth']

            obj_i = Idex.objects.create(
                price_usd=float(usd_price_i),
                price_eth=float(eth_price_i),
                volume=float(volume_i))
            print("Created Idex obj: " + str(obj_i.date))

        if(tiker['market']['name'] == 'TokenJar'):
            volume_tj = tiker['volume']
            usd_price_tj = tiker['converted_last']['usd']
            eth_price_tj = tiker['converted_last']['eth']

            obj_tj = TokenJar.objects.create(
                price_usd=float(usd_price_tj),
                price_eth=float(eth_price_tj),
                volume=float(volume_tj))
            print("Created TokenJar obj: " + str(obj_tj.date))
