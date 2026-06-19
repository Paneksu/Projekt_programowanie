#ifndef GAMEOBJECT_H
#define GAMEOBJECT_H

#include <QPainter>


// Klasa bazowa dla wszystkich obiektów gry.
// Używamy polimorfizmu - każdy obiekt wie, jak się rysować
// i jak się aktualizować. Klasy pochodne MUSZĄ zaimplementować
// metody czysto wirtualne (pure virtual).

class GameObject {
public:
    // Konstruktor domyślny
    GameObject();

    // Konstruktor parametryczny
    GameObject(float x, float y, int width, int height);

    // Wirtualny destruktor
    // Bez tego delete na wskaźniku bazowym nie wywołałby destruktora pochodnego.
    virtual ~GameObject();

    // Czysto wirtualne metody
    virtual void draw(QPainter& painter) = 0;
    virtual void update() = 0;

    // Gettery pozycji i rozmiaru
    float getX() const { return x; }
    float getY() const { return y; }
    int getWidth()  const { return width;  }
    int getHeight() const { return height; }

    // Ustawienie pozycji
    void setPosition(float newX, float newY);

protected:
    float x, y;        // pozycja lewego górnego rogu
    int   width, height; // rozmiar obiektu w pikselach
};

#endif // GAMEOBJECT_H
