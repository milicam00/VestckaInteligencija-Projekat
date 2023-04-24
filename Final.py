from copy import deepcopy
from sys import stdout
import math

prethodnaStanja = []

pocIgrac = 1

def izborIgraca():
    print("Da li zelite da izaberete igraca koji ce da igra prvi?")
    print("Unesite \"da\" ukoliko zelite ili \"ne\" ukoliko ne zelite.")
    odgovor = input()
    if odgovor == "da":
        print("Unesite igraca koji ce da igra prvi: 1 da igra prvo x, a 2 da igra prvo o:")
        igrac = int(input())
        while not igrac==1 or not igrac==2:
            if igrac == 1 or igrac == 2:
                break
            print("Unesite igraca koji ce da igra prvi: 1 da igra prvo x, a 2 da igra prvo o:")
            print("MORATE DA UNESETE 1 ILI 2!!!")
            igrac = int(input())
        unesiVelicinuTable(igrac)
    elif odgovor=="ne":
        igrac = 1
        unesiVelicinuTable(igrac)
    else:
        print("Pogresan unos! Morate da unesite \"da\" ili \"ne\".")
        
def unesiVelicinuTable(pocetniIgrac):
    igrac = pocetniIgrac
    print("Unesite broj vrsta table:")
    brojVrsta = int(input())
    print("Unesite broj kolona table:")
    brojKolona = int(input())
    board = []
    krajIgre = False
    board = napraviTablu(board, brojVrsta, brojKolona)
    print("Igra je pocela")
    print("Pocetni igrac je " + str(igrac))
    ZapocniIgru(board, igrac, brojVrsta, brojKolona, krajIgre)
    
def napraviTablu(board, brojVrsta, brojKolona):
    for x in range(brojVrsta):
        lista = []
        for y in range(brojKolona):
            lista.append([x, y, None])
        board.append(lista)
    prikaziTrenutnoStanjeTable(board, brojVrsta, brojKolona)
    return board

def prikaziTrenutnoStanjeTable(board, brojVrsta, brojKolona):
    listaNaslov=[]
    for i in range(brojKolona):
        listaNaslov.append(i)
        if i==0:
            stdout.write("     " + str(i))
        else:
            stdout.write("    " + str(i))
    stdout.write("\n")
    for i in range(brojKolona):
        if i==0:
            stdout.write("    ___")
        else:
            stdout.write("  ___")
    stdout.write("\n")

    listaNaslova2 = []
    for i in range(brojVrsta):
        listaNaslova2.append(i)
#
    listaPodataka = []
    for i in range(brojVrsta):
        lista = []
        for j in range(brojKolona):
            lista.append(board[i][j][2])
        listaPodataka.append(lista)
    for i in range(brojVrsta):
        stdout.write(str(listaNaslova2[i]) + " |")
        for j in range(brojKolona):
            simbol = " " if listaPodataka[i][j] is None else listaPodataka[i][j]
            stdout.write("| " + str(simbol) + " |" )
        stdout.write("\n")
        
def ZapocniIgru(board, igrac, brojVrsta, brojKolona, krajIgre):
    while krajIgre == False:
        if igrac == 1:
            print("Unesite prvu koordinatu vaseg poteza:")
            pozicija1 = int(input())
            print("Unesite drugu kooridnatu vazeg poteza:")
            pozicija2 = int(input())
            humanMove = [pozicija1, pozicija2]
            board = odigrajPotez(board, humanMove, igrac, brojVrsta, brojKolona)
            print("Uspesno ste odigrali potez")
            prikaziTrenutnoStanjeTable(board, brojVrsta, brojKolona)
            igrac = 2
            krajIgre = proveraKrajIgre(board, igrac, brojVrsta, brojKolona)
        elif igrac == 2:
            botMove = minmax_alpha_beta(board, 3, igrac, brojVrsta, brojKolona, (None, -math.inf),(None, math.inf))
            board = odigrajPotez(board, botMove[0], igrac, brojVrsta, brojKolona)
            print("Bot je odigrao:" + str(botMove))
            print("Uspesno ste odigrali potez")
            prikaziTrenutnoStanjeTable(board, brojVrsta, brojKolona)
            igrac = 1
            krajIgre = proveraKrajIgre(board, igrac, brojVrsta, brojKolona)
            # print("Unesite prvu koordinatu vaseg poteza:")
            # pozicija1 = int(input())
            # print("Unesite drugu kooridnatu vazeg poteza:")
            # pozicija2 = int(input())
            # humanMove = [pozicija1, pozicija2]
            # board = odigrajPotez(board, humanMove, igrac, brojVrsta, brojKolona)
            # print("Uspesno ste odigrali potez")
            # prikaziTrenutnoStanjeTable(board, brojVrsta, brojKolona)
            # igrac = 1
            # krajIgre = proveraKrajIgre(board, igrac, brojVrsta, brojKolona)
    else:        
        print("Stigli ste do kraja igre")
        if igrac == 1:
            igrac = 2
        elif igrac == 2:
            igrac = 1
        print("Pobedio je igrac: " + str(igrac))
        exit()
    
