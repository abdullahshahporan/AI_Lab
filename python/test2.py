# ==========================================================
# MAP COLORING CSP (INTERMEDIATE VERSION)
# Backtracking + Forward Checking (aligns with slide concept)
# ==========================================================

from copy import deepcopy

def is_valid(region, color, assignment, neighbors):
    """
    Constraint: region can't have the same color as any already-colored neighbor.
    """
    for nb in neighbors[region]:
        if nb in assignment and assignment[nb] == color:
            return False
    return True


def forward_check(region, color, domains, assignment, neighbors):
    """
    Forward Checking (Inference):
    After assigning region=color, remove that color from each unassigned neighbor's domain.
    If any neighbor domain becomes empty -> failure.
    """
    new_domains = deepcopy(domains)

    for nb in neighbors[region]:
        if nb not in assignment:  # only for unassigned neighbors
            if color in new_domains[nb]:
                new_domains[nb].remove(color)

            # If neighbor has no colors left, this path is impossible
            if len(new_domains[nb]) == 0:
                return None

    return new_domains


def solve_map_coloring_intermediate(regions, colors, neighbors):
    """
    Intermediate CSP solver:
    - Basic variable selection (first unassigned)
    - Try colors in order
    - Forward checking after each assignment
    """
    assignment = {}

    # Domains: initially every region can take any color
    domains = {r: colors[:] for r in regions}

    def backtrack(domains_now):
        # 1) If all regions are assigned, solved
        if len(assignment) == len(regions):
            return True

        # 2) Pick next uncolored region (same as beginner)
        for r in regions:
            if r not in assignment:
                region = r
                break

        # 3) Try each possible color from current domain of that region
        for color in domains_now[region]:
            if is_valid(region, color, assignment, neighbors):
                assignment[region] = color  # choose

                # 4) Inference step: forward checking
                new_domains = forward_check(region, color, domains_now, assignment, neighbors)

                if new_domains is not None:
                    # 5) Explore deeper
                    if backtrack(new_domains):
                        return True

                # 6) Undo (backtrack)
                del assignment[region]

        return False

    if backtrack(domains):
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
        "T":   []
    }

    solution = solve_map_coloring_intermediate(regions, colors, neighbors)
    print("✅ Intermediate Solution (Backtracking + Forward Checking):")
    print(solution)
