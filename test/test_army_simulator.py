"""
Testy jednostkowe dla symulatora armii Srodziemia.
NIE MODYFIKUJ TESTOW! Powinny przechodzic zarowno przed jak i po refaktoryzacji.

Te testy sprawdzaja ZACHOWANIE, nie implementacje.
Dzieki temu dzialaja zarowno z kodem "przed" (petle) jak i "po" (Composite).
"""
import pytest
from src.army_simulator import (
    Orc, UrukHai, Troll, Nazgul, Elf, Human, Dwarf, Wizard,
    Squad, Legion, Army,
    create_mordor_army, create_gondor_army, compare_forces, merge_armies
)


# ============================================================================
# HELPER: uniwersalny sposob dodawania jednostek (dziala przed i po refaktoryzacji)
# ============================================================================

def add_to_group(group, item):
    """Dodaje element do grupy - dziala z add_unit/add_squad/add_legion/add"""
    if hasattr(group, 'add_unit'):
        group.add_unit(item)
    elif hasattr(group, 'add_squad'):
        group.add_squad(item)
    elif hasattr(group, 'add_legion'):
        group.add_legion(item)
    elif hasattr(group, 'add'):
        group.add(item)
    else:
        raise AttributeError(f"Don't know how to add to {type(group)}")


def get_strength(unit):
    """Pobiera sile - dziala z atrybutem lub metoda"""
    if callable(getattr(unit, 'strength', None)):
        return unit.strength()
    elif hasattr(unit, 'get_strength'):
        return unit.get_strength()
    else:
        return unit.strength


def get_unit_count(group):
    """Pobiera liczbe jednostek - dziala z count_units() lub count()"""
    if hasattr(group, 'count_units'):
        return group.count_units()
    elif hasattr(group, 'count'):
        return group.count()
    else:
        raise AttributeError(f"Don't know how to count {type(group)}")


# ============================================================================
# TESTY POJEDYNCZYCH JEDNOSTEK
# ============================================================================

class TestIndividualUnits:
    """Testy pojedynczych jednostek"""
    
    def test_orc_has_correct_stats(self):
        orc = Orc("Grishnakh")
        assert orc.name == "Grishnakh"
        assert orc.unit_type == "Orc"
        assert get_strength(orc) == 5
    
    def test_uruk_hai_is_stronger_than_orc(self):
        orc = Orc("Weakling")
        uruk = UrukHai("Lurtz")
        assert get_strength(uruk) > get_strength(orc)
    
    def test_troll_has_high_strength(self):
        troll = Troll("Mountain Troll")
        assert get_strength(troll) >= 40
    
    def test_nazgul_is_powerful(self):
        nazgul = Nazgul("Witch-king")
        assert get_strength(nazgul) >= 100
    
    def test_elf_attributes(self):
        elf = Elf("Legolas")
        assert elf.unit_type == "Elf"
        assert get_strength(elf) > 0
    
    def test_human_attributes(self):
        human = Human("Aragorn")
        assert human.unit_type == "Human"
        assert get_strength(human) > 0
    
    def test_dwarf_attributes(self):
        dwarf = Dwarf("Gimli")
        assert dwarf.unit_type == "Dwarf"
        assert get_strength(dwarf) > 0
    
    def test_wizard_is_most_powerful(self):
        wizard = Wizard("Gandalf")
        troll = Troll("Cave Troll")
        nazgul = Nazgul("Ringwraith")
        assert get_strength(wizard) > get_strength(troll)
        assert get_strength(wizard) > get_strength(nazgul)


# ============================================================================
# TESTY ODDZIALOW (SQUAD)
# ============================================================================

class TestSquad:
    """Testy oddzialow"""
    
    def test_empty_squad_has_zero_strength(self):
        squad = Squad("Empty Squad")
        assert squad.get_strength() == 0
    
    def test_empty_squad_has_zero_units(self):
        squad = Squad("Empty Squad")
        assert get_unit_count(squad) == 0
    
    def test_squad_with_one_unit(self):
        squad = Squad("Solo")
        orc = Orc("Lonely Orc")
        add_to_group(squad, orc)
        assert get_unit_count(squad) == 1
        assert squad.get_strength() == 5
    
    def test_squad_strength_is_sum_of_units(self):
        squad = Squad("Mixed Squad")
        add_to_group(squad, Orc("Orc1"))  # 5
        add_to_group(squad, Orc("Orc2"))  # 5
        add_to_group(squad, UrukHai("Uruk"))  # 12
        assert squad.get_strength() == 22
    
    def test_squad_counts_all_units(self):
        squad = Squad("Big Squad")
        for i in range(5):
            add_to_group(squad, Orc(f"Orc{i}"))
        assert get_unit_count(squad) == 5
    
    def test_squad_show_contains_name(self):
        squad = Squad("Elite Warriors")
        add_to_group(squad, UrukHai("Lurtz"))
        output = squad.show()
        assert "Elite Warriors" in output
        assert "Lurtz" in output


# ============================================================================
# TESTY LEGIONOW
# ============================================================================

