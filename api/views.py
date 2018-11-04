import json
import requests
import logging

from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BasicSerializer, MarketSerializer

from .models import Coinmarketcap, Idex, TokenJar, Coinsuper, TOTAL_SUPPLY


logger = logging.getLogger(__name__)


class CoinmarketcapListView(ListView):

    model = Coinmarketcap

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coinmarketcap_list'] = Coinmarketcap.objects.order_by('-date')[:10]
        context['idex_list'] = Idex.objects.order_by('-date')[:10]
        context['tokenjar_list'] = TokenJar.objects.order_by('-date')[:10]
        context['coinsuper_list'] = Coinsuper.objects.order_by('-date')[:10]
        return context


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of API.
    """
    return Response({
        'basic': reverse('basic-metrics', request=request),
        'markets': reverse('markets-info', request=request)})

def parse_coinmarketcap():
    last_date = Coinmarketcap.objects.latest('date').date
    if(timezone.now() >= last_date + timezone.timedelta(hours=1)):
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
        logger.debug("Created coinmarketcap obj: " + str(obj_c.date))
        print("Created coinmarketcap obj: " + str(obj_c.date))

def parse_data():
    last_date = Idex.objects.latest('date').date
    if(timezone.now() >= last_date + timezone.timedelta(hours=1)):
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
                logger.debug("Created Coinsuper obj: " + str(obj_c.date))
                print("Created Coinsuper obj: " + str(obj_c.date))

            if(tiker['market']['name'] == 'Idex'):
                volume_i = tiker['volume']
                usd_price_i = tiker['converted_last']['usd']
                eth_price_i = tiker['converted_last']['eth']

                obj_i = Idex.objects.create(
                    price_usd=float(usd_price_i),
                    price_eth=float(eth_price_i),
                    volume=float(volume_i))
                logger.debug("Created Idex obj: " + str(obj_i.date))
                print("Created Idex obj: " + str(obj_i.date))

            if(tiker['market']['name'] == 'TokenJar'):
                volume_tj = tiker['volume']
                usd_price_tj = tiker['converted_last']['usd']
                eth_price_tj = tiker['converted_last']['eth']

                obj_tj = TokenJar.objects.create(
                    price_usd=float(usd_price_tj),
                    price_eth=float(eth_price_tj),
                    volume=float(volume_tj))
                logger.debug("Created TokenJar obj: " + str(obj_tj.date))
                print("Created TokenJar obj: " + str(obj_tj.date))

class BasicView(APIView):
    """
    Get basic metrics for XTRD token 
    """
    serializer_class = BasicSerializer

    @staticmethod
    def get(request):
        parse_coinmarketcap()
        basic = Coinmarketcap.objects.latest('date')
        data = {
            "supply": TOTAL_SUPPLY,
            "price": {
                "usd": format(basic.price_usd, '.8f'),
                "eth": format(basic.price_eth, '.18f')
            },
            "volume": basic.volume,
            'market_cap': basic.get_market_cap()
        }
        return Response(data, status=status.HTTP_200_OK)


class MarketsView(APIView):
    """
    Get information about markets where the token is trading and corresponding metrics like price and volume. 
    """
    serializer_class = MarketSerializer

    @staticmethod
    def get(request):
        parse_data()
        try:
            idex = Idex.objects.latest('date')
            coin_super = Coinsuper.objects.latest('date')
            jar = TokenJar.objects.latest('date')
            data = [
            {
                "name": "IDEX",
                # "supply": TOTAL_SUPPLY,
                "volume": idex.volume,
                "price": {
                    "usd": format(idex.price_usd, '.8f'),
                    "eth": format(idex.price_eth, '.18f')
                },
                'market_cap': idex.get_market_cap()
            },
            {
                "name": "Coinsuper",
                # "supply": TOTAL_SUPPLY,
                "volume": coin_super.volume,
                "price": {
                    "usd": format(coin_super.price_usd, '.8f'),
                    "eth": format(coin_super.price_eth, '.18f')
                },
                'market_cap': coin_super.get_market_cap()
            },
            {
                "name": "TokenJar",
                # "supply": TOTAL_SUPPLY,
                "volume": jar.volume,
                "price": {
                    "usd": format(jar.price_usd, '.8f'),
                    "eth": format(jar.price_eth, '.18f')
                },
                'market_cap': jar.get_market_cap()
            }
            ]
            return Response(data, status=status.HTTP_200_OK)
        except:
            data = []
        return Response(data, status=status.HTTP_204_NO_CONTENT)
