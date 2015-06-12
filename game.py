import pygame
from gameconfig import GameConfig
from layer import Layer
from control import EventControl
from pegsolitaire import Puzzle


class State(object):
    def __init__(self, state_vars):
        self.state_vars = state_vars

    def run(self):
        return None


class StateHandler(object):
    def __init__(self):
        self.screen = None
        self.current_state = None
        self.state_vars = {}

    def setup(self):
        pygame.init()
        pygame.display.set_caption(GameConfig.CAPTION)
        self.current_state = Game(self.state_vars)

    def run_game(self):
        while self.current_state:
            current_state_object = self.current_state.run()
            if not hasattr(current_state_object, '__call__'):
                self.current_state = current_state_object
            else:
                self.current_state = current_state_object(self.screen, self.state_vars)

    @staticmethod
    def teardown():
        pygame.quit()


class Game(State):
    def __init__(self, *args, **kwargs):
        State.__init__(self, *args, **kwargs)
        self.surface = None
        self.clock = None
        self.controls = None
        self.exit = False
        self.selected_piece = None
        self.puzzle = None
        self.nodes = []
        self.setup()

    def setup(self):
        self.surface = Layer(GameConfig.SCREEN_SIZE)
        self.surface.fill(GameConfig.GAME_BACKGROUND)
        self.clock = pygame.time.Clock()
        self.puzzle = Puzzle()
        self.setup_game_board()
        self.controls = EventControl({
            pygame.QUIT: self.quit,
            pygame.MOUSEBUTTONDOWN: self.mouse_down_event
        })

    def setup_game_board(self):
        padding = GameConfig.GAME_PADDING + (GameConfig.GAME_GRID_PADDING * (GameConfig.GAME_GRID_SIZE - 1))
        sizex = (GameConfig.SCREEN_SIZE[0] - padding) / GameConfig.GAME_GRID_SIZE
        sizey = (GameConfig.SCREEN_SIZE[1] - padding) / GameConfig.GAME_GRID_SIZE
        centerx = (GameConfig.SCREEN_SIZE[0] - sizex) / 2
        centery = (GameConfig.SCREEN_SIZE[1] - sizey) / 2
        for position in self.puzzle.positions:
            node_position = (centerx + position[0] * (sizex + GameConfig.GAME_GRID_PADDING), centery + position[1] * (sizey + GameConfig.GAME_GRID_PADDING))
            self.nodes.append(Node((sizex, sizey), node_position, position))

    def run(self):
        while not self.exit:
            self.clock.tick(GameConfig.FRAMES_PER_SECOND)
            self.controls.poll_event()
            self.draw_menu()
            Layer.update()
        return None

    def draw_menu(self):
        for node in self.nodes:
            if self.puzzle.positions[node.grid_position] == Puzzle.OCCUPIED:
                node.contains_piece()
            else:
                node.no_piece()
            if self.selected_piece:
                self.selected_piece.selected()
            self.surface.blit(node.surface, node.position)

    def mouse_down_event(self, event):
        for node in self.nodes:
            if node.rect.collidepoint(event.pos):
                if not self.selected_piece:
                    if node.fill_state:
                        self.selected_piece = node
                else:
                    if not node.fill_state:
                        if node.grid_position in self.puzzle.valid_moves(self.selected_piece.grid_position):
                            self.puzzle.move_piece(self.selected_piece.grid_position, node.grid_position)
                    self.selected_piece = None

    def quit(self, event):
        self.exit = True


class Node(object):
    FILLED = 1
    EMPTY = 0

    def __init__(self, size, position, grid_position):
        self.surface = pygame.Surface(size)
        self.fill_state = None
        self.grid_position = grid_position
        self.position = position
        self.rect = self.surface.get_rect(left=position[0], top=position[1])

    def contains_piece(self):
        self.surface.fill(GameConfig.GAME_NODE_FILLED)
        self.fill_state = Node.FILLED

    def no_piece(self):
        self.surface.fill(GameConfig.GAME_NODE_EMPTY)
        self.fill_state = Node.EMPTY

    def selected(self):
        self.surface.fill(GameConfig.GAME_NODE_SELECTED)
