# Cash transactions are recorded through this wallet module.
init python:
    def record_wallet_entry(kind, amount, note):
        wallet_ledger.insert(0, {"day": current_day, "kind": kind,
                                 "amount": amount, "note": note})
        del wallet_ledger[100:]

    def add_money(amount, note="Story income"):
        global money
        if amount <= 0:
            return False
        money += amount
        record_wallet_entry("income", amount, note)
        return True

    def spend_money(amount, note="Purchase"):
        global money
        if amount < 0 or money < amount:
            return False
        money -= amount
        record_wallet_entry("expense", -amount, note)
        return True

    def can_afford(amount):
        return amount >= 0 and money >= amount

    def get_balance():
        return money

    def get_wallet_history(limit=20):
        return wallet_ledger[:max(0, limit)]
