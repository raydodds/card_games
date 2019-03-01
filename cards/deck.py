"""
deck.py
Defines a deck object, from which cards are drawn.
"""

__author__ = "Ray Dodds"

import itertools as it
import json
import os
import random
from . import card as crd

class Deck:
    """
    Deck
    A collection of cards which disallows non-standard cards and adds some
    convenience methods
    """

    def __init__(self, decktype=None, cards=None):
        # Check for valid decktypes
        if not decktype:
            if not cards:
                self.type = 'french52j'
            else:
                self.type = cards[0].deck.type
        elif not isinstance(decktype, str):
            raise TypeError
        else:
            self.type = decktype

        deck_file = None
        try:
            deck_file = open(os.path.join(os.path.dirname(__file__),
                                          "decks", self.type+".json"), 'r')
        except FileNotFoundError:
            raise ValueError("Invalid Deck Type")

        deck_info = json.loads(deck_file.read())

        self.name = deck_info['name']
        self.suits = tuple(deck_info['suits'])
        self.ranks = tuple(deck_info['ranks'])
        self.trumps = tuple(deck_info['trumps'])

        if cards is None:
            self.cards = [crd.Card(r, s, self) for s in self.suits for r in self.ranks]
            self.cards += [crd.Trump(self.trumps[i], i, self)\
                            for i in range(len(self.trumps))]
        else:
            for _c in cards:
                if _c.deck.type != self.type:
                    raise ValueError
                self.cards += [_c]

    def __repr__(self):
        return "Deck("+self.type+", "+''.join(str(self.cards))+")"

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        if not isinstance(other, Deck):
            raise TypeError

        if self.type != other.type:
            return False

        if len(self) != len(other):
            return False

        for s_c, o_c in sorted(self.cards), sorted(other.cards):
            if s_c != o_c:
                return False

        return True

    def shuffle(self):
        """Randomizes the order of the cards in the deck in place."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the deck by suit then rank"""
        self.cards.sort()

    def draw(self):
        """Draws a single card from the deck"""
        return self.cards.pop()

    def cut(self, index):
        """Cuts the deck at a given index"""
        self.cards = self.cards[index:] + self.cards[:index]

    def add(self, cards):
        """Adds a card to the top of the deck"""
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            if not isinstance(card, crd.Card):
                raise TypeError

        self.cards += cards

    def deal(self, num_hands, num_cards=0):
        """
        Splits the deck evenly between num_hands lists with removal

        args:
        num_hands   [int] how many groups to split the deck into
        num_cards   [int] how many cards per hand. If 0, deals whole deck

        return:     a tuple of length num_hands of lists of num_cards card objects
        """
        if num_hands > len(self):
            raise ValueError("Too many hands for the remaining cards in the deck")

        if num_cards == 0:
            num_cards = len(self)//num_hands

        if num_cards*num_hands >= len(self):
            raise ValueError("Too many cards per hand for the remaining cards in the deck")

        hands = [None]*num_hands
        for i in range(num_hands):
            hands[i] = []
            for _ in it.repeat(None, num_cards):
                hands[i] += [self.draw()]

        return tuple(hands)
