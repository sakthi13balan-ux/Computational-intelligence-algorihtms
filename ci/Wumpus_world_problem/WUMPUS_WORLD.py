import random

def create_grid(n):
    return [[{
        "pit": None,
        "wumpus": False,
        "gold": False,
        "breeze": False,
        "scent": False,
        "glitter": False
    } for _ in range(n)] for _ in range(n)]


def get_adjacent(n, x, y):
    moves = []
    if x > 0: moves.append((x-1, y))
    if x < n-1: moves.append((x+1, y))
    if y > 0: moves.append((x, y-1))
    if y < n-1: moves.append((x, y+1))
    return moves

def spawn_objects(grid, n):
    total_cells = n * n
    pit_count = random.randint(int(0.20 * total_cells), int(0.25 * total_cells))

    all_positions = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(all_positions)

    occupied = {(0, 0)}   
    gold_pos = None
    for pos in all_positions:
        if pos not in occupied:
            gold_pos = pos
            occupied.add(pos)
            break
    grid[gold_pos[0]][gold_pos[1]]["gold"] = True

    wumpus_pos = None
    for pos in all_positions:
        if pos not in occupied:
            wumpus_pos = pos
            occupied.add(pos)
            break
    grid[wumpus_pos[0]][wumpus_pos[1]]["wumpus"] = True

    spawned_pits = 0
    pit_num = 1
    for pos in all_positions:
        if spawned_pits >= pit_count:
            break
        if pos not in occupied:
            grid[pos[0]][pos[1]]["pit"] = f"P{pit_num}"
            occupied.add(pos)
            spawned_pits += 1
            pit_num += 1

    return gold_pos, wumpus_pos


def update_sensors(grid, n):
    for i in range(n):
        for j in range(n):
            adj = get_adjacent(n, i, j)
            for x, y in adj:
                if grid[x][y]["pit"]:
                    grid[i][j]["breeze"] = True
                if grid[x][y]["wumpus"]:
                    grid[i][j]["scent"] = True
            if grid[i][j]["gold"]:
                grid[i][j]["glitter"] = True

DIRECTIONS = ["right", "down", "left", "up"]

def rotate(facing, turn):
    idx = DIRECTIONS.index(facing)
    if turn == "right":
        return DIRECTIONS[(idx + 1) % 4]
    elif turn == "left":
        return DIRECTIONS[(idx - 1) % 4]
    return facing


def direction_label(facing):
    arrows = {"right": "-->", "left": "<--", "up": "^", "down": "v"}
    return arrows.get(facing, "?")


def show_status(grid, player, score, arrow, facing):
    x, y = player
    cell = grid[x][y]
    display_pos = (x + 1, y + 1)
    print("\nPlayer Position:", display_pos)
    print("Facing          :", facing, direction_label(facing))
    print("Score           :", score)
    print("Arrow Available :", arrow)
    print("Breeze          :", cell["breeze"])
    print("Scent           :", cell["scent"])
    print("Glitter         :", cell["glitter"])


def move_player(n, player, direction):
    x, y = player

    if direction == "up":
        x -= 1
    elif direction == "down":
        x += 1
    elif direction == "left":
        y -= 1
    elif direction == "right":
        y += 1

    if x < 0 or x >= n or y < 0 or y >= n:
        print("BUMP! Wall hit.")
        return player, True

    return (x, y), False

def shoot_arrow(grid, n, player, direction):
    x, y = player
    scream = False

    if direction == "up":
        for i in range(x-1, -1, -1):
            if grid[i][y]["wumpus"]:
                grid[i][y]["wumpus"] = False
                scream = True

    elif direction == "down":
        for i in range(x+1, n):
            if grid[i][y]["wumpus"]:
                grid[i][y]["wumpus"] = False
                scream = True

    elif direction == "left":
        for j in range(y-1, -1, -1):
            if grid[x][j]["wumpus"]:
                grid[x][j]["wumpus"] = False
                scream = True

    elif direction == "right":
        for j in range(y+1, n):
            if grid[x][j]["wumpus"]:
                grid[x][j]["wumpus"] = False
                scream = True

    return scream


def check_game(grid, player):
    x, y = player
    if grid[x][y]["pit"]:
        print("Fell into", grid[x][y]["pit"], "Pit !!!")
        return -1000
    if grid[x][y]["wumpus"]:
        print("Killed by Wumpus !!!")
        return -1000
    return 0

def kb_init():
    kb_visited      = {(0, 0)}
    kb_safe         = {(0, 0)}
    kb_pit_possible = set()
    kb_wmp_possible = set()
    return kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible

def kb_observe(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible, pos, breeze, scent):
    kb_visited.add(pos)
    kb_safe.add(pos)
    kb_pit_possible.discard(pos)
    kb_wmp_possible.discard(pos)

    x, y = pos
    neighbours = get_adjacent(n, x, y)

    if breeze:
        for nb in neighbours:
            if nb not in kb_visited:
                kb_pit_possible.add(nb)
    else:
        for nb in neighbours:
            kb_pit_possible.discard(nb)
            if nb not in kb_wmp_possible:
                kb_safe.add(nb)

    if scent:
        for nb in neighbours:
            if nb not in kb_visited:
                kb_wmp_possible.add(nb)
    else:
        for nb in neighbours:
            kb_wmp_possible.discard(nb)
            if nb not in kb_pit_possible:
                kb_safe.add(nb)

def kb_direction_to(player, target):
    px, py = player
    tx, ty = target
    if tx == px - 1: return "up"
    if tx == px + 1: return "down"
    if ty == py - 1: return "left"
    if ty == py + 1: return "right"
    return None

