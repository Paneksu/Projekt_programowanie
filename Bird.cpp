#include "Bird.h"
#include <QPainter>
#include <QPolygon>
#include <QPoint>

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
    int bx = static_cast<int>(x);
    int by = static_cast<int>(y);

    // --- Ciało ptaka (żółta elipsa) ---
    painter.setBrush(QColor(255, 220, 0));
    painter.setPen(QPen(QColor(180, 140, 0), 2));
    painter.drawEllipse(bx, by, width, height);

    // --- Skrzydło (ciemniejszy owal) ---
    painter.setBrush(QColor(220, 170, 0));
    painter.setPen(Qt::NoPen);
    painter.drawEllipse(bx + 4, by + height / 2, 14, 8);

    // --- Oko (białe + czarna źrenica) ---
    painter.setBrush(Qt::white);
    painter.setPen(Qt::NoPen);
    painter.drawEllipse(bx + width / 2 + 2, by + 4, 11, 11);
    painter.setBrush(Qt::black);
    painter.drawEllipse(bx + width / 2 + 5, by + 7, 5, 5);

    // --- Dziób (pomarańczowy trójkąt) ---
    QPolygon beak;
    beak << QPoint(bx + width,      by + height / 2 - 3)
         << QPoint(bx + width + 10, by + height / 2)
         << QPoint(bx + width,      by + height / 2 + 3);
    painter.setBrush(QColor(255, 140, 0));
    painter.setPen(QPen(QColor(200, 100, 0), 1));
    painter.drawPolygon(beak);
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
    // Kolizja jest trochę mniejsza niż wizualny rozmiar ptaka -
    // dzięki temu gra jest bardziej fair i nie frustruje gracza.
    const int margin = 5;
    return QRect(
        static_cast<int>(x) + margin,
        static_cast<int>(y) + margin,
        width  - 2 * margin,
        height - 2 * margin
    );
}
