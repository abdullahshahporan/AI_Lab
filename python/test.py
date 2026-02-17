# ==========================================================
# MAP COLORING CSP (BEGINNER VERSION)
# Basic Backtracking Search (no heuristics, no forward checking)
# ==========================================================

def is_valid(region, color, assignment, neighbors):
    """
    Rule: A region cannot have the same color as any of its neighbors.
    assignment = {region: color}
    """
    for nb in neighbors[region]:
        if nb in assignment and assignment[nb] == color:
            return False
    return True


def solve_map_coloring_beginner(regions, colors, neighbors):
    """
    Beginner CSP solver using simple backtracking.
    Returns: dictionary {region: color} or None if no solution.
    """
    assignment = {}

    def backtrack():
        # 1) If all regions are colored, we are done
        if len(assignment) == len(regions):
            return True

        # 2) Pick the next uncolored region (first one found)
        for r in regions:
            if r not in assignment:
                region = r
                break

        # 3) Try each color for this region
        for color in colors:
            # 4) Check if this color is allowed (no neighbor conflict)
            if is_valid(region, color, assignment, neighbors):
                assignment[region] = color  # choose

                # 5) Try to color the rest
                if backtrack():
                    return True

                # 6) If it failed later, undo and try another color
                del assignment[region]

        # 7) No color worked for this region
        return False

    # Start backtracking
    if backtrack():
        return assignment
    return None


# ----------------------------
# Example: Australia Map
# ----------------------------
if __name__ == "__main__":
    regions = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    colors = ["Red", "Green", "Blue"]

    neighbors = {
        "WA":  ["NT", "SA"],
        "NT":  ["WA", "SA", "Q"],
        "SA":  ["WA", "NT", "Q", "NSW", "V"],
        "Q":   ["NT", "SA", "NSW"],
        "NSW": ["Q", "SA", "V"],
        "V":   ["SA", "NSW"],
        "T":   []  # Tasmania has no neighbors in this example
    }

    solution = solve_map_coloring_beginner(regions, colors, neighbors)
    print("✅ Beginner Solution:")
    print(solution)