def kb_get_target(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible, player):
    x, y = player

    for nb in get_adjacent(n, x, y):
        if nb in kb_safe and nb not in kb_visited:
            return nb, "safe"
        
    from collections import deque
    queue = deque()
    queue.append((player, []))
    bfs_seen = {player}
    while queue:
        cur, path = queue.popleft()
        for nb in get_adjacent(n, cur[0], cur[1]):
            if nb in bfs_seen:
                continue
            bfs_seen.add(nb)
            new_path = path + [nb]
            if nb in kb_safe and nb not in kb_visited:
                first_step = new_path[0]
                return first_step, "safe (via BFS)"
            if nb in kb_visited:
                queue.append((nb, new_path))
    for nb in get_adjacent(n, x, y):
        if nb in kb_visited:
            return nb, "visited"
    for nb in get_adjacent(n, x, y):
        if nb not in kb_visited and nb not in kb_pit_possible and nb not in kb_wmp_possible:
            return nb, "unknown"

    return None, "none"

def kb_print_suggestion(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible, player, facing):
    target, reason = kb_get_target(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible, player)
    if target is None:
        print("Suggested Move  : No good move found, try rotating.")
        return
    direction = kb_direction_to(player, target)
    display = (target[0]+1, target[1]+1)
    if facing == direction:
        print(f"Suggested Move  : move -> towards {display} ({reason})")
    else:
        print(f"Suggested Move  : rotate to face {direction}, then move -> towards {display} ({reason})")

def manual_mode(grid, n):
    player = (0, 0)
    score = 500
    arrow = True
    facing = "right"

    kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible = kb_init()

    x, y = player
    kb_observe(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible,
               player, grid[x][y]["breeze"], grid[x][y]["scent"])

    print("\nControls:")
    print("  rotate left  -> turn left without moving")
    print("  rotate right -> turn right without moving")
    print("  move         -> move one step in facing direction")
    print("  shoot        -> shoot arrow in facing direction")
    print("  grab         -> pick up gold if present")

    while score > 0:
        show_status(grid, player, score, arrow, facing)
        x, y = player
        if grid[x][y]["glitter"]:
            print("Suggested Move  : GOLD IS HERE! grab it")
        else:
            kb_print_suggestion(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible, player, facing)
        action = input("Action: ").strip().lower()

        if action == "rotate left":
            facing = rotate(facing, "left")
            print("Now facing:", facing, direction_label(facing))

        elif action == "rotate right":
            facing = rotate(facing, "right")
            print("Now facing:", facing, direction_label(facing))

        elif action == "move":
            new_pos, bump = move_player(n, player, facing)
            score -= 1
            if not bump:
                player = new_pos
                x, y = player
                kb_observe(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible,
                           player, grid[x][y]["breeze"], grid[x][y]["scent"])

        elif action == "shoot":
            if arrow:
                scream = shoot_arrow(grid, n, player, facing)
                score -= 50
                arrow = False
                if scream:
                    print("SCREAM! Wumpus killed !!!")
                    kb_wmp_possible.clear()
                    update_sensors(grid, n)
                else:
                    print("Arrow missed.")
            else:
                print("Arrow already used.")

        elif action == "grab":
            x, y = player
            if grid[x][y]["gold"]:
                print("GOLD FOUND . YOU WIN !!!")
                print("Final Score:", score)
                return
            else:
                print("No gold here.")

        else:
            print("Unknown action. Try: rotate left, rotate right, move, shoot, grab")
            continue

        score += check_game(grid, player)
        if score <= 0:
            print("Game Over! Score finished.")
            return


def random_mode(grid, n):
    player = (0, 0)
    score = 500
    arrow = True
    facing = "right"

    kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible = kb_init()

    x, y = player
    kb_observe(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible,
               player, grid[x][y]["breeze"], grid[x][y]["scent"])

    while score > 0:
        x, y = player
        if grid[x][y]["glitter"]:
            print("Random Agent Found Gold !!!")
            print("Final Score:", score)
            return

        target, reason = kb_get_target(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible, player)

        if target is not None:
            direction = kb_direction_to(player, target)
            if facing == direction:
                action = "move"
            else:
                action = random.choice(["rotate left", "rotate right"])
        else:
            action = random.choice(["rotate left", "rotate right"])

        if action == "rotate left":
            facing = rotate(facing, "left")
        elif action == "rotate right":
            facing = rotate(facing, "right")
        else:
            new_pos, bump = move_player(n, player, facing)
            score -= 1
            if not bump:
                player = new_pos
                x, y = player
                kb_observe(n, kb_visited, kb_safe, kb_pit_possible, kb_wmp_possible,
                           player, grid[x][y]["breeze"], grid[x][y]["scent"])

        if arrow and random.random() < 0.2:
            scream = shoot_arrow(grid, n, player, facing)
            score -= 50
            arrow = False
            if scream:
                print("Random Agent killed Wumpus !!!")
                kb_wmp_possible.clear()
                update_sensors(grid, n)

        score += check_game(grid, player)
        if score <= 0:
            print("Random Agent Lost !!!")
            return


def main():
    n = int(input("Enter grid size (n for n x n): "))
    grid = create_grid(n)

    gold_pos, wumpus_pos = spawn_objects(grid, n)
    update_sensors(grid, n)

    print(f"Grid: (1,1) to ({n},{n})")
    print(f"Gold at   : {(gold_pos[0]+1, gold_pos[1]+1)}")
    print(f"Wumpus at : {(wumpus_pos[0]+1, wumpus_pos[1]+1)}")

    mode = input("Choose mode (manual/random): ").lower()

    if mode == "manual":
        manual_mode(grid, n)
    else:
        random_mode(grid, n)


if __name__ == "__main__":
    main()