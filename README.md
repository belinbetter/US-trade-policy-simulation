# US Trade Policy Simulation Program

This repository contains the Python implementation of the simulation model used in the paper:  
**"Measurement and Analysis of China's Industrial Relocation under the US Friend-Shoring and Near-Shoring Strategy"** (美国友岸化近岸化战略下中国产业转移的测度与分析).  

The program simulates the impact of US trade policies (anti-dumping, anti-circumvention, etc.) on global production networks and China's industrial relocation based on multi-regional input-output (MRIO) data, generating counterfactual trade matrices for analysis.

## Overview

The program adjusts trade flows between China, the US, and a set of "transshipment" countries (e.g., Mexico, Vietnam, Malaysia) using intermediate goods trade matrices derived from the ADB-MRIO database (2024 update, 62 economies, 35 sectors). It simulates three policy scenarios:

- **Scenario 1**: The US imposes traditional trade remedies (anti-dumping/anti-subsidy) on China. A fraction of China's exports to the US (determined by the parameter `drop_ratio`) is redirected to transshipment countries, while the US's missing imports are sourced from the rest of the world (excluding China).
- **Scenario 2**: In addition to Scenario 1, the US also applies anti-circumvention measures. China's exports to both the US and transshipment countries are reduced by the same fraction, and the reduced amount is redirected to the rest of the world (excluding China and the affected countries).
- **Scenario 3**: Same as Scenario 2, but the reduced exports are reallocated to China's domestic market (i.e., no foreign replacement).

The program modifies the original input-output matrix and saves the resulting counterfactual matrices as CSV files for subsequent analysis, such as backbone network extraction and centrality measures.

## Requirements

- Python 3.7+
- Required packages (recommended versions based on the test environment):
  - `numpy == 1.26.4`
  - `pandas == 2.2.2`
  - `tqdm == 4.66.4`

Install dependencies with:

```bash
pip install numpy==1.26.4 pandas==2.2.2 tqdm==4.66.4
```

## Data Description

The program expects an **intermediate goods trade matrix** in **CSV format**, with rows representing exporting sectors and columns representing importing sectors. Sector naming must follow the ADB-MRIO 2024 (E62) convention: `[country_code]S[sector_number]`, e.g., `PRCS01` for China's agriculture sector.

The code predefines the following countries with their starting row/column indices (based on the original ADB-MRIO file order):

- China (`PRC`): start index 246 (1‑based; converted to 0‑based in code)
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

**Important Note**: The indices depend on the specific ordering of the MRIO dataset. If you use a different version or a differently organized MRIO table, you must adjust the `start` values accordingly.

## Usage

The main function `trade_transfer` performs the trade flow modification. It is called in the `if __name__ == '__main__':` block as follows:

```python
from pathlib import Path

data_file = r"D:\3.数据库\邻接矩阵\CSV\[GIVCN] ADB2025(E62) 63R35S CSV格式\2024.csv"
drop_ratio = 0.2   # Trade reduction ratio, here 20%

for scenario in ['Scenario1', 'Scenario2', 'Scenario3']:
    trade_transfer(data_file, drop_ratio, scenario)
```

After execution, three new CSV files will be generated in the same directory:

- `2024_Scenario1_DropRatio0.2.csv`
- `2024_Scenario2_DropRatio0.2.csv`
- `2024_Scenario3_DropRatio0.2.csv`

### Function Parameters

- `data_path`: `str`, path to the input CSV file.
- `drop_ratio`: `float`, the fraction (0 to 1) by which trade flows are reduced.
- `trans_type`: `str`, scenario type, one of `'Scenario1'`, `'Scenario2'`, or `'Scenario3'`.

## Output Files

Each scenario produces a CSV file with the same format as the input (row and column order unchanged), with only the affected trade values updated according to the policy assumptions.

## Citation

If you use this code for academic research, please cite the original paper:

> Xing Lizhi, Yin Simeng, Zhang Pengyang, et al. Measurement and Analysis of China's Industrial Relocation under the US Friend-Shoring and Near-Shoring Strategy. Systems Engineering — Theory & Practice, 2024 (online publication)

You may also consider citing this code repository (DOI to be assigned).

## License

This code is provided for research purposes only. For commercial use, please contact the authors for permission.
