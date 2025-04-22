# Gemgem (Clone de Bejeweled)
# Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
# Contact : alain.ng.tech@gmail.com
# Licence : BSD Simplifiée
# Description : Jeu de puzzle où l'objectif est d'aligner trois gemmes ou plus
#               pour marquer des points et progresser dans les niveaux.

import random, time, pygame, sys, copy
from pygame.locals import *

# ---------------------- CONSTANTES ----------------------
FPS = 30  # Nombre d'images par seconde pour l'affichage
WINDOWWIDTH = 900  # Largeur de la fenêtre en pixels
WINDOWHEIGHT = 690  # Hauteur de la fenêtre en pixels

BOARDWIDTH = 11  # Nombre de colonnes du plateau
BOARDHEIGHT = 9  # Nombre de lignes du plateau
GEMIMAGESIZE = 64  # Taille des gemmes en pixels (largeur et hauteur)

NUMGEMIMAGES = 7  # Nombre de types de gemmes différentes
assert NUMGEMIMAGES >= 5  # Le jeu nécessite au moins 5 types pour fonctionner

NUMMATCHSOUNDS = 6  # Nombre de sons différents pour une combinaison réussie

MOVERATE = 25  # Vitesse des animations (1 à 100, plus grand = plus rapide)
DEDUCTSPEED = 0.8  # Réduction du score toutes les DEDUCTSPEED secondes

# Couleurs utilisées
PURPLE = (255, 0, 255)
LIGHTBLUE = (170, 190, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 240, 0)
BLACK = (0, 0, 0)
BROWN = (85, 65, 0)

HIGHLIGHTCOLOR = PURPLE  # Couleur de la bordure de la gemme sélectionnée
BGCOLOR = LIGHTBLUE  # Couleur de fond de l'écran
GRIDCOLOR = BLUE  # Couleur du plateau de jeu
GAMEOVERCOLOR = RED  # Couleur du texte "Game Over"
GAMEOVERBGCOLOR = BLACK  # Couleur de fond du texte "Game Over"
SCORECOLOR = BROWN  # Couleur du score affiché

# Marges pour centrer le plateau dans la fenêtre
XMARGIN = int((WINDOWWIDTH - GEMIMAGESIZE * BOARDWIDTH) / 2)
YMARGIN = int((WINDOWHEIGHT - GEMIMAGESIZE * BOARDHEIGHT) / 2)

# Directions possibles des gemmes
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

EMPTY_SPACE = -1  # Valeur utilisée pour représenter un espace vide
ROWABOVEBOARD = 'row above board'  # Représente une ligne au-dessus du plateau

background = pygame.image.load("back.jpg")
background = pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))

deco1 = pygame.image.load("deco1.png")
deco1 = pygame.transform.scale(deco1, (340, 300))
deco1 = pygame.transform.rotate(deco1, -30)

deco2 = pygame.image.load("deco2.png")
deco2 = pygame.transform.scale(deco2, (340, 300))
deco2 = pygame.transform.rotate(deco2, 30)

name = pygame.image.load("name.png")


# Variables pour les animations
deco1_x, deco1_y = -340, 500  # Position initiale de deco1
deco2_x, deco2_y = WINDOWWIDTH, 500  # Position initiale de deco2
name_x, name_y = WINDOWWIDTH // 2 - 250, -200  # Position initiale du nom
buttons_y = -100  # Position initiale des boutons
fade_alpha = 0  # Opacité initiale pour l'effet de fondu

# Variables pour la rotation
deco1_angle = -30  # Angle initial de deco1
deco2_angle = 30  # Angle initial de deco2

INAC = 0

