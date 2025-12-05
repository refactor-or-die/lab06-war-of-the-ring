"""
Symulator armii Srodziemia.
UWAGA: Ten kod ma ZAGNIEZDZZONE PETLE WSZEDZIE! Uzyj wzorca Composite.

Mamy strukture: Armia -> Legiony -> Oddzialy -> Wojownicy
Kazda operacja (sila, liczenie, wyswietlanie) wymaga tych samych petli!

To nie jest Jedyny Prawdziwy Sposob... jest lepszy.
"""
from typing import List, Dict
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

class Warrior(MilitaryUnit):
    def strength(self) -> int:
        return self._strength  # Zwraca swoją siłę
    
    def count(self) -> int:
        return 1  # Jest jeden!

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self.strength()})"

class UnitGroup(MilitaryUnit):
    def __init__(self, name: str):
        self.children: List[MilitaryUnit] = []
    
    def strength(self) -> int:
        return sum(child.strength() for child in self.children)
    
    def count(self) -> int:
        return sum(child.count() for child in self.children)

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [f"{prefix}[{self.__class__.__name__}: {self.name}] (sila: {self.strength()}, jednostek: {self.count()})"]
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)





# ============================================================================
# POJEDYNCZE JEDNOSTKI (rozne typy wojownikow)
# ============================================================================

class Orc(Warrior):
    """Zwykly ork - mieso armatnie Mordoru"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Orc"
        self.strength = 5
        self.description = "Plugawy sluga Ciemnosci"


class UrukHai(Warrior):
    """Uruk-hai - elitarni wojownicy Sarumana"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Uruk-hai"
        self.strength = 12
        self.description = "Doskonaly wojownik stworzony przez Sarumana"


class Troll(Warrior):
    """Troll jaskiniowy - powolny ale MOCNY"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Troll"
        self.strength = 45
        self.description = "Ogromna bestia, lepiej nie stawac na drodze"


class Nazgul(Warrior):
    """Nazgul - Upiory Pierscienia, terrorysta z nieba"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Nazgul"
        self.strength = 100
        self.description = "Byly krol, teraz sluga Saurona"


class Elf(Warrior):
    """Elf - zwinny lucznik, wieczny wrog orkow"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Elf"
        self.strength = 15
        self.description = "Wieczny, madry i smiertenie celny"


class Human(Warrior):
    """Czlowiek - zwykly zolnierz Gondoru/Rohanu"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Human"
        self.strength = 8
        self.description = "Smiertelnik broniacy swojej ziemi"


class Dwarf(Warrior):
    """Krasnolud - niski ale wytrzymaly"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Dwarf"
        self.strength = 14
        self.description = "Twardy jak skala, z ktorej sie wywodzi"


class Wizard(Warrior):
    """Czarodziej - rzadki ale potezny"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Wizard"
        self.strength = 150
        self.description = "Maiar w ludzkiej postaci"


# ============================================================================
# STRUKTURY GRUPUJACE (tu zaczyna sie koszmar petli)
# ============================================================================

class Squad(UnitGroup):
    """Oddzial - najmniejsza grupa bojowa"""
    
    def __init__(self, name: str):
        self.name = name
        self.units: List = []  # Lista roznych typow jednostek
    
    def add_unit(self, unit):
        self.units.append(unit)
    
    def get_strength(self) -> int:
        """Liczy sile oddzialu"""
        total = 0
        for unit in self.units:
            total += unit.strength
        return total
    
    def count_units(self) -> int:
        """Liczy jednostki w oddziale"""
        return len(self.units)
    
    def show(self, indent: int = 0) -> str:
        """Wyswietla strukture oddzialu"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}[Oddzial: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})")
        for unit in self.units:
            lines.append(f"{prefix}  - {unit.name} ({unit.unit_type}, sila: {unit.strength})")
        return "\n".join(lines)


class Legion(UnitGroup):
    """Legion - duza formacja bojowa skladajaca sie z oddzialow"""
    
    def __init__(self, name: str):
        self.name = name
        self.squads: List[Squad] = []
    
    def add_squad(self, squad: Squad):
        self.squads.append(squad)
    
    def get_strength(self) -> int:
        """Liczy sile legionu - PETLA W PETLI!"""
        total = 0
        for squad in self.squads:
            for unit in squad.units:
                total += unit.strength
        return total
    
    def count_units(self) -> int:
        """Liczy jednostki w legionie - KOLEJNA PETLA!"""
        count = 0
        for squad in self.squads:
            count += len(squad.units)
        return count
    
    def show(self, indent: int = 0) -> str:
        """Wyswietla strukture legionu - I ZNOWU PETLE!"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}[Legion: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})")
        for squad in self.squads:
            lines.append(f"{prefix}  [Oddzial: {squad.name}]")
            for unit in squad.units:
                lines.append(f"{prefix}    - {unit.name} ({unit.unit_type}, sila: {unit.strength})")
        return "\n".join(lines)


class Army(UnitGroup):
    """Armia - cala potega wojskowa"""
    
    def __init__(self, name: str, faction: str):
        self.name = name
        self.faction = faction  # "Mordor", "Isengard", "Gondor", etc.
        self.legions: List[Legion] = []
    
    def add_legion(self, legion: Legion):
        self.legions.append(legion)
    
    def get_strength(self) -> int:
        """Liczy sile armii - MEGA PETLA W PETLI W PETLI!"""
        total = 0
        for legion in self.legions:
            for squad in legion.squads:
                for unit in squad.units:
                    total += unit.strength
        return total
    
    def count_units(self) -> int:
        """Liczy jednostki w armii - TO SAMO CO WYZEJ!"""
        count = 0
        for legion in self.legions:
            for squad in legion.squads:
                count += len(squad.units)
        return count
    
    def count_squads(self) -> int:
        """Liczy oddzialy"""
        count = 0
        for legion in self.legions:
            count += len(legion.squads)
        return count
    
    def show(self, indent: int = 0) -> str:
        """Wyswietla strukture armii - PETLE NA 3 POZIOMACH!"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===")
        lines.append(f"{prefix}Calkowita sila: {self.get_strength()}")
        lines.append(f"{prefix}Liczba jednostek: {self.count_units()}")
        lines.append(f"{prefix}Liczba oddzialow: {self.count_squads()}")
        lines.append(f"{prefix}Liczba legionow: {len(self.legions)}")
        lines.append(f"{prefix}" + "-" * 40)
        
        for legion in self.legions:
            lines.append(f"{prefix}  [Legion: {legion.name}]")
            for squad in legion.squads:
                lines.append(f"{prefix}    [Oddzial: {squad.name}]")
                for unit in squad.units:
                    lines.append(f"{prefix}      - {unit.name} ({unit.unit_type}, sila: {unit.strength})")
        
        return "\n".join(lines)
    
    def get_units_by_type(self, unit_type: str) -> List:
        """Znajduje wszystkie jednostki danego typu - JESZCZE WIECEJ PETLI!"""
        result = []
        for legion in self.legions:
            for squad in legion.squads:
                for unit in squad.units:
                    if unit.unit_type == unit_type:
                        result.append(unit)
        return result
    
    def get_strongest_unit(self):
        """Znajduje najsilniejsza jednostke - PETLE AGAIN!"""
        strongest = None
        max_strength = 0
        for legion in self.legions:
            for squad in legion.squads:
                for unit in squad.units:
                    if unit.strength > max_strength:
                        max_strength = unit.strength
                        strongest = unit
        return strongest


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
    for legion in army1.legions:
        merged.add_legion(legion)
    for legion in army2.legions:
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