# =============================================================================
# Schindler ESG-EBITDA Analysis
# =============================================================================
# This script performs a full analysis of ESG score variations and their
# impact on EBITDA for Schindler, including hypothesis testing, linear
# regressions, and a Monte Carlo simulation.
# =============================================================================

import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


# =============================================================================
# 1. Data Loading
# =============================================================================

data = pd.DataFrame({
    'Year': [2017, 2018, 2019, 2020, 2021, 2022],
    'EBITDA': [1174737278, 1297129815, 1623184191, 1568032991, 1534245845, 1391896149],
    'ESG': [46.69204383, 51.3056519, 53.60191841, 59.56069586, 50.99623897, 53.50251837],
    'Emissions': [73.58078603, 82.67857143, 84.9702381, 80.26315789, 72.94238683, 76.7118531],
    'HumanRights': [26.75, 37.21374046, 29.44983819, 26.77165354, 40.69506726, 56.51769088],
    'Leverage': [0.010085787, 0.062149158, 0.098131723, 0.085593454, 0.090028395, 0.087737127],
    'FirmSize': [22.72209314, 22.9051656, 23.00249398, 23.0203551, 23.169967, 23.20280284]
})


# =============================================================================
# 2. Compute Δ Variables (Rate of Variation)
# =============================================================================

for col in ['ESG', 'EBITDA', 'Emissions', 'HumanRights']:
    data[f'delta_{col}'] = data[col].pct_change()

data.dropna(inplace=True)  # Remove first row (NaN from pct_change)


# =============================================================================
# 3. Hypothesis Testing: Mean & Variance
# =============================================================================

# Two-sample t-test: are means of ΔESG and ΔEBITDA significantly different?
ttest_result = stats.ttest_ind(data['delta_ESG'], data['delta_EBITDA'])

# Levene's test: are variances of ΔESG and ΔEBITDA significantly different?
levene_result = stats.levene(data['delta_ESG'], data['delta_EBITDA'])

print("T-test (mean difference):", ttest_result)
print("Levene's test (variance difference):", levene_result)

# One-sample t-test: is mean of ΔEBITDA significantly different from 0?
t_stat_ebitda, p_val_ebitda = stats.ttest_1samp(data['delta_EBITDA'], popmean=0)
print("\nOne-sample t-test for ΔEBITDA:")
print(f"t-statistic = {t_stat_ebitda:.4f}, p-value = {p_val_ebitda:.4f}")

# One-sample t-test: is mean of ΔESG significantly different from 0?
t_stat_esg, p_val_esg = stats.ttest_1samp(data['delta_ESG'], popmean=0)
print("\nOne-sample t-test for ΔESG:")
print(f"t-statistic = {t_stat_esg:.4f}, p-value = {p_val_esg:.4f}")


# =============================================================================
# 4. Linear Regressions
# =============================================================================

# Model 1: ΔEBITDA ~ ΔESG (simple regression)
X1 = sm.add_constant(data['delta_ESG'])
model1 = sm.OLS(data['delta_EBITDA'], X1).fit()

# Model 2: ΔEBITDA ~ ΔESG + Leverage + FirmSize (full model with controls)
X2 = data[['delta_ESG', 'Leverage', 'FirmSize']]
X2 = sm.add_constant(X2)
model2 = sm.OLS(data['delta_EBITDA'], X2).fit()

# Model 3: ΔEBITDA ~ ΔESG + Leverage (reduced model to avoid multicollinearity)
X3 = data[['delta_ESG', 'Leverage']]
X3 = sm.add_constant(X3)
model3 = sm.OLS(data['delta_EBITDA'], X3).fit()

print(model1.summary())
print(model2.summary())
print(model3.summary())


# =============================================================================
# 5. Monte Carlo Simulation (10 years) — Based on Model 3
# =============================================================================

# Extract coefficients from Model 3: ΔEBITDA ~ ΔESG + Leverage
intercept = model3.params['const']
coef_esg = model3.params['delta_ESG']
coef_lev = model3.params['Leverage']

# Define distribution parameters from historical data
mean_esg = data['delta_ESG'].mean()
std_esg = data['delta_ESG'].std()

mean_lev = data['Leverage'].mean()
std_lev = data['Leverage'].std()

# Run Monte Carlo simulation (1000 iterations)
iterations = 1000
simulated_delta_ebitda = []

for _ in range(iterations):
    sim_esg = np.random.normal(mean_esg, std_esg)
    sim_lev = np.random.normal(mean_lev, std_lev)

    # Apply Model 3 regression equation
    delta_ebitda = (
        intercept
        + coef_esg * sim_esg
        + coef_lev * sim_lev
    )
    simulated_delta_ebitda.append(delta_ebitda)

# Display simulation statistics
sim_array = np.array(simulated_delta_ebitda)
print("\nMonte Carlo Simulation Results (ΔEBITDA based on Model 3):")
print("Mean:   ", np.mean(sim_array))
print("Std Dev:", np.std(sim_array))
print("Min:    ", np.min(sim_array))
print("Max:    ", np.max(sim_array))

# Plot the distribution of simulated ΔEBITDA
plt.figure(figsize=(10, 5))
plt.hist(sim_array, bins=50, color='steelblue', edgecolor='white')
plt.axvline(np.mean(sim_array), color='red', linestyle='--', label='Mean')
plt.title('Monte Carlo Simulation — Distribution of ΔEBITDA (Model 3)')
plt.xlabel('Simulated ΔEBITDA')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('monte_carlo_results.png', dpi=150)
plt.show()
