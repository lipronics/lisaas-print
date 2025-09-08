# lisaas-print
Printqueue for Lisaas

```
docker build -t print .
```

```
docker run \
    -e ACCOUNT='***' \
    -e USR='***' \
    -e PWD='***' \
    --network=host \
    -it print
```


## Environment variable

Name                | Required          | Default           | Description
--------------------|-------------------|-------------------|-------------
`ACCOUNT`           | Yes               | -                 | Lisaas account
`USR`               | Yes               | -                 | Lisaas username
`PWD`               | Yes               | -                 | Lisaas password
`MEDIA`             | No                | -                 | Print media (`A4`/`Letter`/`Custom.8.5x11in`/`Custom.210x297mm`)
`MEDIA_TYPE`        | No                | -                 | Print media type (`Labels`)
`SIDES`             | No                | `one-sided`       | Print sides
`PRINT_COLOR_MODE`  | No                | `auto`            | Printer color mode
`FIT_TO_PAGE`       | No                | `0`               | On=1, Off=0
`PRINTER_NAME`      | No                | _default printer_ | Printer name
`MAX_RETRY`         | No                | `3`               | Retry attempts after failed to print
`WAIT_RETRY`        | No                | `20`              | Wait between retries in seconds
