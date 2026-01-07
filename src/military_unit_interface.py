from abc import ABC, abstractmethod

class MilitaryUnit(ABC):
    @abstractmethod
    def strength(self) -> int:
        pass
    
    @abstractmethod
    def count(self) -> int:
        pass
    
    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass