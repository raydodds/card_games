"""
    accordion.py
    sets up the rules for accordion
"""
from ..cards.deck import Deck

class Accordion:
    """
    Defines the game, its state, and its rules.
    """

    # Internal methods
    def __init__(self):
        self.stacks = []
        self._current_stack = 0
        self.deck = Deck('french52')
        self.deck.shuffle()
        self._state = "Play"

    def __str__(self):
        rstring = []
        for i in range(0, len(self.stacks)):
            if i == self._current_stack:
                rstring += ["[" + str(self.stacks[i][-1]) + "]"]
            else:
                rstring += [str(self.stacks[i][-1])]
        return ", ".join(rstring)

    # Public methods

    def get_moves(self):
        """
        Gets all available moves for the current postition
        """
        return self._get_moves(self._current_stack)

    def get_state(self):
        """
        Gets the current state
        """
        return self._state


    # Private methods

    def _check_state(self):
        if self.deck:
            self._state = "Play"
        elif len(self.stacks) == 1:
            self._state = "Win"
        else:
            all_moves = []
            for i in range(0, len(self.stacks)):
                all_moves += self._get_moves(i)
            if len(all_moves) > 2*len(self.stacks):
                self._state = "Play"
            else:
                self._state = "Loss"

    def _compatible(self, stack_1, stack_2):
        return self.stacks[stack_1][-1].suit == self.stacks[stack_2][-1].suit or\
            self.stacks[stack_1][-1].rank == self.stacks[stack_2][-1].rank

    ## Moves

    def _get_moves(self, pos):
        moves = {}

        # Draw a card and put it in a new stack at the far right.
        # If at the far right stack, move the cursor to the new stack.
        if self.deck:
            def draw():
                if self.stacks and self._current_stack == len(self.stacks)-1:
                    self._current_stack += 1
                self.stacks += [[self.deck.draw()]]
                self._check_state()
            moves["draw"] = draw

        # Move the current stack one stack left
        if len(self.stacks) > 1 and pos > 0 and self._compatible(pos-1, pos):
            def back_one():
                self.stacks[pos-1] += self.stacks[pos]
                del self.stacks[pos]
                self._current_stack -= 1
                self._check_state()
            moves["back_one"] = back_one

        # Move the current stack three stacks left
        if len(self.stacks) > 3 and pos > 2 and self._compatible(pos-3, pos):
            def back_three():
                self.stacks[pos-3] += self.stacks[pos]
                del self.stacks[pos]
                self._current_stack -= 1
                self._check_state()
            moves["back_three"] = back_three

        # Move the cursor one stack left
        if pos > 0:
            def prev_stack():
                self._current_stack -= 1
            moves["prev_stack"] = prev_stack

        # Move the cursor one stack right
        if pos < len(self.stacks)-1:
            def next_stack():
                self._current_stack += 1
            moves["next_stack"] = next_stack
        return moves


def main():
    """ Runs if accordion.py is run on its own
    """
    from msvcrt import getch
    game = Accordion()
    game.get_moves()['draw']()
    move_count = 0

    _ch = b'a'
    while _ch != b'q':
        print("\n\n\n"+game.get_state()+"\t\tMoves: "+str(move_count)+"\n"+str(game))
        _ch = getch()
        moves = game.get_moves()

        if _ch == b' ':
            try:
                moves['draw']()
                move_count += 1
            except KeyError:
                pass
        elif _ch == b'a':
            try:
                moves['prev_stack']()
            except KeyError:
                pass
        elif _ch == b'd':
            try:
                moves['next_stack']()
            except KeyError:
                pass
        elif _ch == b',':
            try:
                moves['back_one']()
                move_count += 1
            except KeyError:
                pass
        elif _ch == b'.':
            try:
                moves['back_three']()
                move_count += 1
            except KeyError:
                pass
        elif _ch == b'r':
            game = Accordion()
            game.get_moves()['draw']()
            print("New game...")
        elif _ch == 'q' or _ch == b'\x03' or _ch == b'\x04':
            exit()


if __name__ == "__main__":
    main()
