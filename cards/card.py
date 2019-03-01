"""
card.py
Defines a card object, the base for all card actions
"""

__author__ = "Ray Dodds"


class Card:
    """
    Card
    Defines a basic card object with a rank and suit
    """
    def __init__(self, rank, suit, deck):
        self.rank = rank
        self.suit = suit
        self.deck = deck

    def __repr__(self):
        return "Card("+str(self.rank)+","+str(self.suit)+")"

    def __str__(self):
        return str(self.rank)+" of "+str(self.suit)

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Cannot compare card and "+str(type(other).__name__))
        return self.rank == other.rank and \
                self.suit == other.suit and \
                self.deck.type == other.deck.type

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if isinstance(other, Card):
            if self.deck.type != other.deck.type:
                raise ValueError("These cards are from different decks.")
            elif isinstance(other, Trump):
                return False
            elif self.__eq__(other):
                return False
            else:
                return (self.deck.suits.index(self.suit) > self.deck.suits.index(other.suit))\
                    or (self.suit == other.suit) and\
                    self.deck.ranks.index(self.rank) > self.deck.ranks.index(other.rank)
        raise TypeError("Cannot compare card and "+str(type(other).__name__))


class Trump(Card):
    """
    Trump
    Defines a type of card that does not have a rank or suit, only a name
    Uses value for comparisons
    """
    def __init__(self, name, value, deck):
        super(Trump, self).__init__('T', 'T', deck)
        self.name = name
        self.value = value

    def __repr__(self):
        return "Trump("+str(self.name)+","+str(self.value)+")"

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Cannot compare card and "+str(type(other).__name__))
        if not isinstance(other, Trump):
            return False
        return self.name == other.name and self.value == other.value

    def __gt__(self, other):
        if isinstance(other, Card):
            if self.deck.type != other.deck.type:
                raise ValueError("These cards are from different decks.")
            if isinstance(other, Trump):
                return self.value > other.value
            return True
        raise TypeError("Cannot compare card and "+str(type(other).__name__))
