# Fictional, offline Bitcoin model; no external market or real-money link.
init python:
    def bitcoin_price(day=None):
        if day is None:
            day = current_day
        return max(20, 100 + ((day * 37) % 121) - 60)

    def buy_bitcoin(amount):
        global bitcoin_units, bitcoin_cost_basis, financial_literacy
        if amount <= 0 or not spend_money(amount, "Bitcoin investment"):
            return False
        bitcoin_units += float(amount) / bitcoin_price()
        bitcoin_cost_basis += amount
        change_stat("financial_literacy", 1)
        return True

    def sell_bitcoin(units):
        global bitcoin_units, bitcoin_cost_basis, bitcoin_realized_gain
        if units <= 0 or units > bitcoin_units:
            return False
        share = units / bitcoin_units
        proceeds = int(units * bitcoin_price())
        basis = bitcoin_cost_basis * share
        bitcoin_units -= units
        bitcoin_cost_basis -= basis
        bitcoin_realized_gain += proceeds - basis
        add_money(proceeds, "Bitcoin sale")
        return proceeds

    def bitcoin_summary():
        value = bitcoin_units * bitcoin_price()
        return {"units": bitcoin_units, "price": bitcoin_price(),
                "value": value, "cost_basis": bitcoin_cost_basis,
                "unrealized_gain": value - bitcoin_cost_basis,
                "realized_gain": bitcoin_realized_gain}
