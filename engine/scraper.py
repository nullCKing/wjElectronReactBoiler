import sys
import os
import json

def create_file(directory, state_checkboxes, industry_checkboxes, unlisted_industry, unlisted_location, unlisted_price, sunbelt_network, synergy,
    minGross_revenue,
    maxGross_revenue,
    minCash_flow,
    maxCash_flow,
    minListing_price,
    maxListing_price):
    with open(os.path.join(directory, 'your_file.txt'), 'w') as f:
        if state_checkboxes:
            f.write("State Checkboxes:\n")
            f.write(json.dumps(state_checkboxes))
            f.write("\n")
        if industry_checkboxes:
            f.write("Industry Checkboxes:\n")
            f.write(json.dumps(industry_checkboxes))
            f.write("\n")
        f.write("Unlisted Industry:\n")
        f.write(str(unlisted_industry))
        f.write("\n")
        f.write("Unlisted Location:\n")
        f.write(str(unlisted_location))
        f.write("\n")
        f.write("Unlisted Price:\n")
        f.write(str(unlisted_price))
        f.write("\n")
        f.write("Sunbelt Network:\n")
        f.write(str(sunbelt_network))
        f.write("\n")
        f.write("Synergy:\n")
        f.write(str(synergy))
        f.write("MinGross:\n")
        f.write(str(minGross_revenue))
        f.write("MaxGross:\n")
        f.write(str(maxGross_revenue))
        f.write("MinCashFlow:\n")
        f.write(str(minCash_flow))
        f.write("MaxCashFlow:\n")
        f.write(str(maxCash_flow))
        f.write("MinListingPrice:\n")
        f.write(str(minListing_price))
        f.write("MaxListingPrice:\n")
        f.write(str(maxListing_price))

if __name__ == "__main__":
    if len(sys.argv) >= 14:
        directory = sys.argv[1]
        state_checkboxes = json.loads(sys.argv[2])
        industry_checkboxes = json.loads(sys.argv[3])
        unlisted_industry = json.loads(sys.argv[4])
        unlisted_location = json.loads(sys.argv[5])
        unlisted_price = json.loads(sys.argv[6])
        sunbelt_network = json.loads(sys.argv[7])
        synergy = json.loads(sys.argv[8])
        minGross_revenue = json.loads(sys.argv[9])
        maxGross_revenue = json.loads(sys.argv[10])
        minCash_flow = json.loads(sys.argv[11])
        maxCash_flow = json.loads(sys.argv[12])
        minListing_price = json.loads(sys.argv[13])
        maxListing_price = json.loads(sys.argv[14])
        create_file(directory, 
            state_checkboxes, 
            industry_checkboxes, 
            unlisted_industry, 
            unlisted_location, 
            unlisted_price, 
            sunbelt_network, 
            synergy, 
            minGross_revenue,
            maxGross_revenue,
            minCash_flow,
            maxCash_flow,
            minListing_price,
            maxListing_price),
    else:
        print("Insufficient arguments given.")
    
    