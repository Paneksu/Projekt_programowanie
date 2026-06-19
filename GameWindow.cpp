#include "GameWindow.h"

#include <QPainter>
#include <QFont>
#include <QRect>

// Konstruktor głównego okna gry

GameWindow::GameWindow(QWidget* parent)
    : QWidget(parent),
      bird(nullptr),
      ground(nullptr),
      pipeFactory(nullptr),
      gameTimer(nullptr),
      frameCount(0),
      pipeSpawnEvery(88),
      score(0),
      bestScore(0),
      gameState(GameState::START)
{
    // Ustaw stały rozmiar okna gry
    setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT);
    setWindowTitle("Flappy Bird – Projekt C++ / Qt 6");

    // Ustaw politykę focusu żeby widget odbierał zdarzenia klawiatury
    setFocusPolicy(Qt::StrongFocus);

    // Utwórz obiekty gry na stercie (heap) - ręczne zarządzanie pamięcią
    bird        = new Bird(100.0f, static_cast<float>(SCREEN_HEIGHT / 2 - 60));
    ground      = new Ground(SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT);
    pipeFactory = new PipeFactory(SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT);

    // Utwórz timer pętli gry i połącz sygnał timeout ze slotem gameLoop.
   
    gameTimer = new QTimer(this);
    connect(gameTimer, &QTimer::timeout, this, &GameWindow::gameLoop);
    gameTimer->start(16); // ~62.5 FPS (16ms na klatkę)
}

// ============================================================
// Destruktor - MUSIMY ręcznie zwolnić wszystką pamięć
// ============================================================
GameWindow::~GameWindow()
{
    delete bird;
    delete ground;
    delete pipeFactory;

    // Usuń wszystkie rury z wektora
    for (Pipe* pipe : pipes) {
        delete pipe;
    }
    pipes.clear();

}

// ============================================================
// paintEvent - rysuje całą klatkę gry
// Wywoływane przez Qt po każdym wywołaniu update()
// ============================================================
void GameWindow::paintEvent(QPaintEvent* /*event*/)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // 1. Tło (niebo, chmury)
    drawBackground(painter);

    // 2. Rury (rysuj przed ptakiem żeby ptak był "przed" rurami)
    for (Pipe* pipe : pipes) {
        if (pipe != nullptr) {
            pipe->draw(painter);
        }
    }

    // 3. Ziemia (rysuj nad rurami - przykrywa dolne końce rur)
    ground->draw(painter);

    // 4. Ptak (na wierzchu)
    bird->draw(painter);

    // 5. UI (wynik)
    drawUI(painter);

    // 6. Nakładki stanu gry
    if (gameState == GameState::START) {
        drawStartScreen(painter);
    } else if (gameState == GameState::GAMEOVER) {
        drawGameOverScreen(painter);
    }
}

// ============================================================
// Obsługa klawiatury
// ============================================================
void GameWindow::keyPressEvent(QKeyEvent* event)
{
    if (event->key() == Qt::Key_Space || event->key() == Qt::Key_Up) {
        switch (gameState) {
            case GameState::START:
                startGame();
                break;
            case GameState::PLAYING:
                bird->jump();
                break;
            case GameState::GAMEOVER:
                resetGame();
                break;
        }
    }

    // Escape - zamknij okno
    if (event->key() == Qt::Key_Escape) {
        close();
    }
}

// ============================================================
// Obsługa kliknięcia myszą / dotyku
// ============================================================
void GameWindow::mousePressEvent(QMouseEvent* event)
{
    if (event->button() == Qt::LeftButton) {
        switch (gameState) {
            case GameState::START:
                startGame();
                break;
            case GameState::PLAYING:
                bird->jump();
                break;
            case GameState::GAMEOVER:
                resetGame();
                break;
        }
    }
}

