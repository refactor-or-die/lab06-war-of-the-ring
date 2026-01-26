from typing import List, Dict, Optional
from abc import ABC, abstractmethod

class MilitaryUnit(ABC):
    @property
    @abstractmethod
    def strength(self) -> int:
        pass

    def get_strength(self) -> int:
        return self.strength

    @abstractmethod
    def count_units(self) -> int:
        pass

    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass

    @abstractmethod
    def get_units_by_type(self, unit_type: str) -> List['Warrior']:
        pass

    @abstractmethod
    def get_strongest_unit(self) -> Optional['Warrior']:
        pass

class Warrior(MilitaryUnit):
    def __init__(self, name: str, unit_type: str, strength: int, description: str):
        self.name = name
        self.unit_type = unit_type
        self._strength_val = strength
        self.description = description

    @property
    def strength(self) -> int:
        return self._strength_val

    def count_units(self) -> int:
        return 1

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self.strength})"

    def get_units_by_type(self, unit_type: str) -> List['Warrior']:
        if self.unit_type == unit_type:
            return [self]
        return []

    def get_strongest_unit(self) -> 'Warrior':
        return self

class Orc(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Orc", 5, "Plugawy sluga Ciemnosci")

class UrukHai(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Uruk-hai", 12, "Doskonaly wojownik stworzony przez Sarumana")

class Troll(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Troll", 45, "Ogromna bestia, lepiej nie stawac na drodze")

class Nazgul(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Nazgul", 100, "Byly krol, teraz sluga Saurona")

class Elf(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Elf", 15, "Wieczny, madry i smiertenie celny")

class Human(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Human", 8, "Smiertelnik broniacy swojej ziemi")

class Dwarf(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Dwarf", 14, "Twardy jak skala, z ktorej sie wywodzi")

class Wizard(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Wizard", 150, "Maiar w ludzkiej postaci")

class CompositeUnit(MilitaryUnit):
    def __init__(self, name: str):
        self.name = name
        self._children: List[MilitaryUnit] = []

    def add(self, unit: MilitaryUnit):
        self._children.append(unit)

    @property
    def strength(self) -> int:
        return sum(child.strength for child in self._children)

    def count_units(self) -> int:
        return sum(child.count_units() for child in self._children)

    def get_units_by_type(self, unit_type: str) -> List[Warrior]:
        result = []
        for child in self._children:
            result.extend(child.get_units_by_type(unit_type))
        return result

    def get_strongest_unit(self) -> Optional[Warrior]:
        candidates = [child.get_strongest_unit() for child in self._children]
        valid_candidates = [c for c in candidates if c is not None]
        if not valid_candidates:
            return None
        return max(valid_candidates, key=lambda u: u.strength)

    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass

    def _show_children(self, indent: int) -> str:
        lines = []
        for child in self._children:
            lines.append(child.show(indent))
        return "\n".join(lines)

class Squad(CompositeUnit):
    @property
    def units(self):
        return self._children

    def add_unit(self, unit: Warrior):
        self.add(unit)

    def show(self, indent: int = 0) -> str:
        lines = []
        prefix = "  " * indent
        header = f"{prefix}[Oddzial: {self.name}] (sila: {self.strength}, jednostek: {self.count_units()})"
        lines.append(header)
        if self._children:
            lines.append(self._show_children(indent))
        child_content = self._show_children(indent + 1)
        if child_content:
            lines.append(child_content)

        return "\n".join(lines)

class Legion(CompositeUnit):
    @property
    def squads(self):
        return self._children

    def add_squad(self, squad: Squad):
        self.add(squad)

    def show(self, indent: int = 0) -> str:
        lines = []
        prefix = "  " * indent
        header = f"{prefix}[Legion: {self.name}] (sila: {self.strength}, jednostek: {self.count_units()})"
        lines.append(header)

        child_content = self._show_children(indent + 1)
        if child_content:
            lines.append(child_content)

        return "\n".join(lines)

class Army(CompositeUnit):
    def __init__(self, name: str, faction: str):
        super().__init__(name)
        self.faction = faction

    @property
    def legions(self):
        return self._children

    def add_legion(self, legion: Legion):
        self.add(legion)

    def count_squads(self) -> int:
        count = 0
        for child in self._children:
            if isinstance(child, CompositeUnit):
                count += len(child._children)
        return count

    def show(self, indent: int = 0) -> str:
        lines = []
        prefix = "  " * indent

        lines.append(f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===")
        lines.append(f"{prefix}Calkowita sila: {self.strength}")
        lines.append(f"{prefix}Liczba jednostek: {self.count_units()}")
        lines.append(f"{prefix}Liczba oddzialow: {self.count_squads()}")
        lines.append(f"{prefix}Liczba legionow: {len(self._children)}")
        lines.append(f"{prefix}" + "-" * 40)

        child_content = self._show_children(indent + 1)
        if child_content:
            lines.append(child_content)

        return "\n".join(lines)

def compare_forces(army1: Army, army2: Army) -> Dict:
    return {
        "army1_name": army1.name,
        "army1_strength": army1.get_strength(),
        "army1_units": army1.count_units(),
        "army2_name": army2.name,
        "army2_strength": army2.get_strength(),
        "army2_units": army2.count_units(),
        "stronger": army1.name if army1.strength > army2.strength else army2.name,
        "difference": abs(army1.strength - army2.strength)
    }

def merge_armies(army1: Army, army2: Army, new_name: str) -> Army:
    merged = Army(new_name, f"{army1.faction}+{army2.faction}")
    for legion in army1.legions:
        merged.add_legion(legion)
    for legion in army2.legions:
        merged.add_legion(legion)
    return merged

def create_mordor_army() -> Army:
    grishnakh = Orc("Grishnakh")
    shagrat = Orc("Shagrat")
    gorbag = Orc("Gorbag")
    muzgash = Orc("Muzgash")

    troll1 = Troll("Rogash")
    troll2 = Troll("Grond-pusher")

    witch_king = Nazgul("Witch-king of Angmar")
    khamul = Nazgul("Khamul")

    orc_scouts = Squad("Orkowi Zwiadowcy")
    orc_scouts.add_unit(grishnakh)
    orc_scouts.add_unit(shagrat)

    orc_warriors = Squad("Orczy Wojownicy")
    orc_warriors.add_unit(gorbag)
    orc_warriors.add_unit(muzgash)

    troll_squad = Squad("Trolle Bojowe")
    troll_squad.add_unit(troll1)
    troll_squad.add_unit(troll2)

    nazgul_squad = Squad("Upiory Pierscienia")
    nazgul_squad.add_unit(witch_king)
    nazgul_squad.add_unit(khamul)

    infantry_legion = Legion("Legion Piechoty")
    infantry_legion.add_squad(orc_scouts)
    infantry_legion.add_squad(orc_warriors)

    elite_legion = Legion("Legion Elitarny")
    elite_legion.add_squad(troll_squad)
    elite_legion.add_squad(nazgul_squad)

    mordor = Army("Armia Mordoru", "Mordor")
    mordor.add_legion(infantry_legion)
    mordor.add_legion(elite_legion)

    return mordor

def create_gondor_army() -> Army:
    faramir = Human("Faramir")
    beregond = Human("Beregond")
    pippin = Human("Pippin")

    legolas = Elf("Legolas")
    haldir = Elf("Haldir")

    gimli = Dwarf("Gimli")

    gandalf = Wizard("Gandalf Bialy")

    rangers = Squad("Strazicy Ithilien")
    rangers.add_unit(faramir)
    rangers.add_unit(beregond)

    guards = Squad("Straze Cytadeli")
    guards.add_unit(pippin)

    elven_archers = Squad("Elfi Lucznicy")
    elven_archers.add_unit(legolas)
    elven_archers.add_unit(haldir)

    fellowship_remnants = Squad("Resztki Druzyny")
    fellowship_remnants.add_unit(gimli)
    fellowship_remnants.add_unit(gandalf)

    gondor_legion = Legion("Legion Gondoru")
    gondor_legion.add_squad(rangers)
    gondor_legion.add_squad(guards)

    allies_legion = Legion("Legion Sojusznikow")
    allies_legion.add_squad(elven_archers)
    allies_legion.add_squad(fellowship_remnants)

    gondor = Army("Armia Gondoru", "Gondor")
    gondor.add_legion(gondor_legion)
    gondor.add_legion(allies_legion)

    return gondor

if __name__ == "__main__":
    print("=" * 60)
    print("SYMULATOR ARMII SRODZIEMIA (COMPOSITE VERSION)")
    print("=" * 60)

    mordor = create_mordor_army()
    gondor = create_gondor_army()

    print("\n" + mordor.show())
    print("\n" + gondor.show())

    comparison = compare_forces(mordor, gondor)
    print(f"\nSilniejsza armia: {comparison['stronger']} (roznica: {comparison['difference']})")