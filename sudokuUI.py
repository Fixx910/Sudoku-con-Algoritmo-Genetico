import pygame
import pygame_gui
import sudokuGeneradorSoluciones as sdk

# Inicializar pygame
pygame.init()

# Configuraciones de la ventana
WINDOW_SIZE = (800, 500)
GRID_SIZE = 450
CELL_SIZE = GRID_SIZE // 9
MARGIN = 20

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Inicializar la pantalla
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Sudoku Solver')

# Inicializar el administrador de interfaz
manager = pygame_gui.UIManager(WINDOW_SIZE)

# Crear el botón de resolver
solve_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 50 + GRID_SIZE, 50), (100, 50)),
    text='Resolver',
    manager=manager
)

# Crear el slider de dificultad
difficulty_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 120), (200, 50)),
    start_value=0,
    value_range=(0, 2),
    manager=manager
)
# Texto para las dificultades
font = pygame.font.Font(None, 36)
difficulty_text = ['Fácil', 'Medio', 'Difícil']

# Crear cuadros de texto para los parámetros
param_1_text = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 210), (200, 30)),
    manager=manager
)
param_2_text = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 250), (200, 30)),
    manager=manager
)
param_3_text = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 290), (200, 30)),
    manager=manager
)

# Crear etiquetas para los cuadros de texto
param_1_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 210), (200, 30)),
    text='Parámetro 1',
    manager=manager
)
param_2_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 250), (200, 30)),
    text='Parámetro 2',
    manager=manager
)
param_3_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 100 + GRID_SIZE, 290), (200, 30)),
    text='Parámetro 3',
    manager=manager
)

# Texto para las dificultades
font = pygame.font.Font(None, 36)
difficulty_text = ['Fácil', 'Medio', 'Difícil']

# sudoku = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]

sudokuDificil = [
    [3, 1, 9, 0, 5, 0, 0, 2, 0],
    [0, 0, 6, 0, 3, 0, 0, 1, 0],
    [4, 5, 2, 0, 0, 0, 6, 8, 3],
    [0, 7, 4, 0, 0, 0, 0, 0, 2],
    [0, 0, 1, 0, 7, 4, 5, 0, 0],
    [8, 0, 5, 1, 0, 9, 7, 6, 0],
    [5, 0, 3, 2, 9, 6, 8, 0, 0],
    [6, 0, 0, 0, 8, 1, 3, 4, 0],
    [0, 9, 8, 0, 4, 0, 0, 0, 6]
]

sudokuMediano = [
    [3, 1, 9, 0, 5, 0, 0, 2, 0],
    [0, 0, 6, 0, 3, 0, 0, 1, 0],
    [4, 5, 2, 0, 1, 0, 6, 8, 3],
    [0, 7, 4, 0, 0, 0, 0, 0, 2],
    [0, 0, 1, 0, 7, 4, 5, 0, 0],
    [8, 0, 5, 1, 2, 9, 7, 6, 0],
    [5, 0, 3, 2, 9, 6, 8, 0, 0],
    [6, 0, 0, 0, 8, 1, 3, 4, 0],
    [1, 9, 8, 0, 4, 0, 0, 0, 6]
]

sudokuFacil = [
    [3, 1, 9, 0, 5, 0, 4, 2, 0],
    [7, 0, 6, 0, 3, 2, 0, 1, 0],
    [4, 5, 2, 0, 1, 0, 6, 8, 3],
    [0, 7, 4, 0, 0, 0, 1, 3, 2],
    [2, 0, 1, 0, 7, 4, 5, 0, 0],
    [8, 0, 5, 1, 2, 9, 7, 6, 4],
    [5, 0, 3, 2, 9, 6, 8, 0, 1],
    [6, 2, 0, 0, 8, 1, 3, 4, 0],
    [1, 9, 8, 0, 4, 3, 0, 0, 6]
]

# Sudoku resuelto (ejemplo)
solved_sudoku = [
    [5, 3, 4, 1, 7, 1, 1, 1, 1],
    [6, 7, 2, 1, 9, 5, 1, 1, 0],
    [1, 9, 8, 1, 1, 1, 1, 6, 1],
    [8, 1, 2, 1, 6, 1, 1, 1, 3],
    [4, 1, 1, 8, 1, 3, 1, 1, 1],
    [7, 1, 1, 1, 2, 1, 1, 1, 6],
    [0, 6, 1, 1, 1, 1, 2, 8, 1],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

sudoku = sudokuFacil

tamanoPoblacion = 10
generacionesTotales = 100

cantidadPadres = 100
cantidadSobrevivientes = tamanoPoblacion

crossoverRate = 0.9
mutationRate = 0.4
rowCrossoverRate = 0.1
swapMutationRate = 0.2
reinitializationMutationRate = 0.2

funcion = sdk.funcionObjetivo

def draw_grid(sudoku):
    for row in range(9):
        for col in range(9):
            cell_value = sudoku[row][col]
            rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if cell_value != 0:
                text_surface = font.render(str(cell_value), True, BLACK)
                screen.blit(text_surface, (rect.x + 15, rect.y + 10))

def validate_input(text):
    try:
        value = int(text)
        if value < 0 or value > 4:
            return ''
        return str(value)
    except ValueError:
        return ''

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == solve_button:
                    # Cambiar el Sudoku a la versión resuelta
                    global sudoku
                    sudoku = sdk.algoritmoGeneticoPermutaciones(sudoku,funcion, sdk.inicializarPoblacion(sudoku, tamanoPoblacion), generacionesTotales, sdk.torneo, crossoverRate, mutationRate)

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == difficulty_slider:
                    difficulty_level = int(difficulty_slider.get_current_value())
                    # Cambiar el sudoku según la dificultad
                    if difficulty_level == 0:
                        sudoku = sudokuFacil
                    elif difficulty_level == 1:
                        sudoku = sudokuMediano
                    elif difficulty_level == 2:
                        sudoku = sudokuDificil

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element in [param_1_text, param_2_text, param_3_text]:
                    event.ui_element.set_text(validate_input(event.text))

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(WHITE)
        draw_grid(sudoku)
        manager.draw_ui(screen)

        # Mostrar el texto de dificultad
        difficulty_level = int(difficulty_slider.get_current_value())
        text_surface = font.render(difficulty_text[difficulty_level], True, BLUE)
        screen.blit(text_surface, ((WINDOW_SIZE[0] - GRID_SIZE) // 2 - 30 + GRID_SIZE, 180))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()