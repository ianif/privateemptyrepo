#!/usr/bin/env python3
"""
Greek Freelancer Tax Calculator - Command Line Interface

Interactive CLI application for calculating taxes for Greek freelancers.
Provides a user-friendly interface with robust input validation and
comprehensive tax calculations including income tax, VAT, and social security.

TYPICAL USAGE:
    python main.py
    
    Then follow the interactive prompts to:
    1. Enter gross annual income (e.g., 35000 for €35,000)
    2. Enter deductible business expenses (e.g., 5000 for €5,000)
    3. Choose payment frequency (monthly, quarterly, or annual)
    4. Review and confirm inputs
    5. View comprehensive tax breakdown and payment schedule
    6. Results are automatically saved to a timestamped file

EXAMPLE SESSION:
    Gross annual income (€): 35000
    Deductible expenses (€): 5000
    Payment frequency: 2 (Quarterly)
    
    → Calculates: 
      - Taxable income: €30,000
      - Income tax: €5,900
      - EFKA: €7,000
      - Total taxes: €12,900
      - Net income: €22,100
      - Quarterly payment: €3,225
"""

import sys
from datetime import datetime
from tax_calculator import (
    calculate_all_taxes,
    calculate_payment_schedule,
    VALID_FREQUENCIES
)


# ============================================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================================

def validate_positive_number(value_str, field_name):
    """
    Validate that input is a positive number (> 0).
    
    Args:
        value_str (str): String input from user
        field_name (str): Name of field for error messages
    
    Returns:
        float: Validated positive number
    
    Raises:
        ValueError: If input is not a valid positive number
    """
    try:
        value = float(value_str.strip())
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than zero.")
        return value
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"{field_name} must be a valid number.")
        raise


def validate_non_negative_number(value_str, field_name):
    """
    Validate that input is a non-negative number (>= 0).
    
    Args:
        value_str (str): String input from user
        field_name (str): Name of field for error messages
    
    Returns:
        float: Validated non-negative number
    
    Raises:
        ValueError: If input is not a valid non-negative number
    """
    try:
        value = float(value_str.strip())
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")
        return value
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"{field_name} must be a valid number.")
        raise


def validate_expenses_against_income(expenses, gross_income):
    """
    Validate that expenses do not exceed gross income.
    
    Args:
        expenses (float): Deductible expenses amount
        gross_income (float): Gross income amount
    
    Raises:
        ValueError: If expenses exceed gross income
    """
    if expenses > gross_income:
        raise ValueError(
            f"Deductible expenses (€{expenses:,.2f}) cannot exceed "
            f"gross income (€{gross_income:,.2f})."
        )


def validate_realistic_amount(value, field_name, max_amount=10000000):
    """
    Validate that amount is realistic (not absurdly high).
    
    Args:
        value (float): Amount to validate
        field_name (str): Name of field for error messages
        max_amount (float): Maximum realistic amount (default: 10 million EUR)
    
    Raises:
        ValueError: If amount exceeds realistic maximum
    """
    if value > max_amount:
        raise ValueError(
            f"{field_name} of €{value:,.2f} seems unrealistic. "
            f"Please enter a value less than €{max_amount:,.0f}."
        )


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_header():
    """Display application header."""
    print("\n" + "=" * 70)
    print("  GREEK FREELANCER TAX CALCULATOR")
    print("=" * 70)


def display_main_menu():
    """Display main menu options."""
    print("\n" + "-" * 70)
    print("MAIN MENU")
    print("-" * 70)
    print("1. New Calculation")
    print("2. Exit")
    print("-" * 70)


def display_frequency_menu():
    """
    Display payment frequency menu and get user selection.
    
    Returns:
        str: Selected frequency ('monthly', 'quarterly', or 'annual')
    """
    print("\n" + "-" * 70)
    print("SELECT PAYMENT FREQUENCY")
    print("-" * 70)
    print("1. Monthly (12 payments per year)")
    print("2. Quarterly (4 payments per year)")
    print("3. Annual (1 payment per year)")
    print("-" * 70)
    
    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                return 'monthly'
            elif choice == '2':
                return 'quarterly'
            elif choice == '3':
                return 'annual'
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except (EOFError, KeyboardInterrupt):
            print("\n\n❌ Input cancelled.")
            sys.exit(0)


