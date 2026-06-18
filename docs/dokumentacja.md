# Dokumentacja projektu

## Gra 2D typu Flappy Bird w języku C++

**Przedmiot:** Programowanie II – C++ obiektowy  
**Prowadzący:** dr inż. Marcin Sobota  
**Uczelnia:** Politechnika Śląska, Wydział Automatyki, Elektroniki i Informatyki  
**Semestr:** 2025/2026, sem. 2  

---

## Autorzy

| Imię i Nazwisko | Rola w projekcie                                     |
|-----------------|------------------------------------------------------|
| Olaf Rysiewicz  | Klasa Bird, fizyka ptaka, rysowanie QPainter         |
| Dawid Skatuła   | Klasa Pipe, PipeFactory (wzorzec Factory), walidacja |
| Szymon Panek    | GameWindow, pętla gry, kolizje, UI, dokumentacja     |

---

## 1. Opis zrealizowanego projektu

### 1.1 Czym jest projekt

Zrealizowaliśmy grę 2D inspirowaną popularną grą Flappy Bird. Aplikacja okienkowa napisana w C++ z użyciem biblioteki Qt 6. Gracz steruje ptakiem, który ciągle opada pod wpływem grawitacji. Naciśnięcie spacji lub kliknięcie myszą daje ptakowi impuls w górę. Celem jest omijanie pionowych rur i zdobywanie punktów za każdą ominiętą parę.

### 1.2 Funkcjonalności

- **Ekran startowy** z tytułem, instrukcją i nazwami autorów
- **Fizyka ptaka**: grawitacja z ograniczeniem prędkości, skok po spacji/kliknięciu
- **Losowe przeszkody**: rury z losową wysokością przerwy, przesuwające się w lewo
- **Detekcja kolizji**: z rurą, ziemią i górną krawędzią ekranu
- **System punktacji**: +1 za każdą ominiętą parę rur, wyświetlanie bieżącego wyniku
- **Zapis rekordu** w trakcie sesji (najlepszy wynik pamiętany między grami)
- **Ekran końca gry** z wynikiem, rekordem i opcją restartu
- **Grafika generowana kodem** — zero zewnętrznych plików graficznych

### 1.3 Stos technologiczny

| Element    | Szczegóły                               |
|------------|-----------------------------------------|
| Język      | C++17                                   |
| GUI        | Qt 6 (moduły: Core, Widgets)            |
| Grafika    | QPainter (rysowanie wektorowe)          |
| Build      | CMake 3.16+, qt_add_executable          |
| IDE        | Visual Studio Code                      |

**Uzasadnienie wyboru QWidget + QPainter + QTimer:**  
To najprostsze podejście do gry 2D w Qt, które nie wymaga nauki API grafów sceny (QGraphicsScene) ani silnika gier. `paintEvent()` z `QPainter` daje pełną kontrolę nad tym co jest rysowane w każdej klatce, a `QTimer` z interwałem 16ms symuluje pętlę gry ~60 FPS. Idealne na poziomie projektu studenckiego.

---

## 2. Architektura i zastosowane elementy OOP

### 2.1 Hierarchia klas

```
QWidget
└── GameWindow          ← główne okno, zarządza stanem gry

GameObject              ← klasa abstrakcyjna (bazowa)
├── Bird                ← ptak gracza
├── Pipe                ← para rur (przeszkoda)
└── Ground              ← podłoże

PipeFactory             ← wzorzec Factory, tworzy rury
```

### 2.2 Dziedziczenie i polimorfizm

Klasa `GameObject` definiuje wspólny interfejs dla wszystkich obiektów gry:

```cpp
class GameObject {
public:
    virtual void draw(QPainter& painter) = 0;  // czysto wirtualna
    virtual void update() = 0;                 // czysto wirtualna
    virtual ~GameObject();                     // wirtualny destruktor!
    // ...
};
```

