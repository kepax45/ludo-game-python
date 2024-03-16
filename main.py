import time
import os
class Player:
    def __init__(self, ah, av, l, symbol):
        self.ah = ah
        self.av = av
        self.l = l
        self.symbol = symbol
        self.travelled = 0
def move(p, speed, y, x, l):
    travelled = p.travelled
    ah = p.ah
    av = p.av
    while speed:
        if y == 0 and x >= 0 and x < l-1:
            ah = 1
            av = 0
        if x == l-1 and y >= 0 and y < l-1:
            ah = 0
            av = 1
        if y == l-1 and x > 0 and x < l:
            ah = -1
            av = 0
        if x == 0 and y > 0 and y < l:
            ah = 0
            av = -1
        old_x = x
        old_y = y
        new_x = x + ah*speed
        new_y = y + av*speed
        new_x = max(0, min(new_x, l - 1))
        new_y = max(0, min(new_y, l-1))
        moves_left = speed - (abs(old_x - new_x)+ abs(old_y - new_y))
        if(travelled + speed - moves_left) >= (l-1)*4+4:
            break
        if (travelled + speed - moves_left) >= (l - 1) * 4 and (new_x == l - 1 or new_y == l - 1 or new_y == 0 or new_x == 0):
            new_y += ah
            new_x -= av
            new_x = max(1, min(new_x, l - 2))
            new_y = max(1, min(new_y, l - 2))
        x = new_x
        y = new_y
        travelled += speed - moves_left
        speed = moves_left
    return (y, x, travelled, ah, av)


class ListNode:
    def __init__(self, info=None):
        self.info = info
        self.next = None
        self.prev = None
class ListHeader:
    def __init__(self):
        self.head = None
        self.tail = None
        self.numElem = None
def insert(index, val, list):
    if index > len(list):
        list.append(val)
        return True
    list.append(-1)
    for i in range(len(list)-1, index, -1):
        list[i] = list[i-1]
    list[index] = val
    return True

class SparseMatrix:
    def __init__(self, rows, cols):
        self.r = [-1 for i in range(rows+1)]
        self.r[rows] = 0
        self.rows = rows
        self.cols = cols
        self.c = []
        self.v = []
    def add(self, i, j, v):
        first = len(self.c)
        if i >= self.rows or j >= self.cols:
            return False
        for z in range(i+1, self.rows):
            if self.r[z] != -1 and first == len(self.c):
                first = self.r[z]
            if self.r[z] != -1:
                self.r[z] += 1
        if self.r[i] == -1:
            self.r[i] = first
            insert(first, j, self.c)
            insert(first, v, self.v)
        else:
            last = self.r[i]
            for z in range(self.r[i], first):
                if j > self.c[z]:
                    last = z+1
            insert(last, j, self.c)
            insert(last, v, self.v)
        self.r[self.rows] += 1
        return True
    def get(self, i, j):
        start = self.r[i]
        end = len(self.c)
        if i >= self.rows or j >= self.cols:
            return False
        if start == -1:
            return 0
        for z in range(i+1, self.rows):
            if self.r[z] != -1:
                end = self.r[z]
                break
        for z in range(start, end):
            if self.c[z] == j:
                return self.v[z]
        return 0
    def print(self):
        print('rows:', end=' ')
        for el in self.r:
            print(el, end=' ')
        print()
        print('cols:', end=' ')
        for el in self.c:
            print(el, end=' ')
        print()
        print('values:', end=' ')
        for el in self.v:
            print(el, end=' ')
        print()
    def remove(self, i, j):
        start = self.r[i]
        if i >= self.rows or j >= self.cols:
            return False
        if self.get(i, j) == 0:
            return False
        end = len(self.c)
        for z in range(i+1, self.rows):
            if self.r[z] != -1 and end == len(self.c):
                end = self.r[z]
            if self.r[z] != -1:
                self.r[z] -= 1
        n_of_elem = end-start
        for z in range(start, end):
            if self.c[z] == j:
                if n_of_elem == 1:
                    self.r[i] = -1
                del self.c[z]
                del self.v[z]
                self.r[self.rows] -= 1
                return True
    def find_coords(self, val):
        col = None
        row = None
        for z in range(len(self.v)):
            if self.v[z].symbol == val:
                col = self.c[z]
                index_col = z
                break
        if col == None:
            return (-1, -1)
        start = -1
        last = -1
        for z in range(self.rows):
            if self.r[z] != -1:
                last = start
                start = self.r[z]
            if last != -1 and start != -1 and last <= index_col < start:
                break
            row = self.r.index(start)
        return (row, col)
    def remove_by_value(self, val):
        i, j = self.find_coords(val)
        if i == -1 or j == -1:
            return False
        return self.remove(i, j)

    def print_dense(self):
        for i in range(self.rows):
            for j in range(self.cols):
                v = self.get(i, j)
                if isinstance(v, Player):
                    print(v.symbol, end=' ')
                else:
                    print(0, end=' ')
            print()
