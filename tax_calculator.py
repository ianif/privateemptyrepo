#!/usr/bin/env python3
"""
Greek Tax Calculator Module for Freelancers

This module provides comprehensive tax calculation functions for Greek freelancers,
implementing the 2024 Greek tax law requirements including:
- Progressive income tax brackets
- VAT (Value Added Tax)
- EFKA social security contributions

All monetary values use floats and calculations are accurate to 2 decimal places.
"""

__author__ = "Tax Calculator"
__version__ = "1.0.0"

from typing import Dict, List, Tuple, Union, Literal

# ============================================================================
# TAX CONSTANTS - Greek Tax Law 2024
# ============================================================================

# Income Tax Brackets (in EUR)
# Progressive tax system with 5 brackets
INCOME_TAX_BRACKETS = [
    (10000.00, 0.09),   # €0 - €10,000: 9%
    (20000.00, 0.22),   # €10,001 - €20,000: 22%
    (30000.00, 0.28),   # €20,001 - €30,000: 28%
    (40000.00, 0.36),   # €30,001 - €40,000: 36%
    (float('inf'), 0.44)  # Over €40,000: 44%
]

# VAT Rate for Greece
VAT_RATE = 0.24  # 24%

# EFKA Social Security Rates for Freelancers
# Main insurance contribution rate
EFKA_MAIN_RATE = 0.1333  # 13.33%

# Additional EFKA contributions (healthcare, auxiliary pension, etc.)
EFKA_ADDITIONAL_RATE = 0.0667  # 6.67%

# Total EFKA rate
EFKA_TOTAL_RATE = EFKA_MAIN_RATE + EFKA_ADDITIONAL_RATE  # 20%

# Payment schedule frequencies
VALID_FREQUENCIES = ['monthly', 'quarterly', 'annual']


# ============================================================================
# CORE TAX CALCULATION FUNCTIONS
# ============================================================================

def calculate_taxable_income(gross_income: float, deductible_expenses: float) -> float:
    """
    Calculate taxable income after deducting eligible expenses.
    
    Taxable income is the base for income tax calculations and is computed
    as gross income minus deductible expenses. Handles edge cases where
    expenses exceed income.
    
    Args:
        gross_income (float): Total gross income in EUR
        deductible_expenses (float): Total deductible business expenses in EUR
    
    Returns:
        float: Taxable income (rounded to 2 decimal places, minimum 0.00)
    
    Examples:
        >>> # Example 1: Standard case with expenses
        >>> calculate_taxable_income(50000, 10000)
        40000.0
        
        >>> # Example 2: Edge case - expenses exceed income
        >>> calculate_taxable_income(10000, 15000)
        0.0
        
        >>> # Example 3: No expenses
        >>> calculate_taxable_income(35000, 0)
        35000.0
        
        >>> # Example 4: Low income with moderate expenses
        >>> calculate_taxable_income(12000, 9000)
        3000.0
    """
    # Handle edge case: expenses exceeding income
    taxable = max(0.0, gross_income - deductible_expenses)
    return round(taxable, 2)


