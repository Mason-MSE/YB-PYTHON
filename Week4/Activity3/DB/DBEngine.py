from abc import ABC, abstractmethod
from contextlib import contextmanager
class DBEngine(ABC):
    #Abstract database engine supporting transactions and MyBatis-style operations.

    @abstractmethod
    def execute(self, sql, params=()):
        pass

    @abstractmethod
    def fetch(self, sql, params=()):
        pass

    @abstractmethod
    def close(self):
        pass

    @contextmanager
    def transaction(self):
        #Context manager for transactional operations.
        try:
            yield
            self.commit()
        except Exception as e:
            self.rollback()
            raise e

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass