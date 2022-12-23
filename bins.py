import pandas as pd
import requests
import json

from yaspin import yaspin
from yaspin.spinners import Spinners


url = "https://opendata.leeds.gov.uk/downloads/bins/dm_premises.csv"
api_root = "https://api.postcodes.io/postcodes/"

# Load premises dataset from council website
with yaspin(Spinners.dots13, text="Loading premises dataset") as sp:
    c = pd.read_csv(url, delimiter=",", header=None, names=["ID", "SAON", "PAON", "Street", "Town", "City", "Postcode"])
    sp.ok("✔")

postcode_valid = False
postcode = ""

# Validate postcode with API
while not postcode_valid:
    postcode = input("\nPostcode: ").replace(" ", "").upper()
    response = requests.get(api_root + postcode)
    if response.status_code == 200:
        result = json.loads(response.text)["result"]
        if result != "null":
            postcode = result['outcode'] + " " + result['incode']
            print(f"{postcode} found in area: {result['admin_ward']}")
            postcode_valid = True
    else:
        print("Invalid postcode or API error.")

# Find only matches on postcode in dataset
matched_addresses = c.loc[c["Postcode"] == postcode]

found_address = False
result_set = ""
while not found_address:
    # If there's an exact match on PAON or SAON
    house_identifier = str(input("\nProperty number (or name): "))
    if house_identifier in matched_addresses["PAON"].values:
        result_set = matched_addresses.loc[matched_addresses['PAON'] == house_identifier]
        found_address = True
    elif house_identifier in matched_addresses["SAON"].values:
        result_set = matched_addresses.loc[matched_addresses['SAON'] == house_identifier]
        found_address = True
    # If there's a like match
    elif not found_address:
        if matched_addresses['PAON'].str.contains(house_identifier).any():
            result_set = matched_addresses[matched_addresses['PAON'].str.contains(house_identifier, na=False)]
            found_address = True
        elif matched_addresses['SAON'].str.contains(house_identifier).any():
            # elif house_identifier in matched_addresses["SAON"].values:
            result_set = matched_addresses[matched_addresses['SAON'].str.contains(house_identifier, na=False)]
            found_address = True
        else:
            print("Could not find address - please try a different identifier!")
            print("Is this address a business? This dataset is mainly for residential addresses.")
            print("Is this address not managed by Leeds City Council? If the address uses another waste management"
                  "company, results may be unavailable.")
            print("If not, try a different address near your property.")

# Return results in dataframe
if len(result_set) > 0:
    print(f"\n{len(result_set)} results found for {house_identifier}, {postcode}:\n") if len(result_set) > 1 else \
        print(f"\n{len(result_set)} result found for {house_identifier}, {postcode}:\n")
    print(result_set.to_string(index=False, header=True))
else:
    print("No results for property found!")

input("\n\nPress any key to exit...")
