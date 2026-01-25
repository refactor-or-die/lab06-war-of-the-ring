from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union

# ============================================================================
# COMPONENT (Interfejs dla wszystkich jednostek i grup)
# ============================================================================

class MilitaryUnit(ABC):
    """
    Wspolny interfejs dla pojedynczych zolnierzy (Leaf) 
    i grup bojowych (Composite).
    """
    
    @abstractmethod
    def get_strength(self) -> int:
        pass
    
    @abstractmethod
    def count_units(self) -> int:
        pass
    
    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass
        
    # Metody opcjonalne dla lisci, ale kluczowe dla Composite
    # W domyslnej implementacji moga nic nie robic lub zwracac puste wartosci
    
    def get_strongest_unit(self) -> Optional['Warrior']:
        return None

    def get_units_by_type(self, unit_type: str) -> List['Warrior']:
        return []

    def count_squads(self) -> int:
        return 0


# ============================================================================
# LEAF (Pojedynczy Wojownik)
# ============================================================================

class Warrior(MilitaryUnit):
    """Bazowa klasa dla wszystkich typow zolnierzy (Liscie)"""
    
    def __init__(self, name: str, strength: int, unit_type: str, description: str):
        self.name = name
        self._strength = strength
        self.unit_type = unit_type
        self.description = description
        
    def get_strength(self) -> int:
        return self._strength
        
    def count_units(self) -> int:
        return 1
        
    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self._strength})"

    def get_strongest_unit(self) -> 'Warrior':
        return self

    def get_units_by_type(self, unit_type: str) -> List['Warrior']:
        return [self] if self.unit_type == unit_type else []


# Konkretne typy jednostek (dziedziczą po Warrior)

class Orc(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 5, "Orc", "Plugawy sluga Ciemnosci")

class UrukHai(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 12, "Uruk-hai", "Doskonaly wojownik stworzony przez Sarumana")

class Troll(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 45, "Troll", "Ogromna bestia, lepiej nie stawac na drodze")

class Nazgul(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 100, "Nazgul", "Byly krol, teraz sluga Saurona")

class Elf(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 15, "Elf", "Wieczny, madry i smiertenie celny")

class Human(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 8, "Human", "Smiertelnik broniacy swojej ziemi")

class Dwarf(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 14, "Dwarf", "Twardy jak skala, z ktorej sie wywodzi")

class Wizard(Warrior):
    def __init__(self, name: str):
        super().__init__(name, 150, "Wizard", "Maiar w ludzkiej postaci")


# ============================================================================
# COMPOSITE (Grupy jednostek: Oddzial, Legion, Armia)
# ============================================================================

