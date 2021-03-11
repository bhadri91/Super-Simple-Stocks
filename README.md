# Super Simple Stocks

This code is submitted as an answer to the assignment _Super Simple Stocks_ included in 
the hiring process at J.P.Morgan.
Its instructions may be found in the document `doc/Problem Statement.pdf`.

## Requirements

The application has been developed using Python 3 (3.7.6)

## Usage

The calculations requested in the assignment instructions are supported by the following properties or methods:

- For a given instance of `Stock`:
  - Calculate the dividend yield_: `Stock.dividend_yield`
  - Calculate the P/E Ratio_: `Stock.price_earnings_ratio`
  - Record a trade, with timestamp, quantity of shares, buy or sell indicator and price_: Create an instance of `Trade` and supply it to an instance of`GlobalBeverageCorporationExchange` that contains the proper stock my means of `record_trade`
  - Calculate Stock Price based on trades recorded in past 15 minutes_: `Stock.price`
- Calculate the GBCE All Share Index using the geometric mean of prices for all stocks_: `GlobalBeverageCorporationExchange.all_share_index`.

Type hints are present in all relevant signatures and basic documentation is included in the code itself.
