from math import inf as infinity
from random import choice
from random import seed as randomseed       # Paul Lu
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)

Andrew Samoil
CCID:  aisamoil
ID: 1621231
"""


class State():
    ''' This class is uses an object to change the current
        state of the board
    '''

    def __init__(self, state, HUMAN=-1, COMP=1):
        ''' initializes an object with attributes

        Arguments:
            state (list): is the current state of the board
            HUMAN (int): the hidden number representation for 
                         the user, used mainly in minimax algo

            COMP (int): hidden number representation for computer 
                        ,used mainly in minimax algo
        '''
        self.state = state
        self.HUMAN = HUMAN
        self.COMP = COMP


    def __str__(self):
        ''' Returns the current state in a string format
        '''
        return str(self.state)


    def __repr__(self):
        ''' Used as a hidden way of displaying information
            about the Object within this class
        '''
        return 'State({})'.format(self.state)


    def getHUMAN(self):
        ''' getter for the Human player number representation
        '''
        return self.HUMAN


    def getCOMP(self):
        ''' getter for the Computer player number representation 
        '''
        return self.COMP


    def getboard(self):
        ''' getter for the current board
        '''
        return self.state


    def update(self, update):
        ''' updates the state to the current board
        '''
        self.state = update
        pass


    def human_turn(self, c_choice, h_choice):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(empty_cells(self.state))
        if depth == 0 or game_over(self):
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        clean()
        print(f'Human turn [{h_choice}]')
        render(self.getboard(), c_choice, h_choice)

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = set_move(self.getboard(), coord[0], coord[1], self.getHUMAN())

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')


    def ai_turn(self, c_choice, h_choice):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(empty_cells(self.state))
        if depth == 0 or game_over(self):
            return

        clean()
        print(f'Computer turn [{c_choice}]')
        render(self.getboard(), c_choice, h_choice)

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, self.COMP)
            x, y = move[0], move[1]

        set_move(self.state, x, y, self.COMP)
        # Paul Lu.  Go full speed.
        # time.sleep(1)


    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or game_over(self):
            score = evaluate(self.state)
            return [-1, -1, score]

        for cell in empty_cells(self.state):
            x, y = cell[0], cell[1]
            self.state[x][y] = player
            score = self.minimax(depth - 1, -player)
            self.state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value
        return best


class Board():
    ''' Where the main game board and players will
        be stored in an object
    '''

    def __init__(self, HUMAN=-1, COMP=1, board=[[0, 0, 0],
                                                [0, 0, 0],
                                                [0, 0, 0],
                                                        ]):
        ''' Initializes attributes to be stored in an object

            Arguments:
                board (list): board to store the game
                HUMAN (int): number representation of human player
                COMP (int): number representation of computer player
        '''
        self.HUMAN = HUMAN
        self.COMP = COMP
        self.board = board


    def __str__(self):
        ''' returns the current board in a string format
        '''
        return str(self.board)


    def __repr__(self):
        ''' Used as a hidden way of displaying information
            about the Object within this class
        '''
        return 'Board({})'.format(self.board)


    def getboard(self):
        ''' getter used to return the current board
        '''
        return self.board


    def setboard(self, new):
        ''' setter used to set the new board as new,

            Arguments:
                new (list): new comes form the state class
                            and re-establishes the board
                            baised on new changes
        '''
        self.board = new
        pass


    def getHUMAN(self):
        ''' getter that returns the number representation of 
            human player
        '''
        return self.HUMAN


    def getCOMP(self):
        ''' getter that returns the number representation of 
            computer player
        '''
        return self.COMP


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, +1):
        score = +1
    elif wins(state, -1):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state.getboard(), state.getHUMAN()) or wins(state.getboard(), state.getCOMP())


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(cur, x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(cur):
        return True
    else:
        return False


def set_move(cur, x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(cur, x, y):
        cur[x][y] = player
        return True
    else:
        return False


def clean():
    """
    Clears the console
    """
    # Paul Lu.  Do not clear screen to keep output human readable.
    print()
    return

    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def changeBoards(game, gamestate):
    ''' Changes the gamestate state of the board to the 
        main board kept in game

        Arguments:
            game (obj): stores the actual game board
            gamestate (obj): stores the changed game state
                             that needs to become the new 
                             board
    '''
    game.setboard(gamestate.getboard())
    gamestate.update(game.getboard())
    pass

def main():
    """
    Main function that calls all functions
    """
    # Paul Lu.  Set the seed to get deterministic behaviour for each run.
    #       Makes it easier for testing and tracing for understanding.
    randomseed(274 + 2020)

    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    
    # Where class code begins

    game = Board()
    # game initialized and will contain the board and players

    gamestate = State(game.getboard())
    ''' takes the board of game and changes it basied on the
        moves of the player and computer
    '''

    # Main loop of this game
    # essentailly changed all to class logic
    while len(empty_cells(game.getboard())) > 0 and not game_over(game):
        if first == 'N':
            gamestate.ai_turn(c_choice, h_choice)
            changeBoards(game, gamestate)
            first = ''

        gamestate.human_turn(c_choice, h_choice)
        changeBoards(game, gamestate)

        gamestate.ai_turn(c_choice, h_choice)
        changeBoards(game, gamestate)

    # Game over message
    if wins(game.getboard(), game.getHUMAN()):
        clean()
        print(f'Human turn [{h_choice}]')
        render(game.getboard(), c_choice, h_choice)
        print('YOU WIN!')
    elif wins(game.getboard(), game.getCOMP()):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(game.getboard(), c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(game.getboard(), c_choice, h_choice)
        print('DRAW!')

    exit()

if __name__ == '__main__':
    main()