class CompositeUnit(MilitaryUnit):
    """
    Klasa bazowa dla grup jednostek (Squad, Legion, Army).
    Implementuje logike rekurencyjna.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.children: List[MilitaryUnit] = []
        
    def add(self, unit: MilitaryUnit):
        self.children.append(unit)
        
    def remove(self, unit: MilitaryUnit):
        self.children.remove(unit)
        
    def get_strength(self) -> int:
        # REKURENCJA ZAMIAST ZAGNIEZDZONYCH PETLI
        return sum(child.get_strength() for child in self.children)
        
    def count_units(self) -> int:
        return sum(child.count_units() for child in self.children)
        
    def get_strongest_unit(self) -> Optional[Warrior]:
        strongest = None
        max_strength = -1
        
        for child in self.children:
            candidate = child.get_strongest_unit()
            if candidate and candidate.get_strength() > max_strength:
                max_strength = candidate.get_strength()
                strongest = candidate
        return strongest

    def get_units_by_type(self, unit_type: str) -> List[Warrior]:
        units = []
        for child in self.children:
            units.extend(child.get_units_by_type(unit_type))
        return units

    def count_squads(self) -> int:
        return sum(child.count_squads() for child in self.children)

    # Abstrakcyjna, bo kazdy poziom (Squad, Legion, Army) wyswietla sie troche inaczej
    @abstractmethod
    def show(self, indent: int = 0) -> str:
        pass


class Squad(CompositeUnit):
    """Oddzial - najmniejsza grupa bojowa"""
    
    # Alias dla kompatybilnosci API
    def add_unit(self, unit: MilitaryUnit):
        self.add(unit)
        
    # Squad jest dla nas najmniejsza jednostka organizacyjna w liczeniu "count_squads"
    def count_squads(self) -> int:
        return 1

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}[Oddzial: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})"]
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)


class Legion(CompositeUnit):
    """Legion - grupa oddzialow"""
    
    # Alias dla kompatybilnosci API
    def add_squad(self, squad: Squad):
        self.add(squad)

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}[Legion: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})"]
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)


class Army(CompositeUnit):
    """Armia - cala potega wojskowa"""
    
    def __init__(self, name: str, faction: str):
        super().__init__(name)
        self.faction = faction
        
    # Alias dla kompatybilnosci API
    def add_legion(self, legion: Legion):
        self.add(legion)
        
    # Army udostepnia pola "legions" dla kompatybilnosci z funkcja merge_armies
    @property
    def legions(self):
        return [child for child in self.children if isinstance(child, Legion)]

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = []
        lines.append(f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===")
        lines.append(f"{prefix}Calkowita sila: {self.get_strength()}")
        lines.append(f"{prefix}Liczba jednostek: {self.count_units()}")
        lines.append(f"{prefix}Liczba oddzialow: {self.count_squads()}")
        lines.append(f"{prefix}Liczba legionow: {len(self.children)}") # Zakladamy ze bezposrednie dzieci to legiony
        lines.append(f"{prefix}" + "-" * 40)
        
        for child in self.children:
            lines.append(child.show(indent + 1))
            
        return "\n".join(lines)


# ============================================================================
# FUNKCJE POMOCNICZE
# ============================================================================

def compare_forces(army1: Army, army2: Army) -> Dict:
    """
    Porownuje dwie armie.
    Teraz korzysta z polimorfizmu Composite!
    """
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
    """
    Laczy dwie armie w jedna.
    """
    merged = Army(new_name, f"{army1.faction}+{army2.faction}")
    # Dzięki property 'legions' w klasie Army, ten kod nadal działa
    for legion in army1.legions:
        merged.add_legion(legion)
    for legion in army2.legions:
        merged.add_legion(legion)
    return merged


# ============================================================================
# PRZYKLADOWE UZYCIE (Bez zmian w logice biznesowej)
# ============================================================================

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
    
    # Legiony
    infantry_legion = Legion("Legion Piechoty")
    infantry_legion.add_squad(orc_scouts)
    infantry_legion.add_squad(orc_warriors)
    
    elite_legion = Legion("Legion Elitarny")
    elite_legion.add_squad(troll_squad)
    elite_legion.add_squad(nazgul_squad)
    
    # Armia
    mordor = Army("Armia Mordoru", "Mordor")
    mordor.add_legion(infantry_legion)
    mordor.add_legion(elite_legion)
    
    return mordor


def create_gondor_army() -> Army:
    """Tworzy przykladowa Armie Gondoru"""
    
    # Jednostki
    faramir = Human("Faramir")
    beregond = Human("Beregond")
    pippin = Human("Pippin")
    
    legolas = Elf("Legolas")
    haldir = Elf("Haldir")
    
    gimli = Dwarf("Gimli")
    
    gandalf = Wizard("Gandalf Bialy")
    
    # Oddzialy
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
    
    # Legiony
    gondor_legion = Legion("Legion Gondoru")
    gondor_legion.add_squad(rangers)
    gondor_legion.add_squad(guards)
    
    allies_legion = Legion("Legion Sojusznikow")
    allies_legion.add_squad(elven_archers)
    allies_legion.add_squad(fellowship_remnants)
    
    # Armia
    gondor = Army("Armia Gondoru", "Gondor")
    gondor.add_legion(gondor_legion)
    gondor.add_legion(allies_legion)
    
    return gondor


if __name__ == "__main__":
    print("=" * 60)
    print("SYMULATOR ARMII SRODZIEMIA (COMPOSITE PATTERN)")
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
    print(f"  Sila: {comparison['army1_strength']}")
    print(f"  Jednostek: {comparison['army1_units']}")
    
    print(f"\n{comparison['army2_name']}:")
    print(f"  Sila: {comparison['army2_strength']}")
    print(f"  Jednostek: {comparison['army2_units']}")
    
    print(f"\nSilniejsza armia: {comparison['stronger']}")
    print(f"Roznica sil: {comparison['difference']}")
    
    # Najsilniejsza jednostka
    print("\n" + "=" * 60)
    print("NAJSILNIEJSZE JEDNOSTKI")
    print("=" * 60)
    
    mordor_strongest = mordor.get_strongest_unit()
    gondor_strongest = gondor.get_strongest_unit()
    
    if mordor_strongest:
        print(f"\nMordor: {mordor_strongest.name} ({mordor_strongest.unit_type}) - sila {mordor_strongest.get_strength()}")
    if gondor_strongest:
        print(f"Gondor: {gondor_strongest.name} ({gondor_strongest.unit_type}) - sila {gondor_strongest.get_strength()}")