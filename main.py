import random


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [1 for x in range(length)]

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move:
            key_x, key_y = self.get_key_orientation()
            self._x = self._x + go * key_x
            self._y = self._y + go * key_y

    def get_coors_ship(self):
        coord_self = []
        key_x, key_y = self.get_key_orientation()
        for step in range(self._length):
            coord_self.append((self._x + step * key_x, self._y + step * key_y))
        return coord_self

    def get_key_orientation(self):
        if self._tp == 1:
            key_x = 1
            key_y = 0
        else:
            key_x = 0
            key_y = 1
        return key_x,key_y

    def get_coors_collide(self):
        coord_self = []
        key_x, key_y = self.get_key_orientation()
        for step in range(-1, self._length + 1):
            coord_self.append((self._x - 1 * key_y + step * key_x, self._y - 1 * key_x + step * key_y))
            coord_self.append((self._x + step * key_x, self._y + step * key_y))
            coord_self.append((self._x + 1 * key_y + step * key_x, self._y + 1 * key_x + step * key_y))
        return coord_self


    def is_collide(self, ship):
        coord_self = self.get_coors_ship()
        coord_ship = ship.get_coors_collide()
        for cell in coord_ship:
            if cell in coord_self:
                return True
        return False

    def is_out_pole(self, size):
        key_x, key_y = self.get_key_orientation()
        for x,y in self.get_coors_ship():
            if 0<=x<size and 0<=y<size:
                pass
            else: return True
        return False

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    count_ships = {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self, size):
        self._size = size
        self._ships = []
        self._kill_ships = []


    def init(self):
        temp_lst =[]
        for ship_size, count_ship in self.count_ships.items():
            for _ in range(count_ship):
                temp_lst.append(Ship(ship_size, tp=random.randint(1, 2)))

        for ship in temp_lst:
            is_collide = True
            while is_collide:
                is_collide = False
                key_x, key_y = ship.get_key_orientation()
                ship.set_start_coords(random.randint(0, self._size - 1 - key_x * ship._length),
                                      random.randint(0, self._size - 1 - key_y * ship._length))
                if ship.is_out_pole(self._size) or self.is_collide_all(ship):
                    is_collide = True


            self._ships.append(ship)


    def get_ships(self):
        return self._ships

    def is_collide_all(self, ship):
        is_collide = False
        for step1 in range(len(self._ships)):
            if ship != self._ships[step1]:
                if ship.is_collide(self._ships[step1]):
                    is_collide = True
                    break
        return is_collide

    def move_ships(self):
        for ship in self._ships:
            lst_move = [-1,1]
            if ship._is_move:
                x_temp, y_temp = ship.get_start_coords()
                move = random.choice(lst_move)
                ship.move(move)
                if ship.is_out_pole(self._size) or self.is_collide_all(ship):
                    ship.move(-move)
                    ship.move(-move)
                if ship.is_out_pole(self._size) or self.is_collide_all(ship):
                    ship.set_start_coords(x_temp,y_temp)



    def show(self):
        print(*self.get_pole(), sep='\n')

    def get_ship_from_coordinat(self,x,y):
        for ship in self._ships:
            if (x,y) in ship.get_coors_ship():
                key_x, key_y = ship.get_key_orientation()
                start_x,start_y = ship.get_start_coords()
                delta = (x-start_x)*key_x+(y-start_y)*key_y
                return (ship,delta)
        return False

    def set_shot(self,x,y):
        if self.get_pole()[y][x]>0:
            ship,cell = self.get_ship_from_coordinat(x, y)
            if ship[cell] == 1:
                ship[cell] = 0
                if sum(ship._cells) == 0:
                    self._ships.remove(ship)
                    self._kill_ships.append(ship)
                    return 'Kill'
                else:
                    ship._is_move = False
                    return 'Damage'
            else: return 'Duble'
        else: return 'Miss'

    def get_pole(self):
        cells = [[0 for y in range(self._size)] for x in range(self._size)]
        for ship in self._ships:
            for c_x, c_y in ship.get_coors_ship():
                try:
                    cells[c_y][c_x] = 1
                except:
                    print(ship._length, c_x, c_y)
        t =[]
        for x in cells:
             t.append( tuple(x))
        return tuple(t)

