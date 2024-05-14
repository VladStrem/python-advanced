import time
from threading import Lock, Thread


class BankAccount:
    def __init__(self, account_id: int, name: str, balance: float):
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.lock = Lock()

    def deposit(self, amount: float) -> None:
        with self.lock:
            self.balance += amount
            print(f'Deposited {amount} UAH to {self.name}. New balance: {self.balance} UAH')

    def withdraw(self, amount: float) -> bool:
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                print(f'Withdraw {amount} UAH from {self.name}. New balance: {self.balance} UAH')
                return True
            else:
                print(f'Not enough funds in {self.name}. Current balance: {self.balance} UAH')
                return False

    def check_balance(self) -> None:
        with self.lock:
            print(f'Balance of {self.name}: {self.balance} UAH')


class ATM:
    def __init__(self, money: float):
        self.money = money
        self.lock = Lock()

    def replenish(self, amount: float) -> None:
        with self.lock:
            self.money += amount
            print(f'ATM replenished with {amount} UAH. New ATM balance: {self.money}')

    def perform_transaction(self, account: BankAccount, amount: float, action: str) -> None:
        with self.lock:
            time.sleep(1)  # імітація затримки обробки операції
            if action == 'withdraw':
                if self.money >= amount and account.withdraw(amount):
                    self.money -= amount
            elif action == 'deposit':
                account.deposit(amount)
                self.money += amount


def user_operation(account: BankAccount, atm: ATM):
    for _ in range(5):
        action = 'withdraw' if _ % 2 == 0 else 'deposit'
        amount = 300 if action == 'withdraw' else 400
        atm.perform_transaction(account, amount, action)
        account.check_balance()
        time.sleep(0.5)


account1 = BankAccount(1, "John", 1000)
account2 = BankAccount(2, "Alice", 1500)
atm = ATM(5000)


if __name__ == "__main__":
    user1_thread = Thread(target=user_operation, args=(account1, atm))
    user2_thread = Thread(target=user_operation, args=(account2, atm))

    user1_thread.start()
    user2_thread.start()

    time.sleep(4)
    atm.replenish(2000)

    user1_thread.join()
    user2_thread.join()

    print(f'Total money in ATM: {atm.money} UAH')
    account1.check_balance()
    account2.check_balance()
