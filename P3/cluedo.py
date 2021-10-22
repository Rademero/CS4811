'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


# **************
#  Question 6 
# **************
def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***"
    tmp = []
    returnArray = []
    tmp.append(Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(cards[0])))
    returnArray.append(tmp)
    tmp[0] = Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(cards[1]))
    returnArray.append(tmp)
    tmp[0] = Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(cards[2]))
    returnArray.append(tmp)
    return returnArray


# **************
#  Question 7 
# **************
def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """
    "*** YOUR CODE HERE ***"
    retArray = []
    tmpArray = []
    for weapon in Cluedo.weapons:
        for suspect in Cluedo.suspects:
            tmpArray.append(Cluedo.getIdentifierFromNames(suspect, weapon))
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
        retArray.append(tmpArray)
        tmpArray = []

    for room in Cluedo.rooms:
        for suspect in Cluedo.suspects:
            tmpArray.append(Cluedo.getIdentifierFromNames(suspect, room))
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
        retArray.append(tmpArray)
        tmpArray = []

    for sus in Cluedo.suspects:
        for suspect in Cluedo.suspects:
            tmpArray.append(Cluedo.getIdentifierFromNames(suspect, sus))
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, sus))
        retArray.append(tmpArray)
        tmpArray = []

    return retArray


# **************
#  Question 7 
# **************
def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    retArray = []
    tmpArray = []
    for player in Cluedo.suspects:
        for weapon in Cluedo.weapons:
            tmpArray.append(Cluedo.getIdentifierFromNames(player, weapon))
            tmpArray.append(-1 * Cluedo.getIdentifierFromNames(player, weapon))
            retArray.append(tmpArray)
            tmpArray = []
        for room in Cluedo.rooms:
            tmpArray.append(Cluedo.getIdentifierFromNames(player, room))
            tmpArray.append(-1 * Cluedo.getIdentifierFromNames(player, room))
            retArray.append(tmpArray)
            tmpArray = []
        for suspect in Cluedo.suspects:
            tmpArray.append(Cluedo.getIdentifierFromNames(player, suspect))
            tmpArray.append(-1 * Cluedo.getIdentifierFromNames(player, suspect))
            retArray.append(tmpArray)
            tmpArray = []

    return retArray


# **************
#  Question 7 
# **************
def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    tmpArray = []
    retArray = []
    for weapon in Cluedo.weapons:
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
    retArray.append(tmpArray)
    tmpArray = []
    for room in Cluedo.rooms:
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
    retArray.append(tmpArray)
    tmpArray = []
    for sus in Cluedo.suspects:
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, sus))
    retArray.append(tmpArray)

    return retArray


# **************
#  Question 7 
# **************
def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"
    tmpArray = []
    retArray = []
    for weapon in Cluedo.weapons:
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
        tmpArray.append(-1 * Cluedo.getIdentifierFromNames(Cluedo.casefile, weapon))
        retArray.append(tmpArray)
        tmpArray = []
    for room in Cluedo.rooms:
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
        tmpArray.append(-1 * Cluedo.getIdentifierFromNames(Cluedo.casefile, room))
        retArray.append(tmpArray)
        tmpArray = []
    for suspect in Cluedo.suspects:
        tmpArray.append(Cluedo.getIdentifierFromNames(Cluedo.casefile, suspect))
        tmpArray.append(-1 * Cluedo.getIdentifierFromNames(Cluedo.casefile, suspect))
        retArray.append(tmpArray)
        tmpArray = []

    return retArray


# **************
#  Question 8 
# **************
def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    tmp = []
    tmp2 = []
    array = []
    if cardShown != None and refuter != None:
        tmp.append(Cluedo.getIdentifierFromNames(refuter, cardShown))
        array.append(tmp)
    elif cardShown == None and refuter != None:
        for i in range(Cluedo.hands.index(suggester) + 1, Cluedo.hands.index(refuter)):
            tmp.append(-1 * Cluedo.getIdentifierFromIndicies(i, Cluedo.cards.index(card1)))
            array.append(tmp)
            tmp = []
            tmp.append(-1 * Cluedo.getIdentifierFromIndicies(i, Cluedo.cards.index(card2)))
            array.append(tmp)
            tmp = []
            tmp.append(-1 * Cluedo.getIdentifierFromIndicies(i, Cluedo.cards.index(card3)))
            array.append(tmp)
            tmp = []
        tmp2.append(1 * Cluedo.getIdentifierFromIndicies(Cluedo.cards.index(refuter), Cluedo.cards.index(card1)))
        tmp2.append(1 * Cluedo.getIdentifierFromIndicies(Cluedo.cards.index(refuter), Cluedo.cards.index(card2)))
        tmp2.append(1 * Cluedo.getIdentifierFromIndicies(Cluedo.cards.index(refuter), Cluedo.cards.index(card3)))
        array.append(tmp2)
    else:
        for suspect in Cluedo.suspects:
            if suspect != suggester:
                tmp.append(-1 * Cluedo.getIdentifierFromNames(suspect, card1))
                array.append(tmp)
                tmp = []
                tmp.append(-1 * Cluedo.getIdentifierFromNames(suspect, card2))
                array.append(tmp)
                tmp = []
                tmp.append(-1 * Cluedo.getIdentifierFromNames(suspect, card3))
                array.append(tmp)
                tmp = []
    return array


# **************
#  Question 9 
# **************
def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    tmpArray = []
    returnArray = []
    if correct:
        tmpArray.append(Cluedo.getIdentifierFromNames("cf", card1))
        returnArray.append(tmpArray)
        tmpArray = []
        tmpArray.append(Cluedo.getIdentifierFromNames("cf", card2))
        returnArray.append(tmpArray)
        tmpArray = []
        tmpArray.append(Cluedo.getIdentifierFromNames("cf", card3))
        returnArray.append(tmpArray)
        tmpArray = []
    else:
        tmpArray.append(Cluedo.getIdentifierFromNames(accuser, card1))
        returnArray.append(tmpArray)
        tmpArray = []
        tmpArray.append(Cluedo.getIdentifierFromNames(accuser, card2))
        returnArray.append(tmpArray)
        tmpArray = []
        tmpArray.append(Cluedo.getIdentifierFromNames(accuser, card3))
        returnArray.append(tmpArray)
        tmpArray = []

        tmpArray.append(-1 * Cluedo.getIdentifierFromNames("cf", card1))
        tmpArray.append(-1 * Cluedo.getIdentifierFromNames("cf", card2))
        tmpArray.append(-1 * Cluedo.getIdentifierFromNames("cf", card3))
        returnArray.append(tmpArray)
    return returnArray