def format_currency(amount):
    """
    Format amount as currency string.
    
    Args:
        amount (float): Amount to format
    
    Returns:
        str: Formatted currency string
    """
    return f"€{amount:,.2f}"


def display_results(calculation_dict, payment_frequency):
    """
    Display comprehensive tax calculation results in terminal.
    
    Shows detailed breakdown including:
    - Input parameters
    - Income and expense details
    - Income tax bracket breakdown
    - VAT and social security contributions
    - Payment schedule
    - Summary with effective tax rates
    
    Args:
        calculation_dict (dict): Results from calculate_all_taxes()
        payment_frequency (str): Payment frequency ('monthly', 'quarterly', 'annual')
    """
    # Extract data for readability
    gross_income = calculation_dict['gross_income']
    expenses = calculation_dict['deductible_expenses']
    taxable_income = calculation_dict['taxable_income']
    income_tax = calculation_dict['income_tax']
    vat = calculation_dict['vat']
    social_security = calculation_dict['social_security']
    total_taxes = calculation_dict['total_taxes']
    net_income = calculation_dict['net_income']
    effective_total_rate = calculation_dict['effective_total_rate']
    
    # Calculate payment schedule
    payment_schedule = calculate_payment_schedule(total_taxes, payment_frequency)
    
    # Display header
    print("\n" + "=" * 70)
    print("TAX CALCULATION RESULTS")
    print("=" * 70)
    print(f"Calculation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Section 1: Input Parameters
    print("\n" + "─" * 70)
    print("INPUT PARAMETERS")
    print("─" * 70)
    print(f"{'Gross Annual Income:':<35} {format_currency(gross_income):>34}")
    print(f"{'Deductible Business Expenses:':<35} {format_currency(expenses):>34}")
    print(f"{'Payment Frequency:':<35} {payment_frequency.capitalize():>34}")
    
    # Section 2: Income Breakdown
    print("\n" + "─" * 70)
    print("INCOME BREAKDOWN")
    print("─" * 70)
    print(f"{'Gross Income:':<35} {format_currency(gross_income):>34}")
    print(f"{'Less: Deductible Expenses:':<35} {format_currency(expenses):>34}")
    print(f"{'Taxable Income:':<35} {format_currency(taxable_income):>34}")
    
    # Section 3: Income Tax Breakdown by Bracket
    print("\n" + "─" * 70)
    print("INCOME TAX BREAKDOWN BY BRACKET")
    print("─" * 70)
    
    if income_tax['bracket_breakdown']:
        for bracket in income_tax['bracket_breakdown']:
            bracket_min = format_currency(bracket['bracket_min'])
            if bracket['bracket_max'] == 'unlimited':
                bracket_range = f"{bracket_min}+"
            else:
                bracket_max = format_currency(bracket['bracket_max'])
                bracket_range = f"{bracket_min} - {bracket_max}"
            
            rate_str = f"{bracket['rate']:.0f}%"
            taxable_amt = format_currency(bracket['taxable_amount'])
            tax_amt = format_currency(bracket['tax_amount'])
            
            print(f"  {bracket_range:<30} @ {rate_str:>4}")
            print(f"    {'Taxable amount:':<30} {taxable_amt:>30}")
            print(f"    {'Tax on this bracket:':<30} {tax_amt:>30}")
            print()
    else:
        print("  No income tax (taxable income is zero)")
    
    print(f"{'Total Income Tax:':<35} {format_currency(income_tax['total_tax']):>34}")
    print(f"{'Effective Income Tax Rate:':<35} {income_tax['effective_rate']:>33.2f}%")
    
    # Section 4: Other Taxes and Contributions
    print("\n" + "─" * 70)
    print("VAT AND SOCIAL SECURITY")
    print("─" * 70)
    print(f"{'VAT (24%):':<35} {format_currency(vat['vat_amount']):>34}")
    print(f"  {'(To be collected from clients)':<35}")
    print()
    print(f"{'Social Security (EFKA - 20%):':<35} {format_currency(social_security['total_contribution']):>34}")
    print(f"  {'Main Insurance (13.33%):':<35} {format_currency(social_security['main_insurance']):>34}")
    print(f"  {'Additional Contributions (6.67%):':<35} {format_currency(social_security['additional_contributions']):>34}")
    
    # Section 5: Payment Schedule
    print("\n" + "─" * 70)
    print(f"PAYMENT SCHEDULE ({payment_frequency.upper()})")
    print("─" * 70)
    print(f"{'Total Annual Tax (excl. VAT):':<35} {format_currency(payment_schedule['annual_total']):>34}")
    print(f"{'Number of Payments:':<35} {payment_schedule['number_of_payments']:>34}")
    print(f"{'Amount per Payment:':<35} {format_currency(payment_schedule['payment_amount']):>34}")
    
    if payment_schedule['number_of_payments'] > 1:
        print(f"\n  Payment Schedule:")
        for payment in payment_schedule['schedule']:
            period_label = f"Payment #{payment['period_number']}"
            print(f"    {period_label:<30} {format_currency(payment['payment_amount']):>34}")
    
    # Section 6: Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"{'Gross Income:':<35} {format_currency(gross_income):>34}")
    print(f"{'Total Taxes (Income Tax + EFKA):':<35} {format_currency(total_taxes):>34}")
    print(f"{'Effective Total Tax Rate:':<35} {effective_total_rate:>33.2f}%")
    print(f"{'Net Income (After Taxes):':<35} {format_currency(net_income):>34}")
    print("=" * 70)
    print(f"\nNote: VAT of {format_currency(vat['vat_amount'])} should be collected from clients")
    print("      and remitted to tax authorities separately.")
    print("=" * 70)


def save_results_to_file(calculation_dict, payment_frequency):
    """
    Save tax calculation results to a timestamped text file.
    
    Creates a file with format: tax_calculation_YYYY-MM-DD_HHMMSS.txt
    Contains the same information as displayed in terminal for record-keeping.
    
    Args:
        calculation_dict (dict): Results from calculate_all_taxes()
        payment_frequency (str): Payment frequency ('monthly', 'quarterly', 'annual')
    
    Returns:
        str: Filename if successful, None if error occurred
    """
    try:
        # Generate timestamp for filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename = f"tax_calculation_{timestamp}.txt"
        
        # Extract data for readability
        gross_income = calculation_dict['gross_income']
        expenses = calculation_dict['deductible_expenses']
        taxable_income = calculation_dict['taxable_income']
        income_tax = calculation_dict['income_tax']
        vat = calculation_dict['vat']
        social_security = calculation_dict['social_security']
        total_taxes = calculation_dict['total_taxes']
        net_income = calculation_dict['net_income']
        effective_total_rate = calculation_dict['effective_total_rate']
        
        # Calculate payment schedule
        payment_schedule = calculate_payment_schedule(total_taxes, payment_frequency)
        
        # Build content
        content_lines = []
        
        # Header
        content_lines.append("=" * 70)
        content_lines.append("GREEK FREELANCER TAX CALCULATION RESULTS")
        content_lines.append("=" * 70)
        content_lines.append(f"Calculation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content_lines.append("=" * 70)
        
        # Section 1: Input Parameters
        content_lines.append("\n" + "-" * 70)
        content_lines.append("INPUT PARAMETERS")
        content_lines.append("-" * 70)
        content_lines.append(f"{'Gross Annual Income:':<35} {format_currency(gross_income):>34}")
        content_lines.append(f"{'Deductible Business Expenses:':<35} {format_currency(expenses):>34}")
        content_lines.append(f"{'Payment Frequency:':<35} {payment_frequency.capitalize():>34}")
        
        # Section 2: Income Breakdown
        content_lines.append("\n" + "-" * 70)
        content_lines.append("INCOME BREAKDOWN")
        content_lines.append("-" * 70)
        content_lines.append(f"{'Gross Income:':<35} {format_currency(gross_income):>34}")
        content_lines.append(f"{'Less: Deductible Expenses:':<35} {format_currency(expenses):>34}")
        content_lines.append(f"{'Taxable Income:':<35} {format_currency(taxable_income):>34}")
        
        # Section 3: Income Tax Breakdown by Bracket
        content_lines.append("\n" + "-" * 70)
        content_lines.append("INCOME TAX BREAKDOWN BY BRACKET")
        content_lines.append("-" * 70)
        
        if income_tax['bracket_breakdown']:
            for bracket in income_tax['bracket_breakdown']:
                bracket_min = format_currency(bracket['bracket_min'])
                if bracket['bracket_max'] == 'unlimited':
                    bracket_range = f"{bracket_min}+"
                else:
                    bracket_max = format_currency(bracket['bracket_max'])
                    bracket_range = f"{bracket_min} - {bracket_max}"
                
                rate_str = f"{bracket['rate']:.0f}%"
                taxable_amt = format_currency(bracket['taxable_amount'])
                tax_amt = format_currency(bracket['tax_amount'])
                
                content_lines.append(f"  {bracket_range:<30} @ {rate_str:>4}")
                content_lines.append(f"    {'Taxable amount:':<30} {taxable_amt:>30}")
                content_lines.append(f"    {'Tax on this bracket:':<30} {tax_amt:>30}")
                content_lines.append("")
        else:
            content_lines.append("  No income tax (taxable income is zero)")
        
        content_lines.append(f"{'Total Income Tax:':<35} {format_currency(income_tax['total_tax']):>34}")
        content_lines.append(f"{'Effective Income Tax Rate:':<35} {income_tax['effective_rate']:>33.2f}%")
        
        # Section 4: Other Taxes and Contributions
        content_lines.append("\n" + "-" * 70)
        content_lines.append("VAT AND SOCIAL SECURITY")
        content_lines.append("-" * 70)
        content_lines.append(f"{'VAT (24%):':<35} {format_currency(vat['vat_amount']):>34}")
        content_lines.append(f"  {'(To be collected from clients)':<35}")
        content_lines.append("")
        content_lines.append(f"{'Social Security (EFKA - 20%):':<35} {format_currency(social_security['total_contribution']):>34}")
        content_lines.append(f"  {'Main Insurance (13.33%):':<35} {format_currency(social_security['main_insurance']):>34}")
        content_lines.append(f"  {'Additional Contributions (6.67%):':<35} {format_currency(social_security['additional_contributions']):>34}")
        
        # Section 5: Payment Schedule
        content_lines.append("\n" + "-" * 70)
        content_lines.append(f"PAYMENT SCHEDULE ({payment_frequency.upper()})")
        content_lines.append("-" * 70)
        content_lines.append(f"{'Total Annual Tax (excl. VAT):':<35} {format_currency(payment_schedule['annual_total']):>34}")
        content_lines.append(f"{'Number of Payments:':<35} {payment_schedule['number_of_payments']:>34}")
        content_lines.append(f"{'Amount per Payment:':<35} {format_currency(payment_schedule['payment_amount']):>34}")
        
        if payment_schedule['number_of_payments'] > 1:
            content_lines.append(f"\n  Payment Schedule:")
            for payment in payment_schedule['schedule']:
                period_label = f"Payment #{payment['period_number']}"
                content_lines.append(f"    {period_label:<30} {format_currency(payment['payment_amount']):>34}")
        
        # Section 6: Summary
        content_lines.append("\n" + "=" * 70)
        content_lines.append("SUMMARY")
        content_lines.append("=" * 70)
        content_lines.append(f"{'Gross Income:':<35} {format_currency(gross_income):>34}")
        content_lines.append(f"{'Total Taxes (Income Tax + EFKA):':<35} {format_currency(total_taxes):>34}")
        content_lines.append(f"{'Effective Total Tax Rate:':<35} {effective_total_rate:>33.2f}%")
        content_lines.append(f"{'Net Income (After Taxes):':<35} {format_currency(net_income):>34}")
        content_lines.append("=" * 70)
        content_lines.append(f"\nNote: VAT of {format_currency(vat['vat_amount'])} should be collected from clients")
        content_lines.append("      and remitted to tax authorities separately.")
        content_lines.append("=" * 70)
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))
        
        return filename
        
    except IOError as e:
        print(f"\n⚠️  Warning: Could not save results to file.")
        print(f"   Error: {str(e)}")
        return None
    except Exception as e:
        print(f"\n⚠️  Warning: An unexpected error occurred while saving file.")
        print(f"   Error: {str(e)}")
        return None


