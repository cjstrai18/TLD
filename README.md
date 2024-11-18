# TLD and Comparison Class Implementation

This script defines the `TLD` class for representing the characteristics of a Thermoluminescent Dosimeter (TLD) and the `Comparison` class for comparing multiple TLDs across datasets.

---

## TLD Class

The `TLD` class encodes the characteristics of a singular TLD.

### Attributes:
- **`number`**: Index of the TLD.
- **`responses`**: List of response values (e.g., nC).
- **`chip_factors`**: List of chip factors calculated from responses.
- **`PMT`**: List of PMT values.
- **`refrence_light`**: List of reference light values.
- **Statistical Metrics**:
  - `nC_mean`, `nC_pct_SD`
  - `CF_mean`, `CF_pct_SD`
 

## Comparison Class

The `Comparison` class is designed to manage and analyze datasets of multiple TLDs, processing data files to calculate statistics and organize data for further analysis.

### Attributes:
- **`read_names`**: A list of names for each dataset being processed.
- **`num_groups`**: The number of TLD types in the dataset.
- **`types`**: A list specifying the types of TLDs (default is `['Chip']`).
- **`TLDs`**: A list to store `TLD` objects representing individual dosimeters.
- **`Reads`**: A Pandas DataFrame to organize processed data and calculated statistics.

### Methods:

1. **`pro_data(path, name, read_num)`**
   - **Purpose**: Processes an input file to extract response and reference values. Initializes or updates `TLD` objects and populates the `Reads` DataFrame.
   - **Key Features**:
     - Divides response values among groups to compute chip factors.
     - Adds PMT and reference light values to TLD objects.
     - Assigns data for each read to the appropriate column in the DataFrame.

2. **`chip_factors(nc)`**
   - **Purpose**: Calculates chip factors for a list of response values by dividing each value by the median of the list.
   - **Returns**: A list of calculated chip factors.

3. **`highlight_row(row)`**
   - **Purpose**: Highlights rows in the DataFrame where the percentage standard deviation (`%SD CF`) of chip factors exceeds a threshold (e.g., 3%).
   - **Returns**: A list of styles to be applied to the row.

4. **`cf()`**
   - **Purpose**: Filters the `Reads` DataFrame to focus on chip factor data and highlights rows exceeding the `%SD CF` threshold.
   - **Returns**: 
     - A styled DataFrame for visualization.
     - A filtered DataFrame showing only rows exceeding the threshold.
     - The full chip factor DataFrame.

5. **`comp_stats()`**
   - **Purpose**: Computes mean and percentage standard deviation statistics for response values (`nC`) and chip factors (`CF`).
   - **Key Features**:
     - Adds calculated statistics to the `Reads` DataFrame.
     - Updates corresponding statistical attributes in the `TLD` objects.

### Workflow:
- **Initialization**: Creates a `Comparison` object, processes the provided datasets, and initializes `TLD` objects.
- **Data Processing**: `pro_data` extracts, organizes, and calculates chip factors and response statistics for each dataset.
- **Visualization**: Use the `cf` method to highlight outliers and analyze chip factor distributions.
