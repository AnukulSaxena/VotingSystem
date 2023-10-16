import tkinter as tk
import openpyxl

# Create a function to save the selected option to an Excel file and disable the button
def vote():
    def save_to_excel_and_disable_button():
        selected_option = option_var.get()

    # Load the existing Excel file or create a new one if it doesn't exist
        try:
            workbook = openpyxl.load_workbook("result.xlsx")
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

    # Select the first sheet in the workbook
        sheet = workbook.active

    # Find the next empty row in the sheet
        next_row = len(sheet["A"]) + 1

    # Write the selected option to the Excel file
        sheet[f'A{next_row}'] = selected_option

    # Save the Excel file
        file_name = "result.xlsx"
        workbook.save(file_name)

        result_label.config(text=f"Result appended to {file_name}")

    # Disable the button after the function has successfully executed
        save_button.config(state='disabled')

# Create the main application window
    root = tk.Tk()
    root.title("Options Selector")

# Create a label
    label = tk.Label(root, text="Select an option:")
    label.pack()

# Create radio buttons for options
    options = ["Congress", "BJP", "AAP", "BSP"]
    option_var = tk.StringVar(root, value=None)  # Initialize to None

# Create radio buttons for each option
    for option in options:
        option_radio = tk.Radiobutton(root, text=option, variable=option_var, value=option)
        option_radio.pack()

# Create a button to save the selected option and disable it
    save_button = tk.Button(root, text="Vote", command=save_to_excel_and_disable_button)
    save_button.pack()

# Create a label to display the result
    result_label = tk.Label(root, text="")
    result_label.pack()

# Start the GUI main loop
    root.mainloop()