class Players:
    def __init__(self, name,type,pole,battle):
        self.name =name
        self.battle = battle
        self._enemy = None
        self._type = type
        self.pole = pole
        self.last_positive = None
        self.last_orientantion = None
        self.last_variant = [(-1,0),(0,-1),(0,1),(1,0)]
        self.last_length = None
        self.logs = []

    def add_enemy(self, enemy):
        self._enemy = enemy

    def reset_last(self):
        self.last_positive = None
        self.last_orientantion = None
        self.last_variant = [(-1,0),(0,-1),(0,1),(1,0)]
        self.last_length = None
        self.delta = None

    def input_coords(self):
        try:
            x, y = map(int, input('Введите координаты клетки для выстрела (0-9): ').split())
        except:
            print('Неправильные координаты, попробуйте снова')
            x, y = self.input_coords()
        if type(x) is not int or not (0 <= x <= 9) or type(y) is not int or not (0 <= y <= 9):
            print('Неправильные координаты, попробуйте снова')
            x, y = self.input_coords()
        return x, y

    def shot(self):
        miss = True
        while miss:
            if self._type == 'Computer':
                x, y = self.input_comp()
            elif self._type == 'Computer1':
                x, y = x, y = random.randint(0, 9), random.randint(0, 9)
            else:
                x, y = self.input_coords()
            shot = (self._enemy.pole.set_shot(x,y))
            s = f"{self.name}: x:{x} - y:{y}  {shot}"
            #print(s)
            self.logs.append(s)
            if shot not in ('Kill','Damage'):
                miss = False
            elif shot == 'Kill':
                if len(self._enemy.pole.get_ships()) == 0:
                    self.battle._is_done = True
                    self. battle.winer = self
                    miss = False
                self.reset_last()
            else:
                if self.last_positive is None:
                    self.last_positive = (x,y)
                    self.last_length = 1
                    self.last_variant = [(-1,0),(0,-1),(0,1),(1,0)]
                else:
                    self.last_length+=1
                    if abs(x-self.last_positive[0])>0:
                        self.last_orientantion = 1
                        delta = x-self.last_positive[0]
                        self.last_positive = (x, y)
                        if delta>0:
                            self.last_variant =[(-self.last_length,0),(1,0)]
                        else:
                            self.last_variant = [(0, -1), ( self.last_length,0)]
                    else:
                        self.last_orientantion =2
                        delta = y - self.last_positive[1]
                        if delta>0:
                            self.last_variant = [(0, -self.last_length), (0, 1)]
                        else:
                            self.last_variant = [(0, -1), (0, self.last_length)]
                        self.last_positive = (x, y)

    def input_comp(self):
        if self.last_positive is None:
            x, y = random.randint(0, 9), random.randint(0, 9)
        else:
            key =0
            x,y = self.last_positive
            while key == 0:
                key = 1
                try:
                    x1,y1 = random.choice(self.last_variant)
                    self.last_variant.remove((x1, y1))
                except:
                    print(self.name,x,y)
                    self.reset_last()
                    x1 =0
                    y1 =0
                if (x + x1<0 or x+x1 >=self.pole._size)or(y + y1<0 or y + y1>=self.pole._size):
                    key=0

            x, y = x + x1, y + y1

        return x, y

class SeaBattle:
    def __init__(self):
        self.player1 = Players('Игрок 1','Computer1',GamePole(10),self)
        self.player2 = Players('Игрок 2','Computer',GamePole(10),self)
        self.player1.pole.init()
        self.player2.pole.init()
        self.player1.add_enemy(self.player2)
        self.player2.add_enemy(self.player1)
        self.winer = None
        self._is_done = False

    def show(self):
        """Немного переделал отображение игрового поля, чтобы слева было ваше поле, справа компьютера"""
        symbol_human = ['~', '□', 'x']
        symbol_comp = ['~', '~', 'x']
        print('Ваше поле:                  Поле ПК:')
        print('0 1 2 3 4 5 6 7 8 9         0 1 2 3 4 5 6 7 8 9')
        for i in range(10):
            for j in range(10):
                print(symbol_human[self.player.get_pole()[i][j]], end=' ')
            print('  ', i, '   ', end='')
            for j in range(10):
                print(symbol_comp[self.computer.get_pole()[i][j]], end=' ')
            print()
    # def input_coords(self):
    #     try:
    #         x, y = map(int, input('Введите координаты клетки для выстрела (0-9): ').split())
    #     except:
    #         print('Неправильные координаты, попробуйте снова')
    #         x, y = self.input_coords()
    #     if type(x) is not int or not (0 <= x <= 9) or type(y) is not int or not (0 <= y <= 9):
    #         print('Неправильные координаты, попробуйте снова')
    #         x, y = self.input_coords()
    #     return x, y
    #
    # def human_shot(self):
    #     """Ход человека"""
    #     miss = True
    #     while miss:
    #         x, y = self.input_coords()
    #         shot = (self.computer.set_shot(x,y))
    #         print(shot)
    #         if shot not in ('Kill','Damage'):
    #             miss = False
    #         elif shot == 'Kill':
    #             if len(self.computer.get_ships()) == 0:
    #                 self._is_done = True
    #                 self.winer = self.player
    #                 miss = False
    #         else: pass
    #
    # def computer_shot(self):
    #     """Ход computer"""
    #     miss = True
    #     while miss:
    #         x, y = random.randint(0,9),random.randint(0,9)
    #         shot = (self.player.set_shot(x,y))
    #         print('Ход computer:',shot)
    #         if shot not in ('Kill','Damage'):
    #             miss = False
    #         elif shot == 'Kill':
    #             if len(self.player.get_ships()) == 0:
    #                 self._is_done = True
    #                 self.winer = self.computer
    #                 miss = False
    #         else: pass
    # def computer_shot1(self):
    #     """Ход computer"""
    #     miss = True
    #     while miss:
    #         x, y = random.randint(0,9),random.randint(0,9)
    #         shot = (self.computer.set_shot(x,y))
    #         print('Ход computer1:',shot)
    #         if shot not in ('Kill','Damage'):
    #             miss = False
    #         elif shot == 'Kill':
    #             if len(self.computer.get_ships()) == 0:
    #                 self._is_done = True
    #                 self.winer = self.player
    #                 miss = False
    #         else: pass




counter =[]
for x in range (1000):
    game = SeaBattle()
    while game._is_done is False:
        game.player1.shot()
        game.player2.pole.move_ships()
        if game._is_done is False:
            game.player2.shot()
            game.player1.pole.move_ships()
    print(game._is_done,game.winer.name, len(game.winer.logs))
    counter.append((game.winer.name, len(game.winer.logs)))

i1 = 0
i2 = 0
i_t1=0
i_t2=0
for winer, step in counter:
    if winer == 'Игрок 1':
        i1+=1
        i_t1+=step
    else:
        i2+=1
        i_t2+=step

print('Игрок 1:',i1,'avg time:',i_t1/i1)
print('Игрок 2:',i2,'avg time:',i_t2/i2)

