#include "Ground.h"
#include <QPainter>

// Konstruktor domyślny - standardowe wartości dla ekranu 480x640
Ground::Ground()
    : GameObject(0.0f, 560.0f, 480, 80),
      screenWidth(480)
{
}

// Konstruktor parametryczny
Ground::Ground(int screenWidth, int screenHeight, int groundHeight)
    : GameObject(0.0f, static_cast<float>(screenHeight - groundHeight),
                 screenWidth, groundHeight),
      screenWidth(screenWidth)
{
}

Ground::~Ground()
{
}

void Ground::draw(QPainter& painter)
{
    painter.setBrush(QColor(80, 170, 70));
    painter.setPen(Qt::NoPen);
    painter.drawRect(0, static_cast<int>(y), screenWidth, height);
}

void Ground::update()
{
    // Ziemia jest statyczna - nic nie robimy
}

QRect Ground::getCollisionRect() const
{
    return QRect(static_cast<int>(x), static_cast<int>(y), screenWidth, height);
}
