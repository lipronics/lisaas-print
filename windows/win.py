import os
import sys
import subprocess
import requests
import time
import tempfile
import pprint
try:
    import win32print  # type: ignore
except ImportError:
    # This is not required, just for listing printers
    win32print = None


PDFPRINT = os.getenv('PDFPRINT', r'PDFtoPrinter.exe')
PRINTER_NAME = os.getenv('PRINTER_NAME', 'Brother PT-P900W')


def get_credentials() -> tuple[str, str, str]:
    ACCOUNT = os.getenv('ACCOUNT')
    USR = os.getenv('USR')
    PWD = os.getenv('PWD')
    assert ACCOUNT, 'Environment variable ACCOUNT is required'
    assert USR, 'Environment variable USR is required'
    assert PWD, 'Environment variable PWD is required'
    return USR, PWD, ACCOUNT


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
    print('printer installed: {printer_name}')


def print_job(printer_name: str, content: bytes):
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fp:
        fp.write(content)
        fname = fp.name
    try:
        cmd_list = [PDFPRINT, fname, printer_name]
        subprocess.run(cmd_list,
                       check=True,
                       capture_output=True,
                       text=True)
    finally:
        os.remove(fname)


def main():
    while True:
        usr, pwd, account = get_credentials()
        url = f'https://{usr}:{pwd}@cloud.lisaas.com/{account}/api/v1/print'
        try:
            # print('check for a print job...')
            r = requests.get(url)
            if r.status_code == 200:
                print_job(PRINTER_NAME, r.content)
                print("print job sent to printer")
        except Exception as e:
            print(f"failed to print: {e}")
        time.sleep(10)


if __name__ == '__main__':
    verify_printer(PRINTER_NAME)
    get_credentials()
    if not os.path.exists(PDFPRINT):
        print(f'PDFtoPrint (PDFPRINT) executable not found: {PDFPRINT}')
        sys.exit(1)
    main()
    print('OK')
