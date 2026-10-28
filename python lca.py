from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


# STEP 1: Make a material inventory and calculate fixed emissions
materials = {
    "Concrete": {
        "mass": 493800.11, "A1_A3": 63355.09, "C1": 3365.74,
        "C2": 5283.66, "C3": 0.0, "EF_C4": 0.00626,
        "EF_primary": 0.0103, "EF_secondary": 0.000578,
    },
    "Steel": {
        "mass": 197255.18, "A1_A3": 327337.69, "C1": 4590.67,
        "C2": 2110.63, "C3": 0.0, "EF_C4": 0.00626,
        "EF_primary": 1.659, "EF_secondary": 0.537,
    },
}

inventory = pd.DataFrame.from_dict(materials, orient="index")
inventory.index.name = "Material"
inventory["Fixed_emissions_kgCO2e"] = inventory[
    ["A1_A3", "C1", "C2", "C3"]
].sum(axis=1) 

print("\nSTEP 1 — FIXED EMISSIONS (A1–A3 + C1 + C2 + C3)")
print(inventory[["mass", "Fixed_emissions_kgCO2e"]].round(2).to_string())
inventory.to_csv(OUT / "lca_fixed_emissions.csv")

# STEP 2: Calculate low, median and high recycling scenarios
scenarios = {
    "Low":    {"Concrete": 0.55, "Steel": 0.825},
    "Median": {"Concrete": 0.70, "Steel": 0.925},
    "High":   {"Concrete": 0.90, "Steel": 0.985},
}

rows = []  

for scenario, rates in scenarios.items():
    for material, values in materials.items():
        rate = rates[material]                
        mass = values["mass"]

        recycled = mass * rate                 # Recovered material (kg)
        disposed = mass * (1 - rate)           # Remaining material for disposal (kg)
        c4 = disposed * values["EF_C4"]        # Disposal emissions (kg CO2e)

        # Negative sign: Module D is a credit outside the building system boundary.
        module_d = -recycled * (
            values["EF_primary"] - values["EF_secondary"]
        )

        fixed = values["A1_A3"] + values["C1"] + values["C2"] + values["C3"]
        gross = fixed + c4
        net = gross + module_d                  # Net balance INCLUDING Module D

        rows.append({
            "Scenario": scenario,
            "Material": material,
            "Recycling_rate": rate,
            "Recycled_kg": recycled,
            "Disposed_kg": disposed,
            "C4_kgCO2e": c4,
            "D_kgCO2e": module_d,
            "Gross_kgCO2e": gross,
            "Net_kgCO2e": net,
        })

results = pd.DataFrame(rows)
results.to_csv(OUT / "lca_scenario_results.csv", index=False)
print("\nSTEP 2 — SCENARIO RESULTS (kg CO2e)")
print(results[["Scenario", "Material", "C4_kgCO2e", "D_kgCO2e", "Net_kgCO2e"]]
      .round(2).to_string(index=False))

# STEP 3: Compare results using a professional Matplotlib bar chart
comparison = results.pivot(
    index="Scenario", columns="Material", values="Net_kgCO2e"
).reindex(["Low", "Median", "High"])

# Divide by 1000 to convert kg CO2e into tonnes CO2e.
concrete_t = comparison["Concrete"] / 1000
steel_t = comparison["Steel"] / 1000

x = np.arange(len(comparison)) 
width = 0.35                   

fig, ax = plt.subplots(figsize=(8, 5))
bars_concrete = ax.bar(x - width / 2, concrete_t, width, label="Concrete")
bars_steel = ax.bar(x + width / 2, steel_t, width, label="Steel")

ax.set_xticks(x, comparison.index)
ax.set_xlabel("Recycling scenario")
ax.set_ylabel("Net balance including Module D (t CO2e)")
ax.set_title("Concrete and steel: net emissions by recycling scenario")
ax.legend()
ax.bar_label(bars_concrete, fmt="%.1f", padding=3)
ax.bar_label(bars_steel, fmt="%.1f", padding=3)
ax.set_ylim(0, max(concrete_t.max(), steel_t.max()) * 1.15)
fig.tight_layout()

chart_path = OUT / "lca_scenario_comparison.png"
fig.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close(fig)

print("\nSTEP 3 — SAVED CHART:", chart_path.name)
print("\nDone! All three steps ran successfully.")
