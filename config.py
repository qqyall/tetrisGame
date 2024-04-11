FPS = 25
WINDOW_HEIGHT, WINDOW_WIDTH = 500, 600
BLOCK, CUP_HEIGTH, CUP_WIDTH = 20, 20, 10

SIDE_FREQ, DOWN_FREQ = 0.15, 0.1  # передвижение в сторону и вниз

side_margin = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK) / 2)
top_margin = WINDOW_HEIGHT - (CUP_HEIGTH * BLOCK) - 5