Klasy `Bird`, `Pipe` i `Ground` dziedziczą po `GameObject` i **nadpisują** (`override`) obie metody. Dzięki temu `GameWindow` może obsługiwać wszystkie typy obiektów jednakowo:

```cpp
// Polimorfizm w działaniu - wszystkie rury rysują się przez jedną pętlę
for (Pipe* pipe : pipes) {
    pipe->draw(painter);  // wywołuje Pipe::draw(), nie GameObject::draw()
    pipe->update();       // każda rura wie jak się poruszać
}
```

### 2.3 Konstruktory i destruktory

Każda klasa ma:
- **Konstruktor domyślny** (bezargumentowy) — bezpieczne wartości domyślne
- **Konstruktor parametryczny** — inicjalizacja ze specyficznymi wartościami
- **Destruktor** — `~GameObject()` jest `virtual` (konieczne przy polimorfizmie!)

Przykład z `Bird`:
```cpp
Bird();                              // domyślny
Bird(float startX, float startY);   // parametryczny
~Bird() override;                   // destruktor
```

### 2.4 Obsługa wyjątków

`Pipe::Pipe()` waliduje parametry i rzuca wyjątki przy błędnych wartościach:

```cpp
Pipe::Pipe(float x, int gapCenterY, int gapHeight, int screenHeight) {
    if (gapHeight < 90) {
        throw std::invalid_argument("Przerwa za mala! Minimum 90px.");
    }
    if (gapCenterY - gapHeight / 2 < 40) {
        throw std::out_of_range("Przerwa za blisko gornej krawedzi.");
    }
    // ...
}
```

`PipeFactory::createPipe()` łapie te wyjątki i w razie problemów używa bezpiecznych wartości domyślnych:

```cpp
try {
    return new Pipe(x, gapCenter, gapHeight, screenHeight);
}
catch (const std::invalid_argument& e) {
    return new Pipe(x, screenHeight/2, 170, screenHeight); // fallback
}
```

### 2.5 Wzorzec projektowy — Factory Method

`PipeFactory` implementuje wzorzec fabryki. Zamiast tworzyć rury bezpośrednio w `GameWindow`, delegujemy to do fabryki:

```cpp
// GameWindow tylko pyta fabrykę o nową rurę
Pipe* newPipe = pipeFactory->createPipe();
pipes.push_back(newPipe);
```

Fabryka sama zajmuje się losowaniem pozycji przerwy, walidacją, obsługą błędów i ustawianiem prędkości. `GameWindow` nie musi znać tych szczegółów.

---

## 3. Instrukcja użytkownika

### 3.1 Wymagania systemowe

- System operacyjny: Windows 10/11, Linux lub macOS
- Qt 6.x zainstalowane i skonfigurowane
- CMake 3.16 lub nowszy
- Kompilator z obsługą C++17 (MSVC 2019+, GCC 10+, Clang 12+)

### 3.2 Kompilacja i uruchomienie

