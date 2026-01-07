"""
Symulator armii Srodziemia.
UWAGA: Ten kod ma ZAGNIEZDZZONE PETLE WSZEDZIE! Uzyj wzorca Composite.

Mamy strukture: Armia -> Legiony -> Oddzialy -> Wojownicy
Kazda operacja (sila, liczenie, wyswietlanie) wymaga tych samych petli!

To nie jest Jedyny Prawdziwy Sposob... jest lepszy.
"""
from abc import ABC,abstractmethod
from typing import List, Dict

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


    def add(self, unit: 'MilitaryUnit') -> None:
        pass


    def get_strength(self):
        return self.strength()

    def count_units(self):
        return self.count()


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
        return f"{prefix}- {self.name} ({self.unit_type}, sila: {self.strength()})"





# ============================================================================
# POJEDYNCZE JEDNOSTKI (rozne typy wojownikow)
# ============================================================================

class Orc(Warrior):
    """Zwykly ork - mieso armatnie Mordoru"""
    
    def __init__(self,name: str):
        super().__init__(name,"Orc",5,"Plugawy sluga Ciemnosci ")

class UrukHai(Warrior):
    """Uruk-hai - elitarni wojownicy Sarumana"""
    
    def __init__(self, name: str):
        super().__init__(
        name,
        "Uruk-hai",
        12
        ,"Doskonaly wojownik stworzony przez Sarumana"
        )




class Troll(Warrior):
    """Troll jaskiniowy - powolny ale MOCNY"""
    
    def __init__(self, name: str):


        super().__init__(name,"Troll",45,"Ogromna bestia, lepiej nie stawac na drodze")


class Nazgul(Warrior):
    """Nazgul - Upiory Pierscienia, terrorysta z nieba"""
    
    def __init__(self, name: str):

        super().__init__(name,"Nazgul",100,"Byly krol, teraz sluga Saurona")



class Elf(Warrior):
    """Elf - zwinny lucznik, wieczny wrog orkow"""
    
    def __init__(self, name: str):

        super().__init__(name,"Elf",15,"Wieczny, madry i smiertenie celny")




class Human(Warrior):
    """Czlowiek - zwykly zolnierz Gondoru/Rohanu"""
    
    def __init__(self, name: str):


        super().__init__(name,"Human",8,"Smiertelnik broniacy swojej ziemi")




class Dwarf(Warrior):
    """Krasnolud - niski ale wytrzymaly"""
    
    def __init__(self, name: str):

        super().__init__(name,"Dwarf",14,"Twardy jak skala, z ktorej sie wywodzi")

class Wizard(Warrior):
    """Czarodziej - rzadki ale potezny"""
    
    def __init__(self, name: str):

        super().__init__(name,"Wizard",150,"Maiar w ludzkiej postaci")



# ============================================================================
# STRUKTURY GRUPUJACE (tu zaczyna sie koszmar petli)
# ============================================================================


class UnitGroup(MilitaryUnit):
    def __init__(self, name: str,unit_type: str ="Grupa"):
        self.name = name
        self.unit_type = unit_type
        self.children: List[MilitaryUnit] = []

    def add(self, child: MilitaryUnit):
        self.children.append(child)

    def strength(self) -> int:
        return sum(child.strength() for child in self.children)

    def count(self) -> int:
        return sum(child.count() for child in self.children)

    def show(self,indent: int = 0) -> str:
        prefix = "  " * indent
        lines =[f"{prefix}[{self.unit_type}: {self.name}] (sila: {self.strength()}, jednostek: {self.count()})"]
        for child in self.children:
            lines.append(child.show(indent+1))

        return "\n".join(lines)

    def get_warriors(self) -> List[Warrior]:
        warriors = []
        for child in self.children:
            if isinstance(child, Warrior):
                warriors.append(child)

            elif isinstance(child, UnitGroup):
                warriors.extend(child.get_warriors())

        return warriors

class Squad(UnitGroup):
    """Oddzial - najmniejsza grupa bojowa"""
    
    def __init__(self, name: str):
        super().__init__(name,"Oddzial")  # Lista roznych typow jednostek


    



class Legion(UnitGroup):
    """Legion - duza formacja bojowa skladajaca sie z oddzialow"""
    
    def __init__(self, name: str):

        super().__init__(name,"Legion")
    



class Army(UnitGroup):
    """Armia - cala potega wojskowa"""
    
    def __init__(self, name: str, faction: str):
        super().__init__(name,"Army")
        self.faction = faction

    def count_legions(self) -> int:
        return sum(1 for child in self.children if isinstance(child, Legion))



    

    
    def count_squads(self) -> int:
        """Liczy oddzialy"""
        count = 0
        for legion in self.children:
            if isinstance(legion, Legion):

                count += sum(1 for unit in legion.children if isinstance(unit, Squad))
        return count
    def show(self, indent: int = 0) -> str:
        """Wyswietla strukture armii - PETLE NA 3 POZIOMACH!"""
        lines = []
        prefix = "  " * indent
        lines.append(f"{prefix}=== ARMIA: {self.name} ({self.faction}) ===")
        lines.append(f"{prefix}Calkowita sila: {self.strength()}")
        lines.append(f"{prefix}Liczba jednostek: {self.count()}")
        lines.append(f"{prefix}Liczba oddzialow: {self.count_squads()}")
        lines.append(f"{prefix}Liczba legionow: {(self.count_legions())}")
        lines.append(f"{prefix}" + "-" * 40)
        
        for child in self.children:
            lines.append(child.show(indent+1))
        
        return "\n".join(lines)
    
    def get_units_by_type(self, unit_type: str) -> List:
        """Znajduje wszystkie jednostki danego typu - JESZCZE WIECEJ PETLI!"""

        return [w for w in self.get_warriors() if w.unit_type == unit_type]
    
    def get_strongest_unit(self):
        """Znajduje najsilniejsza jednostke - PETLE AGAIN!"""


        return max(self.get_warriors(), key=lambda w: w.strength()) if self.get_warriors() else None


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
    for unit in army1.children:
        if isinstance(unit, Legion):
            merged.add(unit)

    for unit in army2.children:
        if isinstance(unit, Legion):
            merged.add(unit)

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
    
    print(f"\nMordor: {mordor_strongest.name} ({mordor_strongest.unit_type}) - sila {mordor_strongest.strength}")
    print(f"Gondor: {gondor_strongest.name} ({gondor_strongest.unit_type}) - sila {gondor_strongest.strength}")