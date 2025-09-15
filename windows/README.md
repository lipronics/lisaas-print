## Printer script for Windows

When using windows, we need `PDFtoPrinter.exe` which is included in this repository.

see: [https://github.com/emendelson/pdftoprinter](https://github.com/emendelson/pdftoprinter)

Install Python 3.10 or higher.

## Install requirements

```
pip install pywin32
pip install requests
```

## Usage

```
python win.py -a <account> -u <username> -n <printer name>
```

Next, provide the password when asked


## Help

All command line options:

```
usage: Print Queue Windows [-h] -n PRINTER_NAME [-e EXECUTABLE] -a ACCOUNT -u USER [-p PASSWORD]

options:
  -h, --help            show this help message and exit
  -n PRINTER_NAME, --printer-name PRINTER_NAME
  -e EXECUTABLE, --executable EXECUTABLE
  -a ACCOUNT, --account ACCOUNT
  -u USER, --user USER
  -p PASSWORD, --password PASSWORD
  ```
