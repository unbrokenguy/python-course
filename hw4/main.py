from transactions.manager import TransactionManager
from transactions.manager import InvalidTransactionException

manager = TransactionManager()
if __name__ == "__main__":
    user_input = input()
    while user_input != "quit":
        try:
            manager.add(user_input)
        except InvalidTransactionException as e:
            print(e.message)
        user_input = input()
    manager.quit()
