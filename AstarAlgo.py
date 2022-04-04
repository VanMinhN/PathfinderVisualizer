import pygame
import math
from queue import PriorityQueue
from PathFinder import h


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_Set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