// ============================================================
// PĘTLA GRY - wywoływana przez QTimer co ~16ms
// ============================================================
void GameWindow::gameLoop()
{
    // W stanach START i GAMEOVER nie aktualizujemy obiektów gry,
    // ale odświeżamy widok (żeby ekran nie był statyczny)
    if (gameState != GameState::PLAYING) {
        update();
        return;
    }

    frameCount++;

    // --- Aktualizuj ptaka ---
    bird->update();

    // --- Spawn nowych rur co pipeSpawnEvery klatek ---
    if (frameCount % pipeSpawnEvery == 0) {
        try {
            Pipe* newPipe = pipeFactory->createPipe();
            pipes.push_back(newPipe);
        }
        catch (const std::exception& e) {
            // Nie powinno się zdarzać - PipeFactory ma własny fallback.
            // Gdyby jednak - gra gra dalej bez tej jednej rury.
        }
    }

    // --- Aktualizuj rury i usuń te, które wyszły za ekran ---
    for (int i = static_cast<int>(pipes.size()) - 1; i >= 0; --i) {
        pipes[i]->update();

        if (pipes[i]->isOffScreen()) {
            delete pipes[i];
            pipes.erase(pipes.begin() + i);
        }
    }

    // --- Sprawdź kolizje ---
    checkCollisions();

    // --- Aktualizuj wynik ---
    if (gameState == GameState::PLAYING) {
        updateScore();
    }

    // --- Odśwież widok (wywołuje paintEvent) ---
    update();
}

// ============================================================
// Rozpocznij grę
// ============================================================
void GameWindow::startGame()
{
    gameState    = GameState::PLAYING;
    frameCount   = 0;
    score        = 0;

    bird->reset();
    bird->jump(); // od razu daj impuls do góry żeby gracz widział ruch

    // Wyczyść poprzednie rury (na wypadek gdyby były z poprzedniej rozgrywki)
    for (Pipe* p : pipes) delete p;
    pipes.clear();
}

// ============================================================
// Reset do ekranu startowego
// ============================================================
void GameWindow::resetGame()
{
    for (Pipe* p : pipes) delete p;
    pipes.clear();

    bird->reset();
    frameCount   = 0;
    score        = 0;
    gameState    = GameState::START;
}

// ============================================================
// Detekcja kolizji
// ============================================================
void GameWindow::checkCollisions()
{
    QRect birdRect = bird->getCollisionRect();

    // Kolizja z ziemią
    if (birdRect.intersects(ground->getCollisionRect())) {
        gameState = GameState::GAMEOVER;
        if (score > bestScore) bestScore = score;
        return;
    }

    // Kolizja z górną krawędzią ekranu
    if (bird->getY() < -bird->getHeight()) {
        gameState = GameState::GAMEOVER;
        if (score > bestScore) bestScore = score;
        return;
    }

    // Kolizja z rurami
    for (Pipe* pipe : pipes) {
        if (pipe == nullptr) continue;

        if (birdRect.intersects(pipe->getTopRect()) ||
            birdRect.intersects(pipe->getBottomRect())) {
            gameState = GameState::GAMEOVER;
            if (score > bestScore) bestScore = score;
            return;
        }
    }
}

// ============================================================
// Aktualizacja wyniku
// ============================================================
void GameWindow::updateScore()
{
    float birdCenterX = bird->getX() + bird->getWidth() / 2.0f;

    for (Pipe* pipe : pipes) {
        if (pipe == nullptr || pipe->isPassed()) continue;

        // Środek ptaka przekroczył środek rury - zdobyto punkt
        float pipeCenterX = pipe->getX() + Pipe::PIPE_WIDTH / 2.0f;

        if (birdCenterX > pipeCenterX) {
            pipe->setPassed(true); // oznacz rurę - BEZ tej flagi liczylibyśmy punkt
            score++;               // co klatkę (błąd #4 z dziennika)
        }
    }
}

// ============================================================
// Rysowanie tła (gradient nieba + chmury)
// ============================================================
void GameWindow::drawBackground(QPainter& painter)
{
    painter.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, QColor(135, 206, 235));
}

