import sys
import os
import json
import random
import time

def create_file(directory, state_checkboxes, industry_checkboxes, unlisted_industry, unlisted_location, unlisted_price, sunbelt_network, synergy,
    minGross_revenue,
    maxGross_revenue,
    minCash_flow,
    maxCash_flow,
    minListing_price,
    maxListing_price):
    timmy = time.ctime()
    with open(os.path.join(directory, '{timmy}.txt'), 'a') as f: # 'a' for appending instead of 'w' for writing
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
        f.write("\n")
        f.write("MinGross:\n")
        f.write(str(minGross_revenue))
        f.write("\n")
        f.write("MaxGross:\n")
        f.write(str(maxGross_revenue))
        f.write("\n")
        f.write("MinCashFlow:\n")
        f.write(str(minCash_flow))
        f.write("\n")
        f.write("MaxCashFlow:\n")
        f.write(str(maxCash_flow))
        f.write("\n")
        f.write("MinListingPrice:\n")
        f.write(str(minListing_price))
        f.write("\n")
        f.write("MaxListingPrice:\n")
        f.write(str(maxListing_price))
        f.write("\n")
        f.write("Random number:\n")
        f.write(str(random.randint(0, 100)))  # Prints a random integer between 0 and 100
        f.write("\n")
        f.write("Current Information:\n")
        f.write(time.ctime()) # Prints current date and time
        f.write("\n")

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

        start_time = time.time()
        while True:
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
                        maxListing_price)
            time.sleep(30) # Waits for 30 seconds before next iteration

            # Break the loop if 2 minutes (120 seconds) have passed
            if time.time() - start_time > 120:
                break
    else:
        print("Insufficient arguments given.")