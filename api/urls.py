from django.urls import path

from .views import (CoinmarketcapListView, BasicView, MarketsView,
	api_root, )

urlpatterns = [
	path('', api_root, name='root'),
	path('db', CoinmarketcapListView.as_view(), name='db'),
    path('rest/explorer/xtrd/basic', BasicView.as_view(), name='basic-metrics'),
    path('rest/explorer/xtrd/markets', MarketsView.as_view(), name='markets-info'),
]