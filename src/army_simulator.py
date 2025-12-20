from abc import ABC, abstractmethod
from typing import List, Optional


class MilitaryUnit(ABC):
    @abstractmethod
    def get_strength(self) -> int:
        pass
    @abstractmethod
    def count_units(self) -> int:
        pass
    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass

class Warrior(MilitaryUnit):
    def __init__(self, name: str, unit_type: str, strength: int, description: str):
        self.name = name
        self.unit_type = unit_type
        self._strength = strength
        self.description = description

    def get_strength(self) -> int:
        return self._strength

    def count_units(self) -> int:
        return 1

    def show(self, indent: int = 0) -> str:
        prefix = " " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self._strength})"
    def get_strongest_unit(self) -> MilitaryUnit:
        return self
    def get_units_by_type(self, unit_type: str) -> List:
        return [self] if unit_type == self.unit_type else []


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
        super().__init__(name, "Elf", 15, "Wieczny, madry i smiertelnie celny")

class Human(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Human", 8, "Smiertelnik broniacy swojej ziemi")

class Dwarf(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Dwarf", 14, "Twardy jak skala, z ktorej sie wywodzi")

class Wizard(Warrior):
    def __init__(self, name: str):
        super().__init__(name, "Wizard", 150, "Maiar w ludzkiej postaci")

class UnitGroup(MilitaryUnit):
    def __init__(self, name: str, unit_type: str):
        self.name = name
        self.unit_type = unit_type
        self.children: List[MilitaryUnit] = []

    def add(self, unit: MilitaryUnit):
        self.children.append(unit)

    def get_strength(self) -> int:
        return sum(child.get_strength() for child in self.children)

    def count_units(self) -> int:
        return sum(child.count_units() for child in self.children)

    def get_strongest_unit(self) -> Warrior:
        if not self.children:
            return None
        candidates = [child.get_strongest_unit() for child in self.children if child.get_strongest_unit()]
        return max(candidates, key=lambda u: u.get_strength())

    def show(self, indent: int = 0) -> str:
        lines = []
        prefix = " " * indent
        lines.append(f"{prefix}[{self.unit_type}: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})")
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)
    def get_units_by_type(self, unit_type: str)-> List:
        units = []
        for child in self.children:
            units.extend(child.get_units_by_type(unit_type))
        if unit_type == self.unit_type:
            units.append(self)
        return units

class Squad(UnitGroup):
    def __init__(self, name: str):
        super().__init__(name, "Squad")


class Legion(UnitGroup):
    def __init__(self, name: str):
        super().__init__(name, "Legion")

class Army(UnitGroup):
    def __init__(self, name: str, faction: str):
        super().__init__(name, "Army")
        self.faction = faction

    def show(self, indent: int = 0) -> str:
        lines = []
        prefix = " " * indent
        lines.append(f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===")
        lines.append(f"{prefix}Calkowita sila: {self.get_strength()}")
        lines.append(f"{prefix}Liczba jednostek: {self.count_units()}")
        lines.append(f"{prefix}liczba odzialow: {len(self.get_units_by_type('Squad'))}")
        lines.append(f"{prefix}Calkowita sila: {len(self.get_units_by_type('Legion'))}")
        lines.append(f"{prefix}" + "-" * 40)

        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)


def compare_forces(army1: Army, army2: Army) -> dict:
    return {
        "army1_name": army1.name,
        "army1_strength": army1.get_strength(),
        "army1_units": army1.count_units(),
        "army2_name": army2.name,
        "army2_strength": army2.get_strength(),
        "army2_units": army2.count_units(),
        "stronger": army1.name if army1.get_strength() > army2.get_strength() else army2.name,
        "difference": abs(army1.get_strength() - army2.get_strength())
    }

def merge_armies(army1: Army, army2: Army, new_name: str) -> Army:
    merged = Army(new_name, f"{army1.faction}+{army2.faction}")
    for child in army1.children:
        merged.add(child)
    for child in army2.children:
        merged.add(child)
    return merged


def create_mordor_army() -> Army:
    """Tworzy przykladowa Armie Mordoru"""
    # Jednostki
    grishnakh = Orc("Grishnakh")
    shagrat = Orc("Shagrat")
    gorbag = Orc("Gorbag")
    muzgash = Orc("Muzgash")
    troll1 = Troll("Rogash")
    troll2 = Troll("Grond-pusher")
    witch_king = Nazgul("Witch-king of Angmar")
    khamul = Nazgul("Khamul")
    # Oddzialy
    orc_scouts = Squad("Orkowi Zwiadowcy")
    orc_scouts.add(grishnakh)
    orc_scouts.add(shagrat)
    orc_warriors = Squad("Orczy Wojownicy")
    orc_warriors.add(gorbag)
    orc_warriors.add(muzgash)
    troll_squad = Squad("Trolle Bojowe")
    troll_squad.add(troll1)
    troll_squad.add(troll2)
    nazgul_squad = Squad("Upiory Pierscienia")
    nazgul_squad.add(witch_king)
    nazgul_squad.add(khamul)
    # Legiony
    infantry_legion = Legion("Legion Piechoty")
    infantry_legion.add(orc_scouts)
    infantry_legion.add(orc_warriors)
    elite_legion = Legion("Legion Elitarny")
    elite_legion.add(troll_squad)
    elite_legion.add(nazgul_squad)
    # Armia
    mordor = Army("Armia Mordoru", "Mordor")
    mordor.add(infantry_legion)
    mordor.add(elite_legion)
    return mordor


def create_gondor_army() -> Army:
    """Tworzy przykladowa Armie Gondoru"""
    # Jednostki
    faramir = Human("Faramir")
    beregond = Human("Beregond")
    pippin = Human("Pippin") # Honorary human :)
    legolas = Elf("Legolas")
    haldir = Elf("Haldir")
    gimli = Dwarf("Gimli")
    gandalf = Wizard("Gandalf Bialy")
    # Oddzialy
    rangers = Squad("Strazicy Ithilien")
    rangers.add(faramir)
    rangers.add(beregond)
    guards = Squad("Straze Cytadeli")
    guards.add(pippin)
    elven_archers = Squad("Elfi Lucznicy")
    elven_archers.add(legolas)
    elven_archers.add(haldir)
    fellowship_remnants = Squad("Resztki Druzyny")
    fellowship_remnants.add(gimli)
    fellowship_remnants.add(gandalf)
    # Legiony
    gondor_legion = Legion("Legion Gondoru")
    gondor_legion.add(rangers)
    gondor_legion.add(guards)
    allies_legion = Legion("Legion Sojusznikow")
    allies_legion.add(elven_archers)
    allies_legion.add(fellowship_remnants)
    # Armia
    gondor = Army("Armia Gondoru", "Gondor")
    gondor.add(gondor_legion)
    gondor.add(allies_legion)
    return gondor


if __name__ == "__main__":
    print("=" * 60)
    print("SYMULATOR ARMII SRODZIEMIA")
    print("=" * 60)
    # Tworzymy armie
    mordor = create_mordor_army()
    gondor = create_gondor_army()
    # Wyswietlamy struktury
    print("\n" + mordor.show())
    print("\n" + gondor.show())
    # Porownujemy sily
    print("\n" + "=" * 60)
    print("POROWNANIE SIL")
    print("=" * 60)
    comparison = compare_forces(mordor, gondor)
    print(f"\n{comparison['army1_name']}:")
    print(f" Sila: {comparison['army1_strength']}")
    print(f" Jednostek: {comparison['army1_units']}")
    print(f"\n{comparison['army2_name']}:")
    print(f" Sila: {comparison['army2_strength']}")
    print(f" Jednostek: {comparison['army2_units']}")
    print(f"\nSilniejsza armia: {comparison['stronger']}")
    print(f"Roznica sil: {comparison['difference']}")
    # Najsilniejsza jednostka
    print("\n" + "=" * 60)
    print("NAJSILNIEJSZE JEDNOSTKI")
    print("=" * 60)
    mordor_strongest = mordor.get_strongest_unit()
    gondor_strongest = gondor.get_strongest_unit()
    print(f"\nMordor: {mordor_strongest.name} ({mordor_strongest.unit_type}) - sila {mordor_strongest.strength}")
    print(f"Gondor: {gondor_strongest.name} ({gondor_strongest.unit_type}) - sila {gondor_strongest.strength}")