def get_parity_bit(n):
    parity = 0b0
    while n:
        parity = parity ^ (n & 1)
        n >>= 1
    return parity

def bbs(bits, p, q):
    global seed
    m = p*q
    res = 0
    for i in range(bits):
        seed = seed**2 % m
        res = res + (2**(bits-1-i))*get_parity_bit(seed)
    return res
def kocka():
    res = 1+bbs(3, 29996224275867, 35858495927467)
    while res >= 7:
        res = 1+bbs(3, 29996224275867, 35858495927467)
    return res
def ispis_talona(retka_matrica, dimenzije_talona):
    for i in range(dimenzije_talona):
        for j in range(dimenzije_talona):
            if isinstance(retka_matrica.get(i, j), Player):
                print(retka_matrica.get(i, j).symbol, end=' ')
            elif retka_matrica.get(i, j) != 0:
                print(retka_matrica.get(i, j), end=' ')
            elif i == 0 or j == 0 or j == dimenzije_talona-1 or i == dimenzije_talona-1:
                print('#', end=' ')
            else: print('0', end=' ')
        print()
def generisi_figure(oznaka1, oznaka2, oznaka3, oznaka4):
    prvi = ListNode(oznaka1)
    drugi = ListNode(oznaka2)
    treci = ListNode(oznaka3)
    cetvrti = ListNode(oznaka4)
    prvi.prev = cetvrti
    prvi.next = drugi
    drugi.prev = prvi
    drugi.next = treci
    treci.prev = drugi
    treci.next = cetvrti
    cetvrti.prev = treci
    cetvrti.next = prvi
    header = ListHeader()
    header.head = prvi
    header.tail = cetvrti
    header.numElem = 4
    return header
def print_figures(figures):
    tmp = figures.head
    if not figures.head:
        return
    while True:
        print(tmp.info, end=' ')
        if tmp.next == figures.head:
            break
        tmp = tmp.next
    print()
def get_koef(i, j, l):
    if i == 0 and j == 0:
        return (1, 0)
    if i == 0 and j == l-1:
        return (0, 1)
    if i == l-1 and j == 0:
        return (0, -1)
    if i == l-1 and j == l-1:
        return (-1, 0)
    return (0, 0)
def eject_figure(figures, player_index):
    if figures.numElem == 0:
        return False
    figures.numElem -= 1
    if figures.head == figures.tail:
        info = figures.head.info
        figures.head = None
        figures.tail = None
        return info
    info = figures.head.info
    q = figures.head.next
    r = figures.head.prev
    figures.head = q
    q.prev = r
    r.next = q
    i, j = pocetne_koordinate[player_index]
    ah, av = get_koef(i, j, dimenzije_talona)
    return Player(ah, av, dimenzije_talona, info)
def inject_figure(figures, v):
    q = ListNode(info=v)
    if figures.numElem == 0:
        q.prev = q
        q.next = q
        figures.head = q
        figures.tail = q
        figures.numElem += 1
        return True
    r = figures.tail
    p = figures.head
    r.next = q
    q.prev = r
    p.prev = q
    q.next = p
    figures.tail = q
    figures.numElem += 1
    return True
def get_top_figure(figures, player_index):
    i, j = pocetne_koordinate[player_index]
    info = figures.head.info
    ah, av = get_koef(i, j, dimenzije_talona)
    return Player(ah, av, dimenzije_talona, info)
