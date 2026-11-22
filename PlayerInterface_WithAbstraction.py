from abc import ABC, abstractmethod
import random

# Abstract base class defining the blueprint for all players
class Player(ABC):

    @abstractmethod
    def level_up(self):
        # Forces child classes to implement their own level up logic
        pass

    def __init__(self):
        # Initialize default starting stats for any player
        self.moves = []              # List to hold available (x, y) movement tuples
        self.position = (0, 0)       # Starting coordinate on the grid
        self.path = [(0, 0)]         # History of movements, starting with the origin

    def make_move(self):
        # Select a random (x, y) movement from the available moves
        move = random.choice(self.moves)
        
        # Calculate the new position by adding the move's X and Y to the current position
        self.position = (self.position[0] + move[0], self.position[1] + move[1])
        
        # Record the new position in the path history
        self.path.append(self.position)
        
        # Return the updated position
        return self.position


# Concrete child class representing a Pawn piece
class Pawn(Player):

    def __init__(self):
        # Call the parent class __init__ to set up base attributes (position, path)
        super().__init__()
        
        # Override the empty moves list with standard orthogonal moves (up, down, left, right)
        self.moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    def level_up(self):
        # Add diagonal moves (up-right, up-left, down-left, down-right) to the existing moves list
        self.moves.extend([(1, 1), (-1, 1), (-1, -1), (1, -1)])


# --- EXECUTION TESTING ---

# Instantiate a new Pawn object
my_pawn = Pawn()
print("Starting position:", my_pawn.position)

# Execute a random orthogonal move
new_pos = my_pawn.make_move()
print("Moved to:", new_pos)

# Upgrade the pawn to unlock diagonal moves
my_pawn.level_up()
print("Moves after leveling up:", my_pawn.moves)

# Execute another random move (can now be orthogonal OR diagonal)
new_pos2 = my_pawn.make_move()
print("Moved again to:", new_pos2)

# Print the complete history of where the pawn has been
print("Full path history:", my_pawn.path)
