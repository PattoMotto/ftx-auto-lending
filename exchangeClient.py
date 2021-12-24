class ExchangeClient:
  def __init__(self, exchange):
    self.exchange = exchange

  def getBalance(self, tokenCode):
    balance = self.exchange.fetch_balance()
    if tokenCode in balance:
      return balance[tokenCode]['total']
    else:
      return 0.0

  def lendAsset(self, coin, size, rate=1e-06):
    self.exchange.private_post_spot_margin_offers({
      'coin': coin,
      'size': size,
      'rate': rate
    })
