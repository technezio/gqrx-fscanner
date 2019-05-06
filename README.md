# gqrx-fscanner
> Script that drives gqrx via telnet to implement frequency scanning.

# Setup
1) **Configure** *Allowed hosts* and *Port* in gqrx from Tools>Remote control settings
2) **Enable** remote control by checking Tools>Remote control
3) **Change** `HOST` and `PORT` in the code to match your configuration (default values should work)

# Usage
## Scan frequencies from file
`./gqrx-fscanner file.txt`

`file.txt` must contain a list of integer frequencies in Hz, one per line.

## Scan frequencies from gqrx bookmarks
`./gqrx-fscanner 145000000 148000000`

Scan bookmarked frequencies between 145MHz and 148MHz.
