# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    # *********************
    #    Question 1
    # *********************
    def runValueIteration(self):
        # Write value iteration code here
        """ 
        Question 1: runValueIteration method 
        """
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            counter = util.Counter()
            for state in self.mdp.getStates():
                val = float("-inf")
                for action in self.mdp.getPossibleActions(state):
                    qval = self.computeQValueFromValues(state, action)
                    if qval > val:
                        val = qval
                    counter[state] = val
            self.values = counter


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # *********************
    #    Question 1
    # *********************
    def computeQValueFromValues(self, state, action):
        """
        Question 1 

          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qval = 0
        for nState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qval += prob*(self.mdp.getReward(state, action, nState)+(self.discount*self.values[nState]))
        return qval

    # *********************
    #    Question 1 
    # *********************
    def computeActionFromValues(self, state):
        """
        Question 1 

          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0: return None
        value = result = None
        
        for action in actions:
            temp = self.computeQValueFromValues(state, action)
            if value == None or temp > value:
                value = temp
                result = action
        
        return result

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    # *********************
    #    Question 4
    # *********************
    def runValueIteration(self):
        """
        Question 4
        """
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        size = len(states)
        updatedVal = util.Counter()
        for i in range(self.iterations):
            j = i % size;
            if self.mdp.isTerminal(states[j]):
                continue
            qval2 = -float("inf")
            for action in self.mdp.getPossibleActions(states[j]):
                qval = self.computeQValueFromValues(states[j], action)
                if qval > qval2:
                    qval2 = qval
            if qval2 == -float("inf"):
                qval2 = 0
            updatedVal[states[j]] = qval2
            self.values = updatedVal


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    # *********************
    #    Question 5 
    # *********************
    def runValueIteration(self):
        """
        Question 5 - Extra Credit
        """
        "*** YOUR CODE HERE ***"
        predecessors = {state: set() for state in self.mdp.getStates()}
        for origState in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(origState):
                for destState, prob in self.mdp.getTransitionStatesAndProbs(origState, action):
                    if prob != 0:
                        predecessors[destState].add(origState)
        minHeap = util.PriorityQueue()
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                continue
            maxQvalue = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
            diff = abs(maxQvalue - self.values[state])
            minHeap.push(item=state, priority=-diff)
        #
        for k in range(self.iterations):
            if minHeap.isEmpty():
                return
            state = minHeap.pop()
            if self.mdp.isTerminal(state):
                continue

            for action in self.mdp.getPossibleActions(state):
                self.qValues[(state, action)] = self.getQValue(state, action)
            self.values[state] = max([self.qValues[(state, action)] for action in self.mdp.getPossibleActions(state)])

            for predecessor in predecessors[state]:
                maxQvalue = max(
                    [self.getQValue(predecessor, action) for action in self.mdp.getPossibleActions(predecessor)])
                diff = abs(maxQvalue - self.values[predecessor])
                if diff > self.theta:
                    minHeap.update(item=predecessor, priority=-diff)