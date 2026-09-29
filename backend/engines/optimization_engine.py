from __future__ import annotations

try:
    from ortools.sat.python import cp_model
except ImportError:  # pragma: no cover
    cp_model = None


def allocate_population(population: int, sites: list, max_distance_km: int = 35) -> dict:
    """Use CP-SAT to allocate population across safe candidate sites."""
    if cp_model is None:
        total_capacity = sum(site["land_capacity"] for site in sites if site["status"] == "SAFE")
        allocation = []
        for site in sites:
            if site["status"] != "SAFE":
                continue
            amount = min(site["land_capacity"], population)
            allocation.append({"site": site["name"], "allocation": amount})
        return {
            "allocations": allocation,
            "total_allocated": min(population, total_capacity),
            "feasible": total_capacity >= population,
        }

    model = cp_model.CpModel()
    x = {}
    for idx, site in enumerate(sites):
        if site["status"] != "SAFE" or site["distance_km"] > max_distance_km:
            continue
        x[idx] = model.NewIntVar(0, site["land_capacity"], f"alloc_{idx}")

    if not x:
        return {"allocations": [], "total_allocated": 0, "feasible": False}

    model.Add(sum(x.values()) >= population)
    # Minimize distance + infrastructure deficit + residual risk
    objective_terms = []
    for idx, site in enumerate(sites):
        if idx not in x:
            continue
        objective_terms.append(x[idx] * (site["distance_km"] * 5 + (100 - site["water_capacity"]) * 0.03))
    model.Minimize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5
    status = solver.Solve(model)

    allocations = []
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for idx, site in enumerate(sites):
            if idx not in x:
                continue
            allocated = solver.Value(x[idx])
            allocations.append({"site": site["name"], "allocation": allocated, "capacity": site["land_capacity"]})

        return {
            "allocations": allocations,
            "total_allocated": sum(item["allocation"] for item in allocations),
            "feasible": sum(item["allocation"] for item in allocations) >= population,
        }

    return {"allocations": [], "total_allocated": 0, "feasible": False}
