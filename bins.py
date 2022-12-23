import argparse

import pandas as pd
import requests
import json

from yaspin import yaspin
from yaspin.spinners import Spinners


url = "https://opendata.leeds.gov.uk/downloads/bins/dm_premises.csv"
api_root = "https://api.postcodes.io/postcodes/"
postcode = ""
house_identifier = ""

parser = argparse.ArgumentParser(prog="Leeds Bins Property ID Finder", description="Search the premises.csv file "
                                                                                   "hosted by LCC/Data Mill North to "
                                                                                   "find a property's unique "
                                                                                   "reference (different to the "
                                                                                   "actual UPRN). This is used in the "
                                                                                   "collections.csv to find bin "
                                                                                   "collections for a property.")
parser.add_argument("-p", "--postcode", help="Postcode: remove any spaces", required=False, type=str)
parser.add_argument("-n", "--number", help="House number or name", required=False, type=str)
parser.add_argument("-o", "--output", help="Choice of json or txt for output", required=False, type=str,
                    choices=["json", "txt"])
parsed_args = parser.parse_args()

postcode_valid = False

# Get parsed postcode and number
if parsed_args.postcode:
    postcode = parsed_args.postcode
if parsed_args.number:
    house_identifier = parsed_args.number

# Get optional output mode
if parsed_args.output:
    output_mode = parsed_args.output
else:
    output_mode = "txt"

# Load premises dataset from council website
with yaspin(Spinners.dots13, text="Grabbing latest premises dataset from DMN") as sp:
    c = pd.read_csv(url, delimiter=",", header=None, names=["ID", "SAON", "PAON", "Street", "Town", "City", "Postcode"])
    sp.ok("✔")

# Validate postcode with API
while not postcode_valid:
    if not postcode:
        postcode = input("\nPostcode: ").replace(" ", "").upper()
    with yaspin(Spinners.dots13, text="Validating postcode") as sp:
        response = requests.get(api_root + postcode)
        if response.status_code == 200:
            result = json.loads(response.text)["result"]
            if result != "null":
                postcode = result['outcode'] + " " + result['incode']
                postcode_valid = True
                sp.text = "Postcode validated"
                sp.ok("✔")
        else:
            sp.text = "Invalid postcode or API error"
            sp.fail("💥")
            postcode = ""

with yaspin(Spinners.dots13, text="Finding postcode in dataset") as sp:
    # Find only matches on postcode in dataset
    matched_addresses = c.loc[c["Postcode"] == postcode]
    sp.text = f"postcodes found matching '{postcode}'"
    sp.ok(f"✔ {len(matched_addresses)}")

found_address = False
result_set = ""
while not found_address:
    # If there's an exact match on PAON or SAON
    if not house_identifier:
        house_identifier = str(input("\nProperty number (or name): "))

    with yaspin(Spinners.dots13, text="Finding property identifier in dataset") as sp:
        if house_identifier in matched_addresses["PAON"].values:
            result_set = matched_addresses.loc[matched_addresses['PAON'] == house_identifier]
            found_address = True
            sp.text = "Property found"
            sp.ok(f"✔")
        elif house_identifier in matched_addresses["SAON"].values:
            result_set = matched_addresses.loc[matched_addresses['SAON'] == house_identifier]
            found_address = True
            sp.text = "Property found"
            sp.ok(f"✔")
        # If there's a like match
        elif not found_address:
            if matched_addresses['PAON'].str.contains(house_identifier).any():
                result_set = matched_addresses[matched_addresses['PAON'].str.contains(house_identifier, na=False)]
                found_address = True
                sp.text = "Properties found"
                sp.ok(f"✔")
            elif matched_addresses['SAON'].str.contains(house_identifier).any():
                # elif house_identifier in matched_addresses["SAON"].values:
                result_set = matched_addresses[matched_addresses['SAON'].str.contains(house_identifier, na=False)]
                found_address = True
                sp.text = "Properties found"
                sp.ok(f"✔")
            else:
                sp.fail("💥 Could not find address - please try a different identifier!")
                house_identifier = ""


# Return results in dataframe
if len(result_set) > 0:
    print(f"\n{len(result_set)} results found for {house_identifier}, {postcode}:\n") if len(result_set) > 1 else \
        print(f"\n{len(result_set)} result found for {house_identifier}, {postcode}:\n")
    if output_mode == "json":
        print(result_set.to_json(orient="records"))
    else:
        print(result_set.to_string(index=False, header=True))

else:
    print("No results for property found!")

input("\n\nPress any key to exit...")
