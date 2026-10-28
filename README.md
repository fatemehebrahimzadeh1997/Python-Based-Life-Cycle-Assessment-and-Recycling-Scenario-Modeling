# Python-Based LCA & Recycling Scenario Modeling

A Python-based Life Cycle Assessment (LCA) workflow developed from my ongoing research on embodied carbon and material recovery in post-war residential buildings.

The model calculates environmental impacts across production (A1–A3) and end-of-life stages (C1–C4), alongside potential avoided emissions from material recycling (Module D), following the EN 15978 framework.

The analysis focuses on concrete and steel, comparing three recycling scenarios to evaluate how different material recovery rates influence overall carbon emissions.

## Key Features

- **LCA Calculations:** Calculates material-specific emissions across A1–A3 and C1–C4, including Module D avoided-burden credits.
- **Recycling Scenario Modeling:** Compares low, median, and high recovery scenarios for concrete and steel based on material-specific recycling rates.
- **Material Flow Calculations:** Quantifies recycled and disposed material masses under each scenario.
- **Automated Data Processing:** Uses Pandas and NumPy to organize material inventories, calculate emissions, and compare results.
- **Data Visualization:** Generates comparative charts using Matplotlib to illustrate changes in net emissions across recycling scenarios.

## Generated Outputs

- `LCA_All_3_Steps_Unified.py`: Python script integrating LCA calculations, recycling scenarios, and visualization.
- `lca_fixed_emissions.csv`: Material-specific emissions from A1–A3 and C1–C3.
- `lca_scenario_results.csv`: Calculated emissions and material recovery results for each scenario.
- `lca_scenario_comparison.png`: Comparison of net carbon emissions across recycling scenarios.

## Tools & Libraries

**Python | Pandas | NumPy | Matplotlib**

The workflow demonstrates how Python can support transparent and reproducible LCA calculations and the evaluation of circular economy strategies in the built environment.
