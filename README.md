# Leeds Bins Property ID Finder
Search the premises.csv file hosted by [LCC/Data Mill North](https://datamillnorth.org/dataset/household-waste-collections) to find a property's unique reference (different to the actual UPRN).
This is used in the collections.csv to find bin collections for a property.

Intended for use with the Leeds scraper in [UK Bin Collection Data](https://github.com/robbrad/UKBinCollectionData).

# Usage
1) Download a zip of this repo from the Code... menu and extract somewhere on your computer.
2) Open your favorite terminal/CMD and run `pip install -r requirements.txt` to install the necessary packages.
3) Run `python bins.py` and follow the onscreen prompts.

## Notes
- The script will only work for *household* properties whose waste management is provided by LCC.
- Internet is needed to run the script:
    - To open the hosted csv
    - To verify and format the given postcode with [Postcodes.io](https://postcodes.io/). This makes it easier to check it exists
      and match the format to the one used in the CSV. No data is otherwise processed or retained.
- Most people will only see one result for their property, but if the script cannot find an exact match for your address, it may return multiple results.
  This depends on how the data is stored in the CSV - it first tries to find exact matches in the PAON and SAON columns, but will then find any for the given postcode.
- The necessary ID is the leftmost number in the results table.

# Issues
If you encounter an issue with the script, please open a [new issue](https://github.com/dp247/LeedsBinIDFinder/issues/new), including any messages or data.