def calculate_income_tax(taxable_income: float) -> Dict[str, Union[float, List[Dict[str, Union[float, str]]]]]:
    """
    Calculate progressive income tax based on Greek tax brackets for 2024.
    
    Applies progressive taxation where each bracket is taxed at its own rate.
    Only the portion of income within each bracket is taxed at that bracket's rate.
    
    Greek Income Tax Brackets:
    - €0 - €10,000: 9%
    - €10,001 - €20,000: 22%
    - €20,001 - €30,000: 28%
    - €30,001 - €40,000: 36%
    - Over €40,000: 44%
    
    Args:
        taxable_income (float): Taxable income in EUR (after deductions)
    
    Returns:
        dict: Dictionary containing:
            - 'total_tax' (float): Total income tax owed
            - 'effective_rate' (float): Effective tax rate as percentage
            - 'bracket_breakdown' (list): List of dicts with tax per bracket
    
    Examples:
        >>> # Example 1: Low income (single bracket)
        >>> result = calculate_income_tax(3000)
        >>> result['total_tax']
        270.0
        >>> result['effective_rate']
        9.0
        
        >>> # Example 2: Medium income (spans 2 brackets)
        >>> result = calculate_income_tax(15000)
        >>> result['total_tax']
        2000.0
        >>> # €10,000 @ 9% = €900, plus €5,000 @ 22% = €1,100, total = €2,000
        
        >>> # Example 3: High income (spans all brackets)
        >>> result = calculate_income_tax(50000)
        >>> result['total_tax']
        13900.0
        >>> result['effective_rate']
        27.8
        >>> # Breakdown: €900 + €2,200 + €2,800 + €3,600 + €4,400 = €13,900
        
        >>> # Example 4: Zero income
        >>> result = calculate_income_tax(0)
        >>> result['total_tax']
        0.0
    """
    if taxable_income <= 0:
        return {
            'total_tax': 0.0,
            'effective_rate': 0.0,
            'bracket_breakdown': []
        }
    
    total_tax = 0.0
    bracket_breakdown = []
    remaining_income = taxable_income
    previous_bracket_limit = 0.0
    
    for bracket_limit, rate in INCOME_TAX_BRACKETS:
        if remaining_income <= 0:
            break
        
        # Calculate taxable amount in this bracket
        bracket_size = bracket_limit - previous_bracket_limit
        taxable_in_bracket = min(remaining_income, bracket_size)
        
        # Calculate tax for this bracket
        tax_in_bracket = taxable_in_bracket * rate
        total_tax += tax_in_bracket
        
        # Record breakdown
        bracket_breakdown.append({
            'bracket_min': previous_bracket_limit,
            'bracket_max': bracket_limit if bracket_limit != float('inf') else 'unlimited',
            'rate': rate * 100,  # Convert to percentage
            'taxable_amount': round(taxable_in_bracket, 2),
            'tax_amount': round(tax_in_bracket, 2)
        })
        
        remaining_income -= taxable_in_bracket
        previous_bracket_limit = bracket_limit
    
    # Calculate effective tax rate
    effective_rate = (total_tax / taxable_income * 100) if taxable_income > 0 else 0.0
    
    return {
        'total_tax': round(total_tax, 2),
        'effective_rate': round(effective_rate, 2),
        'bracket_breakdown': bracket_breakdown
    }


def calculate_vat(gross_income: float) -> Dict[str, float]:
    """
    Calculate Value Added Tax (VAT) for Greek freelancers.
    
    Greek standard VAT rate is 24%. This is typically collected from clients
    and must be remitted to tax authorities.
    
    Args:
        gross_income (float): Total gross income in EUR (excluding VAT)
    
    Returns:
        dict: Dictionary containing:
            - 'vat_amount' (float): Total VAT to be collected/paid
            - 'rate' (float): VAT rate as percentage
            - 'total_with_vat' (float): Gross income plus VAT
    
    Examples:
        >>> # Example 1: €10,000 project
        >>> calculate_vat(10000)
        {'vat_amount': 2400.0, 'rate': 24.0, 'total_with_vat': 12400.0}
        >>> # Invoice client €12,400 total (you keep €10,000, remit €2,400)
        
        >>> # Example 2: €35,000 annual income
        >>> result = calculate_vat(35000)
        >>> result['vat_amount']
        8400.0
        >>> # Collect €8,400 VAT from clients throughout the year
        
        >>> # Example 3: Small project
        >>> calculate_vat(1500)
        {'vat_amount': 360.0, 'rate': 24.0, 'total_with_vat': 1860.0}
    """
    vat_amount = gross_income * VAT_RATE
    total_with_vat = gross_income + vat_amount
    
    return {
        'vat_amount': round(vat_amount, 2),
        'rate': VAT_RATE * 100,
        'total_with_vat': round(total_with_vat, 2)
    }


def calculate_social_security(gross_income: float) -> Dict[str, float]:
    """
    Calculate EFKA social security contributions for Greek freelancers.
    
    EFKA (Unified Social Security Entity) contributions include:
    - Main insurance: 13.33%
    - Additional contributions (healthcare, auxiliary pension, etc.): 6.67%
    - Total: 20%
    
    These contributions are mandatory for all freelancers in Greece and provide
    access to healthcare, pension, and other social benefits.
    
    Args:
        gross_income (float): Total gross income in EUR
    
    Returns:
        dict: Dictionary containing:
            - 'total_contribution' (float): Total EFKA contribution
            - 'main_insurance' (float): Main insurance contribution (13.33%)
            - 'additional_contributions' (float): Additional contributions (6.67%)
            - 'rate' (float): Total contribution rate as percentage
    
    Examples:
        >>> # Example 1: €30,000 gross income
        >>> result = calculate_social_security(30000)
        >>> result['total_contribution']
        6000.0
        >>> result['main_insurance']
        3999.0
        >>> result['additional_contributions']
        2001.0
        
        >>> # Example 2: €15,000 income (20% = €3,000)
        >>> calculate_social_security(15000)['total_contribution']
        3000.0
        
        >>> # Example 3: €60,000 income
        >>> result = calculate_social_security(60000)
        >>> result['total_contribution']
        12000.0
        >>> # Note: EFKA is always 20% of GROSS income, not taxable income!
        
        >>> # Example 4: Low income scenario
        >>> calculate_social_security(12000)['total_contribution']
        2400.0
    """
    main_insurance = gross_income * EFKA_MAIN_RATE
    additional_contributions = gross_income * EFKA_ADDITIONAL_RATE
    total_contribution = gross_income * EFKA_TOTAL_RATE
    
    return {
        'total_contribution': round(total_contribution, 2),
        'main_insurance': round(main_insurance, 2),
        'additional_contributions': round(additional_contributions, 2),
        'rate': EFKA_TOTAL_RATE * 100
    }


