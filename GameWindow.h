#ifndef GAMEWINDOW_H
#define GAMEWINDOW_H

#include <QWidget>
#include <QTimer>
#include <QKeyEvent>
#include <QMouseEvent>
#include <vector>

#include "Bird.h"
#include "Pipe.h"
#include "Ground.h"
#include "PipeFactory.h"

// Możliwe stany gry
enum class GameState {
    START,    // ekran startowy (przed grą)
    PLAYING,  // gra trwa
    GAMEOVER  // ptak zginął
};


// Główne okno gry - dziedziczy po QWidget.
// Odpowiada za:
//   - pętle gry (via QTimer)
//   - rysowanie wszystkich obiektów (paintEvent)
//   - obsługę wejścia gracza (klawiatura / mysz)
//   - zarządzanie stanem gry i wynikiem

class GameWindow : public QWidget {
    Q_OBJECT  // makro Qt wymagane dla systemu sygnałów/slotów

public:
    // Konstruktor
    explicit GameWindow(QWidget* parent = nullptr);

    // Destruktor - zwalnia pamięć obiektów gry
    ~GameWindow() override;

    // Stałe rozmiaru ekranu gry
    static const int SCREEN_WIDTH  = 480;
    static const int SCREEN_HEIGHT = 640;
    static const int GROUND_HEIGHT = 80;

protected:
    // Nadpisane metody QWidget
    void paintEvent(QPaintEvent* event) override;
    void keyPressEvent(QKeyEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;

private slots:
    // Slot połączony z QTimer - wywoływany ~60 razy na sekundę
    void gameLoop();

private:
    // Pomocnicze metody gry
    void startGame();
    void resetGame();
    void checkCollisions();
    void updateScore();

    // Pomocnicze metody rysowania
    void drawBackground(QPainter& painter);
    void drawUI(QPainter& painter);
    void drawStartScreen(QPainter& painter);
    void drawGameOverScreen(QPainter& painter);

    // === Obiekty gry (surowe wskaźniki - ręczna zarządza pamięcią) ===
    Bird*        bird;
    Ground*      ground;
    PipeFactory* pipeFactory;
    std::vector<Pipe*> pipes;

    // Timer pętli gry
    QTimer* gameTimer;

    // Licznik klatek (do sterowania spawnem rur)
    int frameCount;
    int pipeSpawnEvery; // co ile klatek pojawia się nowa rura

    // Wynik bieżący i najlepszy
    int score;
    int bestScore;

    // Aktualny stan gry
    GameState gameState;
};

#endif // GAMEWINDOW_H
