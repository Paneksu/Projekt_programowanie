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
    int gy = static_cast<int>(y);

    // Pas trawy (zielony)
    painter.setBrush(QColor(80, 170, 70));
    painter.setPen(Qt::NoPen);
    painter.drawRect(0, gy, screenWidth, 16);

    // Linia oddzielająca trawę od ziemi
    painter.setBrush(QColor(60, 140, 50));
    painter.drawRect(0, gy + 14, screenWidth, 4);

    // Ziemia (piaskowo-brązowa)
    painter.setBrush(QColor(210, 170, 110));
    painter.drawRect(0, gy + 18, screenWidth, height - 18);

    // Ciemniejszy pas w ziemi (linia podziemna)
    painter.setBrush(QColor(180, 140, 80));
    painter.drawRect(0, gy + 30, screenWidth, 8);
}

void Ground::update()
{
    // Ziemia jest statyczna - nic nie robimy
}

QRect Ground::getCollisionRect() const
{
    return QRect(static_cast<int>(x), static_cast<int>(y), screenWidth, height);
}
