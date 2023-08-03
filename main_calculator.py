class NewCostCalculator:
    def __init__(self, starting_weight: int, quantity_used: int, total_used_weight: int, paid_value: float):
        self.starting_weight = starting_weight
        self.quantity_used = quantity_used
        self.total_used_weight = total_used_weight
        self.paid_value = paid_value

    
    def get_total_weight(self):
        total_weight = self.starting_weight * self.quantity_used

        return total_weight
    

    def get_total_paid(self):
        total_paid = self.paid_value * self.quantity_used

        return total_paid


    def get_cost(self):
        total_paid = NewCostCalculator.get_total_paid(self)
        total_weight = NewCostCalculator.get_total_weight(self)

        cost = total_paid / total_weight * self.total_used_weight

        return cost
    
