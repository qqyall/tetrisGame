import random
import sys
import time

import pygame as pg
from colors import (bg_color, brd_color, colors, info_color, lightcolors,
                    title_color, txt_color)
from config import (BLOCK, CUP_HEIGTH, CUP_WIDTH, DOWN_FREQ, FPS, SIDE_FREQ,
                    WINDOW_HEIGHT, WINDOW_WIDTH, side_margin, top_margin)
from figures import empty, fig_h, fig_w, figures
from pygame import locals


class Game():

    def __init__(self):
        pg.init()
        self.fps_clock = pg.time.Clock()
        self.display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.basic_font = pg.font.SysFont('arial', 20)
        self.big_font = pg.font.SysFont('verdana', 45)
        pg.display.set_caption('Проект "Тетрис"')
        self.showText('Проект "Тетрис"')

    def pauseScreen(self):
        pause = pg.Surface((WINDOW_HEIGHT, WINDOW_WIDTH), pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.display_surf.blit(pause, (0, 0))

    def runTetris(self):
        cup = self.emptycup()
        last_move_down = time.time()
        last_side_move = time.time()
        last_fall = time.time()
        going_down = False
        going_left = False
        going_right = False
        points = 0
        level, fall_speed = self.calcSpeed(points)
        fallingFig = self.getNewFigure()
        nextFig = self.getNewFigure()

        while True:
            if fallingFig is None:
                # если нет падающих фигур, генерируем новую
                fallingFig = nextFig
                nextFig = self.getNewFigure()
                last_fall = time.time()

                if not self.checkPos(cup, fallingFig):
                    return  # если на игровом поле нет свободного места - игра закончена
            self.quitGame()
            for event in pg.event.get():
                if event.type == locals.KEYUP:
                    if event.key == locals.K_SPACE:
                        self.pauseScreen()
                        self.showText('Пауза')
                        last_fall = time.time()
                        last_move_down = time.time()
                        last_side_move = time.time()
                    elif event.key == locals.K_LEFT:
                        going_left = False
                    elif event.key == locals.K_RIGHT:
                        going_right = False
                    elif event.key == locals.K_DOWN:
                        going_down = False

                elif event.type == locals.KEYDOWN:
                    # перемещение фигуры вправо и влево
                    if event.key == locals.K_LEFT and self.checkPos(cup, fallingFig, adjX=-1):
                        fallingFig['x'] -= 1
                        going_left = True
                        going_right = False
                        last_side_move = time.time()

                    elif event.key == locals.K_RIGHT and self.checkPos(cup, fallingFig, adjX=1):
                        fallingFig['x'] += 1
                        going_right = True
                        going_left = False
                        last_side_move = time.time()

                    # поворачиваем фигуру, если есть место
                    elif event.key == locals.K_UP:
                        fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                        if not self.checkPos(cup, fallingFig):
                            fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])

                    # ускоряем падение фигуры
                    elif event.key == locals.K_DOWN:
                        going_down = True
                        if self.checkPos(cup, fallingFig, adjY=1):
                            fallingFig['y'] += 1
                        last_move_down = time.time()

                    # мгновенный сброс вниз
                    elif event.key == locals.K_RETURN:
                        going_down = False
                        going_left = False
                        going_right = False
                        for i in range(1, CUP_HEIGTH):
                            if not self.checkPos(cup, fallingFig, adjY=i):
                                break
                        fallingFig['y'] += i - 1

            # управление падением фигуры при удержании клавиш
            if (going_left or going_right) and time.time() - last_side_move > SIDE_FREQ:
                if going_left and self.checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                elif going_right and self.checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                last_side_move = time.time()

            if going_down and time.time() - last_move_down > DOWN_FREQ and self.checkPos(cup, fallingFig, adjY=1):
                fallingFig['y'] += 1
                last_move_down = time.time()

            # свободное падение фигуры 
            if time.time() - last_fall > fall_speed:
                # проверка "приземления" фигуры
                if not self.checkPos(cup, fallingFig, adjY=1):
                    # фигура приземлилась, добавляем ее в содержимое стакана
                    self.addToCup(cup, fallingFig)
                    points += self.clearCompleted(cup)
                    level, fall_speed = self.calcSpeed(points)
                    fallingFig = None
                else:
                    # фигура пока не приземлилась, продолжаем движение вниз
                    fallingFig['y'] += 1
                    last_fall = time.time()

            # рисуем окно игры со всеми надписями
            self.display_surf.fill(bg_color)
            self.drawTitle()
            self.gamecup(cup)
            self.drawInfo(points, level)
            self.drawnextFig(nextFig)
            if fallingFig is not None:
                self.drawFig(fallingFig)
            pg.display.update()
            self.fps_clock.tick(FPS)

    @staticmethod
    def txtObjects(text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    @staticmethod
    def checkKeys():
        Game.quitGame()
        for event in pg.event.get([locals.KEYDOWN, locals.KEYUP]):
            if event.type == locals.KEYDOWN:
                continue
            return event.key
        return None

    def showText(self, text):
        titleSurf, titleRect = self.txtObjects(text, self.big_font, title_color)
        titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
        self.display_surf.blit(titleSurf, titleRect)

        pressKeySurf, pressKeyRect = self.txtObjects('Нажмите любую клавишу для продолжения', self.basic_font, title_color)
        pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
        self.display_surf.blit(pressKeySurf, pressKeyRect)

        while self.checkKeys() is None:
            pg.display.update()
            self.fps_clock.tick()

    @staticmethod
    def quitGame():
        # проверка всех событий, приводящих к выходу из игры
        for event in pg.event.get(locals.QUIT):
            pg.quit()
            sys.exit()
        for event in pg.event.get(locals.KEYUP):
            if event.key == locals.K_ESCAPE:
                pg.quit()
                sys.exit()
            pg.event.post(event)

    @staticmethod
    def calcSpeed(points):
        # вычисляет уровень
        level = int(points / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed

    @staticmethod
    def getNewFigure():
        # возвращает новую фигуру со случайным цветом и углом поворота
        shape = random.choice(list(figures.keys()))
        newFigure = {
            'shape': shape,
            'rotation': random.randint(0, len(figures[shape]) - 1),
            'x': int(CUP_WIDTH / 2) - int(fig_w / 2),
            'y': -2,
            'color': random.randint(0, len(colors)-1)
        }
        return newFigure

    @staticmethod
    def addToCup(cup, fig):
        for x in range(fig_w):
            for y in range(fig_h):
                if figures[fig['shape']][fig['rotation']][y][x] != empty:
                    cup[x + fig['x']][y + fig['y']] = fig['color']

    @staticmethod
    def emptycup():
        # создает пустой стакан
        cup = []
        for i in range(CUP_WIDTH):
            cup.append([empty] * CUP_HEIGTH)
        return cup

    @staticmethod
    def incup(x, y):
        return x >= 0 and x < CUP_WIDTH and y < CUP_HEIGTH

    @staticmethod
    def checkPos(cup, fig, adjX=0, adjY=0):
        # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
        for x in range(fig_w):
            for y in range(fig_h):
                abovecup = y + fig['y'] + adjY < 0
                if abovecup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                    continue
                if not Game.incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                    return False
                if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                    return False
        return True

    @staticmethod
    def isCompleted(cup, y):
        # проверяем наличие полностью заполненных рядов
        for x in range(CUP_WIDTH):
            if cup[x][y] == empty:
                return False
        return True

    @staticmethod
    def clearCompleted(cup):
        # Удаление заполенных рядов и сдвиг верхних рядов вниз
        removed_lines = 0
        y = CUP_HEIGTH - 1
        while y >= 0:
            if Game.isCompleted(cup, y):
                for pushDownY in range(y, 0, -1):
                    for x in range(CUP_WIDTH):
                        cup[x][pushDownY] = cup[x][pushDownY-1]
                for x in range(CUP_WIDTH):
                    cup[x][0] = empty
                removed_lines += 1
            else:
                y -= 1
        return removed_lines

    @staticmethod
    def convertCoords(block_x, block_y):
        return (side_margin + (block_x * BLOCK)), (top_margin + (block_y * BLOCK))

    def drawBlock(self, block_x, block_y, color, pixelx=None, pixely=None):
        # отрисовка квадратных блоков, из которых состоят фигуры
        if color == empty:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = Game.convertCoords(block_x, block_y)
        pg.draw.rect(self.display_surf, colors[color], (pixelx + 1, pixely + 1, BLOCK - 1, BLOCK - 1), 0, 3)
        pg.draw.rect(self.display_surf, lightcolors[color], (pixelx + 1, pixely + 1, BLOCK - 4, BLOCK - 4), 0, 3)
        pg.draw.circle(self.display_surf, colors[color], (pixelx + BLOCK / 2, pixely + BLOCK / 2), 5)

    def gamecup(self, cup):
        # граница игрового поля-стакана
        pg.draw.rect(self.display_surf, brd_color, (side_margin - 4, top_margin - 4, (CUP_WIDTH * BLOCK) + 8, (CUP_HEIGTH * BLOCK) + 8), 5)

        # фон игрового поля
        pg.draw.rect(self.display_surf, bg_color, (side_margin, top_margin, BLOCK * CUP_WIDTH, BLOCK * CUP_HEIGTH))
        for x in range(CUP_WIDTH):
            for y in range(CUP_HEIGTH):
                self.drawBlock(x, y, cup[x][y])

    def drawTitle(self):
        titleSurf = self.big_font.render('Тетрис Lite', True, title_color)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (WINDOW_WIDTH - 425, 30)
        self.display_surf.blit(titleSurf, titleRect)

    def drawInfo(self, points, level):
        pointsSurf = self.basic_font.render(f'Баллы: {points}', True, txt_color)
        pointsRect = pointsSurf.get_rect()
        pointsRect.topleft = (WINDOW_WIDTH - 550, 180)
        self.display_surf.blit(pointsSurf, pointsRect)

        levelSurf = self.basic_font.render(f'Уровень: {level}', True, txt_color)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (WINDOW_WIDTH - 550, 250)
        self.display_surf.blit(levelSurf, levelRect)

        pausebSurf = self.basic_font.render('Пауза: пробел', True, info_color)
        pausebRect = pausebSurf.get_rect()
        pausebRect.topleft = (WINDOW_WIDTH - 550, 420)
        self.display_surf.blit(pausebSurf, pausebRect)

        escbSurf = self.basic_font.render('Выход: Esc', True, info_color)
        escbRect = escbSurf.get_rect()
        escbRect.topleft = (WINDOW_WIDTH - 550, 450)
        self.display_surf.blit(escbSurf, escbRect)

    def drawFig(self, fig, pixelx=None, pixely=None):
        figToDraw = figures[fig['shape']][fig['rotation']]
        if pixelx is None and pixely is None:
            pixelx, pixely = Game.convertCoords(fig['x'], fig['y'])

        # отрисовка элементов фигур
        for x in range(fig_w):
            for y in range(fig_h):
                if figToDraw[y][x] != empty:
                    self.drawBlock(None, None, fig['color'], pixelx + (x * BLOCK), pixely + (y * BLOCK))

    def drawnextFig(self, fig):
        # превью следующей фигуры
        nextSurf = self.basic_font.render('Следующая:', True, txt_color)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (WINDOW_WIDTH - 150, 180)
        self.display_surf.blit(nextSurf, nextRect)
        self.drawFig(fig, pixelx=WINDOW_WIDTH-150, pixely=230)