pauseButton = None
quitButton = None
# ---------------------- FONCTION PRINCIPALE ----------------------
def main():

    """
    Fonction principale du jeu.
    
    Initialise Pygame, charge les ressources et démarre le jeu.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """

    global FPSCLOCK, DISPLAYSURF, GEMIMAGES, GAMESOUNDS, BASICFONT, BOARDRECTS, DEDUCTSPEED, MOVERATE, BOARDWIDTH, BOARDHEIGHT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('GEMGEM GAME')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 42)

    # Afficher le menu de sélection de difficulté
    difficulty, INAC = showDifficultyMenu()
    DEDUCTSPEED = difficulty['DEDUCTSPEED']
    MOVERATE = difficulty['MOVERATE']
    BOARDWIDTH = difficulty['BOARDWIDTH']
    BOARDHEIGHT = difficulty['BOARDHEIGHT']

    # Charger les images
    GEMIMAGES = []
    for i in range(1, NUMGEMIMAGES + 1):
        gemImage = pygame.image.load(f'gem{i}.png')
        if gemImage.get_size() != (GEMIMAGESIZE, GEMIMAGESIZE):
            gemImage = pygame.transform.smoothscale(gemImage, (GEMIMAGESIZE, GEMIMAGESIZE))
        GEMIMAGES.append(gemImage)

    # Charger les sons
    GAMESOUNDS = {}
    GAMESOUNDS['bad swap'] = pygame.mixer.Sound('badswap.wav')
    GAMESOUNDS['match'] = [pygame.mixer.Sound(f'match{i}.wav') for i in range(NUMMATCHSOUNDS)]
    GAMESOUNDS['explosion'] = pygame.mixer.Sound('badswap.wav')
    GAMESOUNDS['shuffle'] = pygame.mixer.Sound('badswap.wav')

    # Musique de fond
    pygame.mixer.music.load('back.mp3')
    pygame.mixer.music.play(-1)

    # Créer les rectangles pour chaque espace du plateau
    BOARDRECTS = []
    for x in range(BOARDWIDTH):
        BOARDRECTS.append([])
        for y in range(BOARDHEIGHT):
            r = pygame.Rect((XMARGIN + (x * GEMIMAGESIZE), YMARGIN + (y * GEMIMAGESIZE), GEMIMAGESIZE, GEMIMAGESIZE))
            BOARDRECTS[x].append(r)

    while True:
        runGame(INAC)


# ---------------------- MENU DE DIFFICULTÉ ----------------------

def showDifficultyMenu():

    """
    Affiche un menu de sélection de difficulté et retourne la configuration choisie.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
     
    global deco1_x, deco1_y, deco2_x, deco2_y, name_x, name_y, buttons_y, fade_alpha, deco1_angle, deco2_angle

    difficulty = None
    while difficulty is None:
        DISPLAYSURF.blit(background, (0, 0))

        # Animation de déplacement des éléments
        if deco1_x < -70:
            deco1_x += 10
        if deco2_x > 450:
            deco2_x -= 10
        if name_y < 40:
            name_y += 4
        if buttons_y < 200:
            buttons_y += 4

        # Animation de fondu
        if fade_alpha < 255:
            fade_alpha += 5

        # Animation de rotation
        deco1_angle += 0.08  # Augmenter l'angle de rotation
        deco2_angle -= 0.08  # Diminuer l'angle de rotation

        # Appliquer la rotation aux éléments
        rotated_deco1 = pygame.transform.rotate(deco1, deco1_angle)
        rotated_deco2 = pygame.transform.rotate(deco2, deco2_angle)

        # Appliquer l'opacité aux éléments
        rotated_deco1.set_alpha(fade_alpha)
        rotated_deco2.set_alpha(fade_alpha)
        name.set_alpha(fade_alpha)

        # Afficher les éléments avec leurs nouvelles positions, opacité et rotation
        DISPLAYSURF.blit(rotated_deco1, (deco1_x, deco1_y))
        DISPLAYSURF.blit(rotated_deco2, (deco2_x, deco2_y))
        DISPLAYSURF.blit(name, (name_x, name_y))

        # Boutons (identique à la version précédente)
        easyButton = pygame.Rect(WINDOWWIDTH // 2 - 100, buttons_y, 200, 50)
        pygame.draw.rect(DISPLAYSURF, GREEN, easyButton)
        drawText('Facile', BASICFONT, WHITE, DISPLAYSURF, WINDOWWIDTH // 2, buttons_y + 25)

        mediumButton = pygame.Rect(WINDOWWIDTH // 2 - 100, buttons_y + 100, 200, 50)
        pygame.draw.rect(DISPLAYSURF, BLUE, mediumButton)
        drawText('Moyen', BASICFONT, WHITE, DISPLAYSURF, WINDOWWIDTH // 2, buttons_y + 125)

        hardButton = pygame.Rect(WINDOWWIDTH // 2 - 100, buttons_y + 200, 200, 50)
        pygame.draw.rect(DISPLAYSURF, RED, hardButton)
        drawText('Difficile', BASICFONT, WHITE, DISPLAYSURF, WINDOWWIDTH // 2, buttons_y + 225)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                if easyButton.collidepoint(mouseX, mouseY):
                    difficulty = {'DEDUCTSPEED': 1.5, 'MOVERATE': 20, 'BOARDWIDTH': 8, 'BOARDHEIGHT': 8}
                    INAC = 3
                elif mediumButton.collidepoint(mouseX, mouseY):
                    difficulty = {'DEDUCTSPEED': 1.0, 'MOVERATE': 25, 'BOARDWIDTH': 10, 'BOARDHEIGHT': 8}
                    INAC = 5
                elif hardButton.collidepoint(mouseX, mouseY):
                    difficulty = {'DEDUCTSPEED': 0.5, 'MOVERATE': 30, 'BOARDWIDTH': 11, 'BOARDHEIGHT': 9}
                    INAC = 7

    return difficulty, INAC


# ---------------------- FONCTION D'AFFICHAGE DE TEXTE ----------------------
def drawText(text, font, color, surface, x, y):

    """
    Dessine du texte à l'écran.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# ---------------------- FONCTION DE JEU ----------------------
