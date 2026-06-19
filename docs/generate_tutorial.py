"""
Generuje PDF z kompletnym tutorialem projektu Flappy Bird.
Wymaga: fpdf2 (pip install fpdf2)
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


class Doc(FPDF):
    def __init__(self, title, margin=18):
        super().__init__()
        self.doc_title = title
        _f = r"C:\Windows\Fonts"
        self.add_font("Ar",  "",   _f + r"\arial.ttf")
        self.add_font("Ar",  "B",  _f + r"\arialbd.ttf")
        self.add_font("Ar",  "I",  _f + r"\ariali.ttf")
        self.add_font("Ar",  "BI", _f + r"\arialbi.ttf")
        self.add_font("Co",  "",   _f + r"\cour.ttf")
        self.add_font("Co",  "B",  _f + r"\courbd.ttf")
        self.set_margins(margin, margin, margin)
        self.set_auto_page_break(True, margin=margin)
        self.add_page()

    def header(self):
        pass

    def footer(self):
        self.set_y(-13)
        self.set_font("Ar", "", 8)
        self.cell(0, 8, f"Strona {self.page_no()}", align="C")

    def h1(self, text):
        self.ln(4)
        self.set_font("Ar", "B", 17)
        self.multi_cell(0, 9, text)
        self.set_draw_color(60, 80, 160)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.ln(4)

    def h2(self, text):
        self.ln(4)
        self.set_font("Ar", "B", 13)
        self.set_text_color(30, 60, 140)
        self.multi_cell(0, 8, text)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def h3(self, text):
        self.ln(3)
        self.set_font("Ar", "B", 11)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body(self, text, size=10):
        self.set_font("Ar", "", size)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def note(self, text):
        """Niebieskie pole z objaśnieniem."""
        self.set_fill_color(230, 235, 255)
        self.set_draw_color(100, 120, 200)
        self.set_font("Ar", "I", 9)
        self.multi_cell(0, 5.5, text, fill=True, border=1)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(0, 0, 0)
        self.set_font("Ar", "", 10)
        self.ln(2)

    def bullet(self, text, size=10):
        self.set_font("Ar", "", size)
        x0 = self.get_x()
        self.set_x(x0 + 4)
        self.multi_cell(0, 6, "* " + text)
        self.set_x(x0)
        self.ln(0.5)

    def bold_label(self, label, value, size=10):
        self.set_font("Ar", "B", size)
        self.write(6, label + " ")
        self.set_font("Ar", "", size)
        self.write(6, value)
        self.ln(6)

    def code(self, text):
        self.set_fill_color(242, 242, 242)
        self.set_draw_color(180, 180, 180)
        self.set_font("Co", "", 7.5)
        self.multi_cell(0, 4.8, text, fill=True, border=1)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(0, 0, 0)
        self.set_font("Ar", "", 10)
        self.ln(2)

    def table_row(self, cols, widths, bold=False, font_size=9):
        style = "B" if bold else ""
        self.set_font("Ar", style, font_size)
        line_h = 4.5
        pad = 1.5
        # Oblicz wysokosc wiersza
        row_h = line_h + 2 * pad
        for text, w in zip(cols, widths):
            with self.offset_rendering() as rec:
                y0 = rec.get_y()
                rec.multi_cell(w - 2 * pad, line_h, text, border=0)
                content_h = rec.get_y() - y0
            row_h = max(row_h, content_h + 2 * pad)
        if self.get_y() + row_h > self.page_break_trigger:
            self.add_page()
        x0 = self.get_x()
        y0 = self.get_y()
        x = x0
        for text, w in zip(cols, widths):
            self.rect(x, y0, w, row_h)
            self.set_xy(x + pad, y0 + pad)
            self.multi_cell(w - 2 * pad, line_h, text, border=0)
            x += w
        self.set_xy(x0, y0 + row_h)

    def hr(self):
        self.ln(2)
        self.set_draw_color(180, 180, 180)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_draw_color(0, 0, 0)
        self.ln(3)

    def _row_height(self, cols, widths, line_h, pad):
        row_h = line_h + 2 * pad
        for text, w in zip(cols, widths):
            with self.offset_rendering() as rec:
                y0 = rec.get_y()
                rec.multi_cell(w - 2 * pad, line_h, text, border=0)
                content_h = rec.get_y() - y0
            row_h = max(row_h, content_h + 2 * pad)
        return row_h


# ============================================================
def make_tutorial():
    pdf = Doc("Tutorial - FlappyBird C++/Qt6")

    # -------------------------------------------------------
    # STRONA TYTULOWA
    # -------------------------------------------------------
    pdf.set_fill_color(30, 60, 140)
    pdf.rect(0, 0, 210, 80, "F")
    pdf.set_font("Ar", "B", 26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 20)
    pdf.cell(210, 16, "FLAPPY BIRD  -  TUTORIAL", align="C")
    pdf.set_font("Ar", "", 13)
    pdf.set_xy(0, 42)
    pdf.cell(210, 8, "Kompletny przewodnik po projekcie C++ / Qt 6", align="C")
    pdf.set_font("Ar", "I", 10)
    pdf.set_xy(0, 56)
    pdf.cell(210, 7, "Od zera do egzaminu - kazda linijka kodu wyjasnicona", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(18, 90)

    pdf.set_font("Ar", "", 10)
    pdf.bold_label("Projekt:", "Gra 2D Flappy Bird w C++/Qt 6")
    pdf.bold_label("Przedmiot:", "Programowanie II - C++ obiektowy")
    pdf.bold_label("Uczelnia:", "Politechnika Slaska")
    pdf.bold_label("Autorzy:", "Olaf Rysiewicz, Dawid Skatula, Szymon Panek")
    pdf.bold_label("Data:", "19.06.2026")

    pdf.ln(6)
    pdf.set_font("Ar", "B", 11)
    pdf.cell(0, 7, "SPIS TRESCI", align="L")
    pdf.ln(8)

    toc = [
        ("1.", "Co to jest Qt 6 i jak dziala?"),
        ("2.", "Struktura plikow projektu"),
        ("3.", "CMakeLists.txt - jak projekt sie buduje"),
        ("4.", "main.cpp - punkt startowy programu"),
        ("5.", "GameObject - baza dla wszystkich obiektow"),
        ("6.", "Bird - ptak i fizyka grawitacji"),
        ("7.", "Pipe - rury i kolizje"),
        ("8.", "Ground - podloga"),
        ("9.", "PipeFactory - fabryka rur"),
        ("10.", "GameWindow - serce calej gry"),
        ("11.", "Petla gry i jak Qt ja napedza"),
        ("12.", "Rysowanie - QPainter od zera"),
        ("13.", "Obsluga wejscia - klawiatura i mysz"),
        ("14.", "Detekcja kolizji"),
        ("15.", "System punktacji"),
        ("16.", "Wzorce projektowe - OOP w praktyce"),
        ("17.", "Zarzadzanie pamiecia - new i delete"),
        ("18.", "Pytania egzaminacyjne i odpowiedzi"),
    ]
    for num, title in toc:
        pdf.set_font("Ar", "B", 10)
        pdf.write(6, f"  {num} ")
        pdf.set_font("Ar", "", 10)
        pdf.write(6, title)
        pdf.ln(6)

    # -------------------------------------------------------
    # SEKCJA 1 - Qt 6
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("1. Co to jest Qt 6 i jak dziala?")
    pdf.body(
        "Qt (czytaj: 'kjut') to ogromna kolekcja gotowych narzedzi do budowania aplikacji "
        "w C++. Zamiast pisac wszystko od zera - obsluge okien, rysowanie pikseli, timery, "
        "zdarzenia myszy - uzywasz gotowych klas Qt."
    )
    pdf.h3("Co Qt daje temu projektowi")
    items = [
        "QWidget       - okno z ekranem, po ktorym mozna rysowac",
        "QPainter      - narzedzie do rysowania ksztaltow i tekstu",
        "QTimer        - licznik czasu wywolujacy funkcje co 16 ms (petla gry)",
        "QKeyEvent     - zdarzenia klawiatury",
        "QMouseEvent   - zdarzenia myszy",
        "QRect         - prostokat do detekcji kolizji",
        "QString       - string Qt (obsluguje Unicode)",
    ]
    for i in items:
        pdf.bullet(i)

    pdf.h3("Q_OBJECT i sygnaly/sloty")
    pdf.body(
        "Qt uzywa specjalnego systemu komunikacji zwanego sygnalami i slotami. "
        "To Qt-owy odpowiednik 'zdarzen' (events). "
        "Kiedy timer 'odtyknie', wysyla sygnal timeout(). "
        "Nasz slot gameLoop() jest podlaczony do tego sygnalu i reaguje na nie."
    )
    pdf.code(
        "// Kiedy timer 'odtyknie' (sygnal timeout), wywoluje gameLoop (slot)\n"
        "connect(gameTimer, &QTimer::timeout, this, &GameWindow::gameLoop);"
    )
    pdf.body(
        "Zeby klasa mogla uzywac sygnalow i slotow, musi miec w naglowku makro Q_OBJECT:"
    )
    pdf.code(
        "class GameWindow : public QWidget {\n"
        "    Q_OBJECT   // to makro Qt - aktywuje caly system sygnalow/slotow\n"
        "    ..."
    )
    pdf.note(
        "Q_OBJECT to makro - specjalny skrot, ktory Qt zamienia w dlugi kod podczas kompilacji "
        "(Meta-Object Compiler = moc). Bez niego connect() nie zadziala."
    )

    pdf.h3("Uklad wspolrzednych w Qt")
    pdf.body(
        "WAZNE: W grafice komputerowej os Y jest ODWROCONA wzgledem matematyki. "
        "y=0 to GORA ekranu, y=640 to DOL ekranu. x=0 to lewa krawedz, x=480 to prawa."
    )
    pdf.code(
        "(0,0) --------------------------------- (480,0)\n"
        "  |     x rosnie w PRAWO -->              |\n"
        "  |     y rosnie w DOL                    |\n"
        "  |          (standardowe w grafice!)     |\n"
        "(0,640) ------------------------------- (480,640)"
    )

    # -------------------------------------------------------
    # SEKCJA 2 - struktura plikow
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("2. Struktura plikow projektu")
    pdf.code(
        "FlappyBird/\n"
        "+-- CMakeLists.txt       <- przepis budowania (co kompilowac, jakie biblioteki)\n"
        "+-- main.cpp             <- punkt startowy, funkcja main()\n"
        "|\n"
        "+-- GameObject.h/.cpp    <- klasa bazowa dla WSZYSTKICH obiektow gry\n"
        "+-- Bird.h/.cpp          <- ptak (gracz) - fizyka, rysowanie\n"
        "+-- Pipe.h/.cpp          <- rury (przeszkody) - ruch, kolizje\n"
        "+-- Ground.h/.cpp        <- podloga - kolizja, rysowanie\n"
        "+-- PipeFactory.h/.cpp   <- fabryka rur - tworzy losowe rury\n"
        "+-- GameWindow.h/.cpp    <- glowne okno - petla gry, ekrany, wejscie\n"
        "|\n"
        "+-- docs/\n"
        "    +-- generate_pdfs.py     <- dokumentacja projektu\n"
        "    +-- generate_tutorial.py <- ten tutorial"
    )

    pdf.h3("Zasada: kazda klasa ma dwa pliki")
    pdf.table_row(["Plik", "Zawartosci", "Po co?"], [40, 80, 54], bold=True)
    pdf.table_row([".h (header)", "deklaracja klasy - co potrafi, jakie ma pola",
                   "inne pliki moga #include ten naglowek"], [40, 80, 54])
    pdf.table_row([".cpp (implementacja)", "cialo funkcji - jak to dziala, kod metod",
                   "kompilator tu szuka kodu"], [40, 80, 54])

    pdf.ln(3)
    pdf.note(
        "Rozdzielenie .h i .cpp to konwencja C++. Plik .h mowi 'co istnieje', "
        ".cpp mowi 'jak dziala'. Dzieki temu mozna uzyc klasy bez znajomosci implementacji."
    )

    # -------------------------------------------------------
    # SEKCJA 3 - CMakeLists
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("3. CMakeLists.txt - jak projekt sie buduje")
    pdf.body(
        "CMakeLists.txt to przepis, ktory mowi kompilatorowi co robic. "
        "CMake sam nie kompiluje kodu - organizuje kompilacje."
    )

    pdf.h3("Linia po linii")
    pdf.code("cmake_minimum_required(VERSION 3.16)")
    pdf.body("Qt 6 wymaga CMake w wersji co najmniej 3.16.")

    pdf.code("project(FlappyBird VERSION 1.0 LANGUAGES CXX)")
    pdf.body("Nazwa projektu: FlappyBird. Wersja: 1.0. Jezyk: CXX = C++.")

    pdf.code(
        "set(CMAKE_CXX_STANDARD 17)\n"
        "set(CMAKE_CXX_STANDARD_REQUIRED ON)"
    )
    pdf.body(
        "Uzywamy C++17 - wersji C++ z 2017 roku. REQUIRED ON = jesli kompilator "
        "nie obsluguje C++17, kompilacja sie nie uda."
    )

    pdf.code("find_package(Qt6 REQUIRED COMPONENTS Core Widgets)")
    pdf.body("Szukaj biblioteki Qt6 na komputerze. Potrzebujemy dwoch komponentow:")
    pdf.bullet("Core   - podstawy (QString, QTimer, sygnaly/sloty)")
    pdf.bullet("Widgets - okna i grafika (QWidget, QPainter, QKeyEvent)")

    pdf.code("qt_standard_project_setup()")
    pdf.body("Standardowe ustawienia Qt - m.in. uruchomienie narzedzia moc dla makr Q_OBJECT.")

    pdf.code(
        "qt_add_executable(FlappyBird\n"
        "    main.cpp\n"
        "    GameObject.h  GameObject.cpp\n"
        "    Bird.h        Bird.cpp\n"
        "    Pipe.h        Pipe.cpp\n"
        "    Ground.h      Ground.cpp\n"
        "    PipeFactory.h PipeFactory.cpp\n"
        "    GameWindow.h  GameWindow.cpp\n"
        ")"
    )
    pdf.body("Lista WSZYSTKICH plikow, ktore tworza program FlappyBird.exe.")

    pdf.code(
        "target_link_libraries(FlappyBird PRIVATE\n"
        "    Qt6::Core\n"
        "    Qt6::Widgets\n"
        ")"
    )
    pdf.body("Zlinkuj (polacz) nasz program z bibliotekami Qt. Bez tego kompilator nie znajdzie klas Qt.")

    pdf.code(
        "set_target_properties(FlappyBird PROPERTIES\n"
        "    WIN32_EXECUTABLE TRUE\n"
        ")"
    )
    pdf.body("Na Windowsie nie otwieraj czarnego okna konsoli - tylko okno graficzne.")

    # -------------------------------------------------------
    # SEKCJA 4 - main.cpp
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("4. main.cpp - punkt startowy programu")
    pdf.body(
        "main.cpp to najkrotszy plik, ale od niego wszystko sie zaczyna. "
        "Kazdy program C++ startuje od funkcji main()."
    )
    pdf.code(
        "#include <QApplication>\n"
        "#include \"GameWindow.h\"\n"
        "\n"
        "int main(int argc, char* argv[])\n"
        "{\n"
        "    QApplication app(argc, argv);\n"
        "    GameWindow window;\n"
        "    window.show();\n"
        "    return app.exec();\n"
        "}"
    )

    pdf.h3("Linia po linii")
    pdf.bold_label("#include <QApplication>", "- nawias ostry = plik z biblioteki Qt")
    pdf.bold_label("#include \"GameWindow.h\"", "- cudzyslowy = nasz wlasny plik")

    pdf.ln(2)
    pdf.set_font("Ar", "B", 10)
    pdf.write(6, "QApplication app(argc, argv);")
    pdf.ln(6)
    pdf.body(
        "QApplication to SERCE kazdej aplikacji Qt. Inicjalizuje cale Qt - "
        "rejestruje aplikacje w systemie operacyjnym, ustawia obsluge zdarzen, "
        "zarzadza okienkami. Bez tego zadne okno sie nie otworzy. "
        "Przekazujemy argc i argv bo Qt moze odczytywac wlasne argumenty (np. -style)."
    )

    pdf.set_font("Ar", "B", 10)
    pdf.write(6, "GameWindow window;")
    pdf.ln(6)
    pdf.body(
        "Tworzymy obiekt GameWindow - nasze glowne okno gry. W tym momencie "
        "uruchamia sie konstruktor GameWindow::GameWindow(), ktory tworzy ptaka, "
        "podloge, fabryke rur i timer."
    )

    pdf.set_font("Ar", "B", 10)
    pdf.write(6, "window.show();")
    pdf.ln(6)
    pdf.body("Wyswietl okno. Domyslnie okna Qt sa ukryte - trzeba je pokazac.")

    pdf.set_font("Ar", "B", 10)
    pdf.write(6, "return app.exec();")
    pdf.ln(6)
    pdf.body(
        "To jest PETLA ZDARZEN Qt - program tu 'wisi' i czeka na zdarzenia "
        "(klawisze, klikniecia, uplyw czasu timera). Gdy uzytkownik zamknie okno, "
        "exec() zwraca 0 i program sie konczy."
    )
    pdf.note(
        "Bez app.exec() program natychmiast by sie zamknal po wyswietleniu okna! "
        "exec() utrzymuje program przy zyciu czekajac na zdarzenia."
    )

    # -------------------------------------------------------
    # SEKCJA 5 - GameObject
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("5. GameObject - baza dla wszystkich obiektow")

    pdf.h2("5.1 GameObject.h - deklaracja klasy")
    pdf.code(
        "#ifndef GAMEOBJECT_H\n"
        "#define GAMEOBJECT_H\n"
        "#include <QPainter>\n"
        "\n"
        "class GameObject {\n"
        "public:\n"
        "    GameObject();\n"
        "    GameObject(float x, float y, int width, int height);\n"
        "    virtual ~GameObject();\n"
        "\n"
        "    virtual void draw(QPainter& painter) = 0;  // czysto wirtualna!\n"
        "    virtual void update() = 0;                 // czysto wirtualna!\n"
        "\n"
        "    float getX()     const { return x;      }\n"
        "    float getY()     const { return y;      }\n"
        "    int getWidth()   const { return width;  }\n"
        "    int getHeight()  const { return height; }\n"
        "\n"
        "    void setPosition(float newX, float newY);\n"
        "\n"
        "protected:\n"
        "    float x, y;\n"
        "    int   width, height;\n"
        "};\n"
        "\n"
        "#endif"
    )

    pdf.h3("#ifndef / #define / #endif  - Include Guard")
    pdf.body(
        "Zapobiega dwukrotnemu dolaczeniu tego samego naglowka. Gdyby ten plik byl "
        "dolaczony dwa razy, kompilator dostalbmy dwie definicje tej samej klasy i zglosil blad. "
        "#ifndef = 'jesli NIE zdefiniowano', #define = 'zdefiniuj', #endif = koniec warunku."
    )

    pdf.h3("virtual ~GameObject()  - wirtualny destruktor")
    pdf.body("KLUCZOWE! Wyobraz sobie:")
    pdf.code(
        "GameObject* obj = new Bird();  // wskaznik na baze, ale obiekt to Bird\n"
        "delete obj;                    // ktory destruktor sie wyola?"
    )
    pdf.body(
        "Bez 'virtual' - wywola sie destruktor GameObject, a destruktor Bird NIE zostanie "
        "wywolany => wyciek pamieci. Z 'virtual' - C++ wie, zeby wywolac wlasciwy destruktor podklasy."
    )

    pdf.h3("virtual void draw(...) = 0  - czysto wirtualna metoda")
    pdf.body("Oznaczenie '= 0' sprawia ze:")
    pdf.bullet("GameObject jest klasa ABSTRAKCYJNA - nie mozna stworzyc: new GameObject() = blad")
    pdf.bullet("Kazda klasa dziedziczaca MUSI zaimplementowac draw() i update()")
    pdf.bullet(
        "Gdy masz wskaznik GameObject*, wywolanie obj->draw() automatycznie "
        "wywoluje odpowiednia implementacje (ptaka, rury, podlogi) - to jest POLIMORFIZM"
    )

    pdf.h3("protected vs public vs private")
    pdf.table_row(["Dostep", "Opis"], [35, 135], bold=True)
    pdf.table_row(["public", "dostepne dla wszystkich - z zewnatrz i w podklasach"], [35, 135])
    pdf.table_row(["protected", "dostepne tylko w tej klasie i jej podklasach (Bird moze uzywac x, y)"], [35, 135])
    pdf.table_row(["private", "dostepne tylko w tej samej klasie"], [35, 135])

    pdf.h2("5.2 GameObject.cpp - implementacja")
    pdf.code(
        "GameObject::GameObject()\n"
        "    : x(0.0f), y(0.0f), width(0), height(0)\n"
        "{}\n"
        "\n"
        "GameObject::GameObject(float x, float y, int width, int height)\n"
        "    : x(x), y(y), width(width), height(height)\n"
        "{}\n"
        "\n"
        "GameObject::~GameObject() {}\n"
        "\n"
        "void GameObject::setPosition(float newX, float newY) {\n"
        "    x = newX;\n"
        "    y = newY;\n"
        "}"
    )
    pdf.body(
        "Lista inicjalizacyjna (: x(0.0f), y(0.0f)...) to preferowany sposob inicjalizacji pol w C++. "
        "Sa inicjalizowane ZANIM wykona sie cialo konstruktora {}. "
        "W 'x(x)' - pierwsze x to pole klasy, drugie x to parametr konstruktora."
    )

    # -------------------------------------------------------
    # SEKCJA 6 - Bird
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("6. Bird - ptak i fizyka grawitacji")

    pdf.h2("6.1 Bird.h - naglowek")
    pdf.code(
        "class Bird : public GameObject {\n"
        "public:\n"
        "    Bird();\n"
        "    Bird(float startX, float startY);\n"
        "    ~Bird() override;\n"
        "\n"
        "    void draw(QPainter& painter) override;  // override = nadpisuje metode bazowej\n"
        "    void update() override;\n"
        "\n"
        "    void jump();\n"
        "    void reset();\n"
        "    QRect getCollisionRect() const;\n"
        "\n"
        "private:\n"
        "    float velocityY;   // aktualna predkosc pionowa\n"
        "    float gravity;     // przyspieszenie grawitacyjne\n"
        "    float jumpForce;   // sila skoku (ujemna = do gory)\n"
        "    float startX, startY;  // pozycja startowa (do resetu)\n"
        "};"
    )
    pdf.body(
        "Slowo kluczowe 'override' (C++11) mowi kompilatorowi: ta metoda nadpisuje "
        "wirtualna metode z klasy bazowej. Jesli popelnisz literowke (np. Draw zamiast draw), "
        "kompilator zglosi blad. Bez override kompilator by po cichu stworzyl nowa metode."
    )

    pdf.h2("6.2 Konstruktory Bird")
    pdf.code(
        "Bird::Bird()\n"
        "    : GameObject(100.0f, 270.0f, 34, 24),\n"
        "      velocityY(0.0f),\n"
        "      gravity(0.5f),\n"
        "      jumpForce(-9.0f),\n"
        "      startX(100.0f),\n"
        "      startY(270.0f)\n"
        "{}"
    )
    pdf.body(
        "Wywoluje konstruktor klasy bazowej GameObject(100, 270, 34, 24) - "
        "ptak zaczyna na pozycji (100, 270), ma wymiary 34x24 piksele."
    )
    pdf.note(
        "Dlaczego jumpForce = -9.0f? W grafice y=0 jest na GORZE ekranu. "
        "Zeby leciec w gore, musisz ZMNIEJSZAC y, czyli predkosc musi byc UJEMNA."
    )

    pdf.h2("6.3 Fizyka grawitacji - Bird::update()")
    pdf.code(
        "void Bird::update()\n"
        "{\n"
        "    velocityY += gravity;               // predkosc rosnie o 0.5 kazda klatke\n"
        "    if (velocityY > 14.0f) velocityY = 14.0f;  // max predkosc spadania\n"
        "    y += velocityY;                     // zmien pozycje o predkosc\n"
        "}"
    )

    pdf.h3("Tabela - symulacja fizyki klatka po klatce")
    pdf.table_row(
        ["Klatka", "velocityY przed", "po += gravity", "y zmienia sie o", "Kierunek"],
        [22, 32, 30, 34, 26], bold=True, font_size=8
    )
    rows = [
        ["1 (skok)", "-9.0", "-8.5", "-8.5", "GORA"],
        ["5", "-7.0", "-6.5", "-6.5", "GORA"],
        ["10", "-4.5", "-4.0", "-4.0", "GORA"],
        ["19", "+0.5", "+1.0", "+1.0", "DOL"],
        ["28", "+5.0", "+5.5", "+5.5", "DOL"],
        ["35+", "+14.0", "+14.0", "+14.0", "DOL (max)"],
    ]
    for r in rows:
        pdf.table_row(r, [22, 32, 30, 34, 26], font_size=8)
    pdf.ln(2)
    pdf.body(
        "Ograniczenie velocityY > 14.0f to 'terminal velocity' (predkosc koncowa). "
        "Zapobiega nierealistycznie szybkiemu spadaniu."
    )

    pdf.h2("6.4 Skok - Bird::jump()")
    pdf.code(
        "void Bird::jump()\n"
        "{\n"
        "    velocityY = jumpForce;  // = -9.0f, resetuje predkosc na ujemna\n"
        "}"
    )
    pdf.body(
        "Skok nie DODAJE predkosci - USTAWIA ja na -9. Dzieki temu wielokrotne "
        "klikniecie nie pozwala leciec w nieskonczonosc."
    )

    pdf.h2("6.5 Prostokat kolizji - getCollisionRect()")
    pdf.code(
        "QRect Bird::getCollisionRect() const\n"
        "{\n"
        "    const int margin = 5;\n"
        "    return QRect(\n"
        "        static_cast<int>(x) + margin,\n"
        "        static_cast<int>(y) + margin,\n"
        "        width  - 2 * margin,\n"
        "        height - 2 * margin\n"
        "    );\n"
        "}"
    )
    pdf.body(
        "Kolizja sprawdzana jest na prostokacje MNIEJSZYM o 5 pikseli ze wszystkich stron. "
        "Dlaczego? Bo rysowanie ptaka (elipsa z dziobem) wychodzi poza prostokata. "
        "Gdybysmy uzywali pelnych wymiarow, gra bylaby niesprawiedliwa."
    )

    pdf.h2("6.6 Rysowanie ptaka - Bird::draw()")
    pdf.code(
        "void Bird::draw(QPainter& painter) {\n"
        "    int bx = static_cast<int>(x);  // float -> int dla rysowania\n"
        "    int by = static_cast<int>(y);\n"
        "\n"
        "    // Cialo (zolta elipsa)\n"
        "    painter.setBrush(QColor(255, 220, 0));\n"
        "    painter.setPen(QPen(QColor(180, 140, 0), 2));\n"
        "    painter.drawEllipse(bx, by, width, height);\n"
        "\n"
        "    // Skrzydlo (ciemniejszy oval)\n"
        "    painter.setBrush(QColor(220, 170, 0));\n"
        "    painter.setPen(Qt::NoPen);\n"
        "    painter.drawEllipse(bx + 4, by + height / 2, 14, 8);\n"
        "\n"
        "    // Oko (biale + czarna zrenica)\n"
        "    painter.setBrush(Qt::white);\n"
        "    painter.drawEllipse(bx + width/2 + 2, by + 4, 11, 11);\n"
        "    painter.setBrush(Qt::black);\n"
        "    painter.drawEllipse(bx + width/2 + 5, by + 7, 5, 5);\n"
        "\n"
        "    // Dziob (pomaranczowy trojkat - QPolygon)\n"
        "    QPolygon beak;\n"
        "    beak << QPoint(bx + width,      by + height/2 - 3)\n"
        "         << QPoint(bx + width + 10, by + height/2)\n"
        "         << QPoint(bx + width,      by + height/2 + 3);\n"
        "    painter.setBrush(QColor(255, 140, 0));\n"
        "    painter.drawPolygon(beak);\n"
        "}"
    )
    pdf.body("setBrush = kolor wypelnienia, setPen = kolor/grubosc konturu, Qt::NoPen = brak konturu.")
    pdf.body(
        "QPolygon = wielokat z punktow. Trzy punkty tworza trojkat (dziob). "
        "<< to operator Qt do dodawania punktow do wielokata."
    )

    # -------------------------------------------------------
    # SEKCJA 7 - Pipe
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("7. Pipe - rury i kolizje")

    pdf.h2("7.1 Pipe.h - stala PIPE_WIDTH")
    pdf.code("static constexpr int PIPE_WIDTH = 58;")
    pdf.body(
        "static = nalezy do klasy, nie do obiektu (jeden egzemplarz dla wszystkich rur). "
        "constexpr = wartosc znana w czasie kompilacji, nie moze sie zmienic. "
        "Dostep: Pipe::PIPE_WIDTH."
    )
    pdf.note(
        "Dlaczego static constexpr zamiast #define? Bo ma typ int i nalezy do przestrzeni "
        "nazw klasy. #define jest globalny i moze kolidowac z innymi nazwami."
    )

    pdf.h2("7.2 Konstruktor - walidacja i wyjatki")
    pdf.code(
        "Pipe::Pipe(float x, int gapCenterY, int gapHeight, int screenHeight)\n"
        "    : GameObject(x, 0.0f, PIPE_WIDTH, screenHeight), ...\n"
        "{\n"
        "    // Walidacja: minimalna przerwa\n"
        "    if (gapHeight < 90) {\n"
        "        throw std::invalid_argument(\n"
        "            \"Przerwa miedzy rurami jest za mala! Minimum to 90 pikseli.\"\n"
        "        );\n"
        "    }\n"
        "\n"
        "    // Walidacja: min odleglosc od gory\n"
        "    if (gapCenterY - gapHeight / 2 < 40) {\n"
        "        throw std::out_of_range(\n"
        "            \"Srodek przerwy jest za blisko gornej krawedzi ekranu.\"\n"
        "        );\n"
        "    }\n"
        "\n"
        "    // Walidacja: min odleglosc od dolu\n"
        "    if (gapCenterY + gapHeight / 2 > screenHeight - 100) {\n"
        "        throw std::out_of_range(\n"
        "            \"Srodek przerwy jest za blisko dolnej krawedzi ekranu.\"\n"
        "        );\n"
        "    }\n"
        "}"
    )
    pdf.body("Rura zaczyna na y=0 (gora ekranu) i ma wysokosc calego ekranu - rysuje zarowno gorna jak i dolna rure.")
    pdf.body(
        "throw rzuca wyjatek - sygnalizuje ze cos poszlo nie tak. "
        "std::invalid_argument = nieprawidlowy argument. "
        "std::out_of_range = wartosc poza dopuszczalnym zakresem."
    )

    pdf.h2("7.3 Schemat rysowania rury")
    pdf.code(
        "y=0\n"
        "  +----------+  <- gorna rura (cialo)\n"
        "  |          |\n"
        "  +----------+  <- topEnd = gapCenterY - gapHeight/2\n"
        "  +------------+  <- kapitel (szerszy o 6px z kazdej strony)\n"
        "  \n"
        "  [  przerwa  ]  <- ptak tu leci\n"
        "  \n"
        "  +------------+  <- kapitel dolnej rury\n"
        "  +----------+  <- bottomStart = gapCenterY + gapHeight/2\n"
        "  |          |\n"
        "  +----------+  <- screenHeight (y=640)\n"
        "y=640"
    )

    pdf.h2("7.4 Ruch i sprawdzenie czy poza ekranem")
    pdf.code(
        "void Pipe::update() {\n"
        "    x -= speed;  // przesuń w lewo o 'speed' pikseli (domyslnie 3.0)\n"
        "}\n"
        "\n"
        "bool Pipe::isOffScreen() const {\n"
        "    return (x + PIPE_WIDTH + 10) < 0;  // prawa krawedz za lewa krawedzia ekranu\n"
        "}"
    )

    pdf.h2("7.5 Prostokaty kolizji - dwa oddzielne")
    pdf.code(
        "QRect Pipe::getTopRect() const {\n"
        "    int topEnd = gapCenterY - gapHeight / 2;\n"
        "    return QRect(static_cast<int>(x), 0, PIPE_WIDTH, topEnd);\n"
        "}\n"
        "\n"
        "QRect Pipe::getBottomRect() const {\n"
        "    int bottomStart = gapCenterY + gapHeight / 2;\n"
        "    int bottomH = screenHeight - bottomStart;\n"
        "    return QRect(static_cast<int>(x), bottomStart, PIPE_WIDTH, bottomH);\n"
        "}"
    )
    pdf.body("Dwa oddzielne prostokaty - top od y=0 do topEnd, bottom od bottomStart do dolu ekranu.")

    # -------------------------------------------------------
    # SEKCJA 8 - Ground
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("8. Ground - podloga")

    pdf.h2("8.1 Konstruktor")
    pdf.code(
        "Ground::Ground()\n"
        "    : GameObject(0.0f, 560.0f, 480, 80),  // y=640-80=560\n"
        "      screenWidth(480)\n"
        "{}"
    )
    pdf.body(
        "Podloga zaczyna na y=560 (640 - 80 = 560), ma szerokosc 480px i wysokosc 80px. "
        "Wyrownana do dolnej krawedzi ekranu."
    )

    pdf.h2("8.2 Rysowanie")
    pdf.code(
        "void Ground::draw(QPainter& painter) {\n"
        "    int gy = static_cast<int>(y);  // y=560\n"
        "\n"
        "    painter.setBrush(QColor(80, 170, 70));   // zielona trawa\n"
        "    painter.drawRect(0, gy, screenWidth, 16);        // 16px trawa\n"
        "\n"
        "    painter.setBrush(QColor(60, 140, 50));   // ciemniejszy pasek\n"
        "    painter.drawRect(0, gy + 14, screenWidth, 4);    // 4px separator\n"
        "\n"
        "    painter.setBrush(QColor(210, 170, 110)); // piasek/ziemia\n"
        "    painter.drawRect(0, gy + 18, screenWidth, height - 18);  // reszta\n"
        "\n"
        "    painter.setBrush(QColor(180, 140, 80));  // ciemniejsza linia w ziemi\n"
        "    painter.drawRect(0, gy + 30, screenWidth, 8);\n"
        "}"
    )
    pdf.body("Podloga to 4 prostokata tworzace warstwowy efekt: trawa -> separator -> piasek -> podpowierzchniowa warstwa.")

    pdf.h2("8.3 Pusta metoda update()")
    pdf.code(
        "void Ground::update()\n"
        "{\n"
        "    // Static - no movement\n"
        "}"
    )
    pdf.body(
        "Podloga sie nie rusza - override MUSI istniec (klasa bazowa ma = 0), "
        "ale cialo jest puste. To jest legalne C++."
    )

    # -------------------------------------------------------
    # SEKCJA 9 - PipeFactory
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("9. PipeFactory - fabryka rur")

    pdf.h2("9.1 Wzorzec Factory Method")
    pdf.body(
        "PipeFactory implementuje wzorzec Factory Method. Zamiast tworzyc rury bezposrednio "
        "(new Pipe(...)) w GameWindow, delegujemy to do fabryki. Korzysci:"
    )
    pdf.bullet("Logika losowania pozycji jest w jednym miejscu")
    pdf.bullet("Mozna latwo zmienic trudnosc")
    pdf.bullet("GameWindow nie musi znac szczegolów tworzenia rur")

    pdf.h2("9.2 Konstruktor i inicjalizacja losowania")
    pdf.code(
        "PipeFactory::PipeFactory(int screenWidth, int screenHeight, int groundHeight)\n"
        "    : screenWidth(screenWidth), screenHeight(screenHeight),\n"
        "      groundHeight(groundHeight),\n"
        "      gapHeight(165),      // domyslna wysokosc przerwy\n"
        "      pipeSpeed(3.0f)      // domyslna szybkosc\n"
        "{\n"
        "    srand(static_cast<unsigned int>(time(nullptr)));\n"
        "}"
    )
    pdf.body(
        "srand(time(nullptr)) - inicjalizacja generatora liczb pseudolosowych. "
        "time(nullptr) zwraca czas w sekundach od 1970-01-01 (Unix timestamp). "
        "Dzieki temu kazde uruchomienie daje inne rury."
    )
    pdf.note(
        "Bez srand(), rand() zawsze daje ta sama sekwencje liczb - rury bylyby "
        "zawsze w tych samych miejscach!"
    )

    pdf.h2("9.3 createPipe - losowanie pozycji")
    pdf.code(
        "Pipe* PipeFactory::createPipe()\n"
        "{\n"
        "    int minGapCenter = 60 + gapHeight / 2;\n"
        "    int maxGapCenter = (screenHeight - groundHeight) - 60 - gapHeight / 2;\n"
        "\n"
        "    // Losuj srodek przerwy w bezpiecznym zakresie\n"
        "    int range = maxGapCenter - minGapCenter;\n"
        "    int gapCenter = minGapCenter + (range > 0 ? rand() % range : 0);\n"
        "\n"
        "    try {\n"
        "        Pipe* pipe = new Pipe(\n"
        "            static_cast<float>(screenWidth + 10),  // start za prawym brzegiem\n"
        "            gapCenter,\n"
        "            gapHeight,\n"
        "            screenHeight\n"
        "        );\n"
        "        pipe->setSpeed(pipeSpeed);\n"
        "        return pipe;\n"
        "    }\n"
        "    catch (const std::invalid_argument& e) {\n"
        "        // Jesli walidacja nie przeszla, stworz bezpieczna rure\n"
        "        Pipe* safePipe = new Pipe(\n"
        "            static_cast<float>(screenWidth + 10),\n"
        "            screenHeight / 2,  // srodek ekranu\n"
        "            170,               // bezpieczna przerwa\n"
        "            screenHeight\n"
        "        );\n"
        "        safePipe->setSpeed(pipeSpeed);\n"
        "        return safePipe;\n"
        "    }\n"
        "    catch (const std::out_of_range& e) {\n"
        "        // Podobnie - fallback\n"
        "        ...\n"
        "    }\n"
        "}"
    )
    pdf.body(
        "rand() % range - operator modulo. Losuje liczbe z zakresu [0, range-1]. "
        "catch lapie wyjatki rzucone przez konstruktor Pipe. "
        "Dzieki temu fabryka NIGDY nie zwraca nullptr."
    )

    pdf.h2("9.4 setDifficulty - poziomy trudnosci")
    pdf.code(
        "void PipeFactory::setDifficulty(int level)\n"
        "{\n"
        "    if (level < 1) level = 1;\n"
        "    if (level > 5) level = 5;\n"
        "\n"
        "    gapHeight = 165 - (level - 1) * 15;    // 165, 150, 135, 120, 105\n"
        "    pipeSpeed = 3.0f + (level - 1) * 0.5f; // 3.0, 3.5, 4.0, 4.5, 5.0\n"
        "\n"
        "    if (gapHeight < 100) gapHeight = 100;  // minimalny prog bezpieczenstwa\n"
        "}"
    )

    pdf.table_row(["Poziom", "Przerwa (px)", "Predkosc (px/kl.)"], [30, 45, 50], bold=True)
    for lvl, gap, spd in [("1", "165", "3.0"), ("2", "150", "3.5"),
                           ("3", "135", "4.0"), ("4", "120", "4.5"), ("5", "105", "5.0")]:
        pdf.table_row([lvl, gap, spd], [30, 45, 50])

    # -------------------------------------------------------
    # SEKCJA 10 - GameWindow
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("10. GameWindow - serce calej gry")

    pdf.h2("10.1 Stany gry - enum class GameState")
    pdf.code(
        "enum class GameState {\n"
        "    START,    // ekran startowy - gra jeszcze nie zaczeta\n"
        "    PLAYING,  // gra w toku\n"
        "    GAMEOVER  // ptak umarl\n"
        "};"
    )
    pdf.body(
        "enum class (C++11) to silnie typowany enum. Nie mozna przypadkowo porownac "
        "GameState z liczba. GameState::START nie jest rowne 0 tak po prostu - "
        "musisz byc jawny. Zamiast wielu flag (isStarted, isDead...) jeden GameState."
    )

    pdf.h2("10.2 Stale rozmiaru i pola klasy")
    pdf.code(
        "static const int SCREEN_WIDTH  = 480;\n"
        "static const int SCREEN_HEIGHT = 640;\n"
        "static const int GROUND_HEIGHT = 80;\n"
        "\n"
        "Bird*        bird;           // wskaznik na obiekt ptaka\n"
        "Ground*      ground;         // wskaznik na podloge\n"
        "PipeFactory* pipeFactory;    // wskaznik na fabryke rur\n"
        "std::vector<Pipe*> pipes;    // dynamiczna lista wskaznikow na rury\n"
        "\n"
        "QTimer* gameTimer;           // timer wywolujacy gameLoop co 16ms\n"
        "\n"
        "int frameCount;              // licznik klatek\n"
        "int pipeSpawnEvery;          // co ile klatek spawnowac rure (=88)\n"
        "int score;                   // aktualny wynik\n"
        "int bestScore;               // rekord sesji\n"
        "GameState gameState;         // aktualny stan gry"
    )

    pdf.h2("10.3 Konstruktor GameWindow")
    pdf.code(
        "GameWindow::GameWindow(QWidget* parent)\n"
        "    : QWidget(parent),\n"
        "      bird(nullptr), ground(nullptr), pipeFactory(nullptr),\n"
        "      gameTimer(nullptr),\n"
        "      frameCount(0), pipeSpawnEvery(88),\n"
        "      score(0), bestScore(0),\n"
        "      gameState(GameState::START)\n"
        "{\n"
        "    setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT); // staly rozmiar 480x640\n"
        "    setWindowTitle(\"Flappy Bird - Projekt C++ / Qt 6\");\n"
        "    setFocusPolicy(Qt::StrongFocus); // odbieraj klawisze\n"
        "\n"
        "    bird        = new Bird(100.0f, static_cast<float>(SCREEN_HEIGHT/2 - 60));\n"
        "    ground      = new Ground(SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT);\n"
        "    pipeFactory = new PipeFactory(SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT);\n"
        "\n"
        "    gameTimer = new QTimer(this);  // 'this' = rodzic; Qt usunie timer auto.\n"
        "    connect(gameTimer, &QTimer::timeout, this, &GameWindow::gameLoop);\n"
        "    gameTimer->start(16);  // co 16ms = ~62.5 FPS\n"
        "}"
    )
    pdf.body(
        "Wskazniki inicjalizowane na nullptr - dobra praktyka. "
        "new Bird/Ground/PipeFactory tworzy obiekty na STERCIE (heap) - "
        "musza zyc przez caly czas dzialania okna."
    )
    pdf.body(
        "gameTimer = new QTimer(this) - 'this' to RODZIC timera. "
        "Qt automatycznie usunie timera gdy GameWindow zostanie zniszczony."
    )

    pdf.h2("10.4 Destruktor GameWindow")
    pdf.code(
        "GameWindow::~GameWindow()\n"
        "{\n"
        "    delete bird;\n"
        "    delete ground;\n"
        "    delete pipeFactory;\n"
        "    // gameTimer - NIE delete, Qt robi to przez system rodzic-dziecko\n"
        "\n"
        "    for (Pipe* pipe : pipes) {\n"
        "        delete pipe;   // usun OBIEKT Pipe\n"
        "    }\n"
        "    pipes.clear();     // usun WSKAZNIKI z wektora\n"
        "}"
    )
    pdf.note(
        "Dlaczego dwa kroki dla rur? std::vector<Pipe*> przechowuje wskazniki (adresy). "
        "pipes.clear() usuwa adresy z wektora, ale nie usuwa obiektow Pipe pod tymi adresami. "
        "Najpierw delete pipe (usun obiekt), potem pipes.clear() (wyczysc wektor)."
    )

    # -------------------------------------------------------
    # SEKCJA 11 - Petla gry
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("11. Petla gry i jak Qt ja napedza")

    pdf.h2("11.1 Schemat przepływu")
    pdf.code(
        "QTimer (co 16ms)\n"
        "  | sygnal: timeout\n"
        "  v\n"
        "GameWindow::gameLoop()\n"
        "  +-- bird->update()           <- fizyka ptaka\n"
        "  +-- spawn rur (co 88 klatek) <- nowa rura z fabryki\n"
        "  +-- pipes[i]->update()       <- ruch rur w lewo\n"
        "  +-- usun rury za ekranem     <- delete + erase\n"
        "  +-- checkCollisions()        <- czy ptak zyje?\n"
        "  +-- updateScore()            <- punkty\n"
        "  +-- update()                 <- prosba o przerysowanie\n"
        "         |\n"
        "         v\n"
        "    paintEvent()               <- Qt wywola, rysuje klatke"
    )

    pdf.h2("11.2 Kod gameLoop()")
    pdf.code(
        "void GameWindow::gameLoop()\n"
        "{\n"
        "    if (gameState != GameState::PLAYING) {\n"
        "        update();  // odswiezaj ekran nawet na menu/game over\n"
        "        return;\n"
        "    }\n"
        "\n"
        "    frameCount++;\n"
        "\n"
        "    bird->update();\n"
        "\n"
        "    // Co 88 klatek (~1.4 sek) spawnuj nowa rure\n"
        "    if (frameCount % pipeSpawnEvery == 0) {\n"
        "        try {\n"
        "            Pipe* newPipe = pipeFactory->createPipe();\n"
        "            pipes.push_back(newPipe);\n"
        "        }\n"
        "        catch (const std::exception& e) { }\n"
        "    }\n"
        "\n"
        "    // Iteracja WSTECZNA dla bezpiecznego usuwania\n"
        "    for (int i = static_cast<int>(pipes.size()) - 1; i >= 0; --i) {\n"
        "        pipes[i]->update();\n"
        "\n"
        "        if (pipes[i]->isOffScreen()) {\n"
        "            delete pipes[i];                      // usun obiekt\n"
        "            pipes.erase(pipes.begin() + i);       // usun wskaznik z wektora\n"
        "        }\n"
        "    }\n"
        "\n"
        "    checkCollisions();\n"
        "\n"
        "    if (gameState == GameState::PLAYING) {\n"
        "        updateScore();\n"
        "    }\n"
        "\n"
        "    update();  // prosba o przerysowanie okna\n"
        "}"
    )

    pdf.h3("Dlaczego iteracja WSTECZNA gdy usuwamy rury?")
    pdf.body(
        "erase() zmienia indeksy! Jesli usuniesz element o indeksie 2, "
        "element o indeksie 3 staje sie nowym indeksem 2. "
        "Przy iteracji do przodu po usunieciu elementu pominiesz nastepny. "
        "Iterujac wstecz, usuniecie indeksu i nie wplywa na indeksy 0..i-1 "
        "ktore jeszcze nie byly sprawdzone."
    )

    pdf.h3("frameCount % pipeSpawnEvery == 0 - operator modulo")
    pdf.body(
        "% to operator reszty z dzielenia. "
        "Gdy frameCount = 88, 88 % 88 = 0 -> spawn. "
        "Gdy frameCount = 176, 176 % 88 = 0 -> spawn. "
        "Co 88 klatek przy 62.5 FPS = co ~1.4 sekundy."
    )

    pdf.h3("update() vs paintEvent()")
    pdf.body(
        "update() w Qt PROSI system o przerysowanie okna. "
        "Nie rysuje bezposrednio - Qt wywola paintEvent() asynchronicznie "
        "(gdy system jest gotowy). Nie mozna wywolac paintEvent bezposrednio."
    )

    pdf.h2("11.3 Kolejnosc rysowania w paintEvent()")
    pdf.code(
        "void GameWindow::paintEvent(QPaintEvent*)\n"
        "{\n"
        "    QPainter painter(this);\n"
        "    painter.setRenderHint(QPainter::Antialiasing);\n"
        "\n"
        "    drawBackground(painter);   // 1. tlo (niebo, chmury)\n"
        "\n"
        "    for (Pipe* pipe : pipes) { // 2. rury (za podloga i ptakiem)\n"
        "        pipe->draw(painter);\n"
        "    }\n"
        "\n"
        "    ground->draw(painter);     // 3. podloga (przykrywa dol rur)\n"
        "    bird->draw(painter);       // 4. ptak (na wierzchu)\n"
        "    drawUI(painter);           // 5. wynik (zawsze na wierzchu)\n"
        "\n"
        "    if (gameState == GameState::START)\n"
        "        drawStartScreen(painter);   // 6. nakladka menu\n"
        "    else if (gameState == GameState::GAMEOVER)\n"
        "        drawGameOverScreen(painter);\n"
        "}"
    )
    pdf.body(
        "Kolejnosc jest krytyczna - kazda nastepna warstwa rysowana jest NA poprzedniej. "
        "Antialiasing = wygładzanie krawedzi (bez 'schodkow' na elipsach i liniach)."
    )

    # -------------------------------------------------------
    # SEKCJA 12 - QPainter
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("12. Rysowanie - QPainter od zera")

    pdf.h2("12.1 Podstawowe metody QPainter")
    pdf.table_row(["Metoda", "Co robi"], [65, 109], bold=True)
    pdf.table_row(["setBrush(kolor)", "ustaw kolor wypelnienia ksztaltow"], [65, 109])
    pdf.table_row(["setPen(kolor/QPen)", "ustaw kolor i grubosc konturu"], [65, 109])
    pdf.table_row(["setPen(Qt::NoPen)", "brak konturu (same wypelnienie)"], [65, 109])
    pdf.table_row(["drawRect(x,y,w,h)", "rysuj prostokat o lewym gornym rogu (x,y)"], [65, 109])
    pdf.table_row(["drawEllipse(x,y,w,h)", "rysuj elipse wpisana w prostokat (x,y,w,h)"], [65, 109])
    pdf.table_row(["drawPolygon(QPolygon)", "rysuj wielokat z listy punktow"], [65, 109])
    pdf.table_row(["drawText(QRect, flagi, tekst)", "rysuj tekst w prostokatie z wyrownaniem"], [65, 109])
    pdf.table_row(["setFont(QFont)", "ustaw czcionke, rozmiar, styl (Bold/Italic)"], [65, 109])
    pdf.table_row(["fillRect(QRect, pedziel)", "szybkie wypelnienie prostokatu gradientem/kolorem"], [65, 109])

    pdf.h2("12.2 QColor - kolory")
    pdf.code(
        "QColor(255, 220, 0)          // RGB - zolty (ptak)\n"
        "QColor(78, 175, 65)          // zielony (rury)\n"
        "QColor(255, 255, 255, 200)   // bialy z alpha=200 (polprzezroczysta chmura)\n"
        "Qt::white                    // predefiniowany bialy\n"
        "Qt::black                    // predefiniowany czarny"
    )
    pdf.body(
        "Czwarty parametr QColor to alpha (przezroczystosc): "
        "0 = pelna przezroczystosc, 255 = pelne wypelnienie."
    )

    pdf.h2("12.3 Gradient nieba")
    pdf.code(
        "QLinearGradient skyGrad(0, 0, 0, SCREEN_HEIGHT - GROUND_HEIGHT);\n"
        "skyGrad.setColorAt(0.0, QColor(100, 180, 210));  // niebieski na gorze\n"
        "skyGrad.setColorAt(1.0, QColor(175, 225, 240));  // jasniejszy na dole\n"
        "painter.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, skyGrad);"
    )
    pdf.body(
        "QLinearGradient(x1,y1,x2,y2) - gradient liniowy od (0,0) do (0,560) (pionowy). "
        "setColorAt(0.0,...) = kolor na poczatku, setColorAt(1.0,...) = kolor na koncu."
    )

    pdf.h2("12.4 Efekt cienia tekstu (drop shadow)")
    pdf.code(
        "// Cien (przesuniety o 2px)\n"
        "painter.setPen(QColor(0, 0, 0, 160));\n"
        "painter.drawText(scoreArea.adjusted(2, 2, 2, 2), Qt::AlignHCenter, scoreStr);\n"
        "\n"
        "// Bialy tekst\n"
        "painter.setPen(Qt::white);\n"
        "painter.drawText(scoreArea, Qt::AlignHCenter, scoreStr);"
    )
    pdf.body(
        "Technika drop shadow: rysuj tekst dwa razy. "
        "Raz ciemny przesuniety o (2,2), raz bialy w normalnej pozycji. "
        "Efekt cienia bez specjalnych shaderow."
    )

    # -------------------------------------------------------
    # SEKCJA 13 - Input
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("13. Obsluga wejscia - klawiatura i mysz")

    pdf.h2("13.1 keyPressEvent")
    pdf.code(
        "void GameWindow::keyPressEvent(QKeyEvent* event)\n"
        "{\n"
        "    if (event->key() == Qt::Key_Space || event->key() == Qt::Key_Up) {\n"
        "        switch (gameState) {\n"
        "            case GameState::START:\n"
        "                startGame();\n"
        "                break;\n"
        "            case GameState::PLAYING:\n"
        "                bird->jump();\n"
        "                break;\n"
        "            case GameState::GAMEOVER:\n"
        "                resetGame();\n"
        "                break;\n"
        "        }\n"
        "    }\n"
        "\n"
        "    if (event->key() == Qt::Key_Escape) {\n"
        "        close();\n"
        "    }\n"
        "}"
    )
    pdf.body(
        "switch na gameState - ta sama akcja (spacja/strzalka gora) robi co innego "
        "zalezne od stanu gry. To implementacja AUTOMATU STANOW (State Machine)."
    )

    pdf.h2("13.2 mousePressEvent")
    pdf.code(
        "void GameWindow::mousePressEvent(QMouseEvent* event)\n"
        "{\n"
        "    if (event->button() == Qt::LeftButton) {\n"
        "        switch (gameState) {\n"
        "            // identyczny switch jak wyzej\n"
        "        }\n"
        "    }\n"
        "}"
    )
    pdf.body(
        "Identyczna logika jak klawiatura - lewy przycisk myszy robi to samo co spacja. "
        "Sprawdzamy event->button() == Qt::LeftButton zeby ignorowac prawy i srodkowy przycisk."
    )

    pdf.h2("13.3 startGame vs resetGame")
    pdf.code(
        "void GameWindow::startGame()\n"
        "{\n"
        "    gameState  = GameState::PLAYING;\n"
        "    frameCount = 0;\n"
        "    score      = 0;\n"
        "    bird->reset();\n"
        "    bird->jump();            // od razu skok zeby nie spasc\n"
        "    for (Pipe* p : pipes) delete p;\n"
        "    pipes.clear();\n"
        "}\n"
        "\n"
        "void GameWindow::resetGame()\n"
        "{\n"
        "    for (Pipe* p : pipes) delete p;\n"
        "    pipes.clear();\n"
        "    bird->reset();\n"
        "    frameCount = 0;\n"
        "    score      = 0;\n"
        "    gameState  = GameState::START;  // wróc do menu, nie PLAYING\n"
        "}"
    )
    pdf.body(
        "startGame -> stan PLAYING. resetGame -> stan START (menu). "
        "Ptak od razu skacze w startGame bo inaczej spadb zanim gracz sie zorientuje."
    )

    pdf.h2("13.4 Diagram przejsc miedzy stanami")
    pdf.code(
        "                [START]\n"
        "                   |\n"
        "            Spacja/klik (startGame)\n"
        "                   |\n"
        "                   v\n"
        "              [PLAYING] ---------> [GAMEOVER]\n"
        "                              kolizja z rura/podloga/granica\n"
        "                                       |\n"
        "                               Spacja/klik (resetGame)\n"
        "                                       |\n"
        "                                       v\n"
        "                                   [START]"
    )

    # -------------------------------------------------------
    # SEKCJA 14 - Kolizje
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("14. Detekcja kolizji")

    pdf.h2("14.1 Kod checkCollisions()")
    pdf.code(
        "void GameWindow::checkCollisions()\n"
        "{\n"
        "    QRect birdRect = bird->getCollisionRect();  // zmniejszony prostokat ptaka\n"
        "\n"
        "    // 1. Kolizja z podloga\n"
        "    if (birdRect.intersects(ground->getCollisionRect())) {\n"
        "        gameState = GameState::GAMEOVER;\n"
        "        if (score > bestScore) bestScore = score;\n"
        "        return;\n"
        "    }\n"
        "\n"
        "    // 2. Kolizja z gorna krawedzia ekranu\n"
        "    if (bird->getY() < -bird->getHeight()) {\n"
        "        gameState = GameState::GAMEOVER;\n"
        "        if (score > bestScore) bestScore = score;\n"
        "        return;\n"
        "    }\n"
        "\n"
        "    // 3. Kolizja z rurami\n"
        "    for (Pipe* pipe : pipes) {\n"
        "        if (pipe == nullptr) continue;\n"
        "\n"
        "        if (birdRect.intersects(pipe->getTopRect()) ||\n"
        "            birdRect.intersects(pipe->getBottomRect())) {\n"
        "            gameState = GameState::GAMEOVER;\n"
        "            if (score > bestScore) bestScore = score;\n"
        "            return;\n"
        "        }\n"
        "    }\n"
        "}"
    )

    pdf.h3("QRect::intersects(QRect)")
    pdf.body(
        "Zwraca true jesli prostokaty maja wspolny obszar (nakladaja sie). "
        "Jest to podstawowa technika AABB (Axis-Aligned Bounding Box) - "
        "najszybsza metoda detekcji kolizji w grach 2D."
    )
    pdf.body(
        "Kolejnosc sprawdzen nie jest przypadkowa: podloga jest sprawdzana pierwsza "
        "(najczestszy przypadek), potem granica, potem rury."
    )
    pdf.body(
        "return po znalezieniu kolizji - nie sprawdzamy dalej. "
        "Wystarczy jedna kolizja zeby gra sie skonczyla. "
        "|| to operator logiczny OR - wystarczy kolizja z GORNA LUB DOLNA rura."
    )

    pdf.h3("Dlaczego zmniejszony hitbox ptaka?")
    pdf.body(
        "Grafika ptaka (elipsa + dziob wystaje) jest wieksza niz prostokata kolizji. "
        "Margines 5px ze wszystkich stron daje graczowi troche taryfy ulgazonej - "
        "gra wyglada sprawiedliwie, ptak nie 'ginie' zanim wizualnie dotknie rury."
    )

    # -------------------------------------------------------
    # SEKCJA 15 - Punktacja
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("15. System punktacji")

    pdf.h2("15.1 Kod updateScore()")
    pdf.code(
        "void GameWindow::updateScore()\n"
        "{\n"
        "    float birdCenterX = bird->getX() + bird->getWidth() / 2.0f;\n"
        "\n"
        "    for (Pipe* pipe : pipes) {\n"
        "        if (pipe == nullptr || pipe->isPassed()) continue;\n"
        "\n"
        "        float pipeCenterX = pipe->getX() + Pipe::PIPE_WIDTH / 2.0f;\n"
        "\n"
        "        if (birdCenterX > pipeCenterX) {\n"
        "            pipe->setPassed(true);\n"
        "            score++;\n"
        "        }\n"
        "    }\n"
        "}"
    )

    pdf.h3("Jak dziala krok po kroku")
    steps = [
        "Obliczamy srodek X ptaka (pozycja + polowa szerokosci)",
        "Dla kazdej rury ktora JESZCZE NIE JEST ZALICZONA (!isPassed())",
        "Obliczamy srodek X rury",
        "Jesli srodek ptaka jest ZA srodkiem rury -> punkt!",
        "Oznaczamy rure jako passed = true zeby nie liczyc jej ponownie",
    ]
    for i, s in enumerate(steps, 1):
        pdf.bullet(f"{i}. {s}")

    pdf.ln(2)
    pdf.body(
        "Dlaczego srodek rury, a nie jej lewa krawedz? "
        "Chcemy przyznac punkt gdy ptak jest w polowie drogi przez rure - "
        "brzmi bardziej naturalnie i sprawiedliwie."
    )
    pdf.body(
        "Flaga 'passed' w klasie Pipe jest konieczna - bez niej ptak zdobylby "
        "punkt w KAZDEJ klatce gdy jest za rura (co 16ms = 62 punkty na sekunde!)."
    )

    # -------------------------------------------------------
    # SEKCJA 16 - Wzorce OOP
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("16. Wzorce projektowe - OOP w praktyce")

    pdf.h2("16.1 Polimorfizm")
    pdf.body(
        "Polimorfizm (wielopostaciowos) - ten sam interfejs, rozna implementacja. "
        "Dzieki 'virtual' w klasie bazowej, wywolanie ->draw() na wskazniku GameObject* "
        "automatycznie trafia do wlasciwej implementacji."
    )
    pdf.code(
        "// Kompilator NIE WIE w czasie kompilacji ktory draw() wywola\n"
        "// Decyzja jest podejmowana w CZASIE WYKONANIA (dynamic dispatch)\n"
        "GameObject* obj = new Bird();\n"
        "obj->draw(painter);  // -> wywoluje Bird::draw(), nie GameObject::draw()"
    )
    pdf.body(
        "Mechanizm: kazda klasa z virtual metoda ma ukryta tablice wskaznikow (vtable). "
        "Wywolanie przez wskaznik bazowy sprawdza vtable i skacze do wlasciwej funkcji."
    )

    pdf.h2("16.2 Dziedziczenie i hierarchia klas")
    pdf.code(
        "GameObject (abstrakcyjna - baza)\n"
        "+-- Bird       : public GameObject\n"
        "+-- Pipe       : public GameObject\n"
        "+-- Ground     : public GameObject\n"
        "\n"
        "QWidget (Qt)\n"
        "+-- GameWindow : public QWidget"
    )
    pdf.body(
        "Bird, Pipe i Ground dziedzicza wszystkie pola z GameObject (x, y, width, height) "
        "i metody (getX, getY, setPosition) bez potrzeby ich powtarzania. "
        "Musza za to zaimplementowac draw() i update()."
    )

    pdf.h2("16.3 Wzorzec Factory Method (PipeFactory)")
    pdf.code(
        "// Zamiast:\n"
        "Pipe* pipe = new Pipe(480+10, rand()%300 + 150, 165, 640); // logika rozrzucona\n"
        "\n"
        "// Uzywamy:\n"
        "Pipe* pipe = pipeFactory->createPipe(); // enkapsulacja logiki w fabryce"
    )
    pdf.body("GameWindow nie musi wiedziec JAK rura jest tworzona - tylko prosi fabryke.")

    pdf.h2("16.4 Automat stanow (State Machine)")
    pdf.body(
        "GameState (START/PLAYING/GAMEOVER) to prosty automat stanow. "
        "Zamiast wielu flag (isStarted, isDead, isPlaying...) jeden enum. "
        "Logika jest czysta - switch(gameState) zamiast gaszczu if/else."
    )

    pdf.h2("16.5 Enkapsulacja")
    pdf.body(
        "Pola klas sa private lub protected - nie mozna ich zmienic z zewnatrz bez "
        "przejscia przez metody klasy. Np. pozycja ptaka zmienia sie tylko przez "
        "update() i reset() - nie mozna przypadkowo ustawic y = -1000."
    )

    # -------------------------------------------------------
    # SEKCJA 17 - Pamiec
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("17. Zarzadzanie pamiecia - new i delete")

    pdf.h2("17.1 Sterta (heap) vs Stos (stack)")
    pdf.code(
        "// STOS - automatycznie zwolnione gdy wyjdziesz z zakresu {}\n"
        "{\n"
        "    Bird bird;   // powstaje na stosie\n"
        "}   // <-- tutaj bird jest automatycznie niszczony\n"
        "\n"
        "// STERTA - zyje dopoki nie wywolasz delete\n"
        "Bird* bird = new Bird();  // powstaje na stercie, zwaraca wskaznik\n"
        "// ... bird zyje przez caly czas ...\n"
        "delete bird;              // teraz jest niszczony"
    )
    pdf.body(
        "Obiekty gry (bird, ground, pipes) musza zyc przez caly czas dzialania GameWindow, "
        "wiec sa na stercie. Lokalne zmienne na stosie znikalyby po wyjsciu z konstruktora."
    )

    pdf.h2("17.2 Regula: kazde new ma delete")
    pdf.table_row(["Gdzie new", "Gdzie delete"], [80, 95], bold=True)
    pdf.table_row(["GameWindow() -> new Bird", "~GameWindow() -> delete bird"], [80, 95])
    pdf.table_row(["GameWindow() -> new Ground", "~GameWindow() -> delete ground"], [80, 95])
    pdf.table_row(["GameWindow() -> new PipeFactory", "~GameWindow() -> delete pipeFactory"], [80, 95])
    pdf.table_row(["GameWindow() -> new QTimer(this)", "automatycznie przez Qt (parent=this)"], [80, 95])
    pdf.table_row(["gameLoop -> pipeFactory->createPipe()", "gameLoop -> delete pipe (gdy offscreen) + ~GameWindow"], [80, 95])
    pdf.ln(2)

    pdf.h2("17.3 Wyciek pamieci (memory leak)")
    pdf.body(
        "Wyciek pamieci = new bez delete. Program zuzywa coraz wiecej RAM az system "
        "zabije proces. W tej grze: gdyby nie usuwac rur wychodzacych za ekran, "
        "kazde uruchomienie by tworzylo setki rur w pamieci."
    )

    pdf.h2("17.4 Bezpieczne usuwanie z wektora")
    pdf.code(
        "// NIEBEZPIECZNE - iteracja w przod\n"
        "for (int i = 0; i < pipes.size(); i++) {\n"
        "    if (pipes[i]->isOffScreen()) {\n"
        "        delete pipes[i];\n"
        "        pipes.erase(pipes.begin() + i); // przesuwa indeksy!\n"
        "        // pipes[i+1] staje sie pipes[i] - pomijamy go!\n"
        "    }\n"
        "}\n"
        "\n"
        "// BEZPIECZNE - iteracja wsteczna\n"
        "for (int i = static_cast<int>(pipes.size()) - 1; i >= 0; --i) {\n"
        "    if (pipes[i]->isOffScreen()) {\n"
        "        delete pipes[i];                     // usun obiekt\n"
        "        pipes.erase(pipes.begin() + i);      // usun wskaznik - bezpieczne!\n"
        "    }\n"
        "}"
    )

    # -------------------------------------------------------
    # SEKCJA 18 - Q&A
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("18. Pytania egzaminacyjne i odpowiedzi")

    qa = [
        (
            "Co to jest klasa abstrakcyjna i dlaczego GameObject nia jest?",
            "Klasa abstrakcyjna to klasa z co najmniej jedna czystą metodą wirtualną (= 0). "
            "GameObject ma draw() i update() jako czyste - nie mozna stworzyc obiektu "
            "new GameObject() bezposrednio. Wymusza to, zeby kazda podklasa (Bird, Pipe, Ground) "
            "miala wlasna implementacje rysowania i aktualizacji."
        ),
        (
            "Co to jest virtual destruktor i dlaczego jest konieczny?",
            "Bez virtual ~GameObject(), jezeli usuniesz obiekt Bird przez wskaznik "
            "GameObject*, wywola sie tylko destruktor GameObject - destruktor Bird nie zostanie "
            "wywolany. To prowadzi do wyciekow pamieci. virtual sprawia ze C++ wywoluje "
            "destruktor wlasciwej podklasy."
        ),
        (
            "Jak dziala Q_OBJECT i po co jest?",
            "Q_OBJECT to makro Qt, ktore musi byc w kazdej klasie uzywajac sygnalow i slotow. "
            "Kompilator Qt (moc = Meta-Object Compiler) przetwarza je i generuje kod "
            "obslugujaący system sygnalow/slotow, introspekcje i inne mechanizmy Qt. "
            "Bez niego connect() nie zadziala."
        ),
        (
            "Dlaczego petla gry korzysta z timera, a nie z petli while(true)?",
            "Qt jest frameworkiem zdarzeniowym - ma wlasna petle zdarzen (app.exec()). "
            "Blokujaca petla while(true) zablokwalaby te petle, uniemozliwiajac obsluge "
            "klawiszy, myszy i rysowania. QTimer wspolpracuje z petla zdarzen - co 16ms "
            "dodaje zdarzenie timeout, ktore jest obslugiwane gdy petla jest gotowa."
        ),
        (
            "Dlaczego iterujesz wstecznie gdy usuwasz rury?",
            "std::vector::erase przesuwa wszystkie elementy za usunietym miejscem o jeden. "
            "Przy iteracji do przodu po usunieciu elementu i, element i+1 staje sie nowym i - "
            "wiec go pominiesz. Iteracja wsteczna eliminuje ten problem: usuniecie i nie "
            "wplywa na elementy 0..i-1."
        ),
        (
            "Co to jest Wzorzec Fabryki i dlaczego go uzywamy?",
            "Factory Method to wzorzec kreacyjny - zamiast tworzyc obiekty bezposrednio, "
            "mamy dedykowana klase (fabryke) ktora to robi. PipeFactory::createPipe() "
            "enkapsuluje losowanie pozycji, walidacje i obsluge wyjatkow. GameWindow nie "
            "musi znac szczegolów - po prostu prosi fabryke o nowa rure."
        ),
        (
            "Jak dziala detekcja kolizji?",
            "Uzywamy QRect::intersects(). Kazdy obiekt moze zwrocic swoj prostokat kolizji. "
            "Ptak ma zmniejszony prostokat (margines 5px). intersects() zwraca true jesli "
            "prostokaty maja wspolny obszar. Sprawdzamy: ptak-podloga, ptak-gorna granica, "
            "ptak-gorna czesc rury, ptak-dolna czesc rury."
        ),
        (
            "Dlaczego pozycja ptaka jest float, a nie int?",
            "Fizyka grawitacji (predkosc 0.5f/klatke) wymaga ulamkowej precyzji. Gdyby y bylo "
            "int, ptak poruszalby sie skokami po 1 piksel i animacja bylaby szarpana. float "
            "pozwala na plynny ruch, a konwersja do int nastepuje tylko przy rysowaniu "
            "(static_cast<int>(y))."
        ),
        (
            "Co robi srand(time(nullptr)) w PipeFactory?",
            "rand() generuje pseudolosowe liczby - zawsze ta sama sekwencje. srand() ustawia "
            "ziarno (seed) - punkt startowy tej sekwencji. time(nullptr) zwraca aktualny czas "
            "Unix (sekundy od 1.1.1970). Poniewaz czas zmienia sie co sekunde, kazde "
            "uruchomienie programu daje inna sekwencje losowa - czyli inne pozycje rur."
        ),
        (
            "Jaka jest roznica miedzy START a PLAYING a GAMEOVER?",
            "START = menu startowe, gra nie zaczeta, brak rur. "
            "PLAYING = gra w toku, petla gry aktywna, rury sie pojawiaja, fizyka dziala. "
            "GAMEOVER = ptak umarl, ekran koncowy. "
            "Wejscie przeklacza: START->PLAYING (startGame), "
            "PLAYING->GAMEOVER (kolizja), GAMEOVER->START (resetGame)."
        ),
        (
            "Dlaczego Pipe::PIPE_WIDTH jest static constexpr?",
            "static = jedna kopia dla calej klasy (nie per-obiekt). "
            "constexpr = wartosc znana w czasie kompilacji, moze byc uzyta w wyrazeniach stalych. "
            "Szerokosc rury jest stala dla wszystkich rur, wiec nie ma sensu przechowywac jej "
            "w kazdym obiekcie. Dostepna jako Pipe::PIPE_WIDTH."
        ),
        (
            "Co to jest enum class i czym rozni sie od zwyklego enum?",
            "enum class (C++11) to silnie typowany enum. Zwykly enum pollutes przestrzen nazw - "
            "START byloby dostepne globalnie i mogloby kolidowac z innymi nazwami. "
            "enum class wymaga pelnej kwalifikacji: GameState::START. "
            "Dodatkowo nie konwertuje sie automatycznie do int."
        ),
        (
            "Co to jest lista inicjalizacyjna w konstruktorze i po co?",
            "Lista inicjalizacyjna to czesc po dwukropku przed cialem konstruktora: "
            "Bird::Bird() : velocityY(0.0f), gravity(0.5f) { }. "
            "Inicjalizuje pola PRZED wejsciem do ciala konstruktora. "
            "Jest wydajniejsza niz przypisanie w {} bo unika podwojnej inicjalizacji. "
            "Dla pol const i referencji jest WYMAGANA."
        ),
        (
            "Co sie dzieje gdy wywolujesz update() w gameLoop?",
            "update() w Qt nie rysuje bezposrednio - to prosba do systemu o przerysowanie "
            "okna. Qt kolejkuje te prosbe i gdy jest gotowy, wywoluje paintEvent(). "
            "Nie mozna wywolac paintEvent() bezposrednio - to blad projektowy."
        ),
    ]

    for i, (q, a) in enumerate(qa, 1):
        pdf.h3(f"P{i}: {q}")
        pdf.body(f"O: {a}")
        pdf.ln(1)

    # -------------------------------------------------------
    # STRONA KONCOWD - PODSUMOWANIE
    # -------------------------------------------------------
    pdf.add_page()
    pdf.h1("Podsumowanie - co pokazuje ten projekt")

    pdf.h2("Elementy OOP")
    pdf.table_row(["Koncept", "Gdzie w projekcie"], [55, 119], bold=True)
    pdf.table_row(["Dziedziczenie", "Bird, Pipe, Ground : public GameObject"], [55, 119])
    pdf.table_row(["Polimorfizm", "virtual draw/update, wywolanie przez wskaznik bazowy"], [55, 119])
    pdf.table_row(["Enkapsulacja", "private/protected pola, publiczne metody dostepowe"], [55, 119])
    pdf.table_row(["Klasa abstrakcyjna", "GameObject z = 0 metodami"], [55, 119])
    pdf.table_row(["Wirtualny destruktor", "~GameObject() virtual"], [55, 119])
    pdf.table_row(["Konstruktory", "domyslny i parametryczny w kazdej klasie"], [55, 119])
    pdf.table_row(["Wyjatki", "throw w Pipe::Pipe(), catch w PipeFactory"], [55, 119])
    pdf.table_row(["Wzorzec Factory", "PipeFactory::createPipe()"], [55, 119])
    pdf.table_row(["Automat stanow", "enum class GameState {START, PLAYING, GAMEOVER}"], [55, 119])

    pdf.ln(3)
    pdf.h2("Elementy C++ i Qt")
    pdf.table_row(["Technika", "Opis"], [55, 119], bold=True)
    pdf.table_row(["static constexpr", "Pipe::PIPE_WIDTH - stala przynalezna do klasy"], [55, 119])
    pdf.table_row(["std::vector<Pipe*>", "dynamiczna tablica wskaznikow na rury"], [55, 119])
    pdf.table_row(["new / delete", "reczne zarzadzanie pamiecia na stercie"], [55, 119])
    pdf.table_row(["static_cast<int>", "bezpieczna konwersja float -> int przy rysowaniu"], [55, 119])
    pdf.table_row(["Q_OBJECT / connect", "system sygnalow i slotow Qt"], [55, 119])
    pdf.table_row(["QTimer (16ms)", "petla gry ~62.5 FPS"], [55, 119])
    pdf.table_row(["QPainter", "rysowanie bez zewnetrznych assetow (plikow PNG)"], [55, 119])
    pdf.table_row(["QRect::intersects", "detekcja kolizji AABB"], [55, 119])
    pdf.table_row(["Override keyword", "bezpieczne nadpisanie metod wirtualnych"], [55, 119])
    pdf.table_row(["Lista inicjalizacyjna", "wydajna inicjalizacja pol w konstruktorze"], [55, 119])

    pdf.ln(5)
    pdf.set_font("Ar", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Olaf Rysiewicz | Dawid Skatula | Szymon Panek", align="C")
    pdf.ln(5)
    pdf.cell(0, 6, "Programowanie II - C++ obiektowy | Politechnika Slaska 2026", align="C")
    pdf.set_text_color(0, 0, 0)

    out = os.path.join(OUTPUT_DIR, "tutorial.pdf")
    pdf.output(out)
    print(f"Zapisano: {out}")


# ============================================================
if __name__ == "__main__":
    make_tutorial()
