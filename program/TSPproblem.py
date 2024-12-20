#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from itertools import permutations


class Problem:
    """Абстрактный базовый класс для формулировки задачи."""

    def __init__(self, initial=None, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Возвращает доступные действия для заданного состояния."""
        raise NotImplementedError

    def result(self, state, action):
        """Возвращает новое состояние после выполнения действия."""
        raise NotImplementedError

    def is_goal(self, state):
        """Проверяет, достигнуто ли целевое состояние."""
        return state == self.goal

    def action_cost(self, s, a, s1):
        """Возвращает стоимость выполнения действия."""
        return 1

    def h(self, node):
        """Возвращает эвристическую оценку стоимости из состояния в цель."""
        return 0


class TSPProblem(Problem):
    def __init__(self, cities, distances, initial):
        """
        :param cities: Список городов.
        :param distances: Матрица расстояний между городами.
        :param initial: Начальный город.
        """
        super().__init__(initial=initial)
        self.cities = cities
        self.distances = distances

    def actions(self, state):
        """Возвращает список доступных действий (следующий город)."""
        visited = set(state)
        return [city for city in self.cities if city not in visited]

    def result(self, state, action):
        """Возвращает новый маршрут после добавления города."""
        return state + (action,)

    def is_goal(self, state):
        """Цель достигнута, если все города посещены и вернулись в начальный.
        """
        return len(state) == len(self.cities) + 1 and state[0] == state[-1]

    def action_cost(self, s, a, s1):
        """Стоимость перехода между городами."""
        return self.distances[s[-1]][a]


def tsp_solver(problem):
    """Решатель задачи коммивояжера полным перебором."""
    start = problem.initial
    min_cost = math.inf
    best_path = None

    for perm in permutations(problem.cities):
        if perm[0] != start:
            continue

        path = perm + (start,)
        cost = sum(
            problem.distances[path[i]][path[i + 1]]
            for i in range(len(path) - 1)
        )

        if cost < min_cost:
            min_cost = cost
            best_path = path

    return best_path, min_cost


if __name__ == "__main__":
    cities = ["A", "B", "C", "D"]
    distances = {
        "A": {"A": 0, "B": 10, "C": 15, "D": 20},
        "B": {"A": 10, "B": 0, "C": 35, "D": 25},
        "C": {"A": 15, "B": 35, "C": 0, "D": 30},
        "D": {"A": 20, "B": 25, "C": 30, "D": 0},
    }
    initial = "A"

    problem = TSPProblem(cities=cities, distances=distances, initial=initial)
    solution, cost = tsp_solver(problem)
    print("Лучший маршрут:", solution)
    print("Стоимость маршрута:", cost)
