If you found this repo useful, consider clicking the sponsor button near the top :) Sponsoring via GitHub is as little as $1/month and if you do not use banks or credit cards, there are crypto links included :)<br /><br />
See This Article in It’s Original Form on dunncreativess.github.io! https://dunncreativess.github.io/2019/11/22/risk-free-futures-market-making-by-hedging-long-straddle-options/

Want to See And Play With The Code? Here it Is On Github! (this repo...)

Sponsor Me On Github! https://github.com/sponsors/dunncreativess


In the quantitative finance world, there are some holy grails: you can decrease the risk of an exposed position generally by doing something in the opposite direction.

In the simplest form, we can both long and short in two opposite positions on exchanges that use the long-short model like OkEx. In doing so, a price movement up or down will have the exact same effect on your position – where you’re losing fees and only fees.

In reality, that’s no good because we don’t want to be losing on every trade 🙂

What I’ve decided to try my hand at is something called a ‘long straddle.’ This was mentioned during my interview with Coindex Labs a long time ago – but basically, if you buy a put option and buy a call option ‘out of the money’ it’s relatively cheap – if the price doesn’t move at all, they both expire worthless.


But: if the price increases OR decreases a significant amount, one of those options expires in the money.. meaning it gianed value from potentially nothing into potentially something!

What this means is that, while the market maker is performing within specifications and earning money from low price volatility and volumes on the bid/ask, these options can expire worthless and our income from market making pays for the expired options – and then more!


If the market moves too much in one direction, we’re risking liquidating our funds if we hold market making positions that go sour.

If this happens – one of our long straddle options expires ‘in the money’ enough for us to cover our losses. What this means is risk-free trading – so long as the assumption holds true that the market making earns more than the cost of the options.


In my code, we loop through all the expiries and all the strikes for all the options, and then find the one whose ratio of cost vs. profits for a 15% movement in price (which is 100% liquidated at 6.66x leverage) yields the minimum threshold we need to cover $15 000 in exposed futures ($99 900 notional). In our example output, the Dec 6 options straddle for $6250 put and $9750 call would cost a total of 0.017 BTC for both the long put and long call, and each would earn $342 profit if the underlying price moved 15% and all else remained the same. This means that spending 0.54 BTC would completely cover the risk of liquidating 2 BTC exposed at 6.66x leverage – at least until implied volatilities change significantly or time value declines as we approach expiry! When these situations occur, the hedging bot would just create new orders in real-time to hedge the risk. Hooah!

!! Click here to subscribe: http://eepurl.com/gIykNL

Be notified about new articles? Welcome to the Jarett Dunn email subscriber list! Each new signup will receive a link to download the Coindex Labs non-NDA teaser, which includes information about the value proposition for my organization – where we’re setting our sights first on a money-printing machine, then returning later as conquering heroes in order to then defeat the world’s greater humanitarian issues.

Remember to CLICK, subscribe: http://eepurl.com/gIykNL !!

(Disclaimer: The Author is the Chief Liquidity Officer at Coindex)
