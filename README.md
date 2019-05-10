# gqrx-fscanner
> Script that drives gqrx to implement frequency scanning. Relies on [gqrxInterface library](https://github.com/technezio/gqrxInterface)

# Setup
1) **Configure** *Allowed hosts* and *Port* in gqrx from Tools>Remote control settings
2) **Enable** remote control by checking Tools>Remote control
3) **Change** `HOST` and `PORT` in the code to match your configuration (default values should work)
4) **Change** `import gqrxInterface` to match your path to the library

# Usage
## Scan frequencies from file
`./gqrx-fscanner file.txt`

`file.txt` must contain a list of integer frequencies in Hz, one per line.

## Scan frequencies from gqrx bookmarks
`./gqrx-fscanner 145000000 148000000`

Scan bookmarked frequencies between 145MHz and 148MHz.
