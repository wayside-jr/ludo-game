from path import PATHS

def move_pawn(pawn, steps, all_pawns=None):
    color = pawn["color"]
    path = PATHS[color]
    reached_home = False
    captured_pawn = None

    # If pawn already reached home, do nothing
    if pawn.get("finished", False):
        return False, None

    # If pawn is still in base
    if not pawn["started"]:
        if steps == 6:
            pawn["started"] = True
            pawn["position_index"] = 0  # place pawn on first square of its path
            return False, None
        else:
            return False, None

    # Pawn already on board
    new_index = pawn["position_index"] + steps

    # If move goes past home, ignore it
    if new_index >= len(path):
        return False, None

    pawn["position_index"] = new_index

    # Check if reached home
    if new_index == len(path) - 1:
        reached_home = True
        pawn["finished"] = True  

    # Check capture
    if all_pawns:
        new_pos = path[new_index]
        for other in all_pawns:
            if other == pawn:
                continue
            if other["color"] != color and other["started"] and not other.get("finished", False):
                other_pos = PATHS[other["color"]][other["position_index"]]
                if other_pos == new_pos:
                    # Send captured pawn home
                    other["started"] = False
                    other["position_index"] = 0
                    captured_pawn = other

    return reached_home, captured_pawn