class TestLegion:
    """Testy legionow"""
    
    def test_empty_legion_has_zero_strength(self):
        legion = Legion("Empty Legion")
        assert legion.get_strength() == 0
    
    def test_empty_legion_has_zero_units(self):
        legion = Legion("Empty Legion")
        assert get_unit_count(legion) == 0
    
    def test_legion_with_one_squad(self):
        legion = Legion("Small Legion")
        squad = Squad("Squad")
        add_to_group(squad, Orc("Orc"))
        add_to_group(squad, Orc("Orc2"))
        add_to_group(legion, squad)
        assert get_unit_count(legion) == 2
        assert legion.get_strength() == 10
    
    def test_legion_with_multiple_squads(self):
        legion = Legion("Big Legion")
        
        squad1 = Squad("Squad 1")
        add_to_group(squad1, Orc("Orc"))  # 5
        
        squad2 = Squad("Squad 2")
        add_to_group(squad2, Troll("Troll"))  # 45
        
        add_to_group(legion, squad1)
        add_to_group(legion, squad2)
        
        assert get_unit_count(legion) == 2
        assert legion.get_strength() == 50
    
    def test_legion_show_contains_squad_info(self):
        legion = Legion("Mordor Legion")
        squad = Squad("Orc Raiders")
        add_to_group(squad, Orc("Gorbag"))
        add_to_group(legion, squad)
        
        output = legion.show()
        assert "Mordor Legion" in output
        assert "Orc Raiders" in output


# ============================================================================
# TESTY ARMII
# ============================================================================

class TestArmy:
    """Testy armii"""
    
    def test_empty_army_has_zero_strength(self):
        army = Army("Empty", "Neutral")
        assert army.get_strength() == 0
    
    def test_empty_army_has_zero_units(self):
        army = Army("Empty", "Neutral")
        assert get_unit_count(army) == 0
    
    def test_army_with_one_legion(self):
        army = Army("Small Army", "Test")
        legion = Legion("Legion")
        squad = Squad("Squad")
        add_to_group(squad, Human("Soldier"))
        add_to_group(legion, squad)
        add_to_group(army, legion)
        
        assert get_unit_count(army) == 1
    
    def test_army_strength_sums_all_units(self):
        army = Army("Test Army", "Test")
        
        legion1 = Legion("Legion 1")
        squad1 = Squad("Squad 1")
        add_to_group(squad1, Orc("O1"))  # 5
        add_to_group(squad1, Orc("O2"))  # 5
        add_to_group(legion1, squad1)
        
        legion2 = Legion("Legion 2")
        squad2 = Squad("Squad 2")
        add_to_group(squad2, Troll("T1"))  # 45
        add_to_group(legion2, squad2)
        
        add_to_group(army, legion1)
        add_to_group(army, legion2)
        
        assert army.get_strength() == 55
        assert get_unit_count(army) == 3
    
    def test_army_show_contains_all_info(self):
        army = Army("Gondor Forces", "Gondor")
        legion = Legion("White Tower Legion")
        squad = Squad("Tower Guards")
        add_to_group(squad, Human("Beregond"))
        add_to_group(legion, squad)
        add_to_group(army, legion)
        
        output = army.show()
        assert "Gondor Forces" in output
        assert "Gondor" in output
        assert "White Tower Legion" in output
        assert "Tower Guards" in output
        assert "Beregond" in output
    
    def test_get_units_by_type(self):
        army = Army("Mixed Army", "Alliance")
        legion = Legion("Legion")
        squad = Squad("Squad")
        add_to_group(squad, Orc("O1"))
        add_to_group(squad, Orc("O2"))
        add_to_group(squad, Elf("E1"))
        add_to_group(squad, Human("H1"))
        add_to_group(legion, squad)
        add_to_group(army, legion)
        
        orcs = army.get_units_by_type("Orc")
        elves = army.get_units_by_type("Elf")
        dwarves = army.get_units_by_type("Dwarf")
        
        assert len(orcs) == 2
        assert len(elves) == 1
        assert len(dwarves) == 0
    
    def test_get_strongest_unit(self):
        army = Army("Test", "Test")
        legion = Legion("Legion")
        squad = Squad("Squad")
        add_to_group(squad, Orc("Weak"))
        add_to_group(squad, Wizard("Gandalf"))
        add_to_group(squad, Troll("Medium"))
        add_to_group(legion, squad)
        add_to_group(army, legion)
        
        strongest = army.get_strongest_unit()
        assert strongest.name == "Gandalf"


# ============================================================================
# TESTY PREDEFINIOWANYCH ARMII
# ============================================================================

