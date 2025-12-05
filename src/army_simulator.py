"""
Symulator armii Srodziemia.
UWAGA: Ten kod ma ZAGNIEZDZZONE PETLE WSZEDZIE! Uzyj wzorca Composite.

Mamy strukture: Armia -> Legiony -> Oddzialy -> Wojownicy
Kazda operacja (sila, liczenie, wyswietlanie) wymaga tych samych petli!

To nie jest Jedyny Prawdziwy Sposob... jest lepszy.
"""
from collections.abc import Callable
from typing import List, Dict
from abc import ABC, abstractmethod

##################
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


class Warrior(MilitaryUnit):
    def __init__(self, name: str, unit_type: str, strength: int, description: str):
        self.name = name
        self.unit_type = unit_type
        self._strength = strength
        self.description = description

    def strength(self) -> int:
        return self._strength

    def count(self) -> int:
        return 1

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self._strength})"

    def get_strength(self) -> int:
        return self.strength()

    def get_unit_count(self) -> int:
        return self.count()



##################
# ============================================================================
# POJEDYNCZE JEDNOSTKI (rozne typy wojownikow)
# ============================================================================

class Orc(Warrior):
    """Zwykly ork - mieso armatnie Mordoru"""
    def __init__(self, name: str):
        super().__init__(name, "Orc", 5, "Plugawy sluga Ciemnosci")


class UrukHai(Warrior):
    """Uruk-hai - elitarni wojownicy Sarumana"""
    def __init__(self, name: str):
        super().__init__(name,"Uruk-hai", 12, "Doskonaly wojownik stworzony przez Sarumana")


class Troll(Warrior):
    """Troll jaskiniowy - powolny ale MOCNY"""
    def __init__(self, name: str):
        super().__init__(name, "Troll", 45, "Ogromna bestia, lepiej nie stawac na drodze")


class Nazgul(Warrior):
    """Nazgul - Upiory Pierscienia, terrorysta z nieba"""
    def __init__(self, name: str):
        super().__init__(name, "Nazgul", 100, "Byly krol, teraz sluga Saurona")


class Elf(Warrior):
    """Elf - zwinny lucznik, wieczny wrog orkow"""
    def __init__(self, name: str):
        super().__init__(name, "Elf", 15, "Wieczny, madry i smiertenie celny")


class Human(Warrior):
    """Czlowiek - zwykly zolnierz Gondoru/Rohanu"""
    def __init__(self, name: str):
        super().__init__(name, "Human", 8, "Smiertelnik broniacy swojej ziemi")


class Dwarf(Warrior):
    """Krasnolud - niski ale wytrzymaly"""
    def __init__(self, name: str):
        super().__init__(name, "Dwarf", 14, "Twardy jak skala, z ktorej sie wywodzi")


class Wizard(Warrior):
    """Czarodziej - rzadki ale potezny"""
    def __init__(self, name: str):
        super().__init__(name, "Wizard", 150, "Maiar w ludzkiej postaci")




class UnitGroup(MilitaryUnit):
    def __init__(self, name: str, group_type: str):
        self.name = name
        self.group_type = group_type
        self.children: List[MilitaryUnit] = []

    def add_unit(self, unit: MilitaryUnit):
        self.children.append(unit)

    def add_squad(self, squad: "Squad"):
        self.children.append(squad)

    def add_legion(self, legion: "Legion"):
        self.children.append(legion)

    def add(self, unit: MilitaryUnit):
        self.children.append(unit)

    def strength(self) -> int:
        return sum(child.strength() for child in self.children)

    def count(self) -> int:
        return sum(child.count() for child in self.children)

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}[{self.group_type}: {self.name}] "
                 f"(sila: {self.strength()}, jednostek: {self.count()})"]
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)

    def find(self, predicate: Callable[[Warrior], bool]) -> List[Warrior]:
        results = []
        for child in self.children:
            if isinstance(child, Warrior):
                if predicate(child):
                    results.append(child)
            else:
                results.extend(child.find(predicate))
        return results

    def get_units_by_type(self, unit_type: str) -> List[Warrior]:
        return self.find(lambda u: u.unit_type == unit_type)

    def get_strongest_unit(self) -> Warrior:
        units = self.find(lambda u: True)
        return max(units, key=lambda u: u.strength())

    def get_strength(self) -> int:
        return self.strength()

    def get_unit_count(self) -> int:
        return self.count()


# ============================================================================
# STRUKTURY GRUPUJACE (tu zaczyna sie koszmar petli)
# ============================================================================

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


# ============================================================================
# FUNKCJE POMOCNICZE (jeszcze wiecej duplikacji!)
# ============================================================================

def compare_forces(army1: Army, army2: Army) -> Dict:
    """
    Porownuje dwie armie.
    SPOJRZ - musimy wywolac te same metody z petlami dla kazdej armii!
    """
    return {
        "army1_name": army1.name,
        "army2_name": army2.name,
        "army1_strength": army1.strength(),
        "army2_strength": army2.strength(),
        "army1_units": army1.count(),
        "army2_units": army2.count(),
        "stronger": army1.name if army1.strength() > army2.strength() else army2.name,
        "difference": abs(army1.strength() - army2.strength())
    }


def merge_armies(army1: Army, army2: Army, new_name: str) -> Army:
    """
    Laczy dwie armie w jedna.
    """
    merged = Army(new_name, f"{army1.faction}+{army2.faction}")
    for legion in army1.children:
        merged.add_legion(legion)
    for legion in army2.children:
        merged.add_legion(legion)
    return merged


# ============================================================================
# PRZYKLADOWE UZYCIE
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
    pippin = Human("Pippin")  # Honorary human :)
    
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
    
    print(f"\nMordor: {mordor_strongest.name} ({mordor_strongest.unit_type}) - sila {mordor_strongest.strength}")
    print(f"Gondor: {gondor_strongest.name} ({gondor_strongest.unit_type}) - sila {gondor_strongest.strength}")