from typing import List
from military_unit_interface import MilitaryUnit
from abc import abstractmethod

class UnitGroup(MilitaryUnit):
    def __init__(self, name: str):
        self.children: List[MilitaryUnit] = []
    
    def strength(self) -> int:
        return sum(child.strength() for child in self.children)
    
    def count(self) -> int:
        return sum(child.count() for child in self.children)
    
    @abstractmethod
    def get_units_by_type(self, unit_type: str) -> List:
        pass

    @abstractmethod
    def get_strongest_unit(self):
        pass
    

# ============================================================================
# STRUKTURY GRUPUJACE (tu konczy sie koszmar petli)
# ============================================================================

class Squad(UnitGroup):
    """Oddzial - najmniejsza grupa bojowa"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
    
    def add_unit(self, unit):
        self.children.append(unit)
    
    def get_strength(self) -> int:
        return self.strength()
    
    def count_units(self) -> int:
        return self.count()
    
    def show(self, indent: int = 0) -> str:
        """Wyswietla strukture oddzialu"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}[Oddzial: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})")
        for unit in self.children:
            lines.append(unit.show(indent+1))
        return "\n".join(lines)
    
    def show_undetailed(self, indent: int = 0) -> str:
        """Wyswietla strukture oddzialu"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}[Oddzial: {self.name}]")
        for unit in self.children:
            lines.append(unit.show(indent+1))
        return "\n".join(lines)
    
    def get_units_by_type(self, unit_type: str) -> List:
        result = []
        for unit in self.children:
            if unit.unit_type == unit_type:
                result.append(unit)
        return result
    
    def get_strongest_unit(self):
        strongest = None
        maxStrength = 0
        for child in self.children:
            if child.strength() > maxStrength:
                strongest = child
                maxStrength = child.strength()
        return strongest



class Legion(UnitGroup):
    """Legion - duza formacja bojowa skladajaca sie z oddzialow"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
    
    def add_squad(self, squad: Squad):
        self.children.append(squad)
    
    def get_strength(self) -> int:
        return self.strength()
    
    def count_units(self) -> int:
        return self.count()
    
    def show(self, indent: int = 0) -> str:
        """Wyswietla strukture legionu - I ZNOWU PETLE!"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}[Legion: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})")
        for squad in self.children:
            lines.append(squad.show_undetailed(indent+1))
        return "\n".join(lines)
    
    def show_undetailed(self, indent: int = 0) -> str:
        """Wyswietla strukture legionu - I ZNOWU PETLE!"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}[Legion: {self.name}]")
        for squad in self.children:
            lines.append(squad.show_undetailed(indent+1))
        return "\n".join(lines)
    
    def get_units_by_type(self, unit_type: str) -> List:
        result = []
        for squad in self.children:
            result.extend(squad.get_units_by_type(unit_type))
        return result
    
    def get_strongest_unit(self):
        strongest = None
        maxStrength = 0
        for child in self.children:
            childStrongest = child.get_strongest_unit()
            if childStrongest.strength() > maxStrength:
                strongest = childStrongest
                maxStrength = childStrongest.strength()
        return strongest


class Army(UnitGroup):
    """Armia - cala potega wojskowa"""
    
    def __init__(self, name: str, faction: str):
        super().__init__(name)
        self.name = name
        self.faction = faction  # "Mordor", "Isengard", "Gondor", etc.
    
    def add_legion(self, legion: Legion):
        self.children.append(legion)
    
    def get_strength(self) -> int:
        return self.strength()
    
    def count_units(self) -> int:
        return self.count()
    
    def count_squads(self) -> int:
        """Liczy oddzialy"""
        count = 0
        for legion in self.children:
            count += len(legion.children)
        return count
    
    def show(self, indent: int = 0) -> str:
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===")
        lines.append(f"{prefix}Calkowita sila: {self.get_strength()}")
        lines.append(f"{prefix}Liczba jednostek: {self.count_units()}")
        lines.append(f"{prefix}Liczba oddzialow: {self.count_squads()}")
        lines.append(f"{prefix}Liczba legionow: {len(self.children)}")
        lines.append(f"{prefix}" + "-" * 40)
        
        for legion in self.children:
            lines.append(legion.show_undetailed())
        
        return "\n".join(lines)
    
    def get_units_by_type(self, unit_type: str) -> List:
        result = []
        for squad in self.children:
            result.extend(squad.get_units_by_type(unit_type))
        return result
        
    def get_strongest_unit(self):
        strongest = None
        maxStrength = 0
        for child in self.children:
            childStrongest = child.get_strongest_unit()
            if childStrongest.strength() > maxStrength:
                strongest = childStrongest
                maxStrength = childStrongest.strength()
        return strongest