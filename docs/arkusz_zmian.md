# Arkusz zmian (Change Log)

**Projekt:** Gra 2D Flappy Bird w C++/Qt 6  
**Zespół:** Olaf Rysiewicz, Dawid Skatuła, Szymon Panek

---

## Iteracja 0 — Inicjalizacja projektu  
*Data: 26.04.2026*

### Dodano
- Szkielet projektu: plik `CMakeLists.txt` i pusty `main.cpp`
- Plik formularza zgłoszenia projektu (wysłany na platformę)
- Arkusz wstępny z zaplanowaną architekturą klas
- Podstawowa struktura katalogów

### Decyzje projektowe
- Wybrano `QWidget + QPainter + QTimer` jako podejście do pętli gry
  (zamiast `QGraphicsScene` — zbyt skomplikowane na ten poziom)
- Grafika w pełni rysowana kodem (bez plików PNG/SVG)
- Surowe wskaźniki + ręczny `delete` (zamiast `shared_ptr`) — bardziej
  edukacyjnie, pokazuje zarządzanie pamięcią

---

## Iteracja 1 — Pierwsza wersja klas i okno Qt  
*Data: 03.05.2026*

### Dodano
- Klasa `GameObject` (abstrakcyjna, z `draw()` i `update()` czysto wirtualnymi)
- Klasa `Bird` (konstruktory, podstawowa fizyka — grawitacja i skok)
- Klasa `Ground` (statyczna, tylko kolizja i rysowanie)
- Klasa `GameWindow` dziedzicząca po `QWidget`
- Podstawowe `paintEvent()` rysujące tło i ptaka
- `QTimer` z interwałem 16ms

### Błędy napotkane w tej iteracji
- **Błąd #1 (krytyczny):** Timer skonfigurowany ale pętla gry NIGDY nie
  działała — zapomniano wywołać `connect()`.  
  → Ekran wyświetlał się ale był statyczny.  
  → Szczegóły: patrz `dziennik_bledow.md`, Błąd #1.

### Zmieniono
- Kolejność inicjalizacji w konstruktorze `GameWindow`: najpierw obiekty
  gry, potem timer. Dzięki temu nie ma ryzyka że timer wystartuje
  zanim obiekty są gotowe.

---

## Iteracja 2 — Rury i pętla gry  
*Data: 10.05.2026*

### Dodano
- Klasa `Pipe` z konstruktorem walidującym parametry (wyjątki)
- Klasa `PipeFactory` (wzorzec fabryki)
- Spawn rur w pętli gry co `pipeSpawnEvery = 88` klatek (~1.4 sekundy)
- Usuwanie rur, które wyszły za ekran (lewy brzeg)
- Podstawowa detekcja kolizji

### Błędy napotkane w tej iteracji
- **Błąd #2 (crash):** Segmentation fault przy usuwaniu rur z wektora
  podczas iteracji w przód — `erase()` unieważniał iterator.  
  → Szczegóły: patrz `dziennik_bledow.md`, Błąd #2.
- **Błąd #3 (logiczny):** Zapomniano o wywołaniu `update()` na końcu
  `gameLoop()` — ekran odświeżał się tylko przy zdarzeniach Qt, nie
  co klatkę.  
  → Szczegóły: patrz `dziennik_bledow.md`, Błąd #3.

### Zmieniono
- Iteracja po rurach zamieniona na odwrotną (`for (int i = size-1; ...)`)
  żeby można było bezpiecznie `erase()` podczas iteracji
- Dodano `update()` na końcu `gameLoop()`

---

## Iteracja 3 — Kolizje i wynik  
*Data: 17.05.2026*

### Dodano
- Wynik wyświetlany w czasie rzeczywistym na górze ekranu
- Zapis i wyświetlanie rekordu (`bestScore`)
- Stany gry (`GameState::START`, `PLAYING`, `GAMEOVER`)
- Ekrany: startowy i końca gry

### Błędy napotkane w tej iteracji
- **Błąd #4 (logiczny):** Kolizja z rurami była wykrywana za wcześnie —
  hitbox rury był o 20px szerszy niż wizualna rura.  
  → Gracz ginął przed dotknięciem rury. Frustrujące.  
  → Szczegóły: patrz `dziennik_bledow.md`, Błąd #4.
- **Błąd #5 (logiczny):** Wynik rósł o kilka punktów za jedną rurę.  
  → Szczegóły: patrz `dziennik_bledow.md`, Błąd #5.

### Zmieniono
- Hitboxy rur dopasowane do wizualnego korpusu (bez paddingu od czapki)
- Dodano flagę `passed` w klasie `Pipe` — punkt naliczany DOKŁADNIE raz
- Hitbox ptaka zmniejszony o margines 5px z każdej strony

---

## Iteracja 4 — Polishing i finalizacja  
*Data: 25.05.2026*

### Dodano
- Ładniejszy rysunek ptaka (skrzydło, oko ze źrenicą, dziób jako `QPolygon`)
- Chmury na tle nieba
- Gradient nieba (`QLinearGradient`)
- Ładniejszy rysunek rur (efekt 3D — jaśniejsza lewa krawędź)
- Linia trawy w ziemi
- Obsługa klawisza `Escape` (zamknięcie okna)
- Wyświetlanie nazw autorów na ekranie startowym
- Ograniczenie maksymalnej prędkości opadania ptaka (14 px/klatkę)
  żeby nie leciał przez podłogę przy wysokim FPS

### Zmieniono
- Komentarze uzupełnione we wszystkich plikach
- Stałe `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `GROUND_HEIGHT` jako `static const`
  w `GameWindow` (zamiast magic numbers rozsianych po kodzie)
- `PipeFactory::setDifficulty()` — teraz zarówno prędkość jak i przerwa
  zmieniają się z poziomem
- Walidacja w `Pipe::Pipe()` — dodano trzeci warunek sprawdzający
  czy dolna krawędź przerwy nie wychodzi poza ekran
- Dokumentacja uzupełniona o wszystkie pliki

### Naprawiono
- Cień tekstu wyniku rysowany PRZED głównym tekstem (poprawna kolejność)
- Sprawdzanie `if (pipe != nullptr)` przed `draw()` i kolizją
  (defensywne — wektorowe wskaźniki nie powinny być null, ale dla bezpieczeństwa)

---

## Wersja finalna — v1.0  
*Data: 07.06.2026*

### Status
- Wszystkie wymagania funkcjonalne i techniczne zrealizowane ✅
- Kod działa poprawnie, brak znanych błędów
- Dokumentacja kompletna

### Pliki w projekcie
```
FlappyBird/
├── CMakeLists.txt
├── main.cpp
├── GameObject.h / .cpp
├── Bird.h / .cpp
├── Pipe.h / .cpp
├── Ground.h / .cpp
├── PipeFactory.h / .cpp
├── GameWindow.h / .cpp
└── docs/
    ├── arkusz_wstepny.md
    ├── lista_wymagan.md
    ├── arkusz_zmian.md     ← ten plik
    ├── dziennik_bledow.md
    ├── dokumentacja.md
    └── scenariusz_filmiku.md
```
