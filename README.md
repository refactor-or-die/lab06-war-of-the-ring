# Lab 06: War of the Ring

## Czy wiesz, że...
Według symulacji przeprowadzonych przez Petera Jacksona, armia Mordoru pod Minas Tirith liczyła około 200 000 orków. Gdyby każdy programista pisał osobną pętlę do zliczania ich siły... no właśnie, dlatego mamy Composite.

## Twoje zadanie
Sauron zatrudnił Cię jako DevOpsa do zarządzania swoimi armiami. Problem? Poprzedni programista (Grima Wormtongue) zostawił kod z **zagnieżdżonymi pętlami na każdym kroku**.

Chcesz policzyć siłę armii? Pętla w pętli w pętli.
Chcesz wyświetlić strukturę? Pętla w pętli w pętli.
Chcesz dodać nowy poziom (np. "Horda")? **Przepisz wszystko.**

Sauron jest niezadowolony. Masz czas do zachodu słońca.

**Rozwiązanie:** Wzorzec Composite!

## Co zawiera repozytorium
- `army_simulator.py` - koszmar zagnieżdżonych pętli
- `test_army_simulator.py` - testy (NIE RUSZAĆ!)
- Ten README
- Bonusy

## Problem do rozwiązania

### Obecna struktura (bez Composite):
```
Army (Armia)
├── Legion (Legion)
│   ├── Squad (Oddział)
│   │   ├── Orc, UrukHai, Troll, Nazgul...
│   │   └── ...
│   └── Squad
│       └── ...
└── Legion
    └── ...
```

### Co jest źle?
Każda operacja wymaga **tych samych pętli**:

```python
def get_strength(self):
    total = 0
    for legion in self.legions:
        for squad in legion.squads:
            for unit in squad.units:
                total += unit.strength
    return total

def count_units(self):
    count = 0
    for legion in self.legions:      # Te same pętle!
        for squad in legion.squads:  # Copy-paste!
            count += len(squad.units)
    return count
```

### Co chcemy osiągnąć?
```python
# TEN SAM interfejs dla pojedynczego orka i całej armii!
orc.strength()       # 5
squad.strength()     # 22 (suma jednostek)
legion.strength()    # 167 (suma oddziałów)
army.strength()      # 10000 (suma legionów)

# Wszystko jest MilitaryUnit!
```

## Instrukcja
1. Sklonuj repo i stwórz branch `lab6_nazwisko1_nazwisko2`
2. Uruchom testy: `pytest` (powinny przejść)
3. Zrefaktoryzuj kod używając wzorca Composite:
   - Stwórz wspólny interfejs `MilitaryUnit` (ABC)
   - Pojedynczy wojownik = Liść (Leaf)
   - Grupa (Squad/Legion/Army) = Kompozyt (Composite)
   - Wszystkie mają te same metody: `strength()`, `count()`, `show()`
4. Uruchom testy ponownie (MUSZĄ przejść!)
5. Commit + push na swój branch

## Wskazówki

### Interfejs (klasa abstrakcyjna)
```python
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
```

### Liść (pojedynczy wojownik)
```python
class Warrior(MilitaryUnit):
    def strength(self) -> int:
        return self._strength  # Zwraca swoją siłę
    
    def count(self) -> int:
        return 1  # Jest jeden!
```

### Kompozyt (grupa)
```python
class UnitGroup(MilitaryUnit):
    def __init__(self, name: str):
        self.children: List[MilitaryUnit] = []
    
    def strength(self) -> int:
        return sum(child.strength() for child in self.children)
    
    def count(self) -> int:
        return sum(child.count() for child in self.children)
```

### Co z istniejącymi klasami?
Masz dwie opcje:
1. **Zachowaj stare klasy** (Orc, Elf, Squad, Legion, Army) ale spraw żeby dziedziczyły po MilitaryUnit
2. **Uprość do Warrior + UnitGroup** - ale wtedy musisz dostosować funkcje pomocnicze

Testy sprawdzają **zachowanie**, nie strukturę klas - więc obie opcje są OK!

## Co zyskasz?
- **Brak zagnieżdżonych pętli** - rekurencja robi robotę
- **Jednolity interfejs** - orc i armia wyglądają tak samo
- **Łatwe rozszerzanie** - dodajesz "Hordę" nad "Armią"? Żaden problem
- **Czytelność** - kod mówi sam za siebie
- **Szacunek Saurona** - bezcenne

## Kryteria oceny
- Testy przechodzą (wszystkie 42)
- Użyty wzorzec Composite
- Wspólny interfejs dla liści i kompozytów
- Brak zagnieżdżonych pętli w operacjach
- Kod jest czytelny

## FAQ

**Q: Czy mogę zmienić nazwy metod?**

A: Nie! Testy sprawdzają konkretne nazwy (`get_strength`, `count_units`, `show`). Zachowaj je lub zrób aliasy.

**Q: Co z `get_units_by_type()` i `get_strongest_unit()`?**

A: To są metody specyficzne dla Army. Możesz je zostawić tam gdzie są, albo przenieść do bazowego interfejsu z domyślną implementacją.

**Q: Czy Orc i UnitGroup mogą mieć tę samą metodę `add()`?**

A: Nie powinny! Liść (Orc) nie ma dzieci. To różnica między Leaf a Composite.

**Q: A co jeśli chcę dodać "Hordę" nad Armią?**

A: Właśnie dlatego używamy Composite! Po refaktoryzacji to będzie banalne - `Horde` to po prostu kolejny `UnitGroup` zawierający `Army`.

**Q: Nazgul jest Orkiem?**

A: Lore-wise nie, ale w naszym modelu wszystko co walczy jest `MilitaryUnit`. Nawet Gandalf.

**Q: Dlaczego te duże orzeły nie zaniosły pierścienia do Mordoru?**

A: Nie interesuj się, bo kociej mordy dostaniesz.

**Q: Java?**

A: "YOU SHALL NOT PASS!"

---

*"I tak to się kończy. Ze wszystkim co widziałem. Ze wszystkim co miałem... Zginie od miecza."* - Boromir, który nie znał wzorca Composite

**Pro tip:** Jak skończysz, spróbuj dodać metodę `battle(other: MilitaryUnit)` która symuluje walkę dwóch jednostek/armii. Z Composite to będzie proste!

**Easter egg:** W kodzie jest jednostka która *technicznie* nie powinna być tam gdzie jest. Znajdziesz ją?

Powodzenia w podboju Śródziemia! (tak, wiem, Frodo mógł wziąć kurę na sznurku)