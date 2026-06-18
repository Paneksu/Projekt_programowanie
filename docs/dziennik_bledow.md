# Dziennik błędów (Bug Log)

**Projekt:** Gra 2D Flappy Bird w C++/Qt 6  
**Zespół:** Olaf Rysiewicz, Dawid Skatuła, Szymon Panek

---

## Błąd #1 — Pętla gry nie działała (brak connect)

**Data wykrycia:** 03.05.2026  
**Priorytet:** Krytyczny  
**Status:** Naprawiony

### Objaw
Okno Qt się wyświetlało, ale ekran był statyczny — ptak nie spadał, nic się nie animowało.

### Diagnoza
W konstruktorze `GameWindow` timer był skonfigurowany, ale brakowało linii `connect()` łączącej sygnał `timeout()` ze slotem `gameLoop()`. Timer odliczał, ale nie wywoływał żadnej metody.

```cpp
// BŁĄD
gameTimer = new QTimer(this);
gameTimer->start(16);  // connect() pominięto

// POPRAWKA
gameTimer = new QTimer(this);
connect(gameTimer, &QTimer::timeout, this, &GameWindow::gameLoop);
gameTimer->start(16);
```

---

## Błąd #2 — Crash (Segmentation Fault) przy usuwaniu rur

**Data wykrycia:** 10.05.2026  
**Priorytet:** Krytyczny  
**Status:** Naprawiony

### Objaw
Gra crashowała po ~5 sekundach, gdy pierwsza rura wychodziła za lewy brzeg ekranu.

### Diagnoza
Podczas iteracji w przód po wektorze `pipes` wywoływano `erase()`, co unieważniało indeksy kolejnych elementów. Skutkowało to odwołaniem do zwolnionej pamięci.

```cpp
// BŁĄD — iteracja w przód z erase()
for (int i = 0; i < pipes.size(); i++) {
    if (pipes[i]->isOffScreen()) {
        delete pipes[i];
        pipes.erase(pipes.begin() + i);  // indeksy się przesuwają!
    }
}

// POPRAWKA — iteracja od końca
for (int i = static_cast<int>(pipes.size()) - 1; i >= 0; --i) {
    if (pipes[i]->isOffScreen()) {
        delete pipes[i];
        pipes.erase(pipes.begin() + i);  // bezpieczne
    }
}
```

---

## Błąd #3 — Kolizja z rurą wykrywana za wcześnie

**Data wykrycia:** 17.05.2026  
**Priorytet:** Wysoki  
**Status:** Naprawiony

### Objaw
Ptak "ginął" kilka pikseli przed dotknięciem rury — gra wyglądała niesprawiedliwie.

### Diagnoza
Hitbox rury zawierał padding wizualny czapki rury (+6px z każdej strony), a hitbox ptaka był równy pełnemu rozmiarowi sprite'a. Kolizja była wykrywana z niewidoczną częścią rury.

```cpp
// BŁĄD — hitbox z paddingiem czapki
return QRect(static_cast<int>(x) - 6, 0, PIPE_WIDTH + 12, topEnd);

// POPRAWKA — hitbox równy korpusowi rury
return QRect(static_cast<int>(x), 0, PIPE_WIDTH, topEnd);
```

Dodatkowo zmniejszono hitbox ptaka o margines 5px z każdej strony, co poprawiło odczucia gracza.

---
