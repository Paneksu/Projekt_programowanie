"""
Generuje proste pliki PDF z dokumentacji projektu Flappy Bird.
Wymaga: fpdf2 (pip install fpdf2)
"""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


class Doc(FPDF):
    def __init__(self, title, margin=20):
        super().__init__()
        self.doc_title = title
        self.set_margins(margin, margin, margin)
        self.set_auto_page_break(True, margin=margin)
        self.add_page()

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.cell(0, 10, f"Strona {self.page_no()}", align="C")

    def h1(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 16)
        self.multi_cell(0, 9, text)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def h2(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 13)
        self.multi_cell(0, 8, text)
        self.ln(1)

    def h3(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body(self, text, size=10):
        self.set_font("Helvetica", "", size)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bold_line(self, label, value):
        self.set_font("Helvetica", "B", 10)
        self.write(6, label + " ")
        self.set_font("Helvetica", "", 10)
        self.write(6, value)
        self.ln(6)

    def code(self, text):
        self.set_fill_color(240, 240, 240)
        self.set_font("Courier", "", 8)
        self.multi_cell(0, 5, text, fill=True, border=1)
        self.set_fill_color(255, 255, 255)
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def _row_height(self, cols, widths, line_h, pad):
        row_h = line_h + 2 * pad
        for text, w in zip(cols, widths):
            with self.offset_rendering() as recorder:
                y0 = recorder.get_y()
                recorder.multi_cell(w - 2 * pad, line_h, text, border=0)
                content_h = recorder.get_y() - y0
            row_h = max(row_h, content_h + 2 * pad)
        return row_h

    def table_row(self, cols, widths, bold=False, font_size=9):
        style = "B" if bold else ""
        self.set_font("Helvetica", style, font_size)
        line_h = 4.5 if font_size <= 8 else 5.0
        pad = 1
        row_h = self._row_height(cols, widths, line_h, pad)
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
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(3)


# ---------------------------------------------------------------------------
# 1. ARKUSZ WSTEPNY
# ---------------------------------------------------------------------------
def make_arkusz_wstepny():
    pdf = Doc("Arkusz wstepny - Flappy Bird")

    pdf.h1("Arkusz wstepny projektu")
    pdf.bold_line("Przedmiot:", "Programowanie II - C++ obiektowy")
    pdf.bold_line("Prowadzacy:", "dr inz. Marcin Sobota")
    pdf.bold_line("Uczelnia:", "Politechnika Slaska")
    pdf.bold_line("Semestr:", "2025/2026, sem. 2")
    pdf.ln(2)

    pdf.h2("Dane grupy")
    pdf.table_row(["Lp.", "Imie i Nazwisko"], [15, 80], bold=True)
    pdf.table_row(["1", "Olaf Rysiewicz"], [15, 80])
    pdf.table_row(["2", "Dawid Skatula"], [15, 80])
    pdf.table_row(["3", "Szymon Panek"], [15, 80])
    pdf.ln(3)

    pdf.h2("Temat projektu")
    pdf.body("Gra 2D typu Flappy Bird w jezyku C++")
    pdf.ln(1)

    pdf.h2("Opis pomyslu")
    pdf.body(
        "Planujemy stworzyc gre inspirowana Flappy Bird. Gracz steruje ptakiem, "
        "ktory leci w prawo i musi omijac pionowe rury. Ptak ciagle opada (grawitacja), "
        "a gracz klika/naciska spacje zeby dac impuls w gore. Za kazda ominieta pare rur "
        "dostaje punkt. Gra konczy sie gdy ptak uderzy w rure lub ziemie."
    )
    pdf.ln(1)

    pdf.h2("Planowana architektura klas")
    pdf.body("Hierarchia dziedziczenia:")
    pdf.code(
        "GameObject  (klasa abstrakcyjna - bazowa)\n"
        "+-- Bird    (ptak gracza)\n"
        "+-- Pipe    (para rur - przeszkoda)\n"
        "+-- Ground  (ziemia - kolizja)\n\n"
        "PipeFactory  (wzorzec Factory - tworzy rury)\n"
        "GameWindow   (QWidget - glowne okno gry)"
    )

    pdf.h3("Klasa GameObject (abstrakcyjna)")
    pdf.body("Pola: x, y, width, height. Metody czysto wirtualne: draw(QPainter&), update(). Wirtualny destruktor.")

    pdf.h3("Klasa Bird")
    pdf.body("Predkosc pionowa, grawitacja, sila skoku. Metody: jump(), reset(), getCollisionRect().")

    pdf.h3("Klasa Pipe")
    pdf.body("Srodek przerwy (gapCenterY), wysokosc przerwy (gapHeight), predkosc, flaga passed. Walidacja w konstruktorze.")

    pdf.h3("Klasa PipeFactory (wzorzec Factory)")
    pdf.body("Tworzy rury z losowymi przerwami. Parametr trudnosci zmienia predkosc i rozmiar przerwy.")

    pdf.ln(2)
    pdf.h2("Stos technologiczny")
    pdf.table_row(["Element", "Wybor"], [30, 120], bold=True)
    pdf.table_row(["Jezyk", "C++17"], [30, 120])
    pdf.table_row(["GUI / grafika", "Qt 6 (Widgets + QPainter)"], [30, 120])
    pdf.table_row(["Build system", "CMake + qt_add_executable"], [30, 120])
    pdf.table_row(["IDE", "Visual Studio Code"], [30, 120])
    pdf.ln(3)

    pdf.h2("Planowany podzial pracy")
    pdf.table_row(["Osoba", "Zakres"], [45, 105], bold=True)
    pdf.table_row(["Olaf Rysiewicz", "Klasa Bird, rysowanie ptaka, fizyka (grawitacja)"], [45, 105])
    pdf.table_row(["Dawid Skatula", "Klasa Pipe + PipeFactory, wzorzec Factory"], [45, 105])
    pdf.table_row(["Szymon Panek", "GameWindow (petla gry, kolizje, UI, ekrany)"], [45, 105])
    pdf.table_row(["Wszyscy", "GameObject, Ground, dokumentacja, testowanie"], [45, 105])
    pdf.ln(3)

    pdf.h2("Elementy OOP do pokazania")
    items = [
        ("Konstruktory/destruktory", "wszystkie klasy; ~GameObject() wirtualny"),
        ("Dziedziczenie", "Bird, Pipe, Ground dziedzicza po GameObject"),
        ("Polimorfizm", "petla for(pipe:pipes) pipe->draw(painter) przez wskaznik"),
        ("Wyjatki", "walidacja w Pipe::Pipe(), obsluga w PipeFactory"),
        ("Wzorzec projektowy", "PipeFactory - wzorzec fabryki"),
        ("Walidacja danych", "parametry rury, poziom trudnosci"),
    ]
    for label, desc in items:
        pdf.set_font("Helvetica", "B", 9)
        pdf.write(6, f"* {label}: ")
        pdf.set_font("Helvetica", "", 9)
        pdf.write(6, desc)
        pdf.ln(6)

    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "Data sporzadzenia arkusza: kwiecien 2026", align="R")

    pdf.output(os.path.join(OUTPUT_DIR, "arkusz_wstepny.pdf"))
    print("Zapisano: arkusz_wstepny.pdf")


