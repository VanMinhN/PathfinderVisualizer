import pygame
import math
import Button
from queue import PriorityQueue

WIDTH = 800
pygame.font.init()
pygame.init()  # Initiate pygame
pygame.mixer.pre_init(44100, -16, 2, 512)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Node on the grid


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap),
                         (width, i * gap))  # horizontal lines
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0),
                         (j * gap, width))  # vertical lines


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos  # 0,0 is at top left, and going right is x value represent as columns, going down is y value represent as rows

    row = y // gap
    col = x // gap

    return row, col

#
#   THE SECTION BELOW IS FOR PATH FINDING ALGO
#

# Algorithm: A*


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # keep track of the distance between current node to end node
    f_score = {node: float("inf") for row in grid for node in row}
    # heuristic -> guess from start to end node
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        # Safety measurement -> in case something when wrong eg. take too long, or can't find end node
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # Index at 2 to get node based on line 10
        open_set_hash.remove(current)  # remove dup

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

# Algorithm: BFS
# THis is unweighted graph


def BFS(draw, grid, start, end, pos):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # keep track of the distance between current node to end node
    f_score = {node: float("inf") for row in grid for node in row}
    # heuristic -> guess from start to end node
    f_score[start] = pos

    open_set_hash = {start}

    while not open_set.empty():
        # Safety measurement -> in case something when wrong eg. take too long, or can't find end node
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # Index at 2 to get node based on line 10
        open_set_hash.remove(current)  # remove dup

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    pos
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

# Algorithm DFS


def DFS(draw, grid, start, end):
    pass

# Algorithm: dijkstra's algorithm


def Dijkstra(draw, grid, start, end):
    pass


# -------------------------------------------------------------------------

# Main Loop


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    testing = False
    run = True
    # game loop
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT MOUSE
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT MOUSE
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            # Checking if the Algo is already run and find the path
            # Will reset if the user pressed any button
            if event.type == pygame.MOUSEBUTTONDOWN and testing:
                start = None
                end = None
                grid = make_grid(ROWS, width)
                testing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # algorithm(lambda: draw(win, grid, ROWS, width),
                    #           grid, start, end)
                    BFS(lambda: draw(win, grid, ROWS, width), grid,
                        start, end, h(start.get_pos(), end.get_pos()))
                    testing = True  # flag to reset
                # Reset
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                # go back to Menu
                if event.key == pygame.K_ESCAPE:
                    run = False
    pygame.quit()


def MainMenu(win):
    run = True
    BFS_BTN = Button.BTN(WIDTH/2-50, WIDTH/2, BFSbtn_img, 1)
    Astar_BTN = Button.BTN(WIDTH/2-50, WIDTH/2+100, Astarbtn_img, 1)
    Control_BTN = Button.BTN(WIDTH/2-50, WIDTH/2+200, Controlbtn_img, 1)
    EXIT_BTN = Button.BTN(WIDTH/2-50, WIDTH/2+300, Exitbtn_img, 1)
    while run:
        win.fill((255, 255, 255))  # fill the screen with White
        if(BFS_BTN.draw(win)):
            main(win, WIDTH)
        if(Astar_BTN.draw(win)):
            main(win, WIDTH)
        if(Control_BTN.draw(win)):
            main(win, WIDTH)
        if(EXIT_BTN.draw(win)):
            run = False
        pygame.display.update()
        for event in pygame.event.get():  # event game handler
            if event.type == pygame.QUIT:  # quit game
                run = False
    pygame.display.quit()  # quit the window


WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Visualizer")

# Load BFS button option
BFSbtn_img = pygame.image.load("./img/BFS_img.png").convert_alpha()
# Load A* button option
Astarbtn_img = pygame.image.load("./img/Astar_img.png").convert_alpha()
# Load Control button option
Controlbtn_img = pygame.image.load("./img/Control.png").convert_alpha()
# Load Control button option
Exitbtn_img = pygame.image.load("./img/Exit_img.png").convert_alpha()

MainMenu(WIN)
