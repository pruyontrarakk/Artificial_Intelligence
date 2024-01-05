import random
import time
import math
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        alpha = float('-inf')
        beta = float('inf')
        self.prev_time = time.process_time()
        move = None

        for depth in range(5):
            (move, _) = self.maximize(grid, depth, alpha, beta)

        return move[0]


    def maximize(self, grid, depth, alpha, beta):

        (max_child, max_utility) = (None, float('-inf'))

        if depth <= 0 or len(grid.getAvailableMoves()) == 0 or (time.process_time() - self.prev_time > 0.2):
            self.prev_time = time.process_time()
            return (None, self.eval(grid))

        for child in grid.getAvailableMoves():

            # print("Max Child", child[1].map, child[0])

            # Chance of 2 or 4
            (_, utility2) = self.minimize(child[1], depth - 1, alpha, beta, 2)
            (_, utility4) = self.minimize(child[1], depth - 1, alpha, beta, 4)
            utility = 0.9 * utility2 + 0.1 * utility4


            if utility > max_utility:
                (max_child, max_utility) = (child, utility)

            # alpha beta pruning
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

        return (max_child, max_utility)




    def minimize(self, grid, depth, alpha, beta, value):

        (min_child, min_utility) = (None, float('inf'))

        if depth <= 0 or len(grid.getAvailableCells()) == 0 or (time.process_time() - self.prev_time > 0.2):
            self.prev_time = time.process_time()
            return (None, self.eval(grid))

        for child in grid.getAvailableCells():

            grid.setCellValue(child, value)
            # print("Min Child", grid.map, child[0])
            (_, utility) = self.maximize(grid, depth-1, alpha, beta)
            grid.setCellValue(child, 0)
            if utility < min_utility:
                (min_child, min_utility) = (child, utility)

            # alpha beta pruning
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility

        return (min_child, min_utility)


    def eval(self, grid):
        return self.snake(grid) * 3.5 + self.smoothness(grid) * 1.5 + self.maxTile(grid)


    def snake(self, grid):
        points = 0
        weight_array = [
            [pow(4, 15), pow(4, 14), pow(4, 13), pow(4, 12)],
            [pow(4, 8), pow(4, 9), pow(4, 10), pow(4, 11)],
            [pow(4, 7), pow(4, 6), pow(4, 5), pow(4, 4)],
            [1, 4, -pow(4, 2), pow(4, 3)]
            ]

        max_weight = 0
        for i in range(4):
            weight = 0

            # make board array
            for row in range(4):
                for col in range(4):
                    weight = weight + (grid.map[row][col] * weight_array[row][col])

            if weight > max_weight:
                max_weight = weight

            #rotate weight array
            rotated_array = [[0] * 4 for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    rotated_array[j][4 - i - 1] = weight_array[i][j]
            weight_array = rotated_array

        if max_weight != 0:
            points = math.log2(max_weight)

        return points




    def smoothness(self, grid):
        point = 0

        for row in range(4):
            for col in range(3):
                current = grid.map[row][col]
                adjacent = grid.map[row][col + 1]
                if (current != 0 and adjacent != 0):
                    point += abs(current - adjacent)


        for row in range(3):
            for col in range(4):
                current = grid.map[row][col]
                adjacent = grid.map[row + 1][col]
                if (current != 0 and adjacent != 0):
                    point += abs(current - adjacent)

        if point != 0:
            point = -math.log2(point)

        return point




    def maxTile(self, grid):
        points = grid.getMaxTile()
        return math.log2(points)