# ---------------------------------------------------------------------------
# 2. LISTA WYMAGAN
# ---------------------------------------------------------------------------
def make_lista_wymagan():
    pdf = Doc("Lista wymagan - Flappy Bird", margin=12)
    TW = [62, 106, 18]   # widths: Nazwa, Opis, Status  (total = 186 = 210-2*12)
    NW = [168, 18]        # widths: Opis, Status
    FS = 8                # font size for all table rows

    pdf.h1("Lista wymagan projektu")
    pdf.bold_line("Projekt:", "Gra 2D typu Flappy Bird")
    pdf.ln(1)

    pdf.h2("Wymagania funkcjonalne")

    reqs_f = [
        ("Ekran startowy", "Wyswietla tytul i instrukcje startu."),
        ("Start gry", "Spacja lub klik LPM rozpoczyna gre; pojawiaja sie rury."),
        ("Grawitacja ptaka", "Predkosc opadania rosnie (maks. 14 px/kl.)."),
        ("Skok ptaka", "Spacja lub klik nadaje predkosc w gore."),
        ("Przesuwajace sie rury", "Rury z losowa przerwa przesuwaja sie w lewo."),
        ("Detekcja kolizji", "Kolizja z rura, ziemia lub gora ekranu konczy gre."),
        ("System punktacji", "Przelot przez przerwe = +1 pkt; flaga passed zapobiega wielokrotnemu naliczaniu."),
        ("Ekran konca gry", "Wynik i rekord po smierci ptaka."),
        ("Restart gry", "Spacja/klik na ekranie konca = powrot do ekranu startowego."),
        ("Zapis rekordu", "Rekord pamietany w trakcie sesji."),
    ]

    pdf.table_row(["Nazwa", "Opis", "Status"], TW, bold=True, font_size=FS)
    for name, desc in reqs_f:
        pdf.table_row([name, desc, "Zrealiz."], TW, font_size=FS)
    pdf.ln(1)

    pdf.h2("Wymagania techniczne")

    reqs_t = [
        ("Jezyk C++ obiektowy", "Klasy, dziedziczenie, polimorfizm."),
        ("Hierarchia dziedziczenia", "GameObject z pochodnymi Bird, Pipe, Ground."),
        ("Polimorfizm", "Wirtualne draw() i update() przez wskazniki na GameObject."),
        ("Konstruktory i destruktory", "Kazda klasa; ~GameObject() wirtualny."),
        ("Obsluga wyjatkow", "throw w Pipe::Pipe(), catch w PipeFactory."),
        ("Wzorzec projektowy", "Factory Method (PipeFactory)."),
        ("Walidacja danych", "Min. rozmiar przerwy, zakres pozycji, poziom trudnosci."),
        ("Grafika bez assetow", "Wszystko rysowane przez QPainter."),
        ("Qt 6, CMake, VS Code", "Zgodnie z formularzem zgloszenia."),
    ]

    pdf.table_row(["Nazwa", "Opis", "Status"], TW, bold=True, font_size=FS)
    for name, desc in reqs_t:
        pdf.table_row([name, desc, "Zrealiz."], TW, font_size=FS)
    pdf.output(os.path.join(OUTPUT_DIR, "lista_wymagan.pdf"))
    print("Zapisano: lista_wymagan.pdf")