def runGame(INAC):

    """
    Fonction principale gérant la logique du jeu.
    
    Elle gère l'affichage, les événements (clics, touches, etc.), 
    la détection d'inactivité, la suggestion d'un mouvement, 
    le passage de niveau et la vérification de la fin de jeu.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """

    gameBoard = getBlankBoard()   # Initialisation d'un plateau vierge
    score = 0
    niveau = 1
    time_left = 920   # Temps de jeu en secondes
    last_time = time.time()
    lastMoveTime = time.time()   # Temps du dernier mouvement effectué
    firstSelectedGem = None
    lastMouseDownX = None
    lastMouseDownY = None
    gameIsOver = False
    # lastScoreDeduction = time.time()
    # clickContinueTextSurf = None

    fillBoardAndAnimate(gameBoard, [], score)

    while True:

        clickedSpace = None

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_BACKSPACE:
                return
            elif event.type == KEYUP and event.key == K_SPACE:
                pauseGame(gameBoard)  # Pause via la touche ESPACE
            
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                # Vérification si le clic est sur le bouton Pause
                if pauseButton is not None and pauseButton.collidepoint(mouseX, mouseY):
                    pauseGame(gameBoard)
                if gameIsOver:
                    return
                if event.pos == (lastMouseDownX, lastMouseDownY):
                    clickedSpace = checkForGemClick(event.pos)
                else:
                    firstSelectedGem = checkForGemClick((lastMouseDownX, lastMouseDownY))
                    clickedSpace = checkForGemClick(event.pos)
                    if not firstSelectedGem or not clickedSpace:
                        firstSelectedGem = None
                        clickedSpace = None
            elif event.type == MOUSEBUTTONDOWN:
                lastMouseDownX, lastMouseDownY = event.pos

        # Suggestion d'un mouvement si inactivité > inac
        if time.time() - lastMoveTime > INAC:
            suggestion = suggérerMouvement(gameBoard)
            if suggestion:
                afficherSuggestion(gameBoard, *suggestion)
            lastMoveTime = time.time()   # Réinitialisation après suggestion

        # Gestion de la sélection et de l'échange de gemmes
        if clickedSpace and not firstSelectedGem:
            firstSelectedGem = clickedSpace
        elif clickedSpace and firstSelectedGem:
            firstSwappingGem, secondSwappingGem = getSwappingGems(gameBoard, firstSelectedGem, clickedSpace)
            if firstSwappingGem == None and secondSwappingGem == None:
                firstSelectedGem = None
                continue

            boardCopy = getBoardCopyMinusGems(gameBoard, (firstSwappingGem, secondSwappingGem))
            animateMovingGems(boardCopy, [firstSwappingGem, secondSwappingGem], [], score)

            # Échange effectif des gemmes
            gameBoard[firstSwappingGem['x']][firstSwappingGem['y']] = secondSwappingGem['imageNum']
            gameBoard[secondSwappingGem['x']][secondSwappingGem['y']] = firstSwappingGem['imageNum']

            matchedGems = findMatchingGems(gameBoard)
            if matchedGems == []:
                # Si l'échange ne forme pas de combinaison, on le reviens
                GAMESOUNDS['bad swap'].play()
                animateMovingGems(boardCopy, [firstSwappingGem, secondSwappingGem], [], score)
                gameBoard[firstSwappingGem['x']][firstSwappingGem['y']] = firstSwappingGem['imageNum']
                gameBoard[secondSwappingGem['x']][secondSwappingGem['y']] = secondSwappingGem['imageNum']
            else:
                scoreAdd = 0
                lastMoveTime = time.time()
                while matchedGems != []:
                    points = []
                    for gemSet in matchedGems:
                        scoreAdd += (10 + (len(gemSet) - 3) * 10)
                        for gem in gemSet:
                            gameBoard[gem[0]][gem[1]] = EMPTY_SPACE
                        points.append({'points': scoreAdd, 'x': gem[0] * GEMIMAGESIZE + XMARGIN, 'y': gem[1] * GEMIMAGESIZE + YMARGIN})
                    random.choice(GAMESOUNDS['match']).play()
                    score += scoreAdd
                    fillBoardAndAnimate(gameBoard, points, score)
                    matchedGems = findMatchingGems(gameBoard)
            

            # Passage au niveau supérieur si le score atteint le seuil (100 * niveau)
            s = score
            for l in range(niveau):
                s -= l*100
            if s >= niveau * 100:
                niveau += 1
                gameBoard = getBlankBoard()
                transitNiveau(niveau)
                fillBoardAndAnimate(gameBoard, [], score)
                
            firstSelectedGem = None

            # Si aucun mouvement n'est possible, on recharge le plateau
            if not canMakeMove(gameBoard):
                gameBoard = getBlankBoard()
                fillBoardAndAnimate(gameBoard, [], score)

        # Mise à jour de l'affichage
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(gameBoard)
        drawNiveau(niveau)
        if firstSelectedGem != None:
            highlightSpace(firstSelectedGem['x'], firstSelectedGem['y'])
        drawPauseButton()  # Bouton de pause affiché en haut à droite
        # Fin de jeu : affichage du score final et arrêt de la musique
        if gameIsOver:
            afficherFin(score, niveau)
            return

       
        # Gestion du temps
        current_time = time.time()
        if current_time - last_time >= 1:
            time_left -= 1
            last_time = current_time
        if time_left <= 0:
            gameIsOver = True
        if time_left >= 0:
            drawTime(time_left)        

        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# ---------------------- FONCTIONS D'AFFICHAGE ----------------------
