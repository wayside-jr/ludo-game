import random
from move_pawn import move_pawn

def cpu_move(pawns, color):

    dice = random.randint(1, 6)
    cpu_pawns = [p for p in pawns if p["color"] == color and not p.get("finished", False)]

    # Pawns already started on the path
    active_pawns = [p for p in cpu_pawns if p["started"]]

    if active_pawns:
        # Move the pawn that is furthest along the path
        pawn_to_move = max(active_pawns, key=lambda p: p["position_index"])
        move_pawn(pawn_to_move, dice)
    else:
        # If no pawns started, can only move one if dice == 6
        home_pawns = [p for p in cpu_pawns if not p["started"]]
        if dice == 6 and home_pawns:
            move_pawn(home_pawns[0], dice)

    return dice == 6
