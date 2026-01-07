from typing import List, Dict
from units import *
from unit_group import *

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
    
    print(f"\nMordor: {mordor_strongest.name} ({mordor_strongest.unit_type}) - sila {mordor_strongest.strength()}")
    print(f"Gondor: {gondor_strongest.name} ({gondor_strongest.unit_type}) - sila {gondor_strongest.strength()}")