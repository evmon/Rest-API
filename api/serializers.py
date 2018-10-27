from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from .models import Coinmarketcap


class BasicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Coinmarketcap
		fields = ('volume', 'supply', 'price_eth', 'price_usd')


class MarketSerializer(serializers.HyperlinkedModelSerializer):
	pass