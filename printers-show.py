import cups

conn = cups.Connection()
printers = conn.getPrinters()
print("Available printers:", printers)

# Replace 'Your_Printer_Name' with the actual printer name
printer_name = 'Your_Printer_Name'
conn.setDefault(printer_name)
print(f"Default printer set to: {printer_name}")