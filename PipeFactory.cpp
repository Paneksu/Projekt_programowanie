#include "PipeFactory.h"
#include <cstdlib>
#include <ctime>
#include <stdexcept>

PipeFactory::PipeFactory(int screenWidth, int screenHeight, int groundHeight)
    : screenWidth(screenWidth),
      screenHeight(screenHeight),
      groundHeight(groundHeight),
      gapHeight(165),
      pipeSpeed(3.0f)
{
    // Inicjalizuj generator liczb pseudolosowych
    srand(static_cast<unsigned int>(time(nullptr)));
}

PipeFactory::~PipeFactory()
{
    // Fabryka nie przechowuje wskaźników do rur, więc nic nie zwalniamy
}

Pipe* PipeFactory::createPipe()
{
    // Oblicz zakres dla środka przerwy
    // Minimum: 40px od górnej krawędzi + połowa przerwy
    // Maximum: (screenHeight - groundHeight) - 40px od ziemi - połowa przerwy
    int minGapCenter = 60 + gapHeight / 2;
    int maxGapCenter = (screenHeight - groundHeight) - 60 - gapHeight / 2;

    // Losujemy pozycję środka przerwy
    int range = maxGapCenter - minGapCenter;
    int gapCenter = minGapCenter + (range > 0 ? rand() % range : 0);

    // Próbujemy stworzyć rurę - obsługa wyjątku z Pipe::Pipe()
    try {
        Pipe* pipe = new Pipe(
            static_cast<float>(screenWidth + 10), // zacznij za prawym brzegiem
            gapCenter,
            gapHeight,
            screenHeight
        );
        pipe->setSpeed(pipeSpeed);
        return pipe;
    }
    catch (const std::invalid_argument& e) {
        // Parametry były złe - użyj bezpiecznych wartości domyślnych
        // (to nie powinno się zdarzać przy poprawnie obliczonym zakresie)
        Pipe* safePipe = new Pipe(
            static_cast<float>(screenWidth + 10),
            screenHeight / 2,
            170,
            screenHeight
        );
        safePipe->setSpeed(pipeSpeed);
        return safePipe;
    }
    catch (const std::out_of_range& e) {
        // j.w. - fallback do środka ekranu
        Pipe* safePipe = new Pipe(
            static_cast<float>(screenWidth + 10),
            screenHeight / 2,
            170,
            screenHeight
        );
        safePipe->setSpeed(pipeSpeed);
        return safePipe;
    }
}

void PipeFactory::setDifficulty(int level)
{
    // Ogranicz poziom do zakresu 1-5
    if (level < 1) level = 1;
    if (level > 5) level = 5;

    // Im wyższy poziom, tym mniejsza przerwa i szybsze rury
    gapHeight  = 165 - (level - 1) * 15; // 165, 150, 135, 120, 105
    pipeSpeed  = 3.0f + (level - 1) * 0.5f; // 3.0, 3.5, 4.0, 4.5, 5.0

    if (gapHeight < 100) gapHeight = 100; // bezpieczne minimum
}
