import asyncio
import cups
import pprint
import os
import requests
import subprocess
import tempfile


def get_credentials() -> tuple[str, str, str]:
    ACCOUNT = os.getenv('ACCOUNT', '*****')
    USR = os.getenv('USR', '**')
    PWD = os.getenv('PWD', '********')
    return USR, PWD, ACCOUNT


def get_options() -> dict[str, str]:
    # "A4", "Letter", "Legal"
    MEDIA = os.getenv('MEDIA', 'A4')

     # "one-sided", "two-sided-long-edge", "two-sided-short-edge"
    SIDES = os.getenv('SIDES', 'one-sided')

    # "monochrome", "auto"
    PRINT_COLOR_MODE = os.getenv('PRINT_COLOR_MODE', 'auto')

    # On=1, Off=0
    FIT_TO_PAGE = os.getenv('FIT_TO_PAGE', '0')

    options = {
        'media': MEDIA,
        'sides': SIDES,
        'print-color-mode': PRINT_COLOR_MODE,
    }
    if FIT_TO_PAGE:
        # set empty string to enable fit-to-page
        options['fit-to-page'] = ""

    return options


def get_printer(conn: cups.Connection) -> str:
    PRINTER_NAME = os.getenv('PRINTER_NAME')
    if PRINTER_NAME is None:
        PRINTER_NAME = conn.getDefault()
    return PRINTER_NAME


async def main():
    conn = cups.Connection()
    print("Available printers:")
    printers = conn.getPrinters()
    pprint.pprint(printers)

    job_nr = 0

    while True:
        usr, pwd, account = get_credentials()
        url = f'https://{usr}:{pwd}@cloud.lisaas.com/{account}/api/v1/print'
        
        r = requests.get(url)
        if r.status_code==200:
            with tempfile.NamedTemporaryFile() as fp:
                fp.write(r.content)
                fp.close()
                conn.printFile(
                    printer=get_printer(conn),
                    filename=fp.name,
                    title=f'Job #{job_nr}',
                    option=get_options())

            job_nr += 1
            print("Print job sent to printer.")
        else:
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
