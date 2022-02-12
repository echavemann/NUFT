from InvestopediaApi import ita

client = ita.Account("email", "password")

portfolio = client.get_current_securities()

# Portfolio is not a list, it is a namedtuple object with 3 attributes: bought, shorted, options.
# Each of bought, shorted, and options is a list of Security objects, which have attributes
# symbol, description, quantity, purchase_price, current_price, current_value, and gain_loss

bought_securities = portfolio.bought
shorted_securities = portfolio.shorted
options = portfolio.options

for bought in bought_securities:
    print(bought.symbol)
    print(bought.description)
    print(bought.purchase_price)

