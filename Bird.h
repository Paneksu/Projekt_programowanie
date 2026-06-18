#ifndef BIRD_H
#define BIRD_H

#include "GameObject.h"
#include <QRect>

// ============================================================
// Klasa reprezentująca ptaka - postać gracza.
// Dziedziczy po GameObject (polimorfizm).
// Ptak podlega grawitacji i może skakać.
// ============================================================
class Bird : public GameObject {
public:
    // Konstruktor domyślny - ptak w domyślnej pozycji
    Bird();

    // Konstruktor parametryczny - ptak w podanej pozycji startowej
    Bird(float startX, float startY);

    // Destruktor
    ~Bird() override;

    // Implementacja metod wirtualnych z klasy bazowej
    void draw(QPainter& painter) override;
    void update() override;

    // Skok - nadaje prędkość pionową w górę
    void jump();

    // Reset do stanu początkowego (nowa gra)
    void reset();

    // Zwraca prostokąt kolizji (nieco mniejszy niż wizualny rozmiar - bardziej fair)
    QRect getCollisionRect() const;

private:
    float velocityY; // aktualna prędkość pionowa (+ w dół, - w górę)
    float gravity;   // przyspieszenie grawitacji (piksele/klatkę²)
    float jumpForce; // prędkość nadawana przy skoku (ujemna - w górę)

    float startX, startY; // pozycja startowa do resetu
};

#endif // BIRD_H
