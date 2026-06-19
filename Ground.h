#ifndef GROUND_H
#define GROUND_H

#include "GameObject.h"
#include <QRect>


// Klasa reprezentująca ziemię / podłoże.
// Dziedziczy po GameObject.
// Ziemia jest statyczna (nie przesuwa się).

class Ground : public GameObject {
public:
    // Konstruktor domyślny
    Ground();

    // Konstruktor parametryczny
    Ground(int screenWidth, int screenHeight, int groundHeight);

    ~Ground() override;

    // Implementacja metod wirtualnych
    void draw(QPainter& painter) override;
    void update() override; // ziemia się nie porusza - pusta implementacja

    // Prostokąt kolizji
    QRect getCollisionRect() const;

private:
    int screenWidth; // szerokość ekranu (do rysowania pełnej szerokości)
};

#endif // GROUND_H
