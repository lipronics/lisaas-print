#!/usr/bin/python3

account = '*****'
usr = '**'
pwd = '********'

import requests, asyncio, os, platform, tempfile, subprocess, cups

async def main():
    conn = cups.Connection()
    printers = conn.getPrinters()
    print("Available printers:", printers)

    url = 'https://'+usr+':'+pwd+'@cloud.lisaas.com/'+account+'/api/v1/print'
    print("Fetching print jobs ...")

    while True:
        r = requests.get(url)
        if r.status_code==200:
            fp = tempfile.NamedTemporaryFile(delete=False)
            fp.write(r.content)
            fp.close()
            if platform.system() == "Windows":
                os.startfile(fp.name, "print")
            else:
                lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
                lpr.stdin.write(fp.read())
            os.remove(fp.name)
            print("Print job sent to printer.")
        else:
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
