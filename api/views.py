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
from .forms import RecordCreateForm


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


class BasicView(APIView):
    """
    Get basic metrics for XTRD token 
    """
    serializer_class = BasicSerializer

    @staticmethod
    def get(request):
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


class RecordCreateView(APIView):

    @staticmethod
    def post(request):
        data = request.POST
        coinsuper_usd = data['tickers[0][converted_last][usd]']
        coinsuper_eth = data['tickers[0][converted_last][eth]']
        coinsuper_volume = data['tickers[0][volume]']
        idex_usd = data['tickers[1][converted_last][usd]']
        idex_eth = data['tickers[1][converted_last][eth]']
        idex_volume = data['tickers[1][volume]']
        joyso = data['tickers[2][volume]']
        tokenjar_usd = data['tickers[3][converted_last][usd]']
        tokenjar_eth = data['tickers[3][converted_last][eth]']
        tokenjar_volume = data['tickers[3][volume]']
        ETH_USD = float(requests.get(
            'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD').json()['USD'])
        r = requests.get('https://api.coinmarketcap.com/v2/ticker/3067/')
        data = json.loads(r.text)['data']
        coinmarketcap_usd = data['quotes']['USD']['price']
        coinmarketcap_eth = float(coinmarketcap_usd) / ETH_USD
        coinmarketcap_volume = data['quotes']['USD']['volume_24h']
        last_obj = Idex.objects.latest('date')
        # print(timezone.now())
        # print(last_obj.date)
        # print(last_obj.date + timezone.timedelta(minutes=1) >= timezone.now())
        # if(timezone.now() >= last_obj.date + timezone.timedelta(minutes=1)):
        obj_cs = Coinsuper.objects.create(
            price_usd=float(coinsuper_usd),
            price_eth=float(coinsuper_eth),
            volume=float(coinsuper_volume))
        logger.debug("Created Coinsuper obj: " + str(obj_cs.date))
        print("Created Coinsuper obj: " + str(obj_cs.date))

        obj_i = Idex.objects.create(
            price_usd=float(idex_usd),
            price_eth=float(idex_eth),
            volume=float(idex_volume))
        logger.debug("Created Idex obj: " + str(obj_i.date))
        print("Created Idex obj: " + str(obj_i.date))

        obj_tj = TokenJar.objects.create(
            price_usd=float(tokenjar_usd),
            price_eth=float(tokenjar_eth),
            volume=float(tokenjar_volume))
        logger.debug("Created TokenJar obj: " + str(obj_tj.date))
        print("Created TokenJar obj: " + str(obj_tj.date))

        obj_c = Coinmarketcap.objects.create(
            price_usd=coinmarketcap_usd,
            price_eth=coinmarketcap_eth,
            volume=coinmarketcap_volume)
        logger.debug("Created Coinmarketcap obj: " + str(obj_c.date))
        print("Created Coinmarketcap obj: " + str(obj_c.date))

        return HttpResponse('All objects is created at {}'.format(timezone.now()), status=status.HTTP_201_CREATED)
        # else:
        #     return HttpResponse('Data has recently been updated.', status=status.HTTP_200_OK)
