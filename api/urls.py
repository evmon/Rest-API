from django.urls import path

from .views import (CoinmarketcapListView, BasicView, MarketsView,
	api_root, RecordCreateView, )

urlpatterns = [
	path('', api_root, name='root'),
	path('db', CoinmarketcapListView.as_view(), name='db'),
    path('rest/explorer/xtrd/basic', BasicView.as_view(), name='basic-metrics'),
    path('rest/explorer/xtrd/markets', MarketsView.as_view(), name='markets-info'),
	path('rest/explorer/xtrd/create', RecordCreateView.as_view(), name='record-create'),
]