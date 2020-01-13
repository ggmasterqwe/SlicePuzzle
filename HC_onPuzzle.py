#!/usr/bin/python3

# we are trying to solve the sliding-tiles puzzle
# with hill climbing algorithm

from random import randint
from copy import deepcopy as save_state
from node import Node, rout, show_order

right_order = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, None]]


def _p(num):
    if num < 0:
        return (num*(-1))
    return num


def _pos_2(num):
    for i in range(0, 3):
        for j in range(0, 3):
            if right_order[i][j] == num:
                return [i, j]

# first need to define our space:


class puzzle:
    def __init__(self):
        self.board = []
        self.generate_board()

# get the position of given number
    def _pos(self, num):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == num:
                    return [i, j]

# make a puzzle
    def generate_board(self):
        number = [1, 2, 3, 4, 5, 6, 7, 8, None]
        for v in range(0, 3):
            cl = []
            for i in range(0, 3):
                x = randint(0, len(number)-1)
                cl.append(number[x])
                number.remove(number[x])
            self.board.append(cl)

    def generate_solveable_board(self):
        self.board = save_state(right_order)
        f = open('moves.txt',"w+")
        f.write(str(self.board[0])+'\n')
        f.write(str(self.board[1])+'\n')
        f.write(str(self.board[2])+'\n\n')
        for i in range(0, 12093):
            valid_moves = self.valid_moves()
            gen = randint(0, len(valid_moves)-1)
            self.move(valid_moves[gen])
            f.write(str(self.board[0])+'\n')
            f.write(str(self.board[1])+'\n')
            f.write(str(self.board[2])+'\n\n')
        f.close()

# show the puzzle


    def show_board(self):
        board = self.board
        print('', board[0], '\n', board[1], '\n', board[2], '\n')


# function for move to new state for given new_pos([x,y])

    def move(self, pos2):
        # pos1 is empty
        pos1 = self.pos_of_empty()
        self.board[pos1[0]][pos1[1]] = self.board[pos2[0]][pos2[1]]
        self.board[pos2[0]][pos2[1]] = None


# find the location of empty place


    def pos_of_empty(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == None:
                    return [i, j]


# give all valid moves for puzzle


    def valid_moves(self):
        x, y = self.pos_of_empty()
        valid_moves = [[x-1, y], [x, y-1], [x+1, y], [x, y+1]]
        invalid_moves = []
        for pos in valid_moves:
            if pos[0] == -1 or pos[0] == 3 or pos[1] == -1 or pos[1] == 3:
                invalid_moves.append(pos)
        for pos in invalid_moves:
            valid_moves.remove(pos)
        return valid_moves


# check if its valid_move


    def is_valid_move(self, pos):
        valid_moves = self.valid_moves()
        x, y = pos[0], pos[1]
        if [x, y] in valid_moves:
            return True
        return False

# then we need estimate function to calculate the distance of
# each element from its currect position
    def estimate_fun(self):
        dis_list = []
        dis_sum = 0
        for x in self.board:
            for num in x:
                pos = self._pos(num)
                cor_pos = _pos_2(num)
                dis = _p(pos[1] - cor_pos[1]) + _p(pos[0] - cor_pos[0])
                if dis == 0:
                  dis_list.append(-1)
                dis_list.append(dis)
        for dis in dis_list:
            dis_sum += dis

        return dis_sum


class Agent:
    def __init__(self, p):
        self.p = p
        self.state = Node(value=save_state(self.p.board))
        self.starting_state = self.state
        self.seen_states = []

    def generate_states(self):
        self.state.value = save_state(self.p.board)
        valid_moves = self.p.valid_moves()
        for move in valid_moves:
            cur_state = save_state(self.state.value)
            self.p.move(move)
            if self.p.board in self.seen_states:
                self.p.board = cur_state
                continue
            new_child = Node(value=save_state(self.p.board),
                             parent=self.state,)
            self.state.add_children(new_child)
            self.p.board = cur_state

        self.state.seen = True

    def find_best_move(self, ):
        estimates = []
        best_state = None
        cur_state = save_state(self.state.value)
        for states in self.state.children:
            if states.seen is True:
                continue

            self.p.board = states.value
            val = self.p.estimate_fun()
            estimates.append(val)
            if val is min(estimates):
                best_state = states
            self.p.board = cur_state
        return best_state

    def solve(self):
        self.seen_states.append(self.state.value)
        print('starting_state: ')
        self.show_state(self.starting_state.value)
        while(True):
            # print('cur_state')
            # self.p.show_board()
            if self.p.board == right_order:
                self.show_path()
                return False
            if self.state.seen is False:
                self.generate_states()
            new_state = self.find_best_move()
            if new_state is None:
                if self.state.parent == None:
                    print('non solveable puzzle!')
                    return False
                new_state = self.state.parent
                self.p.board = new_state.value
                self.state = new_state
            else:
                self.p.board = new_state.value
                self.state.next_node = new_state
                self.state = new_state
                self.seen_states.append(save_state(new_state.value))

    def show_state(self, state):
        print('', state[0], '\n', state[1], '\n', state[2], '\n')

    def show_path(self):
        node = self.starting_state
        f = open('path.txt',"w+")
        i=0
        while(True):

            f.write(str(node.value[0])+'\n')
            f.write(str(node.value[1])+'\n')
            f.write(str(node.value[2])+'\n\n')
            if node.next_node != None:
                node = node.next_node
            else:
                f.close()
                print('number of changing:', i)
                return False
            i=i+1

p = puzzle()
p.generate_solveable_board()
ag = Agent(p)
ag.solve()
# my_board.estimate_fun()
