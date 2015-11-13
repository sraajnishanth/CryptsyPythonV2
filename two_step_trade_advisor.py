from Cryptsy import Cryptsy
from pprint import pprint
import time
import json
import pdb
import copy

originCurrencyCode = 'BTC'
originCurrencyAmount = 0.001
originCurrency = None
currencyMarketId = None



c = Cryptsy("fefa680f20ccea932758caa72b5fd91a4d26b31f", "06525df00812cd6af6503a4856e048e7d5921118a3c591d3798b0152d99fa32843c57594841a7cc3")
# ohlc = c.market_ohlc(133, start=0, stop=time.time(), interval="minute", limit=60)
listMarkets = c.markets()
listCurrencies = c.currencies()

tradeRoute = []


# pprint(listCurrencies[data])
for currency in listCurrencies['data']:
	if currency['code'] == originCurrencyCode:
		originCurrency = currency





def coin1ToCoin2(route, coinCurrencyId, numberOfCoinsToSell):
	temp, tempMarket = 0, None

	coins, secondMarket = 0, None
	for market in listMarkets['data']:
		# Trade with any coin OTHER than the origin coin.
		if int(market['coin_currency_id']) == coinCurrencyId and int(market['market_currency_id']) != int(originCurrency['id']) and int(market['coin_currency_id']) != int(originCurrency['id']):
			# pdb.set_trace()
			# relativeCoinValue = market['last_trade']['price']
			relativeCoinValue = market['24hr']['price_high']

			if relativeCoinValue <= 0:
				continue

			numberOfCoinsBought = numberOfCoinsToSell*relativeCoinValue

			# route[2] = '{:s} at price {:.10f} to buy {:.10f} coins'.format(market['label'],market['last_trade']['price'],numberOfCoinsBought)
			route[2] = '{:s} at price {:.10f} to buy {:.10f} coins'.format(market['label'],market['24hr']['price_high'],numberOfCoinsBought)
			coin2ToOriginCoin(route, int(market['market_currency_id']), numberOfCoinsBought)


def coin2ToOriginCoin(route, coinCurrencyId, numberOfCoinsToSell):
	temp = 0
	tempMarket = None
	for market in listMarkets['data']:
		# Trade with only origin coin.
		if int(market['market_currency_id']) == int(originCurrency['id']) and int(market['coin_currency_id']) == int(coinCurrencyId):
			# pdb.set_trace()
			# relativeCoinValue = market['last_trade']['price']
			relativeCoinValue = market['24hr']['price_low']

			if relativeCoinValue <= 0:
				continue

			numberOfCoinsBought = numberOfCoinsToSell*relativeCoinValue

			# route[3] = '{:s} at price {:.10f} to buy {:.10f} coins'.format(market['label'],market['last_trade']['price'],numberOfCoinsBought)
			route[3] = '{:s} at price {:.10f} to buy {:.10f} coins'.format(market['label'],market['24hr']['price_low'],numberOfCoinsBought)

			route[4] = numberOfCoinsBought
			tradeRoute.append(copy.deepcopy(route))


def init():
	# First Trade
	# pdb.set_trace()
	for market in listMarkets['data']:

		if int(market['market_currency_id']) == int(originCurrency['id']) and int(market['coin_currency_id']) != int(originCurrency['id']):
			# relativeCoinValue = market['last_trade']['price']
			relativeCoinValue = market['24hr']['price_high']

			if relativeCoinValue <= 0:
				continue

			# COIN1/ORIGIN_COIN
			numberOfCoinsBought = originCurrencyAmount/relativeCoinValue
			route = list()
			# route.extend(['{:.10f} {:s}'.format(originCurrencyAmount,originCurrency['code']),'{:s} at price {:.10f} to buy {:.10f} coins'.format(market['label'],market['last_trade']['price'],numberOfCoinsBought),0,0,0])

			route.extend(['{:.10f} {:s}'.format(originCurrencyAmount,originCurrency['code']),'{:s} at price {:.10f} to buy {:.10f} coins'.format(market['label'],market['24hr']['price_high'],numberOfCoinsBought),0,0,0])
			coin1ToCoin2(route, int(market['coin_currency_id']), numberOfCoinsBought)


	print(tradeRoute)



# init()
aa = c.market_orderbook(3,1)
pprint(aa)