def figure_info(m, player_index, kocka):
    vrednosti = [chr(97+player_index*4), chr(98+player_index*4), chr(99+player_index*4), chr(100+player_index*4)]
    nadjene = []
    for el in vrednosti:
        coords = m.find_coords(el)
        if coords != (-1, -1):
            i, j = coords
            if get_belonging(m.get(i, j).symbol) != player_index:
                continue
            r, c, tr, ah, av = move(m.get(i, j), kocka, i, j, dimenzije_talona)
            if m.get(r, c) == 0 or get_belonging(m.get(r, c).symbol)!=player_index:
                figura = m.get(i, j)
                nadjene.append((figura, (r, c, tr)))
    i, j = pocetne_koordinate[player_index]
    if kocka == 6 and figures[player_index].numElem > 0 and (m.get(i, j)==0 or get_belonging(m.get(i,j).symbol)!=player_index):
        figura = get_top_figure(figures[player_index], player_index)
        sr, sc = pocetne_koordinate[player_index]
        nadjene.append((figura, (sr, sc, 0)))
    return nadjene
def get_belonging(symbol):
    return (ord(symbol)-97)//4
broj_igraca = 0
dimenzije_talona = 0
seed = time.time_ns()
while True:
    os.system("cls")
    try:
        print("Molimo Vas unesite validne dimenzije talona (neparan broj >= od 7):", end=' ')
        dimenzije_talona = int(input())
        print("Molimo Vas unesite broj igraca u intervalu [1, 4]:", end=' ')
        broj_igraca = int(input())
    except Exception as e:
        print("Netacni podaci!")
        input()
        continue
    if dimenzije_talona < 7 or broj_igraca < 1 or broj_igraca > 4 or dimenzije_talona % 2 == 0:
        print("Netacni podaci!")
        input()
    else:
        break
m = SparseMatrix(dimenzije_talona, dimenzije_talona)
figures = [generisi_figure(chr(97+i*4), chr(98+i*4), chr(99+i*4), chr(100+i*4)) for i in range(broj_igraca)]
broj_figura_na_talonu = [0 for i in range(broj_igraca)]
pocetne_koordinate = [(0, 0), (0, dimenzije_talona-1), (dimenzije_talona-1, 0), (dimenzije_talona-1, dimenzije_talona-1)]
player_index = 0
while True:
    print("Trenutni igrac je:", (player_index+1))
    ispis_talona(m, dimenzije_talona)
    print("Nisu prisutne na talonu:")
    print_figures(figures[player_index])
    if broj_figura_na_talonu[player_index] == 0:
        print('Bacite kockicu (tri puta bacate)')
        i = 0
        kockica = -1
        while i < 3 and kockica != 6:
            input()
            kockica = kocka()
            print('Dobili ste: ', kockica)
            i+=1
        if kockica == 6:
            broj_figura_na_talonu[player_index] += 1
            val = eject_figure(figures[player_index], player_index)
            i, j = pocetne_koordinate[player_index]
            m.add(i, j, val)
        input()
    else:
        print('Pritisnite ENTER da bacite kockicu')
        input()
        kockica = kocka()
        print('Dobili ste:', kockica)
        info = figure_info(m, player_index, kockica)
        for i in range(len(info)):
            simbol = info[i][0].symbol
            print(str(i+1)+') '+simbol)
        if len(info) == 0:
            print('Nemate validan potez trenutno!')
            input()
        while len(info) > 0:
            try:
                choice = 1
                choice = int(input())
            except Exception as e:
                pass
            if choice-1 < 0 or choice-1 > len(info)-1:
                continue
            simbol = info[choice-1][0].symbol
            koordinate = m.find_coords(simbol)
            if koordinate != (-1, -1):
                m.remove_by_value(simbol)
                red, kolona = koordinate
                if m.get(red, kolona) != 0:
                    sklonjena_figura = m.get(red, kolona)
                    index = get_belonging(sklonjena_figura.symbol)
                    broj_figura_na_talonu[index] -= 1
                    inject_figure(figures[index], sklonjena_figura.symbol)
                    print_figures(figures[index])
                    m.remove_by_value(sklonjena_figura.symbol)
                info[choice-1][0].travelled = info[choice-1][1][2]
                m.add(info[choice-1][1][0], info[choice-1][1][1], info[choice-1][0])
                break
            else:
                r, c = pocetne_koordinate[player_index]
                eject_figure(figures[player_index], player_index)
                m.add(r, c, info[choice-1][0])
                broj_figura_na_talonu[player_index] += 1
                break
    player_index = (player_index + 1) % broj_igraca
    os.system('cls')