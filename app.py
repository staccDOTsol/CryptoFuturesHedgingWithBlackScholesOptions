from blackscholes import black_scholes
import time
from datetime import datetime
#   >>> black_scholes(7598.45, 7000, 0.09587902546296297, 0.679, 0.03, 0.0, -1)
#   >>> black_scholes(7598.45, 9000, 0.09587902546296297, 0.675, 0.03, 0.0, 1)
from deribit_api    import RestClient
import math
from utils          import ( get_logger, lag, print_dict, print_dict_of_dicts, sort_by_key,
                             ticksize_ceil, ticksize_floor, ticksize_round )
URL     = 'https://www.deribit.com'

KEY     = ''
SECRET  = ''
client = RestClient( KEY, SECRET, URL )
while True:

	tty = datetime(2019,12,27).strftime('%s')

	theyield = 0.1541
	therisk = 15000

	spot = client.index()[ 'btc' ]

	insts               = client.getinstruments()
	options        = sort_by_key( { 
	    i[ 'instrumentName' ]: i for i in insts  if i[ 'kind' ] == 'option' and 'BTC' in i['instrumentName']
	} )
	exps = []
	strikes = []

	calls = []
	profits = {}
	puts = []
	es = {}
	for o in options:
		exp = datetime.strptime(options[o]['expiration'][:-13], '%Y-%m-%d')
		exps.append(exp.strftime('%s'))
		strikes.append(int(options[o]['strike']))
	a = -1
	#print(iv)
	strikes = list(dict.fromkeys(strikes))
	exps = list(dict.fromkeys(exps))
	#print(len(options))
	z = -1
	y = -1
	ivs = {}
	insts = {}
	has = {}
	optionsignore = []
	for o in options:
		z = z + 1
		#print(z)
		#print(client.getorderbook(options[o]['instrumentName']))
		ob = client.getorderbook(options[o]['instrumentName'])
		ivs[options[o]['instrumentName']] = ob['bidIv'] / 100
		bids = ob['bids']
		asks = ob['asks']
		lb = 99
		ha = 0
		for bid in bids:
			if bid['price'] < lb:
				lb = bid['price']

		for ask in asks:
			if ask['price'] > ha:
				ha = ask['price']
		if ha == 0:
			optionsignore.append(options[o]['instrumentName'])
		has[options[o]['instrumentName']] = ha

	for e in exps:
		#z = z + 1
		#print(z)
		calls = []
		puts = []
		civs = {}
		pivs = {}
		costc = []
		costp = []
		instsp = []
		instsc = []
		now = time.time() 
		if ((int(e) - int(now)) / 60 / 60 / 24 / 365 > 0):
			diff = (int(e) - int(now)) / 60 / 60 / 24 / 365

			for s in strikes:
				a = a + 1
				#print(a)
				for o in options:
					if 'BTC' in options[o]['instrumentName'] and options[o]['instrumentName'] not in optionsignore:
						iv = ivs[options[o]['instrumentName']]
						if iv != 0:
							exp2 = datetime.strptime(options[o]['expiration'][:-13], '%Y-%m-%d').strftime('%s')
							
							if((options[o]['optionType'] == 'call' and (options[o]['strike']) == s) and exp2 == e):
								calls.append(s)
								#print(calls)
								civs[s] = iv
								pivs[s] = iv

								costc.append(has[options[o]['instrumentName']])
								instsc.append(options[o]['instrumentName'])

								
							if((options[o]['optionType'] == 'put' and (options[o]['strike']) == s) and exp2 == e):
								
								puts.append(s)
								#print(puts)
								civs[s] = iv
								pivs[s] = iv
								costp.append(has[options[o]['instrumentName']])
								instsp.append(options[o]['instrumentName'])

		#print(len(puts))
		#print(len(calls))
		ccount = -1
		for c in calls:
			ccount = ccount+1
			pcount = -1
			for p in puts:
				pcount = pcount + 1
				p1 = black_scholes(spot, p, diff, pivs[p], 0.03, 0.0, -1) 
				c1 = black_scholes(spot, c, diff, civs[c], 0.03, 0.0, 1) 
				if c1 > costc[ccount] * spot:
					print('c1 underpriced!')
					print(c1)
					print ( {'price':  costc[ccount], 'call s' : c, 'put s': p, 'instrument':instsc[ccount], 'e': e})
				if p1 > costp[pcount] * spot:
					print('p1 underpriced!')
					print(p1)
					print ( {'price': costp[pcount], 'call s' : c, 'put s': p, 'instrument': instsp[pcount], 'e': e})
				
				c2 = black_scholes(spot * 1.15, p, diff, pivs[p], 0.03, 0.0, -1) 
				p2 = black_scholes(spot * 1.15, c, diff, civs[c], 0.03, 0.0, 1) 
				c3 = black_scholes(spot * 0.85, p, diff, pivs[p], 0.03, 0.0, -1) 
				p3 = black_scholes(spot * 0.85, c, diff, civs[c], 0.03, 0.0, 1) 
				cost1 =(c1 + p1)
				cost2 = (c2 + p2)
				cost3 = (c3 + p3)
				profit=(cost2-cost1)+(cost3-cost1)
				#print(profit)
				profits[profit] = {'price': costp[pcount] + costc[ccount], 'call s' : c, 'put s': p, 'call': instsc[ccount],'put': instsp[pcount],  'e': e}
				#print(profits[profit])
				#for pos in positions:
					#if 'BTC' in  pos['instrument']:
						#print(pos['floatingPl'] * 100)4
	biggest = 0
	costed = {}
	for p in profits.keys():
		costed[p] = (profits[p]['price'] * (therisk/(p+profits[p]['price'] * spot)))

		if p > biggest:
			biggest = p
	smallest = 9999999999999999
	for c in costed:
		#print(costed[c])
		if float(costed[c]) < smallest:
			smallest = float(costed[c])
			w1 = c
	print(' ')
	print('exposure: ' + str(therisk))
	print('cost to buy: ' + str(smallest))
	print('profit per unit at +/- 15%: ' + str(w1))
	print(profits[w1])
