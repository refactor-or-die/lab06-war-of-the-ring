from abc import ABC, abstractmethod

class MilitaryUnit(ABC):
    @abstractmethod
    def strength(self) -> int:
        return getattr(self, "strength", 0)
    
    @abstractmethod
    def count(self) -> int:
        return getattr(self, "count", 0)
    
    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass