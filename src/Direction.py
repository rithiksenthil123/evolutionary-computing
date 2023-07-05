import enum

# Enum representing the directions an ant can take.
class Direction(enum.Enum):
    east = 0
    north = 1
    west = 2
    south = 3

    # Direction to an int.
    # @param dir the direction.
    # @return an integer from 0-3.
    @classmethod
    def dir_to_int(cls, dir):
        return dir.value

    # Opposite direction.
    # @param dir the direction.
    # @return an integer, the counterpart to the given direction (0-2, 1-3)
    @classmethod
    def opposite(cls, dir):
        if (dir.value < 2):
            return dir.value + 2
        else:
            return dir.value - 2