# ---------------------------------------------------------------------------
# 3. ARKUSZ ZMIAN
# ---------------------------------------------------------------------------
def make_arkusz_zmian():
    pdf = Doc("Arkusz zmian - Flappy Bird")

    pdf.h1("Arkusz zmian")
    pdf.bold_line("Projekt:", "Gra 2D Flappy Bird w C++/Qt 6")
    pdf.bold_line("Grupa:", "Olaf Rysiewicz, Dawid Skatula, Szymon Panek")
    pdf.ln(2)

    pdf.h2("Inicjalizacja projektu  (26.04.2026)")
    pdf.h3("Dodano")
    for item in [
        "Szkielet projektu: CMakeLists.txt i pusty main.cpp",
        "Formularz zgloszenia projektu (wyslany na platforme)",
        "Arkusz wstepny z zaplanowana architektura klas",
        "Podstawowa struktura katalogow",
    ]:
        pdf.body(f"* {item}")
    pdf.h3("Decyzje projektowe")
    pdf.body("* Wybrano QWidget + QPainter + QTimer (zamiast QGraphicsScene - zbyt skomplikowane)")
    pdf.body("* Grafika w pelni rysowana kodem (bez plikow PNG/SVG)")
    pdf.body("* Surowe wskazniki + reczny delete - bardziej edukacyjnie")
    pdf.hr()

    pdf.h2("Pierwsza wersja klas i okno Qt  (03.05.2026)")
    pdf.h3("Dodano")
    for item in [
        "Klasa GameObject (abstrakcyjna, draw() i update() czysto wirtualne)",
        "Klasa Bird (konstruktory, podstawowa fizyka - grawitacja i skok)",
        "Klasa Ground (statyczna, kolizja i rysowanie)",
        "Klasa GameWindow dziedziczaca po QWidget",
        "paintEvent() rysujacy tlo i ptaka; QTimer z interwalem 16 ms",
    ]:
        pdf.body(f"* {item}")
    pdf.hr()

    pdf.h2("Rury i petla gry  (10.05.2026)")
    pdf.h3("Dodano")
    for item in [
        "Klasa Pipe z konstruktorem walidujacym parametry (wyjatki)",
        "Klasa PipeFactory (wzorzec fabryki)",
        "Spawn rur co pipeSpawnEvery = 88 klatek (~1.4 sek.)",
        "Usuwanie rur wychodzacych poza lewy brzeg ekranu",
        "Podstawowa detekcja kolizji",
    ]:
        pdf.body(f"* {item}")
    pdf.h3("Zmieniono")
    pdf.body("* Iteracja po rurach zamieniona na odwrotna (for i = size-1 ... >= 0)")
    pdf.body("* Dodano update() na koncu gameLoop()")
    pdf.hr()

    pdf.h2("Kolizje i wynik  (17.05.2026)")
    pdf.h3("Dodano")
    for item in [
        "Wynik wyswietlany w czasie rzeczywistym na gorze ekranu",
        "Zapis i wyswietlanie rekordu (bestScore)",
        "Stany gry: START, PLAYING, GAMEOVER",
        "Ekrany startowy i konca gry",
    ]:
        pdf.body(f"* {item}")
    pdf.h3("Zmieniono")
    pdf.body("* Hitboxy rur dopasowane do wizualnego korpusu")
    pdf.body("* Flaga passed w klasie Pipe - punkt naliczany dokladnie raz")
    pdf.body("* Hitbox ptaka zmniejszony o margines 5 px z kazdej strony")
    pdf.hr()

    pdf.h2("Polishing i finalizacja  (25.05.2026)")
    pdf.h3("Dodano / zmieniono")
    for item in [
        "Ladniejszy rysunek ptaka (skrzydlo, oko, dziob jako QPolygon)",
        "Chmury na tle nieba; gradient nieba (QLinearGradient)",
        "Efekt 3D rur (jasniejsza lewa krawedz)",
        "Obsluga klawisza Escape (zamkniecie okna)",
        "Nazwy autorow na ekranie startowym",
        "Ograniczenie maks. predkosci opadania ptaka (14 px/kl.)",
        "Stale SCREEN_WIDTH/HEIGHT/GROUND_HEIGHT jako static const zamiast magic numbers",
        "Komentarze uzupelnione we wszystkich plikach",
    ]:
        pdf.body(f"* {item}")

    pdf.output(os.path.join(OUTPUT_DIR, "arkusz_zmian.pdf"))
    print("Zapisano: arkusz_zmian.pdf")