def odigrajPotez(board, potez, igrac, brojVrsta, brojKolona):
    if validno(board, potez, igrac, brojVrsta, brojKolona):
        board = napraviNovoStanjeTable(board, igrac, potez, brojVrsta, brojKolona, True)
        return board
    else:
        print("Ovaj potez nije validan i ne moze da se odigra!")
        ZapocniIgru(board, igrac, brojVrsta, brojKolona, False)

def validno(board, potez, igrac, brojVrsta, brojKolona):
    if igrac == 1:
        return  (potez[0] < brojVrsta) and (potez[0] >= 0) and (potez[0]+1 >= 0) and (potez[0]+1 < brojVrsta) \
               and (potez[1] < brojKolona) and (potez[1] >= 0) and (board[potez[0]][potez[1]][2] == None) and (board[potez[0]+1][potez[1]][2] == None)
    elif igrac == 2:
        return  (potez[0] < brojVrsta) and (potez[0] >= 0) and (potez[1] < brojKolona) and (potez[1] >= 0) \
               and (potez[1]+1 < brojKolona) and (potez[1]+1>=0) and (board[potez[0]][potez[1]][2] == None) and (board[potez[0]][potez[1]+1][2] == None)

def napraviNovoStanjeTable(board, igrac, potez, brojVrsta, brojKolona, prethodna):
    pomocna=[]
    if prethodna:
        prethodnaStanja.append(board)
    pomocna = deepcopy(board)
    flag = False
    for x in range(brojVrsta):
        for y in range(brojKolona):
            if igrac==1:
                if(pomocna[x][y][0] == potez[0] and pomocna[x][y][1]==potez[1]):
                    pomocna[x][y][2] = 'x'
                    pomocna[x+1][y][2] = 'x'
                    flag=True
                    break
            elif igrac==2:
                if (pomocna[x][y][0] == potez[0] and pomocna[x][y][1] == potez[1]):
                    pomocna[x][y][2] = 'o'
                    pomocna[x][y+1][2] = 'o'
                    flag=True
                    break
        if flag == True:
            break
    return pomocna

def sviMoguciPoteziIgraca(board, igrac, brojVrsta, brojKolona):
    svaMogucaStanja = []
    for i in range(brojVrsta):
        for j in range(brojKolona):
            if validno(board, [i,j], igrac, brojVrsta, brojKolona):
                svaMogucaStanja.append([i, j])
    return svaMogucaStanja

def proveraKrajIgre(board, igrac, brojVrsta, brojKolona):
    if igrac == 1:
        for i in range(brojVrsta-1):
            for j in range(brojKolona):
                if board[i][j][2] is None and board[i+1][j][2] is None:
                    return False
        return True
    elif igrac == 2:
        for i in range(brojVrsta):
            for j in range(brojKolona-1):
                if board[i][j][2] is None and board[i][j+1][2] is None:
                    return False
        return True
    else:
        return True       

def minmax_alpha_beta(board, depth, igrac, brojVrsta, brojKolona, alpha=(None,-math.inf), beta=(None,math.inf)):
    if igrac == 1:
        return max_value(board, depth, igrac, brojVrsta, brojKolona, alpha, beta)
    elif igrac == 2:
        return min_value(board, depth, igrac, brojVrsta, brojKolona, alpha, beta)
    

