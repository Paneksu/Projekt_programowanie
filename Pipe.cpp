#include "Pipe.h"
#include <QPainter>
#include <stdexcept>

// Konstruktor domyślny - rura poza ekranem, bezpieczne wartości domyślne
Pipe::Pipe()
    : GameObject(600.0f, 0.0f, PIPE_WIDTH, 640),
      gapCenterY(320), gapHeight(160),
      screenHeight(640), speed(3.0f), passed(false)
{
}

// Konstruktor parametryczny z walidacją parametrów
Pipe::Pipe(float x, int gapCenterY, int gapHeight, int screenHeight)
    : GameObject(x, 0.0f, PIPE_WIDTH, screenHeight),
      gapCenterY(gapCenterY), gapHeight(gapHeight),
      screenHeight(screenHeight), speed(3.0f), passed(false)
{
    // === WALIDACJA DANYCH WEJŚCIOWYCH ===
    // Rzucamy wyjątki jeśli parametry są poza sensownym zakresem.
    // Obsługa wyjątków (try/throw/catch) - wymaganie z laboratorium.

    if (gapHeight < 90) {
        throw std::invalid_argument(
            "Przerwa miedzy rurami jest za mala! Minimum to 90 pikseli."
        );
    }

    if (gapCenterY - gapHeight / 2 < 40) {
        throw std::out_of_range(
            "Srodek przerwy jest za blisko gornej krawedzi ekranu."
        );
    }

    if (gapCenterY + gapHeight / 2 > screenHeight - 100) {
        throw std::out_of_range(
            "Srodek przerwy jest za blisko dolnej krawedzi ekranu."
        );
    }
}

Pipe::~Pipe()
{
    // Rura nie alokuje dodatkowej pamięci
}

void Pipe::draw(QPainter& painter)
{
    int px = static_cast<int>(x);
    int topEnd      = gapCenterY - gapHeight / 2;
    int bottomStart = gapCenterY + gapHeight / 2;

    painter.setBrush(QColor(78, 175, 65));
    painter.setPen(Qt::NoPen);

    painter.drawRect(px, 0, PIPE_WIDTH, topEnd);
    painter.drawRect(px, bottomStart, PIPE_WIDTH, screenHeight - bottomStart);
}

void Pipe::update()
{
    // Przesuń rurę w lewo
    x -= speed;
}

bool Pipe::isOffScreen() const
{
    // Rura wyszła poza ekran po lewej stronie
    return (x + PIPE_WIDTH + 10) < 0;
}

QRect Pipe::getTopRect() const
{
    int topEnd = gapCenterY - gapHeight / 2;
    return QRect(static_cast<int>(x), 0, PIPE_WIDTH, topEnd);
}

QRect Pipe::getBottomRect() const
{
    int bottomStart = gapCenterY + gapHeight / 2;
    int bottomH = screenHeight - bottomStart;
    return QRect(static_cast<int>(x), bottomStart, PIPE_WIDTH, bottomH);
}
