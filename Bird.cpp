#include "Bird.h"
#include <QPainter>

// Konstruktor domyślny - ptak pojawia się mniej więcej na środku ekranu
Bird::Bird()
    : GameObject(100.0f, 270.0f, 34, 24),
      velocityY(0.0f),
      gravity(0.5f),
      jumpForce(-9.0f),
      startX(100.0f),
      startY(270.0f)
{
}

// Konstruktor parametryczny
Bird::Bird(float startX, float startY)
    : GameObject(startX, startY, 34, 24),
      velocityY(0.0f),
      gravity(0.5f),
      jumpForce(-9.0f),
      startX(startX),
      startY(startY)
{
}

Bird::~Bird()
{
    // Ptak nie alokuje dodatkowej pamięci - destruktor pusty
}

void Bird::draw(QPainter& painter)
{
    painter.setBrush(QColor(255, 220, 0));
    painter.setPen(Qt::NoPen);
    painter.drawRect(static_cast<int>(x), static_cast<int>(y), width, height);
}

void Bird::update()
{
    // Zastosuj grawitację - prędkość rośnie w dół co klatkę
    velocityY += gravity;

    // Ogranicz maksymalną prędkość opadania (terminal velocity)
    if (velocityY > 14.0f) velocityY = 14.0f;

    // Przesuń ptaka pionowo
    y += velocityY;
}

void Bird::jump()
{
    // Nadaj prędkość w górę (jumpForce jest ujemne)
    velocityY = jumpForce;
}

void Bird::reset()
{
    x = startX;
    y = startY;
    velocityY = 0.0f;
}

QRect Bird::getCollisionRect() const
{
    // Kolizja jest trochę mniejsza niż wizualny rozmiar ptaka
    const int margin = 5;
    return QRect(
        static_cast<int>(x) + margin,
        static_cast<int>(y) + margin,
        width  - 2 * margin,
        height - 2 * margin
    );
}