# ============================================================================
# USER INPUT COLLECTION FUNCTIONS
# ============================================================================

def get_gross_income():
    """
    Prompt user for gross annual income with validation.
    
    Returns:
        float: Validated gross annual income
    """
    print("\n" + "-" * 70)
    print("GROSS ANNUAL INCOME")
    print("-" * 70)
    print("Enter your total gross annual income (excluding VAT).")
    print("Example: 50000 for €50,000")
    print("-" * 70)
    
    while True:
        try:
            value_str = input("Gross annual income (€): ").strip()
            
            # Handle empty input
            if not value_str:
                print("❌ Please enter a value.")
                continue
            
            # Validate positive number
            gross_income = validate_positive_number(value_str, "Gross income")
            
            # Validate realistic amount
            validate_realistic_amount(gross_income, "Gross income")
            
            return gross_income
            
        except ValueError as e:
            print(f"❌ {str(e)}")
        except (EOFError, KeyboardInterrupt):
            print("\n\n❌ Input cancelled.")
            sys.exit(0)


def get_deductible_expenses(gross_income):
    """
    Prompt user for deductible business expenses with validation.
    
    Args:
        gross_income (float): Gross income for validation
    
    Returns:
        float: Validated deductible expenses
    """
    print("\n" + "-" * 70)
    print("DEDUCTIBLE BUSINESS EXPENSES")
    print("-" * 70)
    print("Enter your total deductible business expenses for the year.")
    print("This includes office rent, equipment, software, etc.")
    print(f"Maximum allowed: {format_currency(gross_income)}")
    print("Enter 0 if you have no deductible expenses.")
    print("-" * 70)
    
    while True:
        try:
            value_str = input("Deductible expenses (€): ").strip()
            
            # Handle empty input (default to 0)
            if not value_str:
                print("❌ Please enter a value (or 0 for no expenses).")
                continue
            
            # Validate non-negative number
            expenses = validate_non_negative_number(value_str, "Expenses")
            
            # Validate against gross income
            validate_expenses_against_income(expenses, gross_income)
            
            # Validate realistic amount
            validate_realistic_amount(expenses, "Expenses")
            
            return expenses
            
        except ValueError as e:
            print(f"❌ {str(e)}")
        except (EOFError, KeyboardInterrupt):
            print("\n\n❌ Input cancelled.")
            sys.exit(0)