// ============================================================
// Rysowanie UI - wynik na górze ekranu
// ============================================================
void GameWindow::drawUI(QPainter& painter)
{
    if (gameState == GameState::PLAYING || gameState == GameState::GAMEOVER) {
        QFont scoreFont("Arial", 38, QFont::Bold);
        painter.setFont(scoreFont);

        QString scoreStr = QString::number(score);
        QRect   scoreArea(0, 8, SCREEN_WIDTH, 55);

        // Cień (rysujemy jako pierwsze, nieco przesunięty)
        painter.setPen(QColor(0, 0, 0, 160));
        painter.drawText(scoreArea.adjusted(2, 2, 2, 2), Qt::AlignHCenter | Qt::AlignTop, scoreStr);

        // Główny tekst (biały)
        painter.setPen(Qt::white);
        painter.drawText(scoreArea, Qt::AlignHCenter | Qt::AlignTop, scoreStr);
    }
}

// ============================================================
// Ekran startowy
// ============================================================
void GameWindow::drawStartScreen(QPainter& painter)
{
    // Lekko przyciemnij tło
    painter.fillRect(rect(), QColor(0, 0, 0, 90));

    // Tytuł
    painter.setPen(Qt::white);
    QFont titleFont("Arial", 42, QFont::Bold);
    painter.setFont(titleFont);
    painter.drawText(QRect(0, 150, SCREEN_WIDTH, 70),
                     Qt::AlignCenter, "Flappy Bird");

    // Instrukcja
    QFont instrFont("Arial", 15);
    painter.setFont(instrFont);
    painter.setPen(Qt::white);
    painter.drawText(QRect(0, 330, SCREEN_WIDTH, 80),
                     Qt::AlignCenter, "Naciśnij SPACJĘ lub kliknij\naby rozpocząć");

    // Najlepszy wynik (jeśli jest)
    if (bestScore > 0) {
        QFont bestFont("Arial", 13);
        painter.setFont(bestFont);
        painter.setPen(QColor(255, 220, 100));
        painter.drawText(QRect(0, 430, SCREEN_WIDTH, 35),
                         Qt::AlignCenter,
                         QString("Najlepszy wynik: %1").arg(bestScore));
    }

    // Autorzy
    QFont authFont("Arial", 10);
    painter.setFont(authFont);
    painter.setPen(QColor(200, 200, 200, 180));
    painter.drawText(QRect(0, SCREEN_HEIGHT - GROUND_HEIGHT - 55, SCREEN_WIDTH, 45),
                     Qt::AlignCenter,
                     "Olaf Rysiewicz | Dawid Skatuła | Szymon Panek\nProjekt – Programowanie II, Politechnika Śląska 2026");
}

// ============================================================
// Ekran końca gry
// ============================================================
void GameWindow::drawGameOverScreen(QPainter& painter)
{
    // Przyciemnij tło
    painter.fillRect(rect(), QColor(0, 0, 0, 140));

    // Napis "KONIEC GRY"
    painter.setPen(QColor(255, 70, 70));
    QFont overFont("Arial", 44, QFont::Bold);
    painter.setFont(overFont);
    painter.drawText(QRect(0, 130, SCREEN_WIDTH, 70),
                     Qt::AlignCenter, "KONIEC GRY");

    // Ramka z wynikami
    QRect scoreBox(SCREEN_WIDTH / 2 - 140, 225, 280, 110);
    painter.setBrush(QColor(0, 0, 0, 120));
    painter.setPen(QColor(255, 255, 255, 80));
    painter.drawRoundedRect(scoreBox, 12, 12);

    // Wyniki w ramce
    painter.setPen(Qt::white);
    QFont scFont("Arial", 20, QFont::Bold);
    painter.setFont(scFont);
    painter.drawText(QRect(0, 235, SCREEN_WIDTH, 40),
                     Qt::AlignCenter,
                     QString("Wynik: %1").arg(score));
    painter.setPen(QColor(255, 220, 80));
    painter.drawText(QRect(0, 280, SCREEN_WIDTH, 40),
                     Qt::AlignCenter,
                     QString("Rekord: %1").arg(bestScore));

    // Instrukcja restartu
    painter.setPen(QColor(180, 255, 180));
    QFont restFont("Arial", 15);
    painter.setFont(restFont);
    painter.drawText(QRect(0, 365, SCREEN_WIDTH, 55),
                     Qt::AlignCenter,
                     "Naciśnij SPACJĘ lub kliknij\naby zagrać ponownie");
}
