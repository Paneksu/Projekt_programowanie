#include <QApplication>
#include "GameWindow.h"


// Punkt wejścia programu.
// Tworzymy QApplication (wymagane przez Qt do wszystkiego),
// potem główne okno gry i wchodzimy w pętlę zdarzeń Qt.

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    GameWindow window;
    window.show();

    // app.exec() uruchamia pętlę zdarzeń Qt - program działa tutaj
    // dopóki okno nie zostanie zamknięte
    return app.exec();
}
