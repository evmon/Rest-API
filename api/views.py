import requests

from django.shortcuts import render
from django.views.generic.list import ListView

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BasicSerializer, MarketSerializer

from .models import Coinmarketcap, Idex, TokenJar, Coinsuper, TOTAL_SUPPLY


class CoinmarketcapListView(ListView):

    model = Coinmarketcap

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Coinmarketcap.objects.last()
        print(context['data'])
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