def max_value(board, depth, igrac, brojVrsta, brojKolona, alpha, beta, potez=None):
    moguci_potezi2 = sviMoguciPoteziIgraca(board, igrac, brojVrsta, brojKolona)
    if depth==0 or len(moguci_potezi2)==0 or proveraKrajIgre(board, igrac, brojVrsta, brojKolona):
        return (potez, oceni(board, brojVrsta, brojKolona, igrac))
    else:
        for p in moguci_potezi2:
            board1 = odigrajPotez(board, p, igrac, brojVrsta, brojKolona)
            bestScore = min_value(board1, depth-1, 2 if igrac==1 else 1, brojVrsta, brojKolona, alpha, beta, p if potez is None else potez)
            alpha = max(alpha, bestScore, key=lambda x: x[1])
            
            if alpha[1] >= beta[1]:
                return beta
        return alpha

def min_value(board, depth, igrac, brojVrsta, brojKolona, alpha, beta, potez=None):
    moguci_potezi = sviMoguciPoteziIgraca(board, igrac, brojVrsta, brojKolona)
    if depth==0 or len(moguci_potezi)==0 or proveraKrajIgre(board, igrac, brojVrsta, brojKolona):
        return (potez, oceni(board, brojVrsta, brojKolona, igrac))
    for p in moguci_potezi:
        board1 = odigrajPotez(board, p, igrac, brojVrsta, brojKolona)
        bestScore = max_value(board1, depth-1, 1 if igrac==2 else 2, brojVrsta, brojKolona, alpha, beta, p if potez is None else potez)
        beta = min(beta, bestScore, key=lambda x: x[1])
            
        if beta[1] <= alpha[1]:
            return alpha
    return beta

def oceni(stanje, brojVrsta, brojKolona, igrac):
  
    heuristika = 0
    my_moves = len(sviMoguciPoteziIgraca(stanje, igrac, brojVrsta, brojKolona))
    if (igrac == 1):
        suprotni_igrac = 2
    else:
        suprotni_igrac = 1
    opponent_moves = len(sviMoguciPoteziIgraca(stanje, suprotni_igrac, brojVrsta, brojKolona))
    
    
    heuristika += my_moves - opponent_moves
    
    vertical_count = 0
    horizontal_count = 0
    for row in stanje:
        for cell in row:
            if cell[2] == 'x':
                vertical_count += 1
            elif cell[2] == 'o':
                horizontal_count += 1

    
    
    if vertical_count > horizontal_count:
        heuristika += (vertical_count + horizontal_count)
    elif horizontal_count > vertical_count:
        heuristika += - (vertical_count + horizontal_count)
    else:
     
        for row in range(len(stanje)):
            for col in range(len(stanje[0])):
                if stanje[row][col][2] == 'x':
                    if row == 0 or row == len(stanje) - 1:
                        heuristika += 5
                    if col == 0 or col == len(stanje[0]) - 1:
                        heuristika += 5
                elif stanje[row][col][2] == 'o':
                    if row == 0 or row == len(stanje) - 1:
                        heuristika -= 5
                    if col == 0 or col == len(stanje[0]) - 1:
                        heuristika -= 5
    
    if heuristika > 0 and igrac == 2:
        heuristika  = -heuristika
    elif heuristika <0 and igrac == 1:
        heuristika = -heuristika
     
    return heuristika 
    
def sviMogucaStanjaIgraca(igrac, board, brVrsta, brKolona):
    print("Board NA POCETKU: ")
    prikaziTrenutnoStanjeTable(board, brVrsta, brKolona)
    svaMogucaStanja = []
    pomocna1 = []
    for i in range(brVrsta):
        for j in range(brKolona):
            pomocna = []
            pomocna = deepcopy(board)
            if(validno(pomocna, [i,j], igrac, brVrsta, brKolona)):
                pomocna1 = napraviNovoStanjeTable(pomocna, igrac, [i,j], brVrsta, brKolona,False)
                svaMogucaStanja.append(((i, j),pomocna1))
    print("Board: ")
    prikaziTrenutnoStanjeTable(board, brVrsta, brKolona)

    print("SVI MOGUCI POTEZI: ")
    for n in svaMogucaStanja:
        print(n[0])
        prikaziTrenutnoStanjeTable(n[1], brVrsta, brKolona)
    return svaMogucaStanja
    
izborIgraca()