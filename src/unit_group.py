
from typing import List
from .military_unit import MilitaryUnit

class UnitGroup(MilitaryUnit):
    def __init__(self, name: str):
        self.children: List[MilitaryUnit] = []
    
    def strength(self) -> int:
        return sum(child.strength() for child in self.children)
    
    def count(self) -> int:
        return sum(child.count() for child in self.children)