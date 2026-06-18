cmake_minimum_required(VERSION 3.16)

project(FlappyBird VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Znajdź Qt6 (Widgets zawiera w sobie Core i Gui)
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)

# Włącz automatyczne przetwarzanie MOC, UIC, RCC
qt_standard_project_setup()

qt_add_executable(FlappyBird
    main.cpp
    GameObject.h
    GameObject.cpp
    Bird.h
    Bird.cpp
    Pipe.h
    Pipe.cpp
    Ground.h
    Ground.cpp
    PipeFactory.h
    PipeFactory.cpp
    GameWindow.h
    GameWindow.cpp
)

target_link_libraries(FlappyBird PRIVATE
    Qt6::Core
    Qt6::Widgets
)

# Na Windows: brak okna konsoli w finalnej wersji
# Zakomentuj podczas debugowania jeśli chcesz widzieć qDebug() w terminalu
set_target_properties(FlappyBird PROPERTIES
    WIN32_EXECUTABLE TRUE
    MACOSX_BUNDLE TRUE
)
