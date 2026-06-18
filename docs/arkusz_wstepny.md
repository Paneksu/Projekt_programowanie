# Arkusz wstępny projektu

**Przedmiot:** Programowanie II – C++ obiektowy  
**Prowadzący:** dr inż. Marcin Sobota  
**Uczelnia:** Politechnika Śląska  
**Semestr:** 2025/2026, sem. 2  

---

## Dane zespołu

| Lp. | Imię i Nazwisko  |
|-----|------------------|
| 1   | Olaf Rysiewicz   |
| 2   | Dawid Skatuła    |
| 3   | Szymon Panek     |

---

## Temat projektu

**Gra 2D typu Flappy Bird w języku C++**

---

## Opis pomysłu

Planujemy stworzyć grę inspirowaną Flappy Bird. Gracz steruje ptakiem, który leci w prawo i musi omijać pionowe rury. Ptak ciągle opada (grawitacja), a gracz klika/naciska spację żeby dać impuls w górę. Za każdą ominiętą parę rur dostaje punkt. Gra kończy się gdy ptak uderzy w rurę lub ziemię.

Wybraliśmy ten temat bo:
- gra jest prosta koncepcyjnie, ale wymaga przemyślanej struktury klas
- da się w niej naturalnie pokazać polimorfizm (ptak, rura, ziemia to różne klasy, ale wszystkie mają `draw()` i `update()`)
- będzie dobrze wyglądać na prezentacji — działa "na żywo" i jest interaktywna

---

## Planowana architektura klas

### Hierarchia dziedziczenia

```
GameObject (klasa abstrakcyjna - bazowa)
├── Bird    (ptak - gracz)
├── Pipe    (para rur - przeszkoda)
└── Ground  (ziemia - kolizja)
```

### Klasa `GameObject` (abstrakcyjna)
- pola: `x`, `y`, `width`, `height`
- metody czysto wirtualne: `draw(QPainter&)`, `update()`
- wirtualny destruktor
- gettery pozycji i rozmiaru

### Klasa `Bird`
- prędkość pionowa, grawitacja, siła skoku
- metody: `jump()`, `reset()`, `getCollisionRect()`
- rysowanie: żółta elipsa z okiem i dziobem (QPainter)

### Klasa `Pipe`
- środek przerwy (`gapCenterY`), wysokość przerwy (`gapHeight`)
- prędkość przesuwania w lewo
- flaga `passed` — żeby nie liczyć punktu dwa razy
- walidacja w konstruktorze (wyjątki)
- metody: `getTopRect()`, `getBottomRect()`, `isOffScreen()`

### Klasa `Ground`
- statyczna (nie przesuwa się)
- prostokąt kolizji

### Klasa `PipeFactory` (wzorzec Factory)
- odpowiada za tworzenie rur z losowymi przerwami
- parametr trudności zmienia prędkość i rozmiar przerwy

### Klasa `GameWindow` (QWidget)
- dziedziczy po `QWidget` (nie po `GameObject` — to okno Qt, nie obiekt gry)
- zarządza stanem gry (START, PLAYING, GAMEOVER)
- posiada `QTimer` do pętli gry (~60 FPS)
- obsługuje zdarzenia klawiatury i myszy
- przechowuje `vector<Pipe*>` z rurami

---

## Stos technologiczny

| Element        | Wybór                        | Powód                                               |
|----------------|------------------------------|-----------------------------------------------------|
| Język          | C++17                        | wymaganie prowadzącego                              |
| GUI / grafika  | Qt 6 (Widgets + QPainter)    | QWidget z QPainter = prosty, obiektowy, dobrze znamy z labów |
| Podejście GUI  | QWidget + QPainter + QTimer  | najprostsze rozsądne podejście do gry 2D w Qt       |
| IDE            | Visual Studio Code           | jak w formularzu zgłoszenia                         |
| Build system   | CMake + qt_add_executable    | standardowy sposób budowania projektów Qt 6          |

**Dlaczego QWidget + QPainter a nie np. QGraphicsScene?**  
QGraphicsScene jest potężniejsza ale znacznie bardziej skomplikowana. QWidget z QPainter w metodzie `paintEvent()` i odświeżaniem przez `update()` + `QTimer` jest najprostszą możliwą architekturą pętli gry w Qt. Nadaje się idealnie dla prostej gry 2D na poziomie projektu studenckiego.

---

## Planowany podział pracy

| Osoba          | Zakres                                              |
|----------------|-----------------------------------------------------|
| Olaf Rysiewicz | Klasa `Bird`, rysowanie ptaka, fizyka (grawitacja)  |
| Dawid Skatuła  | Klasa `Pipe` + `PipeFactory`, wzorzec Factory       |
| Szymon Panek   | `GameWindow` (pętla gry, kolizje, UI, ekrany)       |
| Wszyscy        | `GameObject`, `Ground`, dokumentacja, testowanie    |

---

## Elementy z laboratorium, które planujemy pokazać

| Element                     | Gdzie zastosujemy                                           |
|-----------------------------|-------------------------------------------------------------|
| Konstruktor domyślny        | wszystkie klasy                                             |
| Konstruktor parametryczny   | wszystkie klasy                                             |
| Destruktor                  | wszystkie klasy (`~GameObject()` wirtualny)                 |
| Dziedziczenie               | `Bird`, `Pipe`, `Ground` dziedziczą po `GameObject`         |
| Polimorfizm                 | pętla `for(pipe : pipes) pipe->draw(painter)` przez pointer |
| Wyjątki (try/throw/catch)   | walidacja w `Pipe::Pipe()`, obsługa w `PipeFactory`         |
| Wzorzec projektowy          | `PipeFactory` – wzorzec fabryki                             |
| Walidacja danych            | parametry rury, poziom trudności                            |
| Komentarze                  | w każdym pliku                                              |

---

## Przewidywane trudności

1. Synchronizacja pętli gry z odświeżaniem ekranu Qt (QTimer vs paintEvent)
2. Precyzja wykrywania kolizji — żeby gra była fair
3. Zarządzanie pamięcią (delete rur gdy wyjdą za ekran)
4. Rysowanie grafiki bez plików graficznych (tylko QPainter)

---

*Data sporządzenia arkusza: kwiecień 2026*
