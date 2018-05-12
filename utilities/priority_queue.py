import heapq


class PriorityQueue:
    def __init__(self):
        """
        Defines a Priority Queue
        PriorityQueue is based on Amit Patel's tutorial: "Implementation of A*" at:
        http://www.redblobgames.com/pathfinding/a-star/implementation.html
        """
        self.elements = []

    def empty(self):
        """
        Empty the priority queue
        """
        return len(self.elements) == 0

    def put(self, item, priority):
        """
        Put an item in the priority queue
        :param item: Object
            Item to insert in the Priority Queue
        :param priority: int
            Priority assigned to item
        """
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """
        Get the top element in the queue
        """
        return heapq.heappop(self.elements)[1]