def confirm_inputs(gross_income, expenses, frequency):
    """
    Display input summary and ask for confirmation.
    
    Args:
        gross_income (float): Gross annual income
        expenses (float): Deductible expenses
        frequency (str): Payment frequency
    
    Returns:
        bool: True if user confirms, False otherwise
    """
    print("\n" + "=" * 70)
    print("CONFIRM YOUR INPUTS")
    print("=" * 70)
    print(f"Gross Annual Income:       {format_currency(gross_income)}")
    print(f"Deductible Expenses:       {format_currency(expenses)}")
    print(f"Payment Frequency:         {frequency.capitalize()}")
    print("=" * 70)
    
    while True:
        try:
            response = input("\nProceed with calculation? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("❌ Please enter 'yes' or 'no'.")
        except (EOFError, KeyboardInterrupt):
            print("\n\n❌ Input cancelled.")
            return False


# ============================================================================
# CALCULATION EXECUTION
# ============================================================================

def perform_calculation(gross_income, expenses, frequency):
    """
    Execute tax calculation, display results, and save to file.
    
    This function orchestrates the complete calculation workflow:
    1. Calls calculate_all_taxes() to compute all tax components
    2. Displays formatted results to terminal
    3. Saves results to timestamped file for record-keeping
    
    Args:
        gross_income (float): Gross annual income
        expenses (float): Deductible expenses
        frequency (str): Payment frequency
    
    Example usage:
        # Calculate taxes for €35,000 income with €5,000 expenses
        perform_calculation(35000, 5000, 'quarterly')
        
        # Results include:
        # - Full income tax bracket breakdown
        # - EFKA social security contributions
        # - VAT calculations
        # - Payment schedule (4 quarterly payments)
        # - Net income after taxes
    """
    try:
        print("\n" + "=" * 70)
        print("CALCULATING...")
        print("=" * 70)
        
        # Calculate all taxes using the tax_calculator module
        # This returns a comprehensive dictionary with all tax components
        results = calculate_all_taxes(gross_income, expenses)
        
        # Display comprehensive results to terminal
        # Shows bracket-by-bracket breakdown, payment schedule, and summary
        display_results(results, frequency)
        
        # Save results to file for record-keeping
        # Creates file: tax_calculation_YYYY-MM-DD_HHMMSS.txt
        filename = save_results_to_file(results, frequency)
        
        if filename:
            print(f"\n✅ Results saved to: {filename}")
        
        return results
        
    except Exception as e:
        print(f"\n❌ An error occurred during calculation: {str(e)}")
        print("Please try again or contact support if the problem persists.")
        return None


# ============================================================================
# MAIN APPLICATION LOOP
# ============================================================================

def run_calculator():
    """
    Main application loop for the tax calculator.
    Handles menu navigation and calculation workflow.
    
    The application follows this flow:
    1. Display main menu
    2. User selects "New Calculation" or "Exit"
    3. For new calculation:
       a. Collect gross income input (with validation)
       b. Collect deductible expenses (with validation)
       c. Select payment frequency (monthly/quarterly/annual)
       d. Confirm inputs
       e. Calculate and display results
       f. Save to timestamped file
    4. Loop back to main menu for additional calculations
    
    Example workflow:
        → Main Menu
        → Choose "New Calculation"
        → Enter gross income: €35,000
        → Enter expenses: €5,000
        → Choose quarterly payments
        → Confirm inputs
        → View results showing:
          * Taxable income: €30,000
          * Income tax: €5,900 (bracket breakdown)
          * EFKA: €7,000
          * Total taxes: €12,900
          * Net income: €22,100
          * Quarterly payment: €3,225
        → Results saved to file
        → Return to main menu
    """
    display_header()
    
    while True:
        try:
            display_main_menu()
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == '1':
                # New Calculation workflow
                print("\n" + "=" * 70)
                print("NEW TAX CALCULATION")
                print("=" * 70)
                
                # Step 1: Collect gross income (validated for positive number)
                gross_income = get_gross_income()
                
                # Step 2: Collect deductible expenses (validated against income)
                expenses = get_deductible_expenses(gross_income)
                
                # Step 3: Select payment frequency (monthly, quarterly, annual)
                frequency = display_frequency_menu()
                
                # Step 4: Confirm inputs before proceeding
                if confirm_inputs(gross_income, expenses, frequency):
                    # Step 5: Perform calculation and display/save results
                    perform_calculation(gross_income, expenses, frequency)
                else:
                    print("\n❌ Calculation cancelled. Returning to main menu.")
                    continue
                
            elif choice == '2':
                # Exit application gracefully
                print("\n" + "=" * 70)
                print("Thank you for using the Greek Freelancer Tax Calculator!")
                print("=" * 70 + "\n")
                sys.exit(0)
                
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
                
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+C or EOF gracefully
            print("\n\n" + "=" * 70)
            print("Application interrupted. Exiting gracefully...")
            print("=" * 70 + "\n")
            sys.exit(0)
        except Exception as e:
            # Catch any unexpected errors and return to menu
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            print("Returning to main menu...")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Entry point for the Greek Freelancer Tax Calculator application.
    
    This block ensures the calculator only runs when executed directly
    (not when imported as a module).
    
    USAGE EXAMPLES:
    
    Example 1 - Run interactively:
        $ python main.py
        → Follow the prompts to calculate taxes
    
    Example 2 - Using from Python code:
        from tax_calculator import calculate_all_taxes
        
        # Calculate taxes programmatically
        result = calculate_all_taxes(35000, 5000)
        print(f"Total taxes: €{result['total_taxes']:,.2f}")
        print(f"Net income: €{result['net_income']:,.2f}")
    
    Example 3 - Quick test calculation:
        from tax_calculator import calculate_all_taxes, calculate_payment_schedule
        
        # Get tax breakdown
        taxes = calculate_all_taxes(60000, 10000)
        
        # Get payment schedule
        schedule = calculate_payment_schedule(taxes['total_taxes'], 'monthly')
        print(f"Monthly payment: €{schedule['payment_amount']:,.2f}")
    """
    try:
        # Run the interactive calculator application
        run_calculator()
    except Exception as e:
        # Handle any fatal errors that escape the main loop
        print(f"\n❌ Fatal error: {str(e)}")
        print("Application will now exit.")
        sys.exit(1)
