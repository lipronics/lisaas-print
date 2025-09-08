import asyncio
import cups
import pprint
import os
import requests
import tempfile


def get_credentials() -> tuple[str, str, str]:
    ACCOUNT = os.getenv('ACCOUNT')
    USR = os.getenv('USR')
    PWD = os.getenv('PWD')
    assert ACCOUNT, 'Environment variable ACCOUNT is required'
    assert USR, 'Environment variable USR is required'
    assert PWD, 'Environment variable PWD is required'
    return USR, PWD, ACCOUNT


def get_options() -> dict[str, str]:
    # "A4", "Letter", "Legal", "Custom.210x297mm"
    MEDIA = os.getenv('MEDIA', '')

    # For example: "Labels"
    MEDIA_TYPE = os.getenv('MEDIA_TYPE', '')

    # "one-sided", "two-sided-long-edge", "two-sided-short-edge"
    SIDES = os.getenv('SIDES', 'one-sided')

    # "monochrome", "auto"
    PRINT_COLOR_MODE = os.getenv('PRINT_COLOR_MODE', 'auto')

    # On=1, Off=0
    FIT_TO_PAGE = bool(int(os.getenv('FIT_TO_PAGE', '1')))

    options = {
        'sides': SIDES,
        'print-color-mode': PRINT_COLOR_MODE,
    }

    if MEDIA:
        options['media'] = MEDIA

    if MEDIA_TYPE:
        options['media-type'] = MEDIA_TYPE

    if FIT_TO_PAGE:
        # set empty string to enable fit-to-page
        options['fit-to-page'] = ""

    return options


def get_printer(conn: cups.Connection) -> str:
    PRINTER_NAME = os.getenv('PRINTER_NAME')
    if PRINTER_NAME is None:
        PRINTER_NAME = conn.getDefault()
    return PRINTER_NAME


def more_log(s: str):
    if bool(int(os.getenv('MORE_LOG', '0'))):
        print(s)


async def print_job(conn: cups.Connection, content: bytes, job_nr: int):
    num_attempts = int(os.getenv('MAX_RETRY', '3'))
    wait = float(os.getenv('WAIT_RETRY', '20'))
    while True:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                fp.write(content)
                fname = fp.name
            try:
                conn.printFile(
                    printer=get_printer(conn),
                    filename=fname,
                    title=f'Job #{job_nr}',
                    options=get_options())
            finally:
                os.remove(fname)
        except Exception as e:
            more_log(f'failed to print: {e}')
            if num_attempts > 0:
                num_attempts -= 1
                more_log(f'retry in {wait} seconds....')
                await asyncio.sleep(wait)
                continue
            raise
        break


async def main():
    conn = cups.Connection()
    print("Available printers:")
    printers = conn.getPrinters()
    pprint.pprint(printers)

    job_nr = 0

    while True:
        usr, pwd, account = get_credentials()
        url = f'https://{usr}:{pwd}@cloud.lisaas.com/{account}/api/v1/print'
        try:
            more_log('check for a print job...')
            r = requests.get(url)
            if r.status_code == 200:
                await print_job(conn, r.content, job_nr)
                job_nr += 1
                print(f"print job #{job_nr} sent to printer")
        except Exception as e:
            print(f"failed to send job #{job_nr} to printer: {e}")

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
