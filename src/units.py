from military_unit_interface import MilitaryUnit

# ============================================================================
# POJEDYNCZE JEDNOSTKI (rozne typy wojownikow)
# ============================================================================

class SingleUnit(MilitaryUnit):
    def strength(self) -> int:
        return self.strengthValue
    
    def count(self) -> int:
        return 1
    
    def show(self, indent: int = 0) -> str:
        return f"{"  " * indent}  - {self.name} ({self.unit_type}, sila: {self.strength()})"

class Orc(SingleUnit):
    """Zwykly ork - mieso armatnie Mordoru"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Orc"
        self.strengthValue = 5
        self.description = "Plugawy sluga Ciemnosci"


class UrukHai(SingleUnit):
    """Uruk-hai - elitarni wojownicy Sarumana"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Uruk-hai"
        self.strengthValue = 12
        self.description = "Doskonaly wojownik stworzony przez Sarumana"


class Troll(SingleUnit):
    """Troll jaskiniowy - powolny ale MOCNY"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Troll"
        self.strengthValue = 45
        self.description = "Ogromna bestia, lepiej nie stawac na drodze"


class Nazgul(SingleUnit):
    """Nazgul - Upiory Pierscienia, terrorysta z nieba"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Nazgul"
        self.strengthValue = 100
        self.description = "Byly krol, teraz sluga Saurona"


class Elf(SingleUnit):
    """Elf - zwinny lucznik, wieczny wrog orkow"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Elf"
        self.strengthValue = 15
        self.description = "Wieczny, madry i smiertenie celny"


class Human(SingleUnit):
    """Czlowiek - zwykly zolnierz Gondoru/Rohanu"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Human"
        self.strengthValue = 8
        self.description = "Smiertelnik broniacy swojej ziemi"


class Dwarf(SingleUnit):
    """Krasnolud - niski ale wytrzymaly"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Dwarf"
        self.strengthValue = 14
        self.description = "Twardy jak skala, z ktorej sie wywodzi"


class Wizard(SingleUnit):
    """Czarodziej - rzadki ale potezny"""
    
    def __init__(self, name: str):
        self.name = name
        self.unit_type = "Wizard"
        self.strengthValue = 150
        self.description = "Maiar w ludzkiej postaci"