import os
import sys
import subprocess
import requests
import time
import tempfile
import pprint
import argparse
from getpass import getpass
try:
    import win32print  # type: ignore
except ImportError:
    # This is not required, just for listing printers
    win32print = None


def verify_printer(printer_name: str):
    if win32print is None:
        print('pywin32 not installed, cannot verify printer: {printer_name}')
        return
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_CONNECTIONS |
        win32print.PRINTER_ENUM_LOCAL)
    printer_names = [p[2] for p in printers]
    if printer_name not in printer_names:
        print(f'printer `{printer_name}` not installed')
        print("")
        print("Installed printers:")
        pprint.pprint(printers)
        sys.exit(1)
    print(f'printer installed: {printer_name}')


def print_job(pdfprint: str, printer_name: str, content: bytes):
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fp:
        fp.write(content)
        fname = fp.name
    try:
        cmd_list = [pdfprint, fname, printer_name]
        subprocess.run(cmd_list,
                       check=True,
                       capture_output=True,
                       text=True)
    finally:
        os.remove(fname)


def main(args):
    while True:
        usr, pwd, account = args.user, args.password, args.account
        url = f'https://{usr}:{pwd}@cloud.lisaas.com/{account}/api/v1/print'
        try:
            # print('check for a print job...')
            r = requests.get(url)
            if r.status_code == 200:
                print_job(args.executable, args.printer_name, r.content)
                print("print job sent to printer")
        except Exception as e:
            print(f"failed to print: {e}")
        time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Print Queue Windows')
    parser.add_argument('-n', '--printer-name', required=True)
    parser.add_argument('-e', '--executable', default='PDFtoPrinter.exe')
    parser.add_argument('-a', '--account', required=True)
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--password', required=False, default='')

    args = parser.parse_args()

    # Verify is the provided printer is exists
    verify_printer(args.printer_name)

    # Verify if PDFtoPrint can be found
    if not os.path.exists(args.executable):
        print(f'PDFtoPrint executable not found: {args.executable}')
        sys.exit(1)

    # Ask for a password if not provided
    if not args.password:
        args.password = getpass()

    main(args)
    print('OK')
