# Scenariusz minutowego filmiku prezentującego projekt

**Projekt:** Gra 2D Flappy Bird w C++/Qt 6  
**Wymagany czas:** ~60 sekund  
**Forma:** nagranie ekranu (screen capture) z uruchomioną grą

---

## Przygotowanie przed nagraniem

- Uruchom aplikację i ustaw okno tak, żeby było dobrze widoczne w nagraniu
- Upewnij się że masz dobry wynik do pokazania (potrenuj chwilę przed)
- Opcjonalnie: otwórz edytor kodu obok żeby pokazać fragment kodu
- Rozdzielczość nagrania: najlepiej 1920×1080, okno gry 480×640

---

## Scenariusz klatka po klatce

### [0:00 – 0:08] — Ekran startowy
**Co pokazać:**
- Okno gry z ekranem startowym
- Tytuł "Flappy Bird", podtytuł "C++ / Qt 6"
- Widoczne nazwy autorów na dole

**Co powiedzieć / napisać w opisie:**
> „Projekt zaliczeniowy z Programowania II — gra 2D Flappy Bird napisana w C++ z biblioteką Qt 6.
> Autorzy: Olaf Rysiewicz, Dawid Skatuła, Szymon Panek."

---

### [0:08 – 0:15] — Start gry i pierwsze sekundy
**Co pokazać:**
- Naciśnij spację — gra startuje
- Ptak wykonuje pierwszy skok automatycznie
- Naciskaj spację kilka razy pokazując reakcję ptaka
- Pojawia się pierwsza para rur

**Co powiedzieć:**
> „Grę startujemy spację lub kliknięciem. Ptak podlega grawitacji — cały czas opada,
> a naciśnięcie spacji daje impuls w górę."

---

### [0:15 – 0:35] — Rozgrywka — pokazanie mechanik
**Co pokazać:**
- Przelot przez 3-4 pary rur z widocznym licznikiem punktów rosnącym na górze
- Zróżnicowane wysokości rur — pokaż że są losowe
- Jeden "bliski przelot" przy krawędzi rury (żeby było widać precyzję kolizji)
- Wynik osiąga co najmniej 4-5 punktów

**Co powiedzieć:**
> „Za każdą ominięta parę rur dostajemy punkt — widać go na górze ekranu.
> Rury mają losowe wysokości przerwy. Kolizja z rurą lub ziemią kończy grę."

---

### [0:35 – 0:42] — Śmierć ptaka i ekran końca
**Co pokazać:**
- Ptak celowo uderza w rurę (albo w ziemię)
- Natychmiast wyświetla się ekran "KONIEC GRY"
- Widoczny wynik i "Rekord: X"

**Co powiedzieć:**
> „Po kolizji — ekran końca z wynikiem i rekordem sesji."

---

### [0:42 – 0:52] — Restart i drugi przebieg (szybki)
**Co pokazać:**
- Naciśnij spację → powrót do ekranu startowego → spacja → gra od nowa
- Zagraj kilka sekund drugiej partii pokazując że gra działa powtarzalnie
- Jeśli wynik jest lepszy — pokaż zaktualizowany rekord

---

### [0:52 – 1:00] — Pokazanie kodu (opcjonalnie)
**Co pokazać (opcja A — zostań przy grze):**
- Zagraj dalej, zakończ nagranie gdy ekran gry wygląda dobrze

**Co pokazać (opcja B — pokaż kod):**
- Przełącz na VS Code, pokaż plik `GameObject.h` z wirtualnymi metodami
- Pokaż `Bird.cpp` z metodą `draw()` (rysowanie QPainter)
- Lub pokaż `GameWindow.cpp` z `connect(gameTimer, ...)`

**Co powiedzieć:**
> „Projekt zrealizowany obiektowo: klasa bazowa `GameObject` z wirtualnymi metodami
> `draw()` i `update()`. Klasy `Bird`, `Pipe`, `Ground` dziedziczą i nadpisują metody.
> Grafika rysowana kodem — zero zewnętrznych plików. Qt 6, CMake, C++17."

---

## Wskazówki techniczne

- **Screen recorder:** OBS Studio (darmowy), lub Windows + G (wbudowany w Win 11)
- **Format wyjściowy:** MP4, maksymalnie 10MB zgodnie z wytycznymi prowadzącego
  - Jeśli plik jest większy: kompresja przez HandBrake lub udostępnij link (Google Drive / GitHub)
- **Dźwięk:** nieobowiązkowy; jeśli nagrywasz z mikrofonem, możesz skomentować na żywo
- **Jakość nagrania:** minimalna 720p; wyżej = lepiej ale mniej MB na minutę

## Tekst do opisu filmiku (jeśli wymagany)

> Projekt zaliczeniowy z Programowania II — Politechnika Śląska 2026.
> Gra 2D inspirowana Flappy Bird, napisana w C++17 z biblioteką Qt 6.
> Grafika rysowana w pełni kodem (QPainter). Zastosowano: dziedziczenie,
> polimorfizm, konstruktory/destruktory, wyjątki, wzorzec Factory.
> Autorzy: Olaf Rysiewicz, Dawid Skatuła, Szymon Panek.
