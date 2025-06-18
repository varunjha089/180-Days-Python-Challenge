import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

# Globals to store result for export
export_data = []
final_principal = 0
emi_value = 0


def calculate_emi_with_partial_payment():
    global export_data, final_principal, emi_value
    try:
        # Input parsing
        P = float(loan_amount_var.get())
        annual_rate = float(interest_rate_var.get())
        edu_months = int(education_period_var.get())
        repay_months = int(repayment_period_var.get())
        partial_payment = float(partial_payment_var.get())

        r = annual_rate / (12 * 100)  # Monthly interest rate

        output_box.delete(1.0, tk.END)
        export_data = []
        export_data.append(["Education Period"])
        output_box.insert(tk.END, "--- Education Period Begins (Partial Payments) ---\n")

        # Education period
        for month in range(1, edu_months + 1):
            interest = P * r
            if partial_payment >= interest:
                principal_reduction = partial_payment - interest
                P -= principal_reduction
                output_box.insert(tk.END,
                    f"Month {month}: Paid {partial_payment:.2f} → {interest:.2f} interest, {principal_reduction:.2f} reduced from principal\n"
                )
                export_data.append([f"Month {month}", f"{partial_payment:.2f}", f"{interest:.2f}", f"{principal_reduction:.2f}", f"{P:.2f}"])
            else:
                unpaid_interest = interest - partial_payment
                P += unpaid_interest
                output_box.insert(tk.END,
                    f"Month {month}: Paid {partial_payment:.2f} < interest ({interest:.2f}) → {unpaid_interest:.2f} added to principal\n"
                )
                export_data.append([f"Month {month}", f"{partial_payment:.2f}", f"{interest:.2f}", "0.00", f"{P:.2f}"])

        final_principal = P
        output_box.insert(tk.END, f"\nPrincipal after education period: {P:.2f}\n")

        # EMI Calculation
        n = repay_months
        if r == 0:
            emi = P / n
        else:
            emi = P * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

        emi_value = emi
        output_box.insert(tk.END, f"\n--- Repayment Period Begins ---\n")
        output_box.insert(tk.END, f"EMI for {repay_months} months: {emi:.2f}\n\n")

        export_data.append(["Repayment Period"])
        export_data.append(["Month", "Principal Paid", "Interest Paid", "Remaining Balance"])

        balance = P
        for month in range(1, n + 1):
            interest = balance * r
            principal = emi - interest
            balance -= principal
            output_box.insert(tk.END,
                f"Month {month}: {principal:.2f} is the principal amount, {interest:.2f} is interest\n"
            )
            export_data.append([month, f"{principal:.2f}", f"{interest:.2f}", f"{balance:.2f}"])

    except Exception as e:
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"Error: {str(e)}")


def export_csv():
    if not export_data:
        messagebox.showerror("Error", "Please calculate EMI first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            # Separate into DataFrames and concatenate
            df_blocks = []
            block = []
            for row in export_data:
                if isinstance(row, list) and len(row) == 1:
                    if block:
                        df_blocks.append(pd.DataFrame(block[1:], columns=block[0]))
                        block = []
                block.append(row)
            if block:
                df_blocks.append(pd.DataFrame(block[1:], columns=block[0]))
            final_df = pd.concat(df_blocks, keys=["Education Period", "Repayment Period"])
            final_df.to_csv(file_path)
            messagebox.showinfo("Success", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def export_pdf():
    if not export_data:
        messagebox.showerror("Error", "Please calculate EMI first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            for row in export_data:
                line = "  |  ".join(str(x) for x in row)
                pdf.cell(200, 8, txt=line, ln=1, align='L')
            pdf.output(file_path)
            messagebox.showinfo("Success", f"PDF saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# def plot_graph():
#     if not export_data:
#         messagebox.showerror("Error", "Please calculate EMI first.")
#         return
#     try:
#         months = []
#         principals = []
#         interests = []
#         for row in export_data:
#             if isinstance(row[0], int) or (isinstance(row[0], str) and row[0].startswith("Month")):
#                 try:
#                     months.append(len(months) + 1)
#                     principals.append(float(row[1]))
#                     interests.append(float(row[2]))
#                 except:
#                     pass
#         plt.figure(figsize=(10, 5))
#         plt.plot(months, principals, label="Principal Paid")
#         plt.plot(months, interests, label="Interest Paid")
#         plt.title("Monthly Principal vs Interest Payment")
#         plt.xlabel("Month")
#         plt.ylabel("Amount")
#         plt.legend()
#         plt.grid(True)
#         plt.tight_layout()
#         plt.show()
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

def plot_graph():
    if not export_data:
        messagebox.showerror("Error", "Please calculate EMI first.")
        return
    try:
        months = []
        principals = []
        interests = []
        month_counter = 1

        for row in export_data:
            try:
                # Skip headers or non-data rows
                if isinstance(row, list) and len(row) >= 3:
                    principal = float(row[1])
                    interest = float(row[2])
                    principals.append(principal)
                    interests.append(interest)
                    months.append(month_counter)
                    month_counter += 1
            except:
                continue  # skip non-numeric rows

        if not months:
            messagebox.showerror("Error", "No valid data to plot.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(months, principals, label="Principal Paid")
        plt.plot(months, interests, label="Interest Paid")
        plt.title("Monthly Principal vs Interest Payment")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))



# GUI Setup
root = tk.Tk()
root.title("EMI Calculator (with PDF/CSV/Graph)")

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

# Buttons
ttk.Button(root, text="Calculate EMI", command=calculate_emi_with_partial_payment).grid(row=len(fields), column=0, pady=10)
ttk.Button(root, text="Export to CSV", command=export_csv).grid(row=len(fields), column=1, pady=10)
ttk.Button(root, text="Export to PDF", command=export_pdf).grid(row=len(fields)+1, column=0, pady=5)
ttk.Button(root, text="Plot Graph", command=plot_graph).grid(row=len(fields)+1, column=1, pady=5)

# Output box (scrollable)
output_box = scrolledtext.ScrolledText(root, width=85, height=30)
output_box.grid(row=len(fields)+2, column=0, columnspan=2, padx=10, pady=10)

# Run app
root.mainloop()
