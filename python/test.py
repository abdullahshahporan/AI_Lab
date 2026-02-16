# ----------------------------
# Map Coloring using CSP (Backtracking)
# ----------------------------

def is_valid(region, color, assignment, neighbors):
    """
    Check: region can't have same color as any already-colored neighbor.
    """
    for nb in neighbors[region]:
        if nb in assignment and assignment[nb] == color:
            return False
    return True


def solve_map_coloring(regions, colors, neighbors):
    """
    Backtracking solver.
    Returns a dictionary: {region: color}
    """

    assignment = {}

    def backtrack():
        # If all regions are colored, done
        if len(assignment) == len(regions):
            return True

        # Pick the next uncolored region
        for r in regions:
            if r not in assignment:
                region = r
                break

        # Try each color
        for color in colors:
            if is_valid(region, color, assignment, neighbors):
                assignment[region] = color   # choose

                if backtrack():              # explore
                    return True

                del assignment[region]       # undo (backtrack)

        return False

    if backtrack():
        return assignment
    return None


# ----------------------------
# Example: Australia Map
# ----------------------------

regions = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
colors = ["Red", "Green", "Blue"]

neighbors = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "Q"],
    "SA":  ["WA", "NT", "Q", "NSW", "V"],
    "Q":   ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V":   ["SA", "NSW"],
    "T":   []  # Tasmania has no neighbor in this simple example
}

solution = solve_map_coloring(regions, colors, neighbors)

print("✅ Solution:")
print(solution)
