import random


# takes the game state is input, and returns the move
# This is where the actual gameplay happens
def make_move(state):
    x = random.randint(0, state["width"] - 1)
    y = random.randint(0, state["height"] - 1)
    return {"x": x, "y": y}
