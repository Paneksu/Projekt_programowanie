#include "GameObject.h"

// Konstruktor domyślny - inicjalizuje na pozycji (0,0) z zerowym rozmiarem
GameObject::GameObject()
    : x(0.0f), y(0.0f), width(0), height(0)
{
}

// Konstruktor parametryczny - ustawia pozycję i rozmiar
GameObject::GameObject(float x, float y, int width, int height)
    : x(x), y(y), width(width), height(height)
{
}

// Wirtualny destruktor - nic specjalnego do zwalniania w klasie bazowej,
// ale musi istnieć żeby polimorficzne delete działało poprawnie.
GameObject::~GameObject()
{
}

void GameObject::setPosition(float newX, float newY)
{
    x = newX;
    y = newY;
}
