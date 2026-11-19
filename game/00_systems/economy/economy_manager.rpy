# LOLA - Economy Manager
# Handles money, costs, and transactions
# Ren'Py 8.6.0

init python:
    # ============================================================================
    # ECONOMY SYSTEM
    # ============================================================================
    
    def daily_expenses():
        """Calculate and apply daily essential expenses."""
        global money
        
        total = sum(essential_costs.values())
        if total > 0:
            if money >= total:
                spend_money(total, "Daily essentials")
                return True
            else:
                # Can't afford essentials - financial stress
                return False
        return True
    
    def set_essential_cost(category, amount):
        """Set an essential cost (only when confirmed by story)."""
        if category in essential_costs:
            essential_costs[category] = amount
            return True
        return False
    
    def get_essential_costs():
        """Get all essential costs."""
        return dict(essential_costs)
    
    def format_money(amount=None):
        """Format money for display."""
        if amount is None:
            amount = money
        return f"{amount} {currency}"
