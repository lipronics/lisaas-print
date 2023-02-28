#!/usr/bin/python3

account = '*****'
usr = '**'
pwd = '********'

import requests, asyncio, cups, os

async def main():
    url = 'https://'+usr+':'+pwd+'@cloud.lisaas.com/'+account+'/api/v1/print'

    conn = cups.Connection()
    printers = conn.getPrinters()
    printer = list(printers.keys())[0]

    while True:
        r = requests.get(url)
        if r.status_code==200:
            open('/tmp/job.pdf', 'wb').write(r.content)
            conn.printFile(printer, '/tmp/job.pdf',"",{})
            os.remove('/tmp/job.pdf')
        else:
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
