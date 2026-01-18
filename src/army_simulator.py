from abc import ABC, abstractmethod
from typing import List, Dict, Type, Iterator, Optional


# ============================================================================
# 1. COMPONENT (Interfejs wspólny)
# ============================================================================
class MilitaryUnit(ABC):
    @abstractmethod
    def strength(self) -> int: pass

    @abstractmethod
    def count(self) -> int: pass

    @abstractmethod
    def show(self, indent: int = 0) -> str: pass


# ============================================================================
# 2. LEAF (Wojownicy) - Testy wymagają konkretnych klas i nazw!
# ============================================================================
class Warrior(MilitaryUnit):
    def strength(self) -> int:
        return self._strength

    def count(self) -> int:
        return 1

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self.strength()})"


class Orc(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Orc", 5


class UrukHai(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Uruk-hai", 12


class Troll(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Troll", 45


class Nazgul(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Nazgul", 100


class Elf(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Elf", 15


class Human(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Human", 8


class Dwarf(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Dwarf", 14


class Wizard(Warrior):
    def __init__(self, name: str):
        self.name, self.unit_type, self._strength = name, "Wizard", 150


# ============================================================================
# 3. COMPOSITE (Struktury grupujące)
# ============================================================================
class UnitGroup(MilitaryUnit):
    def __init__(self, name: str):
        self.name = name
        self.children: List[MilitaryUnit] = []

    def add(self, child: MilitaryUnit):
        self.children.append(child)

    def strength(self) -> int:
        return sum(child.strength() for child in self.children)

    def count(self) -> int:
        return sum(child.count() for child in self.children)

    # --- METODY WYMAGANE PRZEZ TESTY (Legacy API Aliases) ---
    def get_strength(self) -> int:
        return self.strength()

    def count_units(self) -> int:
        return self.count()

    def count_type(self, group_type: Type) -> int:
        total = 0
        for child in self.children:
            if isinstance(child, group_type):
                total += 1
            if isinstance(child, UnitGroup):
                total += child.count_type(group_type)
        return total

    def get_singular_units_iterator(self) -> Iterator[Warrior]:
        for child in self.children:
            if isinstance(child, UnitGroup):
                yield from child.get_singular_units_iterator()
            else:
                yield child

    def get_units_by_type(self, unit_type: str) -> List[Warrior]:
        """Testy szukają jednostek po stringu unit_type"""
        return [u for u in self.get_singular_units_iterator() if u.unit_type == unit_type]

    def get_strongest_unit(self) -> Optional[Warrior]:
        units = list(self.get_singular_units_iterator())
        if not units: return None
        return max(units, key=lambda u: u.strength())

    def _get_header(self) -> str:
        return f"[{self.__class__.__name__}: {self.name}] (sila: {self.strength()}, jednostek: {self.count()})"

    def show(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines = [prefix + self._get_header()]
        for child in self.children:
            lines.append(child.show(indent + 1))
        return "\n".join(lines)


# --- Klasy pochodne z metodami specyficznymi dla testów ---

class Squad(UnitGroup):
    def add_unit(self, unit: MilitaryUnit):
        self.add(unit)


class Legion(UnitGroup):
    def add_squad(self, squad: Squad):
        self.add(squad)


class Army(UnitGroup):
    def __init__(self, name: str, faction: str):
        super().__init__(name)
        self.faction = faction

    def add_legion(self, legion: Legion):
        self.add(legion)

    def _get_header(self) -> str:
        return f"=== ARMIA: {self.name} ({self.faction}) === Sila: {self.strength()}"

    def count_squads(self) -> int:
        return self.count_type(Squad)

    def count_legions(self) -> int:
        return self.count_type(Legion)


# ============================================================================
# 4. FUNKCJE GLOBALNE (Również wymagane przez testy)
# ============================================================================

def compare_forces(army1: Army, army2: Army) -> Dict:
    return {
        "army1_name": army1.name,
        "army1_strength": army1.get_strength(),
        "army1_units": army1.count_units(),
        "army2_name": army2.name,
        "army2_strength": army2.get_strength(),
        "army2_units": army2.count_units(),
        "stronger": army1.name if army1.strength() > army2.strength() else army2.name,
        "difference": abs(army1.strength() - army2.strength())
    }


def merge_armies(army1: Army, army2: Army, new_name: str) -> Army:
    merged = Army(new_name, f"{army1.faction}+{army2.faction}")
    for child in army1.children:
        merged.add(child)
    for child in army2.children:
        merged.add(child)
    return merged


# Pomocnicze funkcje do budowania armii
def create_mordor_army() -> Army:
    mordor = Army("Armia Mordoru", "Mordor")

    orc_scouts = Squad("Orkowi Zwiadowcy")
    orc_scouts.add_unit(Orc("Grishnakh"))
    orc_scouts.add_unit(Orc("Shagrat"))

    orc_warriors = Squad("Orczy Wojownicy")
    orc_warriors.add_unit(Orc("Gorbag"))
    orc_warriors.add_unit(Orc("Muzgash"))

    troll_squad = Squad("Trolle Bojowe")
    troll_squad.add_unit(Troll("Rogash"))
    troll_squad.add_unit(Troll("Grond-pusher"))

    nazgul_squad = Squad("Upiory Pierscienia")
    nazgul_squad.add_unit(Nazgul("Witch-king of Angmar"))
    nazgul_squad.add_unit(Nazgul("Khamul"))

    infantry = Legion("Legion Piechoty")
    infantry.add_squad(orc_scouts)
    infantry.add_squad(orc_warriors)

    elite = Legion("Legion Elitarny")
    elite.add_squad(troll_squad)
    elite.add_squad(nazgul_squad)

    mordor.add_legion(infantry)
    mordor.add_legion(elite)
    return mordor


def create_gondor_army() -> Army:
    gondor = Army("Armia Gondoru", "Gondor")

    rangers = Squad("Strazicy Ithilien")
    rangers.add_unit(Human("Faramir"))
    rangers.add_unit(Human("Beregond"))

    fellowship = Squad("Resztki Druzyny")
    fellowship.add_unit(Elf("Legolas"))
    fellowship.add_unit(Dwarf("Gimli"))
    fellowship.add_unit(Wizard("Gandalf Bialy"))

    g_legion = Legion("Legion Gondoru")
    g_legion.add_squad(rangers)

    allies = Legion("Legion Sojusznikow")
    allies.add_squad(fellowship)

    gondor.add_legion(g_legion)
    gondor.add_legion(allies)
    return gondor
