class GameConfig(object):
    SCREEN_SIZE = 640, 640
    CAPTION = "PegSolitare"
    FRAMES_PER_SECOND = 60

    CLEAN_SCREEN = (255, 255, 255)

    GAME_PADDING = 100
    GAME_GRID_PADDING = 10
    # Changing grid will only effect the UI at the moment. The engine has not
    # been written to account for different sized grids.
    GAME_GRID_SIZE = 7

    GAME_BACKGROUND = (60, 60, 60)
    GAME_NODE_EMPTY = (245, 245, 245)
    GAME_NODE_FILLED = (120, 120, 120)
    GAME_NODE_SELECTED = (183, 0, 0)
