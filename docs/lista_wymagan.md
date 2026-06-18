# Lista wymagań projektu

**Projekt:** Gra 2D typu Flappy Bird

---

## Wymagania funkcjonalne

### Ekran startowy
- **Opis:** Po uruchomieniu gra wyświetla ekran startowy z tytułem i instrukcją.
- **Warunek akceptacji:** Widoczny napis „Flappy Bird" i informacja o sposobie startu.
- **Status:** ✅ Zrealizowane

### Start gry
- **Opis:** Naciśnięcie spacji lub kliknięcie lewym przyciskiem myszy na ekranie startowym rozpoczyna grę.
- **Warunek akceptacji:** Ptak zaczyna lecieć, pojawiają się rury.
- **Status:** ✅ Zrealizowane

### Grawitacja ptaka
- **Opis:** Ptak bez interwencji gracza ciągle opada (grawitacja).
- **Warunek akceptacji:** Prędkość opadania rośnie z czasem (przyspieszenie), maksymalna prędkość ograniczona.
- **Status:** ✅ Zrealizowane (prędkość maks. = 14 px/kl.)

### Skok ptaka
- **Opis:** Naciśnięcie spacji lub kliknięcie nadaje ptakowi prędkość w górę.
- **Warunek akceptacji:** Ptak natychmiast zmienia kierunek na górę, może skakać wielokrotnie.
- **Status:** ✅ Zrealizowane

### Przesuwające się rury
- **Opis:** Rury pojawiają się z prawej strony i przesuwają się w lewo ze stałą prędkością.
- **Warunek akceptacji:** Rury mają losową wysokość przerwy; przerwa jest zawsze do przejścia.
- **Status:** ✅ Zrealizowane

### Detekcja kolizji
- **Opis:** Gra wykrywa kolizję ptaka z rurą, ziemią lub górną krawędzią ekranu.
- **Warunek akceptacji:** Każda taka kolizja kończy grę i pokazuje ekran końca.
- **Status:** ✅ Zrealizowane

### System punktacji
- **Opis:** Przelot przez przerwę między rurami zwiększa wynik o 1 punkt.
- **Warunek akceptacji:** Punkt naliczany dokładnie raz za parę rur; wynik widoczny na ekranie.
- **Status:** ✅ Zrealizowane (dzięki fladze `passed` w Pipe)

### Ekran końca gry
- **Opis:** Po śmierci ptaka wyświetlany jest ekran z wynikiem bieżącym i rekordem.
- **Warunek akceptacji:** Widoczny wynik i rekord, informacja o restarcie.
- **Status:** ✅ Zrealizowane

### Restart gry
- **Opis:** Na ekranie końca gry naciśnięcie spacji / kliknięcie restartuje grę.
- **Warunek akceptacji:** Powrót do ekranu startowego, wyczyszczenie rur, reset ptaka.
- **Status:** ✅ Zrealizowane

### Zapis rekordu
- **Opis:** Najlepszy wynik z całej sesji jest pamiętany i wyświetlany.
- **Warunek akceptacji:** Rekord nie resetuje się między grami (tylko przy zamknięciu programu).
- **Status:** ✅ Zrealizowane

---

## Wymagania techniczne

### Język C++ obiektowy
- **Opis:** Wiodącym językiem jest C++ z pełnym wykorzystaniem OOP.
- **Status:** ✅ Zrealizowane (klasy, dziedziczenie, polimorfizm)

### Hierarchia dziedziczenia
- **Opis:** Klasa abstrakcyjna `GameObject` z klasami pochodnymi `Bird`, `Pipe`, `Ground`.
- **Status:** ✅ Zrealizowane

### Polimorfizm
- **Opis:** Wirtualne metody `draw()` i `update()` wywoływane przez wskaźniki/referencje do `GameObject`.
- **Status:** ✅ Zrealizowane (pętla po `std::vector<Pipe*>`)

### Konstruktory i destruktory
- **Opis:** Każda klasa ma konstruktor domyślny, parametryczny i destruktor.
- **Status:** ✅ Zrealizowane; destruktor `~GameObject()` jest wirtualny

### Obsługa wyjątków
- **Opis:** Walidacja parametrów przez `throw`, obsługa przez `try/catch`.
- **Status:** ✅ Zrealizowane w `Pipe::Pipe()` i `PipeFactory::createPipe()`

### Wzorzec projektowy
- **Opis:** Zastosowanie co najmniej jednego wzorca projektowego.
- **Status:** ✅ Zrealizowane — **Factory Method** (`PipeFactory`)

### Walidacja danych
- **Opis:** Program waliduje parametry i obsługuje błędne dane.
- **Status:** ✅ Zrealizowane (min. rozmiar przerwy, zakres pozycji, poziom trudności)

### Grafika bez assetów zewnętrznych
- **Opis:** Wszystkie elementy graficzne rysowane kodem (QPainter).
- **Status:** ✅ Zrealizowane (prostokąty, elipsy, gradienty, tekst)

### Komentarze w kodzie
- **Opis:** Kod opatrzony komentarzami opisującymi działanie.
- **Status:** ✅ Zrealizowane (każda klasa, każda metoda)

### Qt 6, CMake, VS Code
- **Opis:** Projekt budowany przez CMake z Qt 6; tworzony w VS Code.
- **Status:** ✅ Zrealizowane (`CMakeLists.txt` z `qt_add_executable`)

---

## Wymagania odrzucone / niezrealizowane

| Wymaganie                  | Powód odrzucenia                                          |
|----------------------------|-----------------------------------------------------------|
| Efekty dźwiękowe           | Wymagałyby modułu Qt Multimedia; komplikuje build         |
| Zapis rekordu do pliku     | Poza zakresem projektu; rekord żyje tylko przez sesję    |
| Animacja ptaka (klatki)    | Bez assetów zewnętrznych trudne do zrobienia ładnie       |
| Poziomy trudności (menu)   | Uproszczono — trudność rośnie automatycznie co 10 pkt    |