def drawTime(time_left):
    """
    Affiche le temps restant en haut à gauche.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    timeSurf = BASICFONT.render(f"Temps: {time_left}", 1, SCORECOLOR)
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (10, 10)
    DISPLAYSURF.blit(timeSurf, timeRect)


def drawScore(score):
    """
    Affiche le score du joueur en bas à gauche.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    scoreImg = BASICFONT.render(f"Score: {score}", 1, SCORECOLOR)
    scoreRect = scoreImg.get_rect()
    scoreRect.bottomleft = (WINDOWWIDTH // 2 - 50, WINDOWHEIGHT - 6)
    DISPLAYSURF.blit(scoreImg, scoreRect)


def drawNiveau(niveau):
    """
    Affiche le niveau actuel en haut à gauche (sous le temps).
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    niveauSurf = BASICFONT.render(f"Niveau: {niveau}", 1, SCORECOLOR)
    niveauRect = niveauSurf.get_rect()
    niveauRect.topleft = (400, 10)
    DISPLAYSURF.blit(niveauSurf, niveauRect)


def drawPauseButton():
    """
    Dessine le bouton de pause en haut à droite.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    global pauseButton
    pauseButton = pygame.Rect(WINDOWWIDTH - 130, 10, 120, 40)
    pygame.draw.rect(DISPLAYSURF, RED, pauseButton)
    text = BASICFONT.render("Pause", True, WHITE)
    textRect = text.get_rect(center=pauseButton.center)
    DISPLAYSURF.blit(text, textRect)



# ---------------------- FONCTIONS DE GESTION DES GEMMES ----------------------

def getSwappingGems(board, firstXY, secondXY):
    """
    Détermine si deux gemmes (aux coordonnées firstXY et secondXY) sont adjacentes et
    définit leur direction d'échange.
    
    Retourne un tuple (première gemme, deuxième gemme) ou (None, None) si elles ne sont pas
    adjacentes.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """

    firstGem = {'imageNum': board[firstXY['x']][firstXY['y']],
                'x': firstXY['x'],
                'y': firstXY['y']}
    secondGem = {'imageNum': board[secondXY['x']][secondXY['y']],
                 'x': secondXY['x'],
                 'y': secondXY['y']}
    highlightedGem = None
    if firstGem['x'] == secondGem['x'] + 1 and firstGem['y'] == secondGem['y']:
        firstGem['direction'] = LEFT
        secondGem['direction'] = RIGHT
    elif firstGem['x'] == secondGem['x'] - 1 and firstGem['y'] == secondGem['y']:
        firstGem['direction'] = RIGHT
        secondGem['direction'] = LEFT
    elif firstGem['y'] == secondGem['y'] + 1 and firstGem['x'] == secondGem['x']:
        firstGem['direction'] = UP
        secondGem['direction'] = DOWN
    elif firstGem['y'] == secondGem['y'] - 1 and firstGem['x'] == secondGem['x']:
        firstGem['direction'] = DOWN
        secondGem['direction'] = UP
    else:
        # These gems are not adjacent and can't be swapped.
        return None, None
    return firstGem, secondGem


def getBlankBoard():
    """
    Crée et retourne un plateau vierge.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)
    return board



def canMakeMove(board):
    """
    Vérifie si le plateau permet encore de faire un mouvement menant à une combinaison.
    
    Retourne True si un mouvement est possible, sinon False.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    # Return True if the board is in a state where a matching
    # move can be made on it. Otherwise return False.

    # The patterns in oneOffPatterns represent gems that are configured
    # in a way where it only takes one move to make a triplet.
    oneOffPatterns = (((0,1), (1,0), (2,0)),
                      ((0,1), (1,1), (2,0)),
                      ((0,0), (1,1), (2,0)),
                      ((0,1), (1,0), (2,1)),
                      ((0,0), (1,0), (2,1)),
                      ((0,0), (1,1), (2,1)),
                      ((0,0), (0,2), (0,3)),
                      ((0,0), (0,1), (0,3)))

    # The x and y variables iterate over each space on the board.
    # If we use + to represent the currently iterated space on the
    # board, then this pattern: ((0,1), (1,0), (2,0))refers to identical
    # gems being set up like this:
    #
    #     +A
    #     B
    #     C
    #
    # That is, gem A is offset from the + by (0,1), gem B is offset
    # by (1,0), and gem C is offset by (2,0). In this case, gem A can
    # be swapped to the left to form a vertical three-in-a-row triplet.
    #
    # There are eight possible ways for the gems to be one move
    # away from forming a triple, hence oneOffPattern has 8 patterns.

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            for pat in oneOffPatterns:
                # check each possible pattern of "match in next move" to
                # see if a possible move can be made.
                if (getGemAt(board, x+pat[0][0], y+pat[0][1]) == \
                    getGemAt(board, x+pat[1][0], y+pat[1][1]) == \
                    getGemAt(board, x+pat[2][0], y+pat[2][1]) != None) or \
                   (getGemAt(board, x+pat[0][1], y+pat[0][0]) == \
                    getGemAt(board, x+pat[1][1], y+pat[1][0]) == \
                    getGemAt(board, x+pat[2][1], y+pat[2][0]) != None):
                    return True # return True the first time you find a pattern
    return False


def drawMovingGem(gem, progress):
    """
    Dessine une gemme en mouvement selon sa direction et le progrès de l'animation.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    # Draw a gem sliding in the direction that its 'direction' key
    # indicates. The progress parameter is a number from 0 (just
    # starting) to 100 (slide complete).
    movex = 0
    movey = 0
    progress *= 0.01

    if gem['direction'] == UP:
        movey = -int(progress * GEMIMAGESIZE)
    elif gem['direction'] == DOWN:
        movey = int(progress * GEMIMAGESIZE)
    elif gem['direction'] == RIGHT:
        movex = int(progress * GEMIMAGESIZE)
    elif gem['direction'] == LEFT:
        movex = -int(progress * GEMIMAGESIZE)

    basex = gem['x']
    basey = gem['y']
    if basey == ROWABOVEBOARD:
        basey = -1

    pixelx = XMARGIN + (basex * GEMIMAGESIZE)
    pixely = YMARGIN + (basey * GEMIMAGESIZE)
    r = pygame.Rect( (pixelx + movex, pixely + movey, GEMIMAGESIZE, GEMIMAGESIZE) )
    DISPLAYSURF.blit(GEMIMAGES[gem['imageNum']], r)


def pullDownAllGems(board):
    """
    Fait descendre les gemmes pour combler les espaces vides en dessous.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    for x in range(BOARDWIDTH):
        gemsInColumn = []
        for y in range(BOARDHEIGHT):
            if board[x][y] != EMPTY_SPACE:
                gemsInColumn.append(board[x][y])
        board[x] = ([EMPTY_SPACE] * (BOARDHEIGHT - len(gemsInColumn))) + gemsInColumn


def getGemAt(board, x, y):
    """
    Retourne la gemme à la position (x, y) si elle existe, sinon None.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    if x < 0 or y < 0 or x >= BOARDWIDTH or y >= BOARDHEIGHT:
        return None
    else:
        return board[x][y]


def getDropSlots(board):
    """
    Crée une "fente de chute" pour chaque colonne et y insère le nombre
    de gemmes manquantes.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    boardCopy = copy.deepcopy(board)
    pullDownAllGems(boardCopy)

    dropSlots = []
    for i in range(BOARDWIDTH):
        dropSlots.append([])

    # count the number of empty spaces in each column on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT-1, -1, -1): # start from bottom, going up
            if boardCopy[x][y] == EMPTY_SPACE:
                possibleGems = list(range(len(GEMIMAGES)))
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    # Narrow down the possible gems we should put in the
                    # blank space so we don't end up putting an two of
                    # the same gems next to each other when they drop.
                    neighborGem = getGemAt(boardCopy, x + offsetX, y + offsetY)
                    if neighborGem != None and neighborGem in possibleGems:
                        possibleGems.remove(neighborGem)

                newGem = random.choice(possibleGems)
                boardCopy[x][y] = newGem
                dropSlots[x].append(newGem)
    return dropSlots


def findMatchingGems(board):
    """
    Cherche et retourne les combinaisons de gemmes identiques (au moins 3 en ligne)
    à supprimer du plateau.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    gemsToRemove = [] # a list of lists of gems in matching triplets that should be removed
    boardCopy = copy.deepcopy(board)

    # loop through each space, checking for 3 adjacent identical gems
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # look for horizontal matches
            if getGemAt(boardCopy, x, y) == getGemAt(boardCopy, x + 1, y) == getGemAt(boardCopy, x + 2, y) and getGemAt(boardCopy, x, y) != EMPTY_SPACE:
                targetGem = boardCopy[x][y]
                offset = 0
                removeSet = []
                while getGemAt(boardCopy, x + offset, y) == targetGem:
                    # keep checking if there's more than 3 gems in a row
                    removeSet.append((x + offset, y))
                    boardCopy[x + offset][y] = EMPTY_SPACE
                    offset += 1
                gemsToRemove.append(removeSet)

            # look for vertical matches
            if getGemAt(boardCopy, x, y) == getGemAt(boardCopy, x, y + 1) == getGemAt(boardCopy, x, y + 2) and getGemAt(boardCopy, x, y) != EMPTY_SPACE:
                targetGem = boardCopy[x][y]
                offset = 0
                removeSet = []
                while getGemAt(boardCopy, x, y + offset) == targetGem:
                    # keep checking, in case there's more than 3 gems in a row
                    removeSet.append((x, y + offset))
                    boardCopy[x][y + offset] = EMPTY_SPACE
                    offset += 1
                gemsToRemove.append(removeSet)

    return gemsToRemove


def highlightSpace(x, y):
    """
    Met en surbrillance la case de coordonnées (x, y) sur le plateau.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, BOARDRECTS[x][y], 4)


