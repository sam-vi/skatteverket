Automation script to fill in tax data on Skatteverket
===

## Data format
The tax_data is expected in the following format.

First line:

    Year

Remaining lines:

    Dividend/Interest,Country,Month,Day,Currency,Amount,TP,TP_Currency,TP_Amount

where TP = Tax Paid, if you already have any tax paid on the amount. The name of the country and the month need to be in Swedish as in the example.

Also remember, Skatteverket only accepts whole numbers, no decimals.

## Installation
It should be enough to install selenium

    pip install selenium

You may also have to install chrome webdriver.

## Running
As simple as

    python utlandska-skatt.py

## Helpful functions
If you want to extract the month in Swedish, you can use this formula in Google sheets

    =PROPER(GOOGLETRANSLATE(TEXT(K23, "MMMM"), "en", "sv"))

## Contributing
Feel free to contribute with an issue or PR.