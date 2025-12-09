# Greek Freelancer Tax Calculator

A comprehensive command-line tool for calculating taxes, social security contributions, and VAT obligations for freelancers operating in Greece. This calculator implements the 2024 Greek tax law and provides detailed breakdowns of all tax components with multiple payment schedule options.

## Table of Contents

- [Features](#features)
- [Target Users](#target-users)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Calculator](#running-the-calculator)
  - [Input Guide](#input-guide)
- [Examples](#examples) *(See also: [sample_calculations.txt](sample_calculations.txt) for detailed worked examples)*
  - [Example 1: Low Income (€15,000)](#example-1-low-income-15000)
  - [Example 2: Medium Income (€35,000)](#example-2-medium-income-35000)
  - [Example 3: High Income (€60,000)](#example-3-high-income-60000)
  - [Example 4: Income with Deductible Expenses](#example-4-income-with-deductible-expenses)
- [Understanding Greek Freelancer Taxes](#understanding-greek-freelancer-taxes)
  - [Income Tax (Progressive)](#income-tax-progressive)
  - [VAT (Value Added Tax)](#vat-value-added-tax)
  - [EFKA Social Security](#efka-social-security)
- [Tax Rates and Brackets](#tax-rates-and-brackets)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)
- [Legal Disclaimer](#legal-disclaimer)
- [Contributing](#contributing)

## Features

- **Progressive Income Tax Calculation**: Accurately calculates income tax across all 5 Greek tax brackets (9%, 22%, 28%, 36%, 44%)
- **Social Security Contributions**: Computes EFKA contributions (20% total: 13.33% main + 6.67% additional)
- **VAT Computation**: Calculates 24% VAT obligations for client billing
- **Deductible Expenses**: Supports business expense deductions from taxable income
- **Multiple Payment Schedules**: Choose monthly, quarterly, or annual payment frequencies
- **Detailed Breakdowns**: Shows tax calculations per bracket with effective tax rates
- **Results Export**: Automatically saves calculations to timestamped text files
- **Input Validation**: Robust error checking with helpful guidance messages
- **No External Dependencies**: Uses only Python standard library
- **User-Friendly Interface**: Clear prompts and formatted output for easy understanding

## Target Users

This tool is designed for:

- **Greek Freelancers**: Self-employed professionals, consultants, and contractors operating in Greece
- **Tax Planning**: Individuals estimating annual tax obligations for budgeting purposes
- **Scenario Analysis**: Comparing different income levels and expense deduction impacts
- **Accountants**: Quick estimates for client consultations (not a replacement for official calculations)

## Requirements

- **Python 3.6 or higher** (uses f-string formatting)
- No external libraries or dependencies required
- Works on Windows, macOS, and Linux

To check your Python version:

```bash
python3 --version
```

## Installation

1. **Clone or download this repository**:

```bash
git clone <repository-url>
cd greek-freelancer-tax-calculator
```

2. **No additional installation needed** - the calculator uses only Python's standard library.

## Usage

### Running the Calculator

1. Open a terminal or command prompt
2. Navigate to the project directory
3. Run the calculator:

```bash
python3 main.py
```

On Windows, you might need to use:

```bash
python main.py
```

### Input Guide

The calculator will guide you through the following steps:

1. **Gross Annual Income**: Enter your total annual income excluding VAT (e.g., 50000 for €50,000)
2. **Deductible Business Expenses**: Enter your total deductible expenses (e.g., 10000 for €10,000)
   - Enter 0 if you have no expenses to deduct
   - Must not exceed gross income
3. **Payment Frequency**: Choose how you'd like to view payment schedules:
   - Monthly (12 payments)
   - Quarterly (4 payments)
   - Annual (1 payment)
4. **Review and Confirm**: Verify your inputs before calculation

The calculator will then display:
- Detailed tax breakdown by bracket
- VAT obligations
- Social security contributions
- Payment schedule
- Net income after taxes

Results are automatically saved to a timestamped file in the same directory.

## Examples

For a **complete guide with detailed step-by-step calculations**, see [`sample_calculations.txt`](sample_calculations.txt). This file includes:
- Four comprehensive worked examples covering different income scenarios
- Detailed breakdown of progressive tax bracket calculations
- Monthly, quarterly, and annual payment schedules for each scenario
- Tax savings analysis showing the impact of deductible expenses
- Edge cases (low income with high expenses)
- Comparison table and key takeaways

**Quick Examples Overview:**

### Example 1: Low Income (€15,000)

**Scenario**: Freelancer with €15,000 gross annual income and no deductible expenses.

**Input**:
- Gross Annual Income: €15,000
- Deductible Expenses: €0
- Payment Frequency: Monthly

**Expected Results**:
- **Taxable Income**: €15,000
- **Income Tax**: €2,000
  - First €10,000 @ 9% = €900
  - Next €5,000 @ 22% = €1,100
- **Effective Income Tax Rate**: 13.33%
- **EFKA Social Security**: €3,000 (20%)
- **Total Taxes**: €5,000
- **Net Income**: €10,000
- **Effective Total Tax Rate**: 33.33%
- **VAT to Collect**: €3,600 (24%)
- **Monthly Tax Payment**: €416.67

### Example 2: Medium Income (€35,000)

**Scenario**: Freelancer with €35,000 gross annual income and no deductible expenses.

**Input**:
- Gross Annual Income: €35,000
- Deductible Expenses: €0
- Payment Frequency: Quarterly

**Expected Results**:
- **Taxable Income**: €35,000
- **Income Tax**: €8,200
  - First €10,000 @ 9% = €900
  - Next €10,000 @ 22% = €2,200
  - Next €10,000 @ 28% = €2,800
  - Next €5,000 @ 36% = €1,800
  - Remaining €0 @ 44% = €0
- **Effective Income Tax Rate**: 23.43%
- **EFKA Social Security**: €7,000 (20%)
- **Total Taxes**: €15,200
- **Net Income**: €19,800
- **Effective Total Tax Rate**: 43.43%
- **VAT to Collect**: €8,400 (24%)
- **Quarterly Tax Payment**: €3,800

### Example 3: High Income (€60,000)

**Scenario**: High-earning freelancer with €60,000 gross annual income and no deductible expenses.

**Input**:
- Gross Annual Income: €60,000
- Deductible Expenses: €0
- Payment Frequency: Annual

**Expected Results**:
- **Taxable Income**: €60,000
- **Income Tax**: €17,000
  - First €10,000 @ 9% = €900
  - Next €10,000 @ 22% = €2,200
  - Next €10,000 @ 28% = €2,800
  - Next €10,000 @ 36% = €3,600
  - Remaining €20,000 @ 44% = €8,800
- **Effective Income Tax Rate**: 28.33%
- **EFKA Social Security**: €12,000 (20%)
- **Total Taxes**: €29,000
- **Net Income**: €31,000
- **Effective Total Tax Rate**: 48.33%
- **VAT to Collect**: €14,400 (24%)
- **Annual Tax Payment**: €29,000

### Example 4: Income with Deductible Expenses

**Scenario**: Freelancer with €50,000 gross income and €12,000 in deductible business expenses (office rent, equipment, software subscriptions).

**Input**:
- Gross Annual Income: €50,000
- Deductible Expenses: €12,000
- Payment Frequency: Monthly

**Expected Results**:
- **Gross Income**: €50,000
- **Less Deductible Expenses**: -€12,000
- **Taxable Income**: €38,000
- **Income Tax**: €9,680
  - First €10,000 @ 9% = €900
  - Next €10,000 @ 22% = €2,200
  - Next €10,000 @ 28% = €2,800
  - Next €8,000 @ 36% = €2,880
- **Effective Income Tax Rate**: 25.47%
- **EFKA Social Security**: €10,000 (20% of gross income)
- **Total Taxes**: €19,680
- **Net Income**: €30,320
- **Effective Total Tax Rate**: 39.36%
- **VAT to Collect**: €12,000 (24%)
- **Monthly Tax Payment**: €1,640

**Tax Savings from Expenses**: By deducting €12,000 in expenses, this freelancer saves approximately €3,360 in income tax compared to not deducting any expenses.

## Understanding Greek Freelancer Taxes

Greek freelancers are subject to three main types of obligations:

### Income Tax (Progressive)

Income tax in Greece uses a progressive bracket system, meaning different portions of your income are taxed at different rates. Only the income within each bracket is taxed at that bracket's rate.

**How it works**:
1. Deductible business expenses are subtracted from gross income to determine taxable income
2. Taxable income is then split across the appropriate tax brackets
3. Each portion is taxed at its bracket's rate
4. All bracket taxes are summed for total income tax

**Key Points**:
- Higher income doesn't mean all income is taxed at the highest rate
- Deductible expenses can significantly reduce tax burden
- Effective tax rate is usually lower than the highest bracket rate

### VAT (Value Added Tax)

VAT is a 24% tax collected from clients and remitted to tax authorities.

**Important Notes**:
- VAT is **added to** your invoice amounts (not deducted from your income)
- You collect VAT from clients and pay it to the tax authority
- VAT is not part of your personal tax burden
- Example: For €10,000 in services, you invoice €12,400 (€10,000 + €2,400 VAT)
- The €10,000 is your income; the €2,400 is held in trust for the government

### EFKA Social Security

EFKA (Unified Social Security Entity) contributions provide social benefits including healthcare, pension, unemployment protection, and other social insurance.

**Structure**:
- **Main Insurance (13.33%)**: Primary social security contribution
- **Additional Contributions (6.67%)**: Healthcare, auxiliary pension, and other benefits
- **Total: 20%** of gross income

**Key Points**:
- Calculated on gross income (before expense deductions)
- Mandatory for all Greek freelancers
- Provides access to public healthcare system
- Counts toward state pension eligibility
- Cannot be reduced through expense deductions

## Tax Rates and Brackets

### Income Tax Brackets (2024)

| Taxable Income Range | Tax Rate | Tax on Bracket |
|----------------------|----------|----------------|
| €0 - €10,000 | 9% | Up to €900 |
| €10,001 - €20,000 | 22% | Up to €2,200 |
| €20,001 - €30,000 | 28% | Up to €2,800 |
| €30,001 - €40,000 | 36% | Up to €3,600 |
| €40,001 and above | 44% | Variable |

**Example Calculation for €35,000 taxable income**:
- First €10,000 × 9% = €900
- Next €10,000 × 22% = €2,200
- Next €10,000 × 28% = €2,800
- Next €5,000 × 36% = €1,800
- **Total Income Tax**: €7,700
- **Effective Rate**: 22.00%

### Other Tax Rates

| Tax Type | Rate | Applied To | Notes |
|----------|------|------------|-------|
| VAT | 24% | Gross Income | Collected from clients, remitted to authorities |
| EFKA Main | 13.33% | Gross Income | Primary social security |
| EFKA Additional | 6.67% | Gross Income | Healthcare and auxiliary benefits |
| **EFKA Total** | **20%** | **Gross Income** | **Total social security** |

## Output Files

### File Location

Calculation results are automatically saved to text files in the **same directory** as the calculator script.

### File Naming Format

```
tax_calculation_YYYY-MM-DD_HHMMSS.txt
```

**Example**: `tax_calculation_2024-03-15_143022.txt`

### File Contents

Each output file contains:

1. **Header**: Calculation date and time
2. **Input Parameters**: Gross income, expenses, payment frequency
3. **Income Breakdown**: Gross income minus expenses
4. **Income Tax Details**: Breakdown by bracket with amounts
5. **VAT and Social Security**: Detailed contribution breakdown
6. **Payment Schedule**: Installment amounts based on chosen frequency
7. **Summary**: Total taxes, effective rates, net income
8. **Notes**: Important reminders about VAT

### File Format

Files are saved as plain text (`.txt`) with formatted columns for easy reading. You can:
- Open them with any text editor
- Print them for records
- Import into spreadsheets for further analysis
- Share with accountants or financial advisors

## Troubleshooting

### Common Issues and Solutions

#### "Python not found" or "Command not recognized"

**Problem**: Python is not installed or not in system PATH.

**Solutions**:
1. Install Python 3.6+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Try using `python3` instead of `python` command
4. On Windows, try `py main.py` instead

#### "Permission denied" when saving files

**Problem**: The calculator cannot write files to the current directory.

**Solutions**:
1. Run the calculator from a directory where you have write permissions
2. On Linux/Mac, check directory permissions: `ls -la`
3. Move the calculator to your home directory or Documents folder
4. On Windows, avoid running from Program Files; use Desktop or Documents instead

#### "ModuleNotFoundError: No module named 'tax_calculator'"

**Problem**: The calculator files are not in the same directory or Python can't find them.

**Solutions**:
1. Ensure both `main.py` and `tax_calculator.py` are in the same folder
2. Run the calculator from the directory containing both files
3. Use `cd` command to navigate to the correct directory before running

#### Incorrect decimal separator

**Problem**: In some locales, comma is used as decimal separator instead of period.

**Solutions**:
1. Always use period (`.`) as decimal separator: `10000.50` not `10000,50`
2. You can omit decimals for whole numbers: `10000` instead of `10000.00`
3. Don't use thousand separators when entering: `50000` not `50,000`

#### Results seem incorrect

**Problem**: Calculated amounts don't match expectations.

**Solutions**:
1. Double-check your input values
2. Remember: EFKA is calculated on **gross income** (before expenses)
3. Remember: Income tax is calculated on **taxable income** (after expenses)
4. Review the bracket breakdown to understand how progressive taxation works
5. VAT is added to invoices, not deducted from income
6. Compare your results with the examples in this README

#### Calculator crashes or freezes

**Problem**: Application stops responding.

**Solutions**:
1. Press `Ctrl+C` to exit and restart
2. Ensure you're entering numeric values only (no currency symbols)
3. Check Python version meets minimum requirement (3.6+)
4. Try running with: `python3 -u main.py` for unbuffered output

### Getting Help

If you encounter issues not covered here:

1. Check that you're using Python 3.6 or higher
2. Verify both script files are present and unmodified
3. Review error messages carefully - they often indicate the problem
4. Try running the `tax_calculator.py` module directly to test calculations:
   ```bash
   python3 tax_calculator.py
   ```

## Legal Disclaimer

**IMPORTANT**: This calculator is provided for **estimation and planning purposes only**.

### Limitations

- This tool implements general Greek tax law as of 2024
- Tax laws change; rates and brackets may be updated by Greek authorities
- Individual circumstances may affect actual tax obligations
- Special tax regimes, exemptions, or deductions are not included
- Municipal taxes, solidarity contributions, and other levies are not calculated
- Professional activities may have different tax treatments

### Not a Substitute for Professional Advice

This calculator:
- ❌ Is **NOT** a substitute for professional tax advice
- ❌ Does **NOT** constitute official tax calculations
- ❌ Should **NOT** be used for official tax filing
- ❌ Does **NOT** replace consultation with certified accountants

### Recommendations

For official tax filing and personalized advice:
- ✅ Consult a certified Greek tax accountant (λογιστής)
- ✅ Use official tax submission platforms (Taxisnet)
- ✅ Verify current tax rates with Greek tax authorities (AADE)
- ✅ Seek professional advice for complex situations

### Accuracy and Liability

While we strive for accuracy:
- The authors assume no liability for financial decisions based on this tool
- Users are responsible for verifying all calculations
- No warranty of accuracy, completeness, or fitness for purpose is provided
- Use at your own risk

### Official Resources

For authoritative information, consult:
- **Greek Tax Authority (AADE)**: [www.aade.gr](https://www.aade.gr)
- **Taxisnet Portal**: [www.gsis.gr](https://www.gsis.gr)
- **EFKA (Social Security)**: [www.efka.gov.gr](https://www.efka.gov.gr)

## Contributing

Contributions are welcome! If you find bugs, have suggestions, or want to improve the calculator:

1. Test the calculator thoroughly
2. Document any issues with specific examples
3. Suggest improvements with clear rationale
4. Provide updated tax rates with official sources

### Reporting Issues

When reporting problems, please include:
- Python version (`python3 --version`)
- Operating system
- Complete error message
- Steps to reproduce
- Input values used

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**License**: Open source

*This calculator is an educational tool and community resource for Greek freelancers. For official tax compliance, always consult qualified professionals and official government resources.*
