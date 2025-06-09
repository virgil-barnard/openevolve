from player_base import PlayerBase
from game import Direction

class EvolvedPlayer(PlayerBase):
    """
    Initial naive policy (baseline).  OpenEvolve will edit ONLY the code
    inside the marked region.  Outside code stays static for context.
    """

    # EVOLVE-BLOCK-START

    def __init__(self):
        # Could create stateful variables to improve decide method here. 
        pass

    def decide(self, sensors):
        """
        sensors: {
            'food_vec': (dr, dc),
            'danger': {'UP':bool, 'DOWN':bool, ...},
            'current_dir': 'UP'|'DOWN'|'LEFT'|'RIGHT',
            'length': int,
            'steps': int
        }
        Must return one of 'UP','DOWN','LEFT','RIGHT'
        """
        # REFERENCE  policy: greedily move toward food if safe, else turn right
        head_to_food = sensors["food_vec"]
        danger = sensors["danger"]

        # pick axis with larger |delta|
        vertical = abs(head_to_food[0]) >= abs(head_to_food[1])
        if vertical:
            move = "UP" if head_to_food[0] < 0 else "DOWN"
        else:
            move = "LEFT" if head_to_food[1] < 0 else "RIGHT"

        # avoid collisions
        if danger[move]:
            for alt in ["UP", "RIGHT", "DOWN", "LEFT"]:
                if not danger[alt]:
                    move = alt
                    break
        return move
    # EVOLVE-BLOCK-END
