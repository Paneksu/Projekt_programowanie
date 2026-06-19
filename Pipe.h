#ifndef PIPE_H
#define PIPE_H

#include "GameObject.h"
#include <QRect>
#include <stdexcept>


// Klasa reprezentująca parę rur (górna + dolna z przerwą).
// Dziedziczy po GameObject.
// Konstruktor rzuca wyjątek jeśli parametry są nieprawidłowe
// (walidacja danych - wymaganie z laboratorium).

class Pipe : public GameObject {
public:
    // Szerokość rury (stała klasy, public żeby GameWindow mógł jej użyć)
    static constexpr int PIPE_WIDTH = 58;

    // Konstruktor domyślny
    Pipe();

    // Konstruktor parametryczny z walidacją wejścia
    // Rzuca std::invalid_argument lub std::out_of_range przy złych parametrach
    Pipe(float x, int gapCenterY, int gapHeight, int screenHeight);

    ~Pipe() override;

    // Implementacja metod wirtualnych
    void draw(QPainter& painter) override;
    void update() override;

    // Czy rura wyszła za lewy brzeg ekranu?
    bool isOffScreen() const;

    // Flaga - czy ptak już zdobył punkt za tę rurę?
    bool isPassed() const  { return passed; }
    void setPassed(bool p) { passed = p;    }

    // Prostokąty kolizji (oddzielnie górna i dolna rura)
    QRect getTopRect()    const;
    QRect getBottomRect() const;

    // Setter prędkości (używany przez PipeFactory do ustawienia trudności)
    void setSpeed(float s) { speed = s; }

private:
    int   gapCenterY;   // środek przerwy między rurami (Y)
    int   gapHeight;    // wysokość przerwy w pikselach
    int   screenHeight; // wysokość ekranu (potrzebna do rysowania dolnej rury)
    float speed;        // prędkość przesuwania w lewo (piksele/klatkę)
    bool  passed;       // czy ptak już przeleciał przez tę rurę
};

#endif // PIPE_H
