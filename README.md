# Leeds Bins Property ID Finder
Search the premises.csv file hosted by [LCC/Data Mill North](https://datamillnorth.org/dataset/household-waste-collections) to find a property's unique reference (different to the actual UPRN).
This is used in the collections.csv to find bin collections for a property.

Intended for use with the Leeds scraper in [UK Bin Collection Data](https://github.com/robbrad/UKBinCollectionData).

# Setup
1) Download a zip of this repo from the `Code...` menu and extract to a folder somewhere on your computer.
2) Open your favorite terminal/CMD and run `pip install -r requirements.txt` to install the necessary packages.

# Usage
```commandline
python bins.py
usage: Leeds Bins Property ID Finder [-h] [-p POSTCODE] [-n NUMBER] [-o {json,txt}]

Search the premises.csv file hosted by LCC/Data Mill North to find a property's unique reference (different to the
actual UPRN). This is used in the collections.csv to find bin collections for a property.

options:
  -h, --help                            show this help message and exit
  -p POSTCODE, --postcode POSTCODE      Postcode: remove any spaces
  -n NUMBER, --number NUMBER            House number or name
  -o {json,txt}, --output {json,txt}    Choice of json or txt for output
```
## Automatic
The script has support for argparse, which can be used to pass a postcode and house number/name at runtime to bypass
the interactive prompts:
```commandline
python bins.py -p LS18BB -n 4   # Runs the script with postcode as "LS1 8BB" and house number 4
```
The output format can be changed between json and txt as well, by passing `-o json` for JSON or `-o txt` for plain text.

## Interactive
The basic way of running the script is:
```commandline
python bins.py
```
This will cause the script to run in interactive mode, which will require your postcode and house number being entered
at prompts.

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