# ---------------------------------------------------------------------------
# 4. DZIENNIK BLEDOW
# ---------------------------------------------------------------------------
def make_dziennik_bledow():
    pdf = Doc("Dziennik bledow - Flappy Bird")

    pdf.h1("Dziennik bledow")
    pdf.bold_line("Projekt:", "Gra 2D Flappy Bird w C++/Qt 6")
    pdf.bold_line("Grupa:", "Olaf Rysiewicz, Dawid Skatula, Szymon Panek")
    pdf.ln(2)

    # Blad 1
    pdf.h2("Blad #1 - Petla gry nie dzialala (brak connect)")
    pdf.bold_line("Data:", "03.05.2026")
    pdf.h3("Blad")
    pdf.body("Okno Qt sie wyswietlalo, ale ekran byl statyczny - ptak nie spadal, nic sie nie animowalo.")
    pdf.h3("Sposob naprawy")
    pdf.body(
        "Timer byl skonfigurowany, ale brakowalo linii connect() laczacej sygnal timeout() "
        "ze slotem gameLoop(). Timer odliczal, ale nie wywolywak zadnej metody."
    )
    pdf.code(
        "// BLAD\n"
        "gameTimer = new QTimer(this);\n"
        "gameTimer->start(16);  // connect() pominieto\n\n"
        "// POPRAWKA\n"
        "gameTimer = new QTimer(this);\n"
        "connect(gameTimer, &QTimer::timeout, this, &GameWindow::gameLoop);\n"
        "gameTimer->start(16);"
    )
    pdf.hr()

    # Blad 2
    pdf.h2("Blad #2 - Crash (Segmentation Fault) przy usuwaniu rur")
    pdf.bold_line("Data:", "10.05.2026")
    pdf.h3("Blad")
    pdf.body("Gra crashowala po ~5 sekundach, gdy pierwsza rura wychodzila za lewy brzeg ekranu.")
    pdf.h3("Sposob naprawy")
    pdf.body(
        "Podczas iteracji w przod po wektorze pipes wywolywano erase(), co uniewaznialo "
        "indeksy kolejnych elementow. Skutkowalo odwolaniem do zwolnionej pamieci."
    )
    pdf.code(
        "// BLAD - iteracja w przod z erase()\n"
        "for (int i = 0; i < pipes.size(); i++) {\n"
        "    if (pipes[i]->isOffScreen()) {\n"
        "        delete pipes[i];\n"
        "        pipes.erase(pipes.begin() + i);  // indeksy sie przesuwaja!\n"
        "    }\n"
        "}\n\n"
        "// POPRAWKA - iteracja od konca\n"
        "for (int i = static_cast<int>(pipes.size()) - 1; i >= 0; --i) {\n"
        "    if (pipes[i]->isOffScreen()) {\n"
        "        delete pipes[i];\n"
        "        pipes.erase(pipes.begin() + i);  // bezpieczne\n"
        "    }\n"
        "}"
    )
    pdf.hr()

    # Blad 3
    pdf.h2("Blad #3 - Kolizja z rura wykrywana za wczesnie")
    pdf.bold_line("Data:", "17.05.2026")
    pdf.h3("Blad")
    pdf.body("Ptak ginal kilka pikseli przed dotknieciem rury - gra wygladala niesprawiedliwie.")
    pdf.h3("Sposob naprawy")
    pdf.body(
        "Hitbox rury zawierl padding wizualny czapki rury (+6 px z kazdej strony). "
        "Kolizja byla wykrywana z niewidoczna czescia rury. Dodatkowo hitbox ptaka byl rowny "
        "pelnemu rozmiarowi sprite'a."
    )
    pdf.code(
        "// BLAD - hitbox z paddingiem czapki\n"
        "return QRect(static_cast<int>(x) - 6, 0, PIPE_WIDTH + 12, topEnd);\n\n"
        "// POPRAWKA - hitbox rowny korpusowi rury\n"
        "return QRect(static_cast<int>(x), 0, PIPE_WIDTH, topEnd);"
    )
    pdf.body("Dodatkowo zmniejszono hitbox ptaka o margines 5 px z kazdej strony.")
    pdf.hr()


    pdf.output(os.path.join(OUTPUT_DIR, "dziennik_bledow.pdf"))
    print("Zapisano: dziennik_bledow.pdf")