class TestPredefinedArmies:
    """Testy predefiniowanych armii"""
    
    def test_mordor_army_exists(self):
        mordor = create_mordor_army()
        assert mordor is not None
        assert mordor.faction == "Mordor"
    
    def test_mordor_army_has_units(self):
        mordor = create_mordor_army()
        assert get_unit_count(mordor) > 0
    
    def test_mordor_army_has_strength(self):
        mordor = create_mordor_army()
        assert mordor.get_strength() > 0
    
    def test_gondor_army_exists(self):
        gondor = create_gondor_army()
        assert gondor is not None
        assert gondor.faction == "Gondor"
    
    def test_gondor_army_has_units(self):
        gondor = create_gondor_army()
        assert get_unit_count(gondor) > 0
    
    def test_gondor_has_gandalf(self):
        gondor = create_gondor_army()
        wizards = gondor.get_units_by_type("Wizard")
        assert len(wizards) >= 1
        assert any("Gandalf" in w.name for w in wizards)
    
    def test_mordor_has_nazgul(self):
        mordor = create_mordor_army()
        nazgul = mordor.get_units_by_type("Nazgul")
        assert len(nazgul) >= 1


# ============================================================================
# TESTY POROWNYWANIA ARMII
# ============================================================================

class TestCompareForces:
    """Testy porownywania armii"""
    
    def test_compare_returns_dict(self):
        army1 = Army("A1", "F1")
        army2 = Army("A2", "F2")
        result = compare_forces(army1, army2)
        assert isinstance(result, dict)
    
    def test_compare_has_required_keys(self):
        army1 = Army("A1", "F1")
        army2 = Army("A2", "F2")
        result = compare_forces(army1, army2)
        
        assert "army1_name" in result
        assert "army1_strength" in result
        assert "army1_units" in result
        assert "army2_name" in result
        assert "army2_strength" in result
        assert "army2_units" in result
        assert "stronger" in result
        assert "difference" in result
    
    def test_compare_identifies_stronger(self):
        army1 = Army("Strong", "F1")
        legion = Legion("L")
        squad = Squad("S")
        add_to_group(squad, Wizard("Gandalf"))  # 150
        add_to_group(legion, squad)
        add_to_group(army1, legion)
        
        army2 = Army("Weak", "F2")
        legion2 = Legion("L2")
        squad2 = Squad("S2")
        add_to_group(squad2, Orc("Orc"))  # 5
        add_to_group(legion2, squad2)
        add_to_group(army2, legion2)
        
        result = compare_forces(army1, army2)
        assert result["stronger"] == "Strong"
        assert result["difference"] == 145


# ============================================================================
# TESTY LACZENIA ARMII
# ============================================================================

class TestMergeArmies:
    """Testy laczenia armii"""
    
    def test_merge_creates_new_army(self):
        army1 = Army("A1", "F1")
        army2 = Army("A2", "F2")
        merged = merge_armies(army1, army2, "Merged")
        
        assert merged.name == "Merged"
        assert merged is not army1
        assert merged is not army2
    
    def test_merge_preserves_strength(self):
        army1 = Army("A1", "F1")
        legion1 = Legion("L1")
        squad1 = Squad("S1")
        add_to_group(squad1, Orc("O1"))
        add_to_group(legion1, squad1)
        add_to_group(army1, legion1)
        
        army2 = Army("A2", "F2")
        legion2 = Legion("L2")
        squad2 = Squad("S2")
        add_to_group(squad2, Troll("T1"))
        add_to_group(legion2, squad2)
        add_to_group(army2, legion2)
        
        original_strength = army1.get_strength() + army2.get_strength()
        merged = merge_armies(army1, army2, "Merged")
        
        assert merged.get_strength() == original_strength


# ============================================================================
# TESTY GLEBOKIEJ HIERARCHII
# ============================================================================

class TestDeepHierarchy:
    """Testy glebokiej hierarchii"""
    
    def test_many_levels_strength_calculation(self):
        """Test czy sila sie poprawnie sumuje przez wiele poziomow"""
        army = Army("Deep Army", "Test")
        
        total_expected = 0
        
        for i in range(3):  # 3 legiony
            legion = Legion(f"Legion {i}")
            for j in range(4):  # 4 oddzialy w kazdym
                squad = Squad(f"Squad {i}-{j}")
                for k in range(5):  # 5 orkow w kazdym
                    add_to_group(squad, Orc(f"Orc {i}-{j}-{k}"))
                    total_expected += 5
                add_to_group(legion, squad)
            add_to_group(army, legion)
        
        assert army.get_strength() == total_expected
        assert get_unit_count(army) == 60  # 3 * 4 * 5
    
    def test_mixed_unit_types_in_hierarchy(self):
        """Test mieszanych typow jednostek"""
        army = Army("Mixed", "Test")
        legion = Legion("Legion")
        
        squad1 = Squad("Orcs")
        add_to_group(squad1, Orc("O1"))
        add_to_group(squad1, Orc("O2"))
        
        squad2 = Squad("Elite")
        add_to_group(squad2, UrukHai("U1"))
        add_to_group(squad2, Troll("T1"))
        add_to_group(squad2, Nazgul("N1"))
        
        add_to_group(legion, squad1)
        add_to_group(legion, squad2)
        add_to_group(army, legion)
        
        # 5 + 5 + 12 + 45 + 100 = 167
        assert army.get_strength() == 167
        assert get_unit_count(army) == 5