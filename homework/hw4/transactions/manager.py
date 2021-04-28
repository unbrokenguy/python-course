import pickle
import re
from pickle import UnpicklingError
from functools import reduce


class InvalidTransactionException(Exception):
    def __init__(self, message="Value must be number"):
        self.message = message
        super().__init__(self.message)


class TransactionStorageError(Exception):
    pass


class TransactionManager:
    def __init__(self):
        self.storage_file = "transactions.pkl"
        self.storage = None
        try:
            storage = open(self.storage_file, "rb")
        except FileNotFoundError:
            storage = open(self.storage_file, "wb")
            pickle.dump({}, storage)
            storage.close()
            storage = open(self.storage_file, "rb")
        try:
            self.storage = pickle.load(storage)
            storage.close()
        except UnpicklingError:
            raise TransactionStorageError("Corrupted storage file.")
        if type(self.storage) is not dict:
            raise TransactionStorageError("Corrupted storage file.")

    def __dump__(self):
        with open(self.storage_file, "wb") as storage:
            pickle.dump(self.storage, storage)

    def __check__(self, transaction):
        transaction = transaction.split(" ")
        if len(transaction) != 2:
            raise InvalidTransactionException(message="Too many arguments.")
        name = transaction[0]
        if re.match(r"^\d+$", transaction[1]):
            value = int(transaction[1])
        elif re.match(r"^\d+([.]\d+)$", transaction[1]):
            value = float(transaction[1])
        else:
            raise InvalidTransactionException(message="Value must be number.")
        return name, value

    def add(self, transaction):
        name, value = self.__check__(transaction)
        if name not in self.storage.keys():
            self.storage[name] = []
        self.storage[name].append(value)

    def quit(self):
        self.__dump__()
        print("All types of transactions:")
        print("\n".join(list(map(lambda x: x[0] + ", spent: " + str(sum(x[1])), self.storage.items()))))
        print("Total spent: ", reduce(lambda x, y: x + y, map(lambda x: sum(x[1]), self.storage.items())))
