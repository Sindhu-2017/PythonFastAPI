class IncomeNotFoundError(Exception):
    def __init__(self, income_id : int):
        self.income_id = income_id
        super().__init__(f"Income with ID {income_id} was not found")

class InvalidExpenseAmountError(Exception):
    def __init__(self, expense_amount, income_amount):
        self.expense_amount = expense_amount
        self.income_amount = income_amount
        super().__init__(
            f"Expense amount ({expense_amount}) cannot be greater than "
            f"income amount ({income_amount})"
        )
