#ifndef PIPEFACTORY_H
#define PIPEFACTORY_H

#include "Pipe.h"

// ============================================================
// Wzorzec projektowy: Fabryka (Factory Method)
// PipeFactory odpowiada za tworzenie rur z losowymi pozycjami
// przerwy. Centralizuje logikę generowania przeszkód.
//
// Dzięki fabryce GameWindow nie musi znać szczegółów
// generowania losowych pozycji - po prostu prosi fabrykę
// o nową rurę.
// ============================================================
class PipeFactory {
public:
    // Konstruktor - przyjmuje parametry ekranu
    PipeFactory(int screenWidth, int screenHeight, int groundHeight);

    // Destruktor
    ~PipeFactory();

    // Utwórz nową rurę z losową pozycją przerwy.
    // Zwraca wskaźnik - wywołujący jest odpowiedzialny za delete!
    Pipe* createPipe();

    // Ustaw poziom trudności (1 = łatwy, 5 = trudny)
    // Zmienia prędkość rur i rozmiar przerwy
    void setDifficulty(int level);

private:
    int screenWidth;
    int screenHeight;
    int groundHeight;
    int gapHeight;   // aktualna wysokość przerwy (zmienia się z trudnością)
    float pipeSpeed; // aktualna prędkość rur
};

#endif // PIPEFACTORY_H