def getDroppingGems(board):
    """
    Identifie les gemmes qui doivent descendre pour combler les espaces vides.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    boardCopy = copy.deepcopy(board)
    droppingGems = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 2, -1, -1):
            if boardCopy[x][y + 1] == EMPTY_SPACE and boardCopy[x][y] != EMPTY_SPACE:
                # This space drops if not empty but the space below it is
                droppingGems.append( {'imageNum': boardCopy[x][y], 'x': x, 'y': y, 'direction': DOWN} )
                boardCopy[x][y] = EMPTY_SPACE
    return droppingGems


def animateMovingGems(board, gems, pointsText, score):
    """
    Anime le déplacement des gemmes sur le plateau.
    
    pointsText est une liste de dictionnaires contenant des clés 'points', 'x' et 'y'
    pour l'affichage des points.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    progress = 0 # progress at 0 represents beginning, 100 means finished.
    while progress < 100: # animation loop
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        for gem in gems: # Draw each gem.
            drawMovingGem(gem, progress)
        drawScore(score)
        for pointText in pointsText:
            pointsSurf = BASICFONT.render(str(pointText['points']), 1, SCORECOLOR)
            pointsRect = pointsSurf.get_rect()
            pointsRect.center = (pointText['x'], pointText['y'])
            DISPLAYSURF.blit(pointsSurf, pointsRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        progress += MOVERATE # progress the animation a little bit more for the next frame


def moveGems(board, movingGems):
    """
    Met à jour le plateau en déplaçant les gemmes selon leur direction.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    for gem in movingGems:
        if gem['y'] != ROWABOVEBOARD:
            board[gem['x']][gem['y']] = EMPTY_SPACE
            movex = 0
            movey = 0
            if gem['direction'] == LEFT:
                movex = -1
            elif gem['direction'] == RIGHT:
                movex = 1
            elif gem['direction'] == DOWN:
                movey = 1
            elif gem['direction'] == UP:
                movey = -1
            board[gem['x'] + movex][gem['y'] + movey] = gem['imageNum']
        else:
            # gem is located above the board (where new gems come from)
            board[gem['x']][0] = gem['imageNum'] # move to top row


def fillBoardAndAnimate(board, points, score):
    """
    Remplit le plateau de gemmes manquantes en simulant la gravité
    et anime la descente des gemmes.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    dropSlots = getDropSlots(board)
    while dropSlots != [[]] * BOARDWIDTH:
        # do the dropping animation as long as there are more gems to drop
        movingGems = getDroppingGems(board)
        for x in range(len(dropSlots)):
            if len(dropSlots[x]) != 0:
                # cause the lowest gem in each slot to begin moving in the DOWN direction
                movingGems.append({'imageNum': dropSlots[x][0], 'x': x, 'y': ROWABOVEBOARD, 'direction': DOWN})

        boardCopy = getBoardCopyMinusGems(board, movingGems)
        animateMovingGems(boardCopy, movingGems, points, score)
        moveGems(board, movingGems)

        # Make the next row of gems from the drop slots
        # the lowest by deleting the previous lowest gems.
        for x in range(len(dropSlots)):
            if len(dropSlots[x]) == 0:
                continue
            board[x][0] = dropSlots[x][0]
            del dropSlots[x][0]


def checkForGemClick(pos):
    """
    Vérifie si le clic de la souris se trouve sur une case du plateau.
    
    Retourne un dictionnaire contenant les coordonnées 'x' et 'y'
    ou None si le clic n'est pas sur le plateau.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if BOARDRECTS[x][y].collidepoint(pos[0], pos[1]):
                return {'x': x, 'y': y}
    return None # Click was not on the board.


def drawBoard(board):
    """
    Dessine le plateau de jeu et toutes les gemmes.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            pygame.draw.rect(DISPLAYSURF, GRIDCOLOR, BOARDRECTS[x][y], 1)
            gemToDraw = board[x][y]
            if gemToDraw != EMPTY_SPACE:
                DISPLAYSURF.blit(GEMIMAGES[gemToDraw], BOARDRECTS[x][y])


def getBoardCopyMinusGems(board, gems):
    """
    Retourne une copie du plateau avec certaines gemmes (passées dans la liste gems)
    retirées.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    boardCopy = copy.deepcopy(board)

    # Remove some of the gems from this board data structure copy.
    for gem in gems:
        if gem['y'] != ROWABOVEBOARD:
            boardCopy[gem['x']][gem['y']] = EMPTY_SPACE
    return boardCopy



# ---------------------- FONCTIONS POUR LA PAUSE ----------------------

def pauseGame(board):
    """
    Met le jeu en pause, affiche l'écran de pause et met la musique en pause.
    Le jeu reprend lorsque l'utilisateur appuie sur ESPACE ou clique sur "Reprendre".
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    paused = True
    pygame.mixer.music.pause()   # Met la musique en pause
    drawBoard(board)
    drawPauseScreen()

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE:
                paused = False
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                if pauseButton.collidepoint(mouseX, mouseY):  # Clique sur le bouton
                    paused = False
                if quitButton.collidepoint(mouseX, mouseY):  # Clique sur le bouton
                    main()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pygame.mixer.music.unpause()   # Reprend la musique après la pause

def drawPauseScreen():
    """
    Affiche l'écran de pause avec le texte "PAUSE" et un bouton "Reprendre".
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    pauseText = BASICFONT.render("VOTRE PARTIE EST EN PAUSE", True, GAMEOVERCOLOR)
    textRect = pauseText.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3))
    DISPLAYSURF.blit(pauseText, textRect)

    # Bouton "Reprendre"
    global pauseButton
    global quitButton
    pauseButton = pygame.Rect(WINDOWWIDTH // 2 - 110, WINDOWHEIGHT // 2, 220, 50)
    pygame.draw.rect(DISPLAYSURF, GREEN, pauseButton)
    text = BASICFONT.render("Reprendre", True, WHITE)
    textRect = text.get_rect(center=pauseButton.center)
    DISPLAYSURF.blit(text, textRect)

    quitButton = pygame.Rect(WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 2 + 100, 200, 50)
    pygame.draw.rect(DISPLAYSURF, RED, quitButton)
    text = BASICFONT.render("Quitter", True, WHITE)
    textRect = text.get_rect(center=quitButton.center)
    DISPLAYSURF.blit(text, textRect)

    pygame.display.update()


# ---------------------- FONCTIONS DE SUGGESTION DE MOUVEMENT ----------------------
def suggérerMouvement(board):
    """
    Cherche et retourne une paire de gemmes échangeables qui permettraient
    de former une combinaison.
    
    Retourne un tuple ((x1, y1), (x2, y2)) ou None si aucun mouvement n'est trouvé.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if x < BOARDWIDTH - 1:
                # Essayer d'échanger avec la gemme à droite
                if mouvementValide(board, x, y, x + 1, y):
                    return (x, y), (x + 1, y)
            if y < BOARDHEIGHT - 1:
                # Essayer d'échanger avec la gemme en dessous
                if mouvementValide(board, x, y, x, y + 1):
                    return (x, y), (x, y + 1)
    return None  # Aucun mouvement trouvé


def mouvementValide(board, x1, y1, x2, y2):
    """
    Teste si l'échange des gemmes aux positions (x1, y1) et (x2, y2)
    aboutit à une combinaison.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]  # Échange
    foundMatch = findMatchingGems(board)  # Vérifie s'il y a un match
    board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]  # Réinitialise
    return foundMatch != []


def afficherSuggestion(gameBoard, gem1, gem2):
    """
    Affiche une suggestion de mouvement en surlignant deux gemmes suggérées.
    Le clignotement se fait pendant quelques secondes.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    for _ in range(3):  # Clignotement rapide
        drawBoard(gameBoard)
        pygame.draw.rect(DISPLAYSURF, RED, BOARDRECTS[gem1[0]][gem1[1]], 4)
        pygame.draw.rect(DISPLAYSURF, RED, BOARDRECTS[gem2[0]][gem2[1]], 4)
        pygame.display.update()
        time.sleep(0.3)
        drawBoard(gameBoard)
        pygame.display.update()
        time.sleep(0.03)


# ---------------------- FONCTION DE TRANSITION DE NIVEAU ----------------------
def transitNiveau(niveau):
    """
    Affiche le message "NIVEAU X" au centre de l'écran avant de recharger le plateau.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    texte = f"NIVEAU {niveau}"
    niveauSurf = BASICFONT.render(texte, True, RED)
    niveauRect = niveauSurf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
    DISPLAYSURF.blit(niveauSurf, niveauRect)

    pygame.display.update()
    time.sleep(2)

# ---------------------- FONCTION DE FIN DE JEU ----------------------
def afficherFin(score, niveau):
    """
    Affiche le message de fin de jeu avec le score final et le niveau atteint.
    Arrête la musique et attend quelques secondes avant de retourner au menu principal.
    
    Auteur : ALAIN GILDAS NGUEUDJANG DJOMO
    """
    pygame.mixer.music.stop()   # Arrête la musique
    DISPLAYSURF.blit(background, (0,0))
    message = f"Fin du jeu"
    textSurf = BASICFONT.render(message, 1, GAMEOVERCOLOR)
    textRect = textSurf.get_rect() 
    textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 200)
    DISPLAYSURF.blit(textSurf, textRect)

    message = f"Score: {score}"
    textSurf = BASICFONT.render(message, 1, BLUE)
    textRect = textSurf.get_rect()
    textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 60)
    DISPLAYSURF.blit(textSurf, textRect)

    message = f"Niveau atteint: {niveau}"
    textSurf = BASICFONT.render(message, 1, BLUE)
    textRect = textSurf.get_rect()
    textRect.center = (WINDOWWIDTH // 2 , WINDOWHEIGHT // 2 + 60)
    DISPLAYSURF.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(3)  # Pause avant de revenir au menu
    main()



# ---------------------- POINT D'ENTRÉE ----------------------
if __name__ == '__main__':
    main()