def calculate_all_taxes(gross_income: float, deductible_expenses: float) -> Dict[str, Union[float, Dict[str, Union[float, List[Dict[str, Union[float, str]]]]]]]:
    """
    Master function to calculate all tax components for Greek freelancers.
    
    This comprehensive function calculates:
    1. Taxable income (gross income - deductible expenses)
    2. Progressive income tax
    3. VAT obligations
    4. EFKA social security contributions
    5. Total tax burden and net income
    
    Args:
        gross_income (float): Total gross income in EUR (excluding VAT)
        deductible_expenses (float): Total deductible business expenses in EUR
    
    Returns:
        dict: Comprehensive dictionary containing:
            - 'gross_income' (float): Input gross income
            - 'deductible_expenses' (float): Input deductible expenses
            - 'taxable_income' (float): Calculated taxable income
            - 'income_tax' (dict): Full income tax breakdown
            - 'vat' (dict): VAT calculation details
            - 'social_security' (dict): EFKA contribution details
            - 'total_taxes' (float): Sum of income tax and social security
            - 'total_obligations' (float): Total including VAT
            - 'net_income' (float): Income after all taxes and contributions
            - 'effective_total_rate' (float): Total tax burden as percentage
    
    Examples:
        >>> # Example 1: €15,000 income with no expenses
        >>> result = calculate_all_taxes(15000, 0)
        >>> result['taxable_income']
        15000.0
        >>> result['income_tax']['total_tax']
        2000.0
        >>> result['social_security']['total_contribution']
        3000.0
        >>> result['total_taxes']
        5000.0
        >>> result['net_income']
        10000.0
        >>> result['effective_total_rate']
        33.33
        
        >>> # Example 2: €35,000 income with €5,000 expenses
        >>> result = calculate_all_taxes(35000, 5000)
        >>> result['taxable_income']
        30000.0
        >>> result['total_taxes']
        12900.0
        >>> result['net_income']
        22100.0
        
        >>> # Example 3: €60,000 income with €10,000 expenses
        >>> result = calculate_all_taxes(60000, 10000)
        >>> result['income_tax']['total_tax']
        13900.0
        >>> result['social_security']['total_contribution']
        12000.0
        >>> result['vat']['vat_amount']
        14400.0
        
        >>> # Example 4: Low income with high expenses
        >>> result = calculate_all_taxes(12000, 9000)
        >>> result['taxable_income']
        3000.0
        >>> result['income_tax']['total_tax']
        270.0
        >>> result['total_taxes']
        2670.0
    """
    # Handle edge case: zero or negative income
    if gross_income <= 0:
        return {
            'gross_income': round(gross_income, 2),
            'deductible_expenses': round(deductible_expenses, 2),
            'taxable_income': 0.0,
            'income_tax': calculate_income_tax(0),
            'vat': calculate_vat(0),
            'social_security': calculate_social_security(0),
            'total_taxes': 0.0,
            'total_obligations': 0.0,
            'net_income': 0.0,
            'effective_total_rate': 0.0
        }
    
    # Calculate taxable income
    taxable_income = calculate_taxable_income(gross_income, deductible_expenses)
    
    # Calculate individual tax components
    income_tax = calculate_income_tax(taxable_income)
    vat = calculate_vat(gross_income)
    social_security = calculate_social_security(gross_income)
    
    # Calculate totals
    total_taxes = income_tax['total_tax'] + social_security['total_contribution']
    total_obligations = total_taxes + vat['vat_amount']
    net_income = gross_income - total_taxes
    
    # Calculate effective total tax rate (excluding VAT as it's passed to clients)
    effective_total_rate = (total_taxes / gross_income * 100) if gross_income > 0 else 0.0
    
    return {
        'gross_income': round(gross_income, 2),
        'deductible_expenses': round(deductible_expenses, 2),
        'taxable_income': round(taxable_income, 2),
        'income_tax': income_tax,
        'vat': vat,
        'social_security': social_security,
        'total_taxes': round(total_taxes, 2),
        'total_obligations': round(total_obligations, 2),
        'net_income': round(net_income, 2),
        'effective_total_rate': round(effective_total_rate, 2)
    }


