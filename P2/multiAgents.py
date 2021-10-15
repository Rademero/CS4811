# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if action == "Stop":
            return -10;
        # set a return value
        total = successorGameState.getScore()
        # new position of pacman in a pair
        x, y = newPos
        # old position of pacman in a pair
        curX, curY = currentGameState.getPacmanPosition()

        # See if can kill ghost, runs if he can't
        i = 0
        for ghost in newGhostStates:
            gX, gY = newGhostStates[i].getPosition()
            # get distance
            Dist = abs(x - gX) + abs(y - gY)
            # if check if they are scared
            if newScaredTimes[i] < Dist + 5:
                # run
                if Dist < 2:
                    return int(-500)
            else:
                # kill
                total += 500
            i += 1

        # look for nearby food
        if newFood[x][y]:
            total += 200
        else:
            closest = 100;
            # find the closest to pos
            for food in newFood.asList():
                Dist = abs(x - food[0]) + abs(y - food[1])
                if Dist <= closest:
                    closest = Dist
            # is it worth going towrds
            if (closest > 1):
                total += 10 / (closest)
            else:
                total += 20

        return total


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        val = float("-inf")
        action = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            tmp = minimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)

            if tmp > val:
                val = tmp
                action = successor[0]
        return action


def minimax(agent, agentList, state, depth, evalFunc):
    if state.isLose() is True or depth <= 0 or state.isWin() is True:
        return evalFunc(state)

    if agent == 0:
        val = float("-inf")
    else:
        val = float("inf")

    actions = state.getLegalActions(agent)
    successors = [state.generateSuccessor(agent, action) for action in actions]
    for j in range(len(successors)):
        successor = successors[j];

        if agent == 0:

            val = max(val, minimax(agentList[agent + 1], agentList, successor, depth, evalFunc))
        elif agent == agentList[-1]:

            val = min(val, minimax(agentList[0], agentList, successor, depth - 1, evalFunc))
        else:

            val = min(val, minimax(agentList[agent + 1], agentList, successor, depth, evalFunc))

    return val


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max(float("-inf"), float("inf"), gameState, gameState.getLegalActions(0), 0, 0)[0]

    def max(self, alpha, beta, gameState, actions, depth, agentIndex):
        agentIndex = agentIndex + 1
        tmpMax = ("max", float("-inf"))

        # checking if agent index is out of bounds
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            # getting max
        for action in actions:
            tmpSuc = (
                    action, self.alphaBeta(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex,
                        alpha, beta))
            if tmpMax[1] <= tmpSuc[1]:
                tmpMax = tmpSuc
            if alpha < tmpMax[1]:
                alpha = tmpMax[1]
            if tmpMax[1] > beta:
                return tmpMax

        return tmpMax

    def min(self, alpha, beta, gameState, actions, depth, agentIndex):
        tmpMin = ("min", float("inf"))
        agentIndex = agentIndex + 1
        # checking if agent index is out of bounds
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0

        # getting min
        for action in actions:
            tempSuc = (action,
                    self.alphaBeta(depth + 1, gameState.generateSuccessor(agentIndex - 1, action), agentIndex,
                        alpha,
                        beta))
            if tmpMin[1] >= tempSuc[1]:
                tmpMin = tempSuc
            if beta > tmpMin[1]:
                beta = tmpMin[1]
            if tmpMin[1] < alpha:
                return tmpMin

        return tmpMin

    def alphaBeta(self, depth, gameState, agentIndex, alpha, beta):
        if gameState.isLose() or gameState.isWin() or (
                depth >= self.depth * gameState.getNumAgents()):
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.max(alpha, beta, gameState, gameState.getLegalActions(0), depth, 0)[1]
        else:
            return self.min(alpha, beta, gameState, gameState.getLegalActions(agentIndex), depth, agentIndex)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        @author ajdenofr
        """
        "*** YOUR CODE HERE ***"
        val = float("-inf")
        actions = gameState.getLegalActions(0)
        successors = [(action, gameState.generateSuccessor(0, action)) for action in actions]
        for successor in successors:
            tmp = self.expectimax(1, successor[1], self.depth)
            if tmp > val:
                val = tmp
                action = successor[0]
        return action

    def expectimax(self, agent, state, depth):

        # Terminal node, return evaluation function at node
        if state.isLose() or depth == 0 or state.isWin():
            return self.evaluationFunction(state)

        actions = state.getLegalActions(agent)
        successors = [state.generateSuccessor(agent, action) for action in actions] 
        nextAgent = (agent+1) % state.getNumAgents()
        nextDepth = depth-1 if nextAgent == 0 else depth

        # Player is moving, max node
        if agent == 0:
            val = float('-inf')
            for successor in successors:
                newVal = self.expectimax(nextAgent, successor, nextDepth)
                if newVal > val:
                    val = newVal

        # Adversary is moving, exp/min node
        else:
            val = 0
            for successor in successors:
                val += (1.0*self.expectimax(nextAgent, successor, nextDepth))/len(successors)

        return val

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:

    This heuristic is comprised of 5 things:
    
    The first is the current score of the game state
    The second is the minimum distance to a food pellet
    The third is the distance to the nearest bad ghost
    The fourth is the distance to the nearest scared (edible) ghost
    The fifth is the number of power pills left, AKA capsules

    They're all sort of arbitrarily weighted, I just felt that the
    primary goal of the game is to capture all food and maybe pellets,
    but eating edible ghosts is also important because they give a lot
    of points.

    @author ajdenofr
    """
    "*** YOUR CODE HERE ***"
    # To avoid min() exception on distToFood lambda
    if currentGameState.isLose(): return float("-inf")
    elif currentGameState.isWin(): return float("inf")

    # Position, score, capsules
    x, y = currentGameState.getPacmanPosition()
    total = currentGameState.getScore()
    capsLeft = len(currentGameState.getCapsules())

    # Food stuff
    foodList = currentGameState.getFood().asList()
    foodLeft = len(foodList)
    distToFood = min(map(lambda z: manhattanDistance((x,y), z), foodList))
     
    # Spooky ghost stuff
    scaredGhosts = badGhosts = list()
    for ghost in currentGameState.getGhostStates():
        dist = manhattanDistance((x, y), ghost.getPosition()) 
        # Add ghosts to appropriate lists, do not care if not within edible range
        if ghost.scaredTimer and ghost.scaredTimer < dist: scaredGhosts.append(dist)
        else: badGhosts.append(dist)
    distScaredGhost = min(scaredGhosts)
    distBadGhost = min(badGhosts)


    return (total - (distToFood) - (10*(1.0/(distBadGhost))) - (4*distScaredGhost)
            - (10*capsLeft) - (5*foodLeft))

# Abbreviation
better = betterEvaluationFunction
