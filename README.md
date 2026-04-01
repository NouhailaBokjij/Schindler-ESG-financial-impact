# Schindler ESG Financial Impact Analysis

> Quantifying the economic cost (or benefit) of ESG score variations on EBITDA — a statistical study on Schindler Group.

---

## 📌 Overview

This project explores the relationship between **ESG (Environmental, Social, and Governance) score variations** and **EBITDA performance** for **Schindler Group**, a global leader in elevators and escalators listed on the STOXX Europe 600 index.

The analysis covers the period **2017–2022** and combines hypothesis testing, linear regression modeling, and Monte Carlo simulation to quantify the financial impact of ESG management.

---

## 🧠 Methodology

### 1. Data & Variables
- **ESG scores** and **EBITDA** extracted from Refinitiv
- Rates of variation computed as: `δ(V) = (Vᵢ - Vᵢ₋₁) / Vᵢ₋₁`
- Control variables: **Leverage**, **Firm Size**
- ESG sub-components: **Emissions score**, **Human Rights score**

### 2. Hypothesis Testing
- Two-sample t-test: comparing means of ΔESG vs ΔEBITDA
- Levene's test: comparing variances of ΔESG vs ΔEBITDA
- One-sample t-tests: testing if ΔESG and ΔEBITDA are significantly different from 0

### 3. Linear Regressions
Three OLS regression models estimated:
| Model | Specification |
|-------|--------------|
| Model 1 | ΔEBITDA ~ ΔESG |
| Model 2 | ΔEBITDA ~ ΔESG + Leverage + Firm Size |
| Model 3 | ΔEBITDA ~ ΔESG + Leverage *(selected model)* |

### 4. Monte Carlo Simulation
- 1,000 iterations simulating ΔEBITDA over a 10-year horizon
- Based on Model 3 coefficients
- Input variables (ΔESG, Leverage) drawn from normal distributions fitted on historical data

---

## 📁 Repository Structure

```
schindler-esg-financial-impact/
├── schindler_esg_analysis.py   # Full Python analysis script
├── report/
│   └── schindler_esg_report.pdf  # Final written report
└── README.md
```

---

## 🛠️ Libraries Used

| Library | Purpose |
|---------|---------|
| `pandas` | Data manipulation |
| `numpy` | Numerical computation |
| `scipy.stats` | Hypothesis testing |
| `statsmodels` | OLS regression models |
| `matplotlib` | Data visualization |

---

## 🏢 About Schindler Group

Schindler is a Swiss multinational founded in 1874, operating in over 100 countries. It is one of the world's largest providers of elevators, escalators, and related services. The company is part of the **STOXX Europe 600 (SXXP)** index and is classified under the **Industrial Machinery & Equipment** sector.

---

## 📚 Academic Context

This project was completed as part of the **Fil Rouge case study** at ESCP Business School (2024–2025), under the supervision of F. Desmoulins-Lebeault and A. Guéniche.

---

## ⚠️ Disclaimer

Data used in this project was sourced from **Refinitiv Eikon** for academic purposes only. Raw data files are not included in this repository due to licensing restrictions.
