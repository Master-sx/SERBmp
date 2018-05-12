# A* Search is based on Amit Patel's tutorial: "Implementation of A*" at:
# http://www.redblobgames.com/pathfinding/a-star/implementation.html#sec-1-4
from utilities.priority_queue import PriorityQueue


def heuristic(a, b):
    # (x1, y1) = a
    # (x2, y2) = b
    # return abs(x1 - x2) + abs(y1 - y2)
    return 1  # currently no Euclidean metric


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_vertex in graph[current]:
            new_cost = cost_so_far[current] + heuristic(current, next_vertex)
            if next_vertex not in cost_so_far or new_cost < cost_so_far[next_vertex]:
                cost_so_far[next_vertex] = new_cost
                priority = new_cost + heuristic(goal, next_vertex)
                frontier.put(next_vertex, priority)
                came_from[next_vertex] = current

    return reconstruct_path(came_from, start, goal)


def reconstruct_path(came_from, start, goal):
    """
    Build path after searching
    :param came_from: node came from
    :param start: starting point
    :param goal: goal point
    :return: list representing path
    """
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    # path.append(start)  # optional
    path.reverse()  # optional
    path.pop(0)  # remove "start" from path as robot is already on it

    return path
