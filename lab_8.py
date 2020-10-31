from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('900x700') # задаём размеры экрана
canv = tk.Canvas(root, bg='white') # закрашиваем экран
canv.pack(fill=tk.BOTH, expand=1)

class Ball():
    def __init__(self, x = 40, y = 450):
        """ Конструктор класса Ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        vx - скорость шарика по ох
        vy - скорость шарика по оу
        ay - ускорение шарика по оу
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.ay = 1.6
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30


    def set_coords(self):
        """Передаём координаты объекта."""
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )


    def move(self):
        """Переместим мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 900х700).
        """
       
        if self.y + 2*self.r <=700:
            self.y -= self.vy
            self.x += self.vx
            self.vy -= self.ay
            self.set_coords()

        if self.y + 2*self.r >=700:
            self.vy = -self.vy
            self.y = 700 - 2*self.r

        if self.x + self.r >= 900:
            self.vx = - self.vx//3
            self.x = 900 - self.r

        if self.live < 0:
            balls.pop(balls.index(self))
            canv.delete(self.id)
        else:
            self.live -= 0.35
        

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ( round(math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)) <= self.r + obj.r ) :
            return True
        else : return False
        

class Gun():
    def __init__(self, x = 20, y = 450):
        """
        Конструктор класса Gun
        Создаём пушку в виде прямоугольника и оределям силу её выстрела
        Args:
        x - положение пушки по горизонтале
        y - положение пушки по вертикале
        """
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(x, y, x+30, y-30, width=7)


    def fire2_start(self, event):
        """Заряжаем пушку."""
        self.f2_on = 1


    def fire2_end(self, event):
        """
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10


    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an))


    def power_up(self):
        """Увеличиваем скорость вылета шара, при длительном нажатии мыши"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target():
    def __init__(self):
        """
        Конструктор класса Target
        Создаём цель на холсте
        """
        self.points = 1
        self.live = 1
        self.id = canv.create_oval(0,0,0,0)
        self.new_target()


    def set_coords(self):
        """Передаём координаты объекта."""
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move_target(self):
        """Переместим цель по прошествии единицы времени.
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx, self.vy и стен по краям окна (размер окна 900х700).
        """

        if self.y + 2*self.r <=700:
            self.y += self.vy
            self.x += self.vx
            self.set_coords()

        if self.y + 2*self.r >=700:
            self.vy = -self.vy
            self.y = 700 - 2*self.r
            self.set_coords()

        if self.x + self.r >= 900:
            self.vx = - self.vx
            self.x = 900 - self.r
            self.set_coords()

        if self.x + self.r <= 300:
            self.vx = - self.vx
            self.x = 300 + self.r
            self.set_coords()

        if self.y < 0 :
            self.vy = -self.vy
            self.y = self.r
            self.set_coords()


    def new_target(self):
        """ Инициализация новой цели. """
        vx = self.vx = 5
        vy = self.vy = 5
        x = self.x = rnd(400, 850)
        y = self.y = rnd(250, 650)
        r = self.r = rnd(10, 30)
        color = self.color = 'black'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self):
        """Попадание шарика в цель.
           Удаляем цель, если попадание произошло.
        """
        self.live = 0
        canv.delete(self.id)
        

def new_game(event=''):
    """Функция отвечающая за работу игры"""
    global screen1, balls
    score = 0 # Количество очков за попадания
    for i in range(n):
        t[i].new_target()
        t[i].live = 1
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    i = 0
    while t[i].live or balls:
        for b in balls:
            b.move()
            for i in range(len(t)):
                if b.hittest(t[i]) and t[i].live:
                    t[i].hit()
                    t[i] = Target()
                    canv.bind('<Button-1>')
                    canv.bind('<ButtonRelease-1>')
                    canv.bind('<Motion>')
                    score += t[i].points
                    canv.create_rectangle(10, 10, 60, 60, fill = 'white')
                    canv.create_text(30,30,text = score,font = '28')
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
        for i in range(n):
            t[i].move_target()


# Присваиваем переменным значение класса и определяем массив из этих элементов 
g1 = Gun()
n = 4
t = [] 
for i in range(n):
    t.append(Target())
new_game()
mainlop()
