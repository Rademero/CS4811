# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class Node:
    """
    Node class for use in search algorithms. Node should contain a list of actions to get to current node
    The current state & the cost nessicary to make it there. The cosst will only be useful for usc & A* searches
    __author__ npromero
    """

    def __init__(self, state):
        self.actionList = []
        self.state = state
        self.cost = 0

    # Getters

    def getState(self):
        return self.state

    def getActions(self):
        return self.actionList

    def getDepth(self):
        return len(self.actionList)

    def getCost(self):
        return self.cost

    # Setters

    def setActionList(self, actions):
        self.actionList = actions[:]

    def setCost(self, cost):
        self.cost = cost
    # Helper Methods
"""
Expand method to help get a list of children. The method gets all of the legal children of a node given the node & the 
problem. The method then supplies the necessary information for each child
"""
def expand(node, problem):
    parent = node
    childList = []
    successors = problem.getSuccessors(node.getState())  # Getting children
    for i in range(len(successors)):
        successor = successors[i]
        # Setting necessary information
        child = Node(successor[0])
        child.setActionList(parent.getActions())
        child.actionList.append(successor[1])
        child.setCost(parent.getCost() + successor[2])
        childList.append(child)

    return childList


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    closed = set()  # A closed set is needed for graph search
    fringe = util.Stack()  # For the basic searches this should be the biggest change, Stack for FILO design
    fringe.push(Node(problem.getStartState()))

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()

        if problem.isGoalState(node.getState()):
            return node.getActions()
        if node.getState() not in closed:  # Making sure to not keep looping though the same nodes.
            closed.add(node.getState())
            for node in expand(node, problem):  # Getting successors for the fringe
                fringe.push(node)  # adding successor to fringe


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    fringe = util.PriorityQueue()  # Queue is useful for FIFO design
    node = Node(problem.getStartState())
    fringe.push(node, node.getDepth())  # tracking depth to ensure the shallowest depth is expanded first

    while True:
        if fringe.isEmpty():
            return []

        node = fringe.pop()

        if problem.isGoalState(node.getState()):
            return node.getActions()
        if node.getState() not in closed:
            closed.add(node.getState())
            for node in expand(node, problem):
                fringe.push(node, node.getDepth())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