def calculate_payment_schedule(annual_tax: float, frequency: str = 'monthly') -> Dict[str, Union[float, str, int, List[Dict[str, Union[int, float]]]]]:
    """
    Calculate payment schedule breakdown for tax payments.
    
    Greek freelancers can make tax payments on different schedules.
    This function breaks down annual tax obligations into installments
    based on the selected payment frequency.
    
    Args:
        annual_tax (float): Total annual tax amount in EUR
        frequency (str): Payment frequency - 'monthly', 'quarterly', or 'annual'
                        Default is 'monthly'
    
    Returns:
        dict: Dictionary containing:
            - 'annual_total' (float): Total annual tax
            - 'frequency' (str): Payment frequency
            - 'number_of_payments' (int): Number of payment installments
            - 'payment_amount' (float): Amount per payment
            - 'schedule' (list): List of payment details with period numbers
    
    Raises:
        ValueError: If frequency is not one of the valid options
    
    Examples:
        >>> # Example 1: Monthly payments for €12,000 annual tax
        >>> result = calculate_payment_schedule(12000, 'monthly')
        >>> result['payment_amount']
        1000.0
        >>> result['number_of_payments']
        12
        >>> len(result['schedule'])
        12
        
        >>> # Example 2: Quarterly payments
        >>> result = calculate_payment_schedule(12000, 'quarterly')
        >>> result['payment_amount']
        3000.0
        >>> result['number_of_payments']
        4
        
        >>> # Example 3: Annual payment (single lump sum)
        >>> result = calculate_payment_schedule(5000, 'annual')
        >>> result['payment_amount']
        5000.0
        >>> result['number_of_payments']
        1
        
        >>> # Example 4: High tax burden with monthly payments
        >>> result = calculate_payment_schedule(25900, 'monthly')
        >>> result['payment_amount']
        2158.33
        >>> # €2,158.33 per month for 12 months
    """
    # Validate frequency
    if frequency.lower() not in VALID_FREQUENCIES:
        raise ValueError(
            f"Invalid frequency '{frequency}'. Must be one of: {', '.join(VALID_FREQUENCIES)}"
        )
    
    frequency = frequency.lower()
    
    # Determine number of payments based on frequency
    payments_per_year = {
        'monthly': 12,
        'quarterly': 4,
        'annual': 1
    }
    
    num_payments = payments_per_year[frequency]
    
    # Calculate payment amount per installment
    payment_amount = annual_tax / num_payments
    
    # Generate payment schedule
    schedule = []
    for i in range(1, num_payments + 1):
        schedule.append({
            'period_number': i,
            'payment_amount': round(payment_amount, 2)
        })
    
    return {
        'annual_total': round(annual_tax, 2),
        'frequency': frequency,
        'number_of_payments': num_payments,
        'payment_amount': round(payment_amount, 2),
        'schedule': schedule
    }


# ============================================================================
# MODULE TESTING (only runs when module is executed directly)
# ============================================================================

if __name__ == "__main__":
    # This section only runs when the module is executed directly
    # It does not execute when the module is imported
    print("Greek Tax Calculator Module - Test Run")
    print("=" * 60)
    
    # Test case: Freelancer with €50,000 gross income and €10,000 expenses
    test_gross = 50000.0
    test_expenses = 10000.0
    
    print(f"\nTest Case: Gross Income = €{test_gross:,.2f}, Expenses = €{test_expenses:,.2f}")
    print("-" * 60)
    
    results = calculate_all_taxes(test_gross, test_expenses)
    
    print(f"Taxable Income: €{results['taxable_income']:,.2f}")
    print(f"Income Tax: €{results['income_tax']['total_tax']:,.2f}")
    print(f"Social Security (EFKA): €{results['social_security']['total_contribution']:,.2f}")
    print(f"VAT (24%): €{results['vat']['vat_amount']:,.2f}")
    print(f"Total Tax Burden: €{results['total_taxes']:,.2f}")
    print(f"Net Income: €{results['net_income']:,.2f}")
    print(f"Effective Tax Rate: {results['effective_total_rate']:.2f}%")
    
    print("\n" + "=" * 60)
    print("Module can be safely imported without executing test code.")