# ---------------------------------------------------------------------------
# 5. DOKUMENTACJA
# ---------------------------------------------------------------------------
def make_dokumentacja():
    pdf = Doc("Dokumentacja - Flappy Bird")

    pdf.h1("Dokumentacja projektu")
    pdf.h2("Gra 2D typu Flappy Bird w jezyku C++")
    pdf.bold_line("Przedmiot:", "Programowanie II - C++ obiektowy")
    pdf.bold_line("Prowadzacy:", "dr inz. Marcin Sobota")
    pdf.bold_line("Uczelnia:", "Politechnika Slaska, Wydzial RMS")
    pdf.bold_line("Semestr:", "2025/2026, sem. 2")
    pdf.ln(2)

    pdf.h2("Autorzy")
    pdf.table_row(["Imie i Nazwisko", "Rola w projekcie"], [55, 115], bold=True)
    pdf.table_row(["Olaf Rysiewicz", "Klasa Bird, fizyka ptaka, rysowanie QPainter"], [55, 115])
    pdf.table_row(["Dawid Skatula", "Klasa Pipe, PipeFactory (wzorzec Factory), walidacja"], [55, 115])
    pdf.table_row(["Szymon Panek", "GameWindow, petla gry, kolizje, UI, dokumentacja"], [55, 115])
    pdf.ln(3)

    pdf.h2("1. Opis zrealizowanego projektu")
    pdf.body(
        "Zrealizowalismy gre 2D inspirowana Flappy Bird. Aplikacja okienkowa napisana w C++ "
        "z uzyciem Qt 6. Gracz steruje ptakiem, ktory ciagle opada pod wplywem grawitacji. "
        "Nacisnieciem spacji lub kliknieciem myszka gracz daje ptakowi impuls w gore. "
        "Celem jest omijanie pionowych rur i zdobywanie punktow za kazda ominieta pare."
    )

    pdf.h3("Funkcjonalnosci")
    features = [
        "Ekran startowy z tytulem, instrukcja i nazwami autorow",
        "Fizyka ptaka: grawitacja z ograniczeniem predkosci, skok po spacji/kliknieciu",
        "Losowe przeszkody: rury z losowa wysokoscia przerwy, przesuwajace sie w lewo",
        "Detekcja kolizji: z rura, ziemia i gorna krawedzia ekranu",
        "System punktacji: +1 za kazda ominieta pare rur",
        "Zapis rekordu w trakcie sesji",
        "Ekran konca gry z wynikiem, rekordem i opcja restartu",
        "Grafika generowana kodem - zero zewnetrznych plikow",
    ]
    for f in features:
        pdf.body(f"* {f}")

    pdf.h3("Stos technologiczny")
    pdf.table_row(["Element", "Szczegoly"], [30, 140], bold=True)
    pdf.table_row(["Jezyk", "C++17"], [30, 140])
    pdf.table_row(["GUI", "Qt 6 (Core, Widgets)"], [30, 140])
    pdf.table_row(["Grafika", "QPainter (rysowanie wektorowe)"], [30, 140])
    pdf.table_row(["Build", "CMake 3.16+, qt_add_executable"], [30, 140])
    pdf.table_row(["IDE", "Visual Studio Code"], [30, 140])
    pdf.ln(2)

    pdf.add_page()
    pdf.h2("2. Architektura i elementy OOP")

    pdf.h3("Hierarchia klas")
    pdf.code(
        "QWidget\n"
        "+-- GameWindow        glowne okno, zarzadza stanem gry\n\n"
        "GameObject            klasa abstrakcyjna (bazowa)\n"
        "+-- Bird              ptak gracza\n"
        "+-- Pipe              para rur (przeszkoda)\n"
        "+-- Ground            podloze\n\n"
        "PipeFactory           wzorzec Factory, tworzy rury"
    )

    pdf.h3("Dziedziczenie i polimorfizm")
    pdf.body(
        "Klasa GameObject definiuje wspolny interfejs (draw, update - czysto wirtualne). "
        "Klasy Bird, Pipe i Ground dziedzicza po GameObject i nadpisuja obie metody. "
        "Dzieki temu GameWindow obsluguje wszystkie obiekty jednakowo przez wskaznik:"
    )
    pdf.code(
        "for (Pipe* pipe : pipes) {\n"
        "    pipe->draw(painter);   // wywoluje Pipe::draw()\n"
        "    pipe->update();        // kazda rura wie jak sie poruszac\n"
        "}"
    )

    pdf.h3("Konstruktory i destruktory")
    pdf.body(
        "Kazda klasa ma konstruktor domyslny, parametryczny i destruktor. "
        "Destruktor ~GameObject() jest virtual - konieczne przy polimorfizmie, "
        "bo bez tego delete na wskazniku bazowym nie wywolalby destruktora klasy pochodnej."
    )

    pdf.h3("Obsluga wyjatkow")
    pdf.body("Pipe::Pipe() waliduje parametry i rzuca wyjatki. PipeFactory lapie i stosuje bezpieczne wartosci domyslne:")
    pdf.code(
        "// Pipe::Pipe()\n"
        "if (gapHeight < 90)\n"
        "    throw std::invalid_argument(\"Przerwa za mala! Minimum 90px.\");\n\n"
        "// PipeFactory::createPipe()\n"
        "try { return new Pipe(x, gapCenter, gapHeight, screenHeight); }\n"
        "catch (const std::invalid_argument& e) {\n"
        "    return new Pipe(x, screenHeight/2, 170, screenHeight);  // fallback\n"
        "}"
    )

    pdf.h3("Wzorzec Factory Method")
    pdf.body(
        "PipeFactory odpowiada za tworzenie rur (losowanie pozycji, walidacja, predkosc). "
        "GameWindow tylko wywoluje pipeFactory->createPipe() - nie zna szczegolow tworzenia."
    )

    pdf.add_page()
    pdf.h2("3. Instrukcja uzytkownika")

    pdf.h3("Sterowanie")
    pdf.table_row(["Akcja", "Klawiatura", "Mysz"], [55, 55, 60], bold=True)
    pdf.table_row(["Start gry", "Spacja", "Lewy przycisk myszy"], [55, 55, 60])
    pdf.table_row(["Skok ptaka", "Spacja lub strzalka gore", "Lewy przycisk myszy"], [55, 55, 60])
    pdf.table_row(["Restart po smierci", "Spacja", "Lewy przycisk myszy"], [55, 55, 60])
    pdf.table_row(["Zamkniecie gry", "Escape", "Przycisk X okna"], [55, 55, 60])
    pdf.ln(3)

    pdf.h2("4. Ciekawostki z realizacji")

    pdf.h3("Rysowanie bez assetow")
    pdf.body(
        "Dziob ptaka to QPolygon z trzema punktami. Efekt 3D rury to jasniejszy pasek po lewej stronie. "
        "Chmury to nakladajace sie elipsy. Gradient nieba robi QLinearGradient. "
        "Mozna zrobic duzo bez jednego pliku PNG."
    )

    pdf.h2("5. Podsumowanie - odniesienie do zalozen wstepnych")

    pdf.h3("Zrealizowane zalozenia")
    done = [
        ("Dziedziczenie + polimorfizm", "GameObject -> Bird, Pipe, Ground"),
        ("Konstruktory i destruktory", "Kazda klasa; ~GameObject() wirtualny"),
        ("Obsluga wyjatkow", "Pipe::Pipe() rzuca, PipeFactory lapie"),
        ("Wzorzec projektowy", "Factory Method w PipeFactory"),
        ("Walidacja danych", "Parametry rur, poziom trudnosci"),
        ("Grafika bez assetow", "Tylko QPainter"),
    ]
    pdf.table_row(["Zalozenie", "Uwagi"], [70, 100], bold=True)
    for name, note in done:
        pdf.table_row([name, note], [70, 100])
    pdf.ln(3)

    pdf.h3("Czego sie nauczylismy")
    lessons = [
        "Zarzadzanie pamiecia w C++ - new/delete, wektory wskaznikow",
        "Polimorfizm w praktyce - faktyczna technika upraszczajaca petla gry",
        "Hitboxy vs grafika - dwie oddzielne rzeczy; dobry hitbox = dobry gameplay",
    ]
    for l in lessons:
        pdf.body(f"* {l}")

    pdf.h2("6. Mozliwosci rozbudowy projektu")

    rozbudowa = [
        ("Efekty dzwiekowe", "Qt Multimedia (QSoundEffect) - ding przy punkcie, crash"),
        ("Animacja ptaka", "Kilka klatek rysowanych naprzemiennie co 5 klatek gry"),
        ("Zapis rekordu do pliku", "QFile + QDataStream - rekord przetrwa zamkniecie programu"),
        ("Tryb multiplayer (lokalny)", "Drugi ptak sterowany klawiszami"),
        ("Poziomy / motywy", "Rozne tla i kolory rur per poziom"),
    ]
    pdf.table_row(["Pomysl", "Opis"], [60, 110], bold=True)
    for name, desc in rozbudowa:
        pdf.table_row([name, desc], [60, 110])

    pdf.output(os.path.join(OUTPUT_DIR, "dokumentacja.pdf"))
    print("Zapisano: dokumentacja.pdf")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    make_lista_wymagan()
    make_arkusz_zmian()
    make_dziennik_bledow()
    make_dokumentacja()
    print("\nWszystkie PDFy wygenerowane w folderze docs/")
