# ShortestPathSearch.py determines the shortest path of a given graph using Breadth-first search and determines
# the motion plan for our Arduino robot, which it stores in a queue. The resource used for creating
# the breadth-first search and queue class are listed below.
#
# Code for Breadth-First search and shortest path finder used from:
# http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
#
# Code for Queue Class from:
# http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaQueueinPython.html

import random
import serial


# ---------------------PySerial Enable------------------------

# ser = serial.Serial('/dev/ttyACM0', 9600)  # Establish the connection on a specific port


# ---------------------Queue class----------------------------

# Queue class that is for storing locations robot is going to.
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


# ----------------Graph and Motion Queue Setup----------------

# Graph with path that the serb will be following
graph = {'A': {'B', 'E', 'D'},
         'B': {'A', 'F', 'C'},
         'C': {'B', 'G', 'D'},
         'D': {'C', 'H', 'A'},
         'E': {'A'},
         'F': {'B'},
         'G': {'C'},
         'H': {'D'}}


# Selects random node from graph list  
def random_node_one():
    random_node = random.choice(list(graph.keys()))
    return random_node[0]


# Breadth-First Search
def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next_vertex in graph[vertex] - set(path):
            if next_vertex == goal:
                yield path + [next_vertex]
            else:
                queue.append((next_vertex, path + [next_vertex]))


# Finds shortest path
def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


# Converts Path into Motion Queue THEPROJECT.PY
def motion_plan(path):
    q1 = Queue()

    # Takes the current node and next node and stores the
    # commands the arduino has to complete to get to the next node.
    for node in range(0, len(path) - 1):
        # print (node)
        cur = path[node]
        nex = path[node + 1]
        # print (cur, nex)

        # Inner to Outer
        if ((cur == 'E' and nex == 'A') or
                (cur == 'F' and nex == 'B') or
                (cur == 'G' and nex == 'C') or
                (cur == 'H' and nex == 'D')):

            q1.enqueue(2)
            q1.enqueue(0)

        # Outer too Inner
        elif ((cur == 'A' and nex == 'E') or
              (cur == 'B' and nex == 'F') or
              (cur == 'C' and nex == 'G') or
              (cur == 'D' and nex == 'H')):

            q1.enqueue(1)
            q1.enqueue(0)

        # Clockwise
        elif ((cur == 'A' and nex == 'B') or
              (cur == 'B' and nex == 'C') or
              (cur == 'C' and nex == 'D') or
              (cur == 'D' and nex == 'A')):

            q1.enqueue(3)
            q1.enqueue(1)
            q1.enqueue(4)
            q1.enqueue(0)

        # Counter-Clockwise
        elif ((cur == 'B' and nex == 'A') or
              (cur == 'C' and nex == 'B') or
              (cur == 'D' and nex == 'C') or
              (cur == 'A' and nex == 'D')):

            q1.enqueue(4)
            q1.enqueue(1)
            q1.enqueue(3)
            q1.enqueue(0)

        # Default
        else:
            q1.enqueue(0)
        # end For loop
    return q1


# ------------------------Main--------------------------------

# Node the serb is starting at
starting_node = 'E'
ending_node = random_node_one()

# Picks ending node one time
for x in range(0, 1):
    print("Starting Node")
    print(starting_node)
    print("Ending Node")
    print(ending_node)

    # Valid path check (Start /= End)
    path = shortest_path(graph, starting_node, ending_node)
    while True:
        # HERE GIVE INFORMATION TO ROBOT, PARSE THROUGH NODES
        if not path:
            ending_node = random_node_one()
            path = shortest_path(graph, starting_node, ending_node)
            print("Empty Path")
            print("Starting Node")
            print(starting_node)
            print("Ending Node")
            print(ending_node)
        else:
            break

    # Create Queue for Arduino
    q2 = motion_plan(path)

    # Queue header
    print("\n\nQueue")

    # Printing Queue
    for index in range(0, q2.size()):
        print(q2.dequeue())

# -----------------------PySerial-----------------------------
# UNCOMMENT for PySerial
#
# print("dequeue")
# ser.write(q2.dequeue())
# while (True):
#     print(ser.readline())
#
# while (not q2.is_empty()):
#     print("it worked")
#
#     if (ser.readline() >= 0):
#         print("whyyy")
#         ser.write(q2.dequeue())
#         print(ser.readline())
#
# print("end queue")
# ser.write(q2.dequeue())
# ser.write()
# ser.readLine()
