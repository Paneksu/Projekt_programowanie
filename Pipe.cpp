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

    // Kolory rury
    const QColor pipeGreen(78, 175, 65);
    const QColor pipeLight(120, 210, 100);
    const QColor pipeDark (50,  130, 40);
    const QColor capColor (70,  165, 58);

    // Oblicz granice przerwy
    int topEnd    = gapCenterY - gapHeight / 2; // dolna krawędź górnej rury
    int bottomStart = gapCenterY + gapHeight / 2; // górna krawędź dolnej rury

    painter.setPen(Qt::NoPen);

    // ====== GÓRNA RURA ======
    if (topEnd > 10) {
        // Korpus
        painter.setBrush(pipeGreen);
        painter.drawRect(px, 0, PIPE_WIDTH, topEnd - 14);

        // Podświetlenie lewej krawędzi (efekt 3D)
        painter.setBrush(pipeLight);
        painter.drawRect(px, 0, 9, topEnd - 14);

        // Cień prawej krawędzi
        painter.setBrush(pipeDark);
        painter.drawRect(px + PIPE_WIDTH - 6, 0, 6, topEnd - 14);

        // Końcówka (szersza, cappuje rurę od dołu)
        painter.setBrush(capColor);
        painter.drawRect(px - 6, topEnd - 14, PIPE_WIDTH + 12, 14);
        painter.setBrush(pipeLight);
        painter.drawRect(px - 6, topEnd - 14, 9, 14);
    }

    // ====== DOLNA RURA ======
    int bottomBodyH = screenHeight - bottomStart - 14;
    if (bottomBodyH > 0) {
        // Końcówka od góry
        painter.setBrush(capColor);
        painter.drawRect(px - 6, bottomStart, PIPE_WIDTH + 12, 14);
        painter.setBrush(pipeLight);
        painter.drawRect(px - 6, bottomStart, 9, 14);

        // Korpus
        painter.setBrush(pipeGreen);
        painter.drawRect(px, bottomStart + 14, PIPE_WIDTH, bottomBodyH);

        // Podświetlenie
        painter.setBrush(pipeLight);
        painter.drawRect(px, bottomStart + 14, 9, bottomBodyH);

        // Cień
        painter.setBrush(pipeDark);
        painter.drawRect(px + PIPE_WIDTH - 6, bottomStart + 14, 6, bottomBodyH);
    }
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
