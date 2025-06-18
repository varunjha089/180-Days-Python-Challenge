import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

def calculate_emi_with_partial_payment():
    try:
        # Input parsing
        P = float(loan_amount_var.get())
        annual_rate = float(interest_rate_var.get())
        edu_months = int(education_period_var.get())
        repay_months = int(repayment_period_var.get())
        partial_payment = float(partial_payment_var.get())

        r = annual_rate / (12 * 100)  # Monthly interest rate

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "--- Education Period Begins (Partial Payments) ---\n")

        # Education period logic
        for month in range(1, edu_months + 1):
            interest = P * r
            if partial_payment >= interest:
                principal_reduction = partial_payment - interest
                P -= principal_reduction
                output_box.insert(tk.END,
                    f"Month {month}: Paid {partial_payment:.2f} → {interest:.2f} interest, {principal_reduction:.2f} reduced from principal\n"
                )
            else:
                unpaid_interest = interest - partial_payment
                P += unpaid_interest
                output_box.insert(tk.END,
                    f"Month {month}: Paid {partial_payment:.2f} < interest ({interest:.2f}) → {unpaid_interest:.2f} added to principal\n"
                )

        output_box.insert(tk.END, f"\nPrincipal after education period: {P:.2f}\n")

        # EMI Calculation
        n = repay_months
        if r == 0:
            emi = P / n
        else:
            emi = P * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

        output_box.insert(tk.END, f"\n--- Repayment Period Begins ---\n")
        output_box.insert(tk.END, f"EMI for {repay_months} months: {emi:.2f}\n\n")

        balance = P
        for month in range(1, n + 1):
            interest = balance * r
            principal = emi - interest
            balance -= principal
            output_box.insert(tk.END,
                f"Month {month}: {principal:.2f} is the principal amount, {interest:.2f} is interest\n"
            )
    except Exception as e:
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"Error: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("EMI Calculator (Education Loan)")

# Form variables
loan_amount_var = tk.StringVar()
interest_rate_var = tk.StringVar()
education_period_var = tk.StringVar()
repayment_period_var = tk.StringVar()
partial_payment_var = tk.StringVar()

# Layout
fields = [
    ("Loan Amount", loan_amount_var),
    ("Annual Interest Rate (%)", interest_rate_var),
    ("Education Period (months)", education_period_var),
    ("Repayment Period (months)", repayment_period_var),
    ("Partial Payment During Education (per month)", partial_payment_var)
]

for i, (label_text, var) in enumerate(fields):
    ttk.Label(root, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    ttk.Entry(root, textvariable=var, width=30).grid(row=i, column=1, padx=10)

# Calculate button
ttk.Button(root, text="Calculate EMI", command=calculate_emi_with_partial_payment)\
    .grid(row=len(fields), column=0, columnspan=2, pady=10)

# Output box (scrollable)
output_box = scrolledtext.ScrolledText(root, width=80, height=30)
output_box.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=10)

# Run app
root.mainloop()
