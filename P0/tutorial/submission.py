# submission.py
# ----------------
# Attribution Information: This part of the project was adapted from CS221 and 
# the PacMan Projects. 
# For the PacMan Projects: 
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
# 08-2020
 

from __future__ import print_function
import math 
import collections
import shop


############################################################
# Question 1 - addition 

def add(a, b): 
    "Return the sum of a and b"
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE 
    return a + b
    # END_YOUR_CODE


############################################################
# Question 2 - buyLotsOfFruit 
fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order. If some fruit is not in list, print an error 
    message and return None.
    """
    totalCost = 0.0
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE
    for item in orderList:
        fruit = item[0]
        # If fruit in order, add price of that many pounds of the fruit
        if fruit in fruitPrices.keys():
            subCost = item[1] * fruitPrices.get(fruit)
            totalCost += subCost
    return totalCost
    # END_YOUR_CODE


############################################################
# Question 3 - shopSmart 

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops

    Return the FruitShop where your order costs the least.
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE
    tierlist = {}
    for shop in fruitShops:
        # Add shop and order price at shop to dict
        calculated = {shop: shop.getPriceOfOrder(orderList)}
        tierlist.update(calculated)
    # return name of shop with minimum order price
    return min(tierlist, key=tierlist.get)
    # END_YOUR_CODE


############################################################
# Question 4 - findAlphabetLastWord 

def findAlphabetLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return sorted(text.split())[-1]
    # END_YOUR_CODE


############################################################
# Question 5 - euclideanDistance 

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return math.sqrt(((loc1[0]-loc2[0])**2)+((loc1[1]-loc2[1])**2))
    # END_YOUR_CODE


############################################################
# Question 6 - findSingletonWords

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    If no singleton words exist return the emptyset.
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    counts = {}
    for word in text.split():
        # Count words in split text, add to dict
        counts[word] = 1 if word not in counts else counts.get(word) + 1
    # Return set of words with only a single occurrance
    return set(word for word, count in counts.items() if count == 1)
    # END_YOUR_CODE


############################################################
# Question 7 - lenLongestPalindrome

def lenLongestPalindrome(text): 
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana'). 
    Computer the length of the longest palindrome that can be obtained by 
    deleting letters from text. 
    Do not try a brute force approach on this function.  Your algorithm should 
    run in O(len(text)^2) time. 
    Consider defining a recurrence before you begin coding. 
    """
    "*** YOUR CODE HERE ***"
    # BEGIN_YOUR_CODE
    # If string is full palindrome return length of text
    if text == text[::-1]: return len(text)
    # Base case: if string is empty return 0
    if len(text) == 0: return 0
    # Base case: if string is one char return 1
    if len(text) == 1: return 1
    # If string begins/ends with same char, add two to length and check inner substring
    if text[0] == text[-1]:
        return lenLongestPalindrome(text[1:-1]) + 2 
    else:
        # Check string with removed first/last chars, return max length of those
        return max(lenLongestPalindrome(text[0:-1]), lenLongestPalindrome(text[1:]))
    #END_YOUR_CODE    


############################################################
#  Extra Functions you may want to define
