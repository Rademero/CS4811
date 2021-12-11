# naiveBayes.py
# -------------
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


import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in datum.keys() ]))

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        # ************
        #  Question 0
        # ************
        "*** YOUR CODE HERE ***"

        # Accuracy and K values are ints/float, priors and conditional probs are Counters
        bestAccuracy = bestK = 0
        bestPrior = bestCondP = None

        # Overarching prior, conditional prob, and count Counter objects
        mainP = util.Counter()
        mainCondP = util.Counter()
        mainCount = util.Counter()

        # Train those models! Pump those numbers! 
        for i in range(len(trainingData)):
            d = trainingData[i]
            l = trainingLabels[i]
            mainP[l] += 1
            for f, v in d.items():
                mainCount[(f, l)] += 1 
                if v > 0: mainCondP[(f, l)] += 1
        
        # Smoothing of parameter estimates
        for kval in kgrid:

            # Init prior, conditional prob, and count for each k val
            newPrior = util.Counter()
            newCondP = util.Counter()
            newCount = util.Counter()
            for k, v in mainP.items(): newPrior[k] += v
            for k, v in mainCount.items(): newCount[k] += v
            for k, v in mainCondP.items(): newCondP[k] += v

            # Smooth conditional prob
            for l in self.legalLabels:
                for f in self.features:
                    newCondP[(f, l)] += kval
                    # 0 and 1 values are already smooth
                    newCount[(f, l)] += kval*2

            # Normalization
            newPrior.normalize()
            for j, c in newCondP.items(): newCondP[j] = float(c/newCount[j])
        
            # Set priors and conditional probs for next k value
            self.prior = newPrior
            self.conditionalProb = newCondP
        
            # Get performance of k-value on validation data
            predictions = self.classify(validationData)
            accuracies = list()
            for i in range(len(validationLabels)): accuracies.append(predictions[i] == validationLabels[i])
            accuracy = accuracies.count(True)
        
            print(f"Performance when k={kval}: {100*float(accuracy/len(validationLabels))}% correct")
        
            if accuracy > bestAccuracy:
                bestAccuracy = accuracy
                bestPrior = newPrior
                bestCondP = newCondP
                bestK = kval
       
        print(f"Best value of k: {bestK}")
        self.prior = bestPrior
        self.conditionalProb = bestCondP

        # Do I get brownie points for using provided methods
        self.setSmoothing(bestK)


    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()
        # ************
        #  Question 0
        # ************
        "*** YOUR CODE HERE ***"
        for l in self.legalLabels:
            logJoint[l] = math.log(self.prior[l])
            for f, v in datum.items():
                if v > 0: logJoint[l] += math.log(self.conditionalProb[f, l])
                else: logJoint[l] += math.log(1-self.conditionalProb[f, l])
        return logJoint

