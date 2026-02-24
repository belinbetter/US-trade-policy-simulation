# US-China Trade Policy Simulation Program

This program simulates the impact of US trade policies (e.g., anti-dumping, anti-circumvention) on global production networks using multi‑regional input–output (MRIO) data. It generates counterfactual intermediate goods trade matrices that serve as inputs for subsequent network analysis of industrial supply chains.

## Features

The program adjusts trade flows between China, the United States, and a set of “transshipment” economies (e.g., Mexico, Vietnam, Malaysia) according to three policy scenarios:

- **Scenario 1 (Traditional trade remedies)**: The US imposes anti‑dumping or countervailing duties on China. A fraction of China’s exports to the US (specified by the parameter `drop_ratio`) is redirected to the transshipment countries, while the US sources the missing imports from the rest of the world (excluding China).
- **Scenario 2 (Traditional remedies + anti‑circumvention)**: In addition to Scenario 1, the US applies anti‑circumvention measures. China’s exports to both the US and the transshipment countries are reduced by the same fraction, and the reduced amount is reallocated to the rest of the world (excluding China and the affected countries).
- **Scenario 3 (Domestic absorption)**: Same as Scenario 2, but the reduced exports are redirected to China’s domestic market (i.e., no foreign replacement).

## Requirements

- Python 3.12
- Required packages (versions verified in the test environment):
  - `numpy == 1.26.4`
  - `pandas == 2.2.2`
  - `tqdm == 4.66.4`

Install the dependencies with:

```bash
pip install numpy==1.26.4 pandas==2.2.2 tqdm==4.66.4
```

## Data Format

The program expects an **intermediate goods trade matrix** in **CSV format**, where rows represent exporting sectors and columns represent importing sectors. Sector names should follow the convention `[country_code]S[sector_number]`, e.g., `PRCS01` for China’s agriculture sector.

The code predefines the starting row/column indices (1‑based; converted to 0‑based internally) for the following countries, based on the **ADB‑MRIO 2024 E62** database:

- China (`PRC`): start index 246
- USA (`USA`): start index 1471
- Transshipment countries:
  - Brazil (`BRA`, 141)
  - Indonesia (`INO`, 701)
  - Mexico (`MEX`, 1016)
  - Poland (`POL`, 1156)
  - Turkey (`TUR`, 1401)
  - Bangladesh (`BAN`, 1506)
  - Malaysia (`MAL`, 1541)
  - Thailand (`THA`, 1611)
  - Vietnam (`VIE`, 1646)

**Important**: These indices are specific to the ADB‑MRIO 2024 E62 dataset. If you use a different MRIO table or a different version, you **must** adjust the `start` indices accordingly.

## Usage

The main function `trade_transfer` performs the trade‑flow modifications. A typical call is:

```python
from pathlib import Path

data_file = "path/to/your/matrix.csv"
drop_ratio = 0.2   # 20% trade reduction

for scenario in ['Scenario1', 'Scenario2', 'Scenario3']:
    trade_transfer(data_file, drop_ratio, scenario)
```

After execution, three new CSV files are saved in the same directory as the input file:

- `original_filename_Scenario1_DropRatio{drop_ratio}.csv`
- `original_filename_Scenario2_DropRatio{drop_ratio}.csv`
- `original_filename_Scenario3_DropRatio{drop_ratio}.csv`

### Function Parameters

- `data_path` : `str`  
  Path to the input CSV file.
- `drop_ratio` : `float`  
  Fraction of trade to be reduced (between 0 and 1).
- `trans_type` : `str`  
  Scenario type: `'Scenario1'`, `'Scenario2'`, or `'Scenario3'`.

## Output

Each scenario produces a CSV file with the same structure as the input (row/column order preserved), but with affected trade values updated according to the policy assumptions.

## Citation

If you use this code in your research, please cite the relevant literature and consider referencing this repository (DOI to be assigned).

## License

This code is provided for research purposes only. For commercial use, please contact the authors for permission.

---

**Note**: The country/sector indices are hard‑coded for the ADB‑MRIO 2024 E62 dataset. Verify and adjust them if you apply the code to other data sources.