**W Visual Studio Code (z rozszerzeniem CMake Tools):**
1. Otwórz folder projektu w VS Code
2. Naciśnij `Ctrl+Shift+P` → „CMake: Configure"
3. Wybierz zestaw narzędzi (kit) z Qt 6
4. Naciśnij `F7` (lub „CMake: Build")
5. Uruchom plik wykonywalny z folderu `build/`

**Przez terminal:**
```bash
mkdir build && cd build
cmake .. -DCMAKE_PREFIX_PATH="C:/Qt/6.x.x/msvc2019_64"
cmake --build . --config Release
./FlappyBird   # Linux/macOS
FlappyBird.exe  # Windows
```

> **Uwaga:** Zastąp ścieżkę do Qt właściwą dla Twojego systemu.

### 3.3 Sterowanie

| Akcja                  | Klawiatura       | Mysz                  |
|------------------------|------------------|-----------------------|
| Start gry              | Spacja           | Lewy przycisk myszy   |
| Skok ptaka             | Spacja lub ↑     | Lewy przycisk myszy   |
| Restart po śmierci     | Spacja           | Lewy przycisk myszy   |
| Zamknięcie gry         | Escape           | Przycisk X okna       |

### 3.4 Jak grać

1. **Uruchom grę** — zobaczysz ekran startowy z tytułem
2. **Naciśnij spację** lub kliknij aby rozpocząć
3. **Naciskaj spację rytmicznie** aby ptak leciał na odpowiedniej wysokości
4. **Omijaj rury** — przelatuj przez przerwy między górną i dolną rurą
5. Za każdą ominięta parę rur **zyskujesz +1 punkt**
6. Gra kończy się gdy ptak uderzy w rurę, ziemię lub wyleci za górną krawędź
7. Na ekranie końca widać wynik i rekord — **spacja** lub kliknięcie restartuje

---

## 4. Ciekawostki z realizacji projektu

### 4.1 Polimorfizm na wskaźnikach

Ciekawą właściwością C++ jest to, że polimorfizm (wywoływanie właściwej implementacji `draw()`/`update()`) działa **tylko przez wskaźniki lub referencje** do klasy bazowej. Gdybyśmy przechowywali obiekty przez wartość (`std::vector<Pipe>` zamiast `std::vector<Pipe*>`), polimorfizm by nie działał — nastąpiłoby zjawisko **object slicing** (obcięcie do klasy bazowej). Używamy więc `std::vector<Pipe*>`, ale płacimy za to ręcznym zarządzaniem pamięcią (`new`/`delete`).

### 4.2 Wirtualny destruktor i dlaczego to ważne

Bez `virtual ~GameObject()`, wywołanie `delete` na wskaźniku `GameObject*` wskazującym na obiekt `Bird` wywołałoby tylko destruktor `GameObject`, nie `~Bird()`. Przy klasach z zasobami (np. alokującymi pamięć w konstruktorze) to by oznaczało wyciek pamięci. Dlatego każda klasa bazowa z wirtualnymi metodami MUSI mieć wirtualny destruktor.

### 4.3 Rysowanie bez assetów

Cała grafika jest narysowana kodem — okazało się to ciekawym ćwiczeniem z QPainter. Dziób ptaka to `QPolygon` z trzema punktami. Efekt 3D rury to tylko dodatkowy jaśniejszy pasek po lewej stronie. Chmury to nakładające się elipsy. Gradient nieba robi `QLinearGradient`. To pokazuje jak dużo można zrobić bez jednego pliku PNG.

### 4.4 Problem z iteratorem wektora podczas usuwania

Klasyczny problem C++ — `std::vector::erase()` unieważnia wszystkie iteratory za usuniętym elementem. Rozwiązaliśmy go iteracją od końca wektora do początku (pętla `for (int i = size-1; i >= 0; --i)`), co gwarantuje że usunięcie elementu `i` nie wpływa na indeksy `0..i-1`, które jeszcze sprawdzimy.

### 4.5 "Terminal velocity" ptaka

W prawdziwym Flappy Bird prędkość opadania jest ograniczona. Bez tego ograniczenia, po długim locie bez skoku ptak osiągał prędkość 50-100 px/klatkę i "przelatywał przez" ziemię (kolizja była wykrywana dopiero gdy ptak był już pod ziemią — bo w jednej klatce przesuwał się więcej niż wynosił "grubość" ziemi). Dodanie `if (velocityY > 14.0f) velocityY = 14.0f;` naprawiło problem.

---

## 5. Podsumowanie i wnioski — odniesienie do założeń wstępnych

### 5.1 Co udało się zrealizować

Wszystkie założenia wstępne zostały zrealizowane:

| Założenie                    | Status | Uwagi                                         |
|------------------------------|--------|-----------------------------------------------|
| Dziedziczenie + polimorfizm  | ✅     | `GameObject` → `Bird`, `Pipe`, `Ground`       |
| Konstruktory i destruktory   | ✅     | Każda klasa; `~GameObject()` wirtualny        |
| Obsługa wyjątków             | ✅     | `Pipe::Pipe()` rzuca, `PipeFactory` łapie     |
| Wzorzec projektowy           | ✅     | Factory Method w `PipeFactory`                |
| Walidacja danych             | ✅     | Parametry rur, poziom trudności               |
| Grafika bez assetów          | ✅     | Tylko QPainter                                |
| Ekran start/koniec/wynik     | ✅     | Pełna funkcjonalność                          |
| Qt 6, CMake, VS Code         | ✅     | Zgodnie z formularzem                         |

### 5.2 Czego się nauczyliśmy

- **System sygnałów i slotów Qt** — `connect()` jest kluczowe; bez niego nic nie działa
- **Zarządzanie pamięcią w C++** — `new`/`delete`, wektory wskaźników, ryzyko wycieków
- **Polimorfizm w praktyce** — nie tylko w teorii, ale jako faktyczna technika upraszczająca pętlę gry
- **Iteracja po kontenerze z modyfikacją** — klasyczna pułapka C++ którą każdy musi napotkać osobiście
- **Hitboxy vs grafika** — w grach to dwie oddzielne rzeczy; dobry hitbox = dobry gameplay

### 5.3 Co byłoby inaczej gdybyśmy zaczynali od nowa

- Szybciej napisalibyśmy `connect()` (zaoszczędzilibyśmy ~30 minut szukania błędu #1)
- Iteracja od końca byłaby pierwszym wyborem, nie poprawką
- Flaga `passed` trafiłaby do projektu od początku

### 5.4 Trudniejsze elementy

Najtrudniejsze okazało się zrozumienie jak działa pętla zdarzeń Qt i kiedy `paintEvent()` jest wywoływane. Spodziewaliśmy się że Qt "samo" będzie rysować gdy dane się zmienią — w rzeczywistości to programista musi jawnie wywołać `update()` żeby poinformować Qt że widget wymaga przerysowania.

---

## 6. Możliwości rozbudowy projektu

### 6.1 Krótkoterminowe (stosunkowo proste)

| Pomysł                        | Opis                                                        |
|-------------------------------|-------------------------------------------------------------|
| Efekty dźwiękowe              | Qt Multimedia (`QSoundEffect`) — ding przy punkcie, crash   |
| Animacja ptaka                | Kilka klatek rysowanych naprzemiennie co 5 klatek gry       |
| Zapis rekordu do pliku        | `QFile` + `QDataStream` — rekord przetrwa zamknięcie programu |
| Rosnąca trudność w grze       | Co 10 punktów przyspieszyć rury (`pipeFactory->setDifficulty`) |
| Cząsteczki przy kolizji       | Wybuch z elips rozlatujących się przy zderzeniu             |

### 6.2 Długoterminowe (większy nakład pracy)

| Pomysł                        | Opis                                                        |
|-------------------------------|-------------------------------------------------------------|
| Tablica wyników online        | REST API + Qt Network — wysyłanie wyników na serwer         |
| Własna mapa / skórki          | Rozszerzenie hierarchii klas, np. `NightBird : Bird`        |
| Tryb multiplayer (lokalny)    | Drugi ptak sterowany klawiszami, rywalizacja kto dalej zajdzie |
| Poziomy / motywy              | Różne tła, kolory rur per poziom — zmiana przez polimorfizm |
| Fizyka dokładniejsza          | Obrót ptaka proporcjonalny do prędkości pionowej (lerp)     |
| QML zamiast QWidget           | Interfejs w QML dla lepszej animacji i stylistyki           |

### 6.3 Elementy OOP do rozszerzenia

Projekt daje dobry fundament dla ćwiczenia wzorców:
- **Observer** — `GameState` jako obiekt z listą observerów (UI, logger, sound)
- **Strategy** — różne strategie AI dla ptaka (demo mode)
- **Template Method** — `GameObject::gameStep()` = `update() + draw()` jako szablon metody

---

*Dokumentacja sporządzona: czerwiec 2026*  
*Wersja projektu: 1.0 (finalna)*
