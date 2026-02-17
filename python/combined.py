# ==========================================================
# MAP COLORING CSP - COMBINED FILE
#
# 1) BEGINNER VERSION      : Backtracking only
# 2) INTERMEDIATE VERSION  : Backtracking + Forward Checking
#
# Both versions solve the same map coloring CSP and print
# two separate outputs.
# ==========================================================

from copy import deepcopy


# ----------------------------------------------------------
# COMMON: Constraint Check
# ----------------------------------------------------------
def is_valid(region, color, assignment, neighbors):
    """
    Rule: A region cannot have the same color as any of its neighbors.
    assignment = {region: color}
    """
    for nb in neighbors[region]:
        if nb in assignment and assignment[nb] == color:
            return False
    return True


# ==========================================================
# 1) BEGINNER VERSION (Basic Backtracking)
# ==========================================================
def solve_map_coloring_beginner(regions, colors, neighbors):
    assignment = {}

    def backtrack():
        # If all regions are colored, done
        if len(assignment) == len(regions):
            return True

        # Pick the next uncolored region (first one found)
        for r in regions:
            if r not in assignment:
                region = r
                break

        # Try each color
        for color in colors:
            if is_valid(region, color, assignment, neighbors):
                assignment[region] = color  # choose

                if backtrack():             # explore
                    return True

                del assignment[region]      # undo (backtrack)

        return False

    if backtrack():
        return assignment
    return None


# ==========================================================
# 2) INTERMEDIATE VERSION (Backtracking + Forward Checking)
# ==========================================================
def forward_check(region, color, domains, assignment, neighbors):
    """
    Forward Checking:
    After assigning region=color, remove that color from neighbors' domains.
    If any neighbor has no values left -> failure (return None).
    """
    new_domains = deepcopy(domains)

    for nb in neighbors[region]:
        if nb not in assignment:
            if color in new_domains[nb]:
                new_domains[nb].remove(color)

            if len(new_domains[nb]) == 0:
                return None  # failure

    return new_domains


def solve_map_coloring_intermediate(regions, colors, neighbors):
    assignment = {}
    domains = {r: colors[:] for r in regions}  # each region starts with all colors

    def backtrack(domains_now):
        # If all regions are colored, done
        if len(assignment) == len(regions):
            return True

        # Pick the next uncolored region (same as beginner)
        for r in regions:
            if r not in assignment:
                region = r
                break

        # Try each color from the CURRENT domain
        for color in domains_now[region]:
            if is_valid(region, color, assignment, neighbors):
                assignment[region] = color  # choose

                # Forward checking (inference)
                new_domains = forward_check(region, color, domains_now, assignment, neighbors)
                if new_domains is not None:
                    if backtrack(new_domains):  # explore
                        return True

                del assignment[region]  # undo

        return False

    if backtrack(domains):
        return assignment
    return None


# ==========================================================
# TEST CASE: Australia Map
# ==========================================================
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
        "T":   []  # Tasmania isolated
    }

    # Run Beginner
    beginner_solution = solve_map_coloring_beginner(regions, colors, neighbors)
    print("\n================ BEGINNER SOLUTION ================\n")
    print(beginner_solution)

    # Run Intermediate
    intermediate_solution = solve_map_coloring_intermediate(regions, colors, neighbors)
    print("\n============= INTERMEDIATE SOLUTION ==============\n")
    print(intermediate_solution)
