"""
Symulator armii Srodziemia.
UWAGA: Ten kod ma ZAGNIEZDZZONE PETLE WSZEDZIE! Uzyj wzorca Composite.

Mamy strukture: Armia -> Legiony -> Oddzialy -> Wojownicy
Kazda operacja (sila, liczenie, wyswietlanie) wymaga tych samych petli!

To nie jest Jedyny Prawdziwy Sposob... jest lepszy.
"""
from typing import List, Dict
from abc import ABC, abstractmethod


# ============================================================================
# WSPÓLNY INTERFEJS (Composite Pattern)
# ============================================================================

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

    def add(self, unit: 'MilitaryUnit') -> None:
        pass


# ============================================================================
# LIŚCIE (pojedyncze jednostki)
# ============================================================================

class Warrior(MilitaryUnit):
    """Bazowa klasa dla wszystkich pojedynczych wojowników."""

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
        prefix = "  " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self.get_strength()})"


class Orc(Warrior):
    """Zwykły ork - mięso armatnie Mordoru"""

    def __init__(self, name: str):
        super().__init__(name, "Orc", 5, "Plugawy sługa Ciemności")


class UrukHai(Warrior):
    """Uruk-hai - elitarni wojownicy Sarumana"""

    def __init__(self, name: str):
        super().__init__(name, "Uruk-hai", 12, "Doskonały wojownik stworzony przez Sarumana")


class Troll(Warrior):
    """Troll jaskiniowy - powolny ale MOCNY"""

    def __init__(self, name: str):
        super().__init__(name, "Troll", 45, "Ogromna bestia, lepiej nie stawać na drodze")


class Nazgul(Warrior):
    """Nazgul - Upiory Pierścienia, terrorysta z nieba"""

    def __init__(self, name: str):
        super().__init__(name, "Nazgul", 100, "Były król, teraz sługa Saurona")


class Elf(Warrior):
    """Elf - zwinny łucznik, wieczny wróg orków"""

    def __init__(self, name: str):
        super().__init__(name, "Elf", 15, "Wieczny, mądry i śmiertelnie celny")


class Human(Warrior):
    """Człowiek - zwykły żołnierz Gondoru/Rohanu"""

    def __init__(self, name: str):
        super().__init__(name, "Human", 8, "Śmiertelnik broniący swojej ziemi")


class Dwarf(Warrior):
    """Krasnolud - niski ale wytrzymały"""

    def __init__(self, name: str):
        super().__init__(name, "Dwarf", 14, "Twardy jak skała, z której się wywodzi")


class Wizard(Warrior):
    """Czarodziej - rzadki ale potężny"""

    def __init__(self, name: str):
        super().__init__(name, "Wizard", 150, "Maiar w ludzkiej postaci")


# ============================================================================
# KOMPOZYTY (grupy jednostek)
# ============================================================================

class UnitGroup(MilitaryUnit):
    """Grupa jednostek wojskowych - bazowa klasa dla wszystkich kompozytów."""

    def __init__(self, name: str, unit_type: str = "Grupa"):
        self.name = name
        self.unit_type = unit_type
        self.children: List[MilitaryUnit] = []

    def add(self, unit: MilitaryUnit) -> None:
        """Dodaje jednostkę do grupy."""
        self.children.append(unit)

    def get_strength(self) -> int:
        """Liczy siłę grupy - REKURENCYJNIE, bez zagnieżdżonych pętli!"""
        return sum(child.get_strength() for child in self.children)

    def count_units(self) -> int:
        """Liczy jednostki w grupie - REKURENCYJNIE!"""
        return sum(child.count_units() for child in self.children)

    def show(self, indent: int = 0) -> str:
        """Wyświetla strukturę grupy."""
        prefix = "  " * indent
        lines = [f"{prefix}[{self.unit_type}: {self.name}] (sila: {self.get_strength()}, jednostek: {self.count_units()})"]
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)

    def get_all_warriors(self) -> List[Warrior]:
        """Zwraca listę wszystkich pojedynczych wojowników w grupie."""
        warriors = []
        for child in self.children:
            if isinstance(child, Warrior):
                warriors.append(child)
            elif isinstance(child, UnitGroup):
                warriors.extend(child.get_all_warriors())
        return warriors


class Squad(UnitGroup):
    """Oddział - najmniejsza grupa bojowa"""

    def __init__(self, name: str):
        super().__init__(name, "Oddzial")


class Legion(UnitGroup):
    """Legion - duża formacja bojowa składająca się z oddziałów"""

    def __init__(self, name: str):
        super().__init__(name, "Legion")


class Army(UnitGroup):
    """Armia - cała potęga wojskowa"""

    def __init__(self, name: str, faction: str):
        super().__init__(name, "Armia")
        self.faction = faction  # "Mordor", "Isengard", "Gondor", etc.

    def show(self, indent: int = 0) -> str:
        """Wyświetla strukturę armii z dodatkowymi informacjami."""
        prefix = "  " * indent
        lines = [f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===",
                 f"{prefix}Całkowita siła: {self.get_strength()}", f"{prefix}Liczba jednostek: {self.count_units()}",
                 f"{prefix}Liczba oddziałów: {self._count_squads()}", f"{prefix}Liczba legionów: {len(self.children)}",
                 f"{prefix}" + "-" * 40]
        # Dodajemy dzieci (legiony)
        for child in self.children:
            lines.append(child.show(indent + 1))

        return "\n".join(lines)

    def _count_squads(self) -> int:
        """Liczy oddziały w armii."""
        count = 0
        for legion in self.children:
            if isinstance(legion, Legion):
                count += len(legion.children)
        return count

    def get_units_by_type(self, unit_type: str) -> List[Warrior]:
        """Znajduje wszystkie jednostki danego typu - REKURENCYJNIE!"""
        warriors = self.get_all_warriors()
        return [w for w in warriors if w.unit_type == unit_type]

    def get_strongest_unit(self) -> Warrior:
        """Znajduje najsilniejszą jednostkę - REKURENCYJNIE!"""
        warriors = self.get_all_warriors()
        if not warriors:
            return None
        return max(warriors, key=lambda w: w.get_strength())


# ============================================================================
# FUNKCJE POMOCNICZE
# ============================================================================

def compare_forces(army1: Army, army2: Army) -> Dict:
    """
    Porownuje dwie armie.
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
    for legion in army1.children:
        merged.add(legion)
    for legion in army2.children:
        merged.add(legion)
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
    pippin = Human("Pippin")  # Honorary human :)

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

    print(f"\nMordor: {mordor_strongest.name} ({mordor_strongest.unit_type}) - sila {mordor_strongest.get_strength()}")
    print(f"Gondor: {gondor_strongest.name} ({gondor_strongest.unit_type}) - sila {gondor_strongest.get_strength()}")