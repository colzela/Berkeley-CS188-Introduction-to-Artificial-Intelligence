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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        pos = currentGameState.getPacmanPosition()
        GhostStates = currentGameState.getGhostStates()
        ghostPosCurrent = GhostStates[0].getPosition()

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        disFood = []
        disGhost = []
        ghostPos = []
        foodPos = newFood.asList()

        for i in range(len(newGhostStates)):
            ghostPos.append(newGhostStates[i].getPosition())
        for ghost in ghostPos:
            disGhost.append(manhattanDistance(newPos, ghost))
        nearestGhost = min(disGhost)

        for food in foodPos:
            disFood.append(manhattanDistance(food, newPos))
        if len(disFood) != 0:
            nearestFood = min(disFood)
        else:
            nearestFood = 1

        score = nearestGhost/nearestFood**1.5 + 2*successorGameState.getScore()
        return score

def scoreEvaluationFunction(currentGameState: GameState):
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
        self.index = 0 # Pacman is always agent index 0
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
        def maxValue(state, depth):                # Pacman
            depth += 1

            if  state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = -float("inf")                      # initialize
            for action in state.getLegalActions(0):
                successorGameState = state.generateSuccessor(0, action)
                v = max(v, minValue(successorGameState, 1, depth))
            return v
        
        def minValue(state, ghostIndex, depth):     # ghost
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            v = float("inf")
            for action in state.getLegalActions(ghostIndex):
                successorGameState = state.generateSuccessor(ghostIndex, action)
                if ghostIndex == state.getNumAgents() - 1:
                    v = min(v, maxValue(successorGameState, depth))
                else:
                    v = min(v, minValue(successorGameState, ghostIndex+1, depth))
            return v

        legalMoves = gameState.getLegalActions(self.index)
        maximum = -float("inf")
        for action in legalMoves:
            successorGameState = gameState.generateSuccessor(self.index, action)
            score = minValue(successorGameState, 1, 0)
            if score > maximum:
                maximum = score
                result = action
        return result
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth, alpha, beta, actionList):   # actionList stores steps in the maxValue step with the last element corresponding to the first step 
            depth += 1
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            v= -float("inf")
            action = ""
            for action in state.getLegalActions(self.index):
                successorGameState = state.generateSuccessor(self.index, action)
                min = minValue(successorGameState, 1, depth, alpha, beta, actionList)
                if (min > v):
                    v = min
                    actions = action
                if v > beta:         # prune
                    actionList[0] = actions
                    return v 
                alpha = max(alpha, v)
            actionList[0] = actions
            return v

        def minValue(state, ghostIndex, depth, alpha, beta, actionList):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = float("inf")
            for action in state.getLegalActions(ghostIndex):
                successorGameState = state.generateSuccessor(ghostIndex, action)

                if ghostIndex == gameState.getNumAgents() - 1:
                    v = min(v, maxValue(successorGameState, depth, alpha, beta, actionList))
                    if v < alpha:   # prune
                        return v 
                    beta = min(beta, v)
                else:
                    v = min(v, minValue(successorGameState, ghostIndex+1, depth, alpha, beta, actionList))

                    if v < alpha:
                        return v
                    beta = min(v, beta)
            return v

        actionList = [""]           
        maxValue(gameState, -1, -float("inf"), float("inf"), actionList)
        result = actionList[0]
        return result

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth):
            depth += 1

            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = -float("inf")
            for action in state.getLegalActions(0):
                successorGameState = state.generateSuccessor(0, action)
                count = 0    # after one step of the Pacman count the num of state ghost can move, every state has the prob of 1/count
                for ghost in range(1, successorGameState.getNumAgents()):
                    count += len(successorGameState.getLegalActions(ghost))
                if count == 0:
                    v = max(v, expectValue(successorGameState, 1, depth))
                else:
                    v = max(v, expectValue(successorGameState, 1, depth)/count)
            return v

        def expectValue(state, ghostIndex, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            v = 0
            for action in state.getLegalActions(ghostIndex):
                successorGameState = state.generateSuccessor(
                    ghostIndex, action)
                if ghostIndex == state.getNumAgents() - 1:
                    v += maxValue(successorGameState, depth)
                else:
                    v += expectValue(successorGameState, ghostIndex+1, depth)
            return v
        
        legalMoves = gameState.getLegalActions(self.index)
        maximum = -float("inf")
        for action in legalMoves:
            successorGameState = gameState.generateSuccessor(self.index, action)
            count = 0
            for ghost in range(1, successorGameState.getNumAgents()):
                count += len(successorGameState.getLegalActions(ghost))
            if count == 0:
                score = expectValue(successorGameState, 1, 0)
            else:
                score = expectValue(successorGameState, 1, 0) / count
            if score > maximum:
                maximum = score
                result = action

        return result


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Just do some minor changes to the score evaluation function in Q1. We change 
    the score function so that it judge from the current state. When the Pacman
    gets closer to the nearest ghost, the score decreases quicker.
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    foodPos = food.asList()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    minScard = min(scaredTimes)
    disFood = []
    ghostPos = []
    disGhost = []
    score = 0

    for i in range(len(ghostStates)):
        ghostPos.append(ghostStates[i].getPosition())

    if currentGameState.isLose():
        return -float("inf")
    if pos in ghostPos:
        return -float("inf")

    for food in foodPos:
        disFood.append(manhattanDistance(food, pos))
    if len(disFood) != 0:
        nearestFood = min(disFood)
    else:
        nearestFood = 1  

    for i in range(len(ghostStates)):
        ghostPos.append(ghostStates[i].getPosition())
        for ghost in ghostPos:
            disGhost.append(manhattanDistance(pos, ghost))
    nearestGhost = min(disGhost)

    if nearestGhost < 3:
        score -= 2.5
    if nearestGhost < 2:
        score -= 10
    if nearestGhost < 2:
        score = -float("inf")

    if len(currentGameState.getCapsules()) < 2:
        score += 5

    if len(disGhost) == 0 or len(disFood) == 0:
        score += scoreEvaluationFunction(currentGameState) + 10
    else:
        score += scoreEvaluationFunction(currentGameState) + 10/nearestFood - nearestGhost 

    return score

# Abbreviation
better = betterEvaluationFunction
