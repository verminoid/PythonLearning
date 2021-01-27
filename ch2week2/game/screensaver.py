import pygame
import random
import math

from pygame.draw import line

SCREEN_DIM = (800, 600)

class Vec2d():
    """
    Class of vectors.  Zero point of vectors - [0,0]
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, obj):
        return Vec2d((self.x + obj.x),(self.y + obj.y))

    def __sub__(self, obj):
        return Vec2d((self.x - obj.x),(self.y - obj.y))

    def __mul__(self, k):
        return Vec2d((self.x * k),(self.y * k))

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))
    
    
    def int_pair(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, obj):
        if (self.x == obj.x) and (self.y == obj.y):
            return True
        else:
            return False

class Polyline():
    def __init__(self):
        self.points = []
        self.line = []
    
    def add_point(self, pos, speed):
        self.points.append((Vec2d(pos[0],pos[1]), Vec2d(speed[0],speed[1])))
    
    def set_points(self):
        temp_points = []
        for point, speed in self.points:
            point = point + speed
            
            if point.x > SCREEN_DIM[0] or point.x < 0:
                speed = Vec2d(- speed.x, speed.y)
            if point.y > SCREEN_DIM[1] or point.y < 0:
                speed = Vec2d(speed.x, - speed.y)
            temp_points.append((point, speed))
        self.points = temp_points
            

    def draw_points(self, window, style="points", widht=3, color=(255,255,255)):
        if style == "line":
            if len(self.line) > 0:
                for n in range(-1, len(self.line) - 1):
                    pygame.draw.line(window, color, self.line[n].int_pair(), self.line[n + 1].int_pair(), widht)
        
        elif style == "points":
            if len(self.points) > 0:
                for p in self.points:
                    
                    pygame.draw.circle(window, color, Vec2d.int_pair(p[0]), widht)


class Knot(Polyline):
    def __init__(self):
        super().__init__()
        self.steps = int(35)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_point, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_point, i * alpha))
        return res

    def get_knot(self):
        self.line = []
        if len(self.points) > 2:
            for n in range(-2, len(self.points) - 2):
                ptn = []
                ptn.append((self.points[n][0] + self.points[n + 1][0]) * 0.5)
                ptn.append(self.points[n + 1][0])
                ptn.append((self.points[n + 1][0] + self.points[n + 2][0]) * 0.5)

                self.line.extend(self.get_points(ptn, self.steps))

    def add_point(self, pos, speed):
        super().add_point(pos, speed)
        self.get_knot()
        
    def set_points(self):
        super().set_points()
        self.get_knot()
        
def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([newline.steps, "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            str(text[0]), True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            str(text[1]), True, (128, 128, 255)), (200, 100 + 30 * i))

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver VERMIN")

    newline = Knot()
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    newline.points = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    newline.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    newline.steps -= 1 if newline.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                newline.add_point(event.pos, (random.random() * 2, random.random() * 2))
                

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        newline.draw_points(gameDisplay)
        newline.draw_points(gameDisplay, "line", 3, color)
        if not pause:
            newline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

    

