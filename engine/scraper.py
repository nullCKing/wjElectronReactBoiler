import sys
import os
import json
from bs4 import BeautifulSoup
import requests
import uuid
from multiprocessing import Pool
import string
import os
import xlsxwriter
from fuzzywuzzy import fuzz
import re
import time

# creates file in users appdata file where html data is stored
dir_path = '%s\\WJ\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# this dictionary is being used by the detect industry function. This uses fuzzy matching to try and figure out what industry a business is
# based on the name of the listing. Will be used when industry information is not present.
keyword_dict = {
  "Auto (Car, Motorcycle, Marine..)": [
    "Automotive", "Vehicles", "Dealership", "Powersports", "Motorcycles",
    "Boats", "Marine", "Watercraft", "Automobiles"
  ],
  "Marketing and Advertising":
  ["Marketing", "Advertising", "Sales", "Promotion", "Branding"],
  "Construction and Contractors": [
    "Construction", "Subcontractor", "Contractor", "Building", "Renovation",
    "Infrastructure"
  ],
  "Distribution and Wholesale":
  ["Distribution", "Wholesale", "Supplier", "Logistics"],
  "Dry Cleaning and Laundry": ["Laundry", "Drycleaning", "Clothes", "Textile"],
  "Fast Food and Quick-Service Restaurants": [
    "Fast food", "Drive-thru", "Restaurant", "Quick-service", "Takeout",
    "Delivery"
  ],
  "Franchise Businesses, Resale, Existing and New Franchise Offers": [
    "Franchise", "Franchising", "Franchisee", "Franchisor",
    "Business opportunity"
  ],
  "Gas Stations and Car Washes":
  ["Gas station", "Gas", "Car wash", "Detailing", "Fuel"],
  "Health Fitness Clubs, Gyms, Nutrition Food Stores":
  ["Gym", "Health", "Fitness", "Nutrition", "Exercise", "Wellness", "Sports"],
  "Manufacturing and Assembly":
  ["Manufacturing", "Assembly", "Production", "Fabrication"],
  "Marine, Boat, Yacht, PWC, Watercraft":
  ["PWC", "Watercraft", "Marine", "Boat", "Yacht", "Sailboat", "Nautical"],
  "Media, Publishing, Newspaper, and Magazine": [
    "Media", "Publishing", "Newspaper", "Magazine", "Journalism", "Press",
    "Content"
  ],
  "Professional Services, Consulting, CPA, Legal, and Financial Practices": [
    "Legal", "CPA", "Consulting", "Financial services", "Law", "Accounting",
    "Advisory"
  ],
  "Financial Investment, Credit, Insurance Services":
  ["Financial", "Credit", "Insurance", "Investment", "Wealth management"],
  "Real Estate, Commercial, and Land": [
    "Real estate", "Land", "Commercial real estate", "Estate sales",
    "Property", "Development"
  ],
  "Retail Store": ["Retail", "Shop", "Store", "Merchandise", "Consumer goods"],
  "B2B Services": [
    "B2B services", "Business-to-business", "Corporate services",
    "Partnerships"
  ],
  "B2C Services":
  ["B2C", "Business-to-consumer", "Customer services", "Retail services"],
  "Technology, Computing, ISP, and Networking services": [
    "Technology", "Software", "Computing", "Internet", "ISP", "Network",
    "WiFi", "IT services"
  ]
}


# helper function that turns html into a parseable soup object

def turnToSoup(html_doc):
    return BeautifulSoup(html_doc, "html.parser")

# puts in web request to then access a websites html, returns websites html

def getHTMLDocument(session, url, headers):
    NUM_RETRIES = 3
    params = {'api_key': 'cf228aae641a2b4f5c6041d4150dc877', 'url': url}
    for _ in range(NUM_RETRIES):
        try:
            response =  session.get('http://api.scraperapi.com/', params=(params), headers=headers)
            if response.status_code in [200, 404]:
                return response.text
        except requests.exceptions.ConnectionError:
            response = ''

# this class scrapes data from the sunbelt website

class sunbeltScraper:
    def __init__(self):
        self.data = []
        self.pages = []

    # gets all pages and appends them to list that is returned
    def getAllSunbeltPages(self):
        all_pages = []
        for x in range(1, 200):
            all_pages.append(f'https://www.sunbeltnetwork.com/business-search/business-results/page/{x}')
        self.pages = all_pages

    # downloads all html to a directory
    def downloadAllSunbeltHTML(self, page):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        s= requests.Session()
        sunbelt_listings = getHTMLDocument(s, page, headers)
        sunbelt_soup = turnToSoup(sunbelt_listings)
        bizdiv = sunbelt_soup.find_all("div", {"class": "latestBusinesses__item--middle"})
        for bdiv in bizdiv:
            businesess = bdiv.find_all("a", {"class": "latestBusinesses__item--rightButton"})
            for biz in businesess:
                business_page = getHTMLDocument(s, (biz['href']), headers)
                name = str(uuid.uuid4())
                with open(f'{dir_path}\\{name}.html', 'w', encoding='utf8') as business_file:
                    business_file.write(business_page)
                    business_file.close()
        
    # runs the downloadallhtml function in parallel
    def parallelDownloadAllHTML(self):
        self.getAllSunbeltPages()
        p = Pool(5)  # Pool tells how many at a time
        p.map(self.downloadAllSunbeltHTML, self.pages)
        p.terminate()
        p.join()

    """
    this loop gets all names and information from the downloaded businesses page
    returns data_list which is a list of dictionaries
    """
    def scrapeSunbelt(self):
        for filename in os.listdir(dir_path):
            file = os.path.join(dir_path, filename)
            opened_file = open(file, 'r', encoding='utf8')
            soup = turnToSoup(opened_file)
            try:
                id = soup.find('h6', class_='valueItem').text.strip()
                name = soup.find('h1').text.strip()
                if name != 'Listing No Longer Available':
                    url = soup.find("link", {"rel":"canonical"})['href']
                    biz_dict = {'name': name, 'askingprice': "", 'cash_flow': "", 'grossrev': "", 'industry': "", 'down_payment': "",
                                'Franchise': "",'financing': "", 'inventory': "" , 'URL': url, 'location': "", 'ID': id}
                    information = soup.find('ul',  class_=['valuesItems'])
                    info2 = soup.find('ul',  class_=['block'])
                    detailed = soup.find('div', {'class': 'resultsBusiness__detailsInformation'})
                    for li in information.find_all('li'):
                        index = 0
                        current_info = []
                        current_info.append(li.text.replace("\n", '').strip().split(' '))
                        for element in current_info:
                            for elt in element:
                                if elt == 'Asking':
                                    if element[index - 1] == '':
                                        biz_dict['askingprice'] = element[index - 2]
                                    else:
                                        biz_dict['askingprice'] = element[index - 1]
                                elif elt == 'Cash':
                                    biz_dict['cash_flow'] = element[index - 1]
                                elif elt == 'URL':
                                    biz_dict['']
                                elif elt == 'Gross':
                                    if element[index - 1] == 'request':
                                        biz_dict['grossrev'] = 'On Request'
                                    else:
                                        biz_dict['grossrev'] = element[index - 1]
                                elif elt == 'Down':
                                    if element[index - 1] == 'request':
                                        biz_dict['down_payment'] = 'On Request'
                                    else:
                                        biz_dict['down_payment'] = element[index - 1]
                                elif elt == 'YesFinancing':
                                    biz_dict['financing'] = 'Yes'
                                elif elt == 'NoFinancing':
                                    biz_dict['financing'] = 'No'
                                elif elt == 'Inventory':
                                    if element[index - 1] == 'request':
                                        biz_dict['inventory'] = 'On Request'
                                    else:
                                        biz_dict['inventory'] = element[index - 1]
                                index += 1
                    for li in info2.find_all('li'):
                        index = 0 
                        current_info = []
                        current_info.append(li.text.replace("\n", '').strip().split(' '))
                        for element in current_info:
                            for elt in element:
                                if (elt == "State:Confidential"):
                                    biz_dict['location'] = ""
                                else:
                                    loc = elt
                                    loc = loc.replace("State:", "")
                                    biz_dict['location'] = loc
                                index += 1
                    detailed_ul = detailed.find('ul')
                    current_detailed = []
                    for li in detailed_ul.find_all('li'):
                        current_detailed.append(li.text.replace("\n", '').strip().split(' '))
                        for element in current_detailed:
                            for elt in element:
                                if elt == "Franchise:":
                                    biz_dict['Franchise'] = element[-1]
                    self.data.append(biz_dict)
            except:
                pass

# This class creates the scraper that will get data from the VrBusiness brokerage website. 
# Has data list and pages list. data list holds a list of dictionaries
# that contain the information relevant to each business. 
# pages holds the paginated lists of businesses on the brokerage website. this is used for parallelization
class VRScraper:

    def __init__(self):
          self.data = []
          self.pages = []

    def getAllVRPages(self):
        all_pages = []
        for x in range(1, 11):
            all_pages.append(f"https://www.vrbusinessbrokers.com/advancedSearch/P0-U/D0-U/R0-U/C0-U/KW/LN/ctry/Location/cty/Industry.aspx?page={x}")
        self.pages = all_pages

    def downloadVRBusinessHTML(self, page):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        s = requests.Session()
        vr_page = getHTMLDocument(s, page, headers)
        soup = turnToSoup(vr_page)
        table = soup.find("table", {"class": "sale_tbl sale_tbl--responsive"})
        biztr = table.find_all("tr")
        for biz in biztr:
            try:
                biztd = biz.find("td")
                business = biztd.find("a")
                business_link = (f"https://www.vrbusinessbrokers.com{business['href']}")
                business_page = getHTMLDocument(s, business_link, headers)
                name = str(uuid.uuid4())
                with open(f'{dir_path}\\{name}.html', 'w', encoding='utf8') as business_file:
                    business_file.write(business_page)
                    business_file.close()
            except:
                continue

    # runs the downloadallhtml function in parallel
    def parallelDownloadAllHTML(self):
        self.getAllVRPages()
        p = Pool(5)  # Pool tells how many at a time
        p.map(self.downloadVRBusinessHTML, self.pages)
        p.terminate()
        p.join()

    def find_industry(self, string):
        best_match_score = 0
        best_match_industry = None

        for industry, keywords in keyword_dict.items():
            for keyword in keywords:
                score = fuzz.ratio(string, keyword)
                if score > best_match_score:
                    best_match_score = score
                    best_match_industry = industry
        return best_match_industry

    def scrapeVR(self):
        for filename in os.listdir(dir_path):
            file = os.path.join(dir_path, filename)
            opened_file = open(file, 'r', encoding='utf8')
            soup = turnToSoup(opened_file)
            try:
                # gets name from business page
                name = soup.find("span", {"id": "ContentPlaceHolder1_lblbusinessName"}).text.strip()
                # print(f"--------------------------_______________{name}_________________---------------------------------")
                biz_dict = {'name': name, 'askingprice': "", 'cash_flow': "", 'grossrev': "", 'industry': "", 'down_payment': "",
                                'Franchise': "",'financing': "", 'inventory': "" , 'URL': "", 'location': "", 'ID': id}
                information = soup.find('ul',  {"class": 'search-result-item-list'})

                # grabs all li objects that contain the information in a span tag
                reference_li = information.find('li', {"class": 'search-result-item-list__reference'})
                location_li = information.find('li', {"class": 'search-result-item-list__location'})
                price_li = information.find('li', {"class": 'search-result-item-list__price'})
                amount_down_li = information.find('li', {"class": 'search-result-item-list__amountdown'})
                revenues_li = information.find('li', {"class": 'search-result-item-list__revenues'})
                earnings_li = information.find('li', {"class": 'search-result-item-list__earnings'})
                assets_li = information.find('li', {"class": 'search-result-item-list__assets'})
                
                # grabs the information we want from the span tags
                reference_id_a = reference_li.find("span", {"id": "ContentPlaceHolder1_lblListing"}, itemprop='availableAtorFrom').text.strip()
                location = location_li.find("span", {"id": "ContentPlaceHolder1_lblLocation"}, itemprop='availableAtorFrom').text.strip()
                price = price_li.find("span", {"id": "ContentPlaceHolder1_lblPrice"}, itemprop="price").text.strip()
                amount_down = amount_down_li.find("span", {"id": "ContentPlaceHolder1_lblAmoutDown"}).text.strip()
                revenues = revenues_li.find("span", {"id": "ContentPlaceHolder1_lblRevenues"}).text.strip()
                earnings = earnings_li.find("span", {"id": "ContentPlaceHolder1_lblDiscretionaryEarnings"}).text.strip()
                assets = assets_li.find("span", {"id": "ContentPlaceHolder1_lblTotalAssets"}).text.strip()

                biz_dict['askingprice'] = price
                biz_dict['location'] = location
                biz_dict['down_payment'] = amount_down
                biz_dict['industry'] = self.find_industry(biz_dict['name'])
                biz_dict['ID'] = reference_id_a
                biz_dict['grossrev'] = revenues
                self.data.append(biz_dict)
            except:
                continue

# gets time stamp from a file
def getFileTimeStamp(filename):
    path = filename
    time = os.path.getmtime(path) / 86400 # amount of seconds in a day, this converts epoch time from seconds to days 
    return time

# this function takes a file time stamp in epoch time in days, then checks if a week has passed
def checkWeekPassed(file_time):
    current_time = float(time.time()) / 86400
    if current_time - file_time >= 21:
        return True
    else:
        return False

# this grabs a timestamp from the first file and then returns whatever checkWeekPassed returns
def checkAllFilesTime():
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    if (count == 0):
        return True
    else:
        try:
            for filename in os.listdir(dir_path):
                file = os.path.join(dir_path, filename)
                time = getFileTimeStamp(file)
                if checkWeekPassed(time):
                    return True
                else:
                    return False
        except:
            return True

# this clears all files from the directory
def deleteAllFiles():
    try:
        for filename in os.listdir(dir_path):
            file = os.path.join(dir_path, filename)
            os.remove(file)
    except:
        return

# helper function for list to int conversion from json loads
def changeListToInt(list):
    if len(list) == 1:
        return int(list[0])

if __name__ == "__main__":
    print("hello im main")
    vrscraper = VRScraper()
    vrscraper.scrapeVR()
    sunbelt_scraper = sunbeltScraper()
    sunbelt_scraper.scrapeSunbelt()
    if len(sys.argv) >= 14:
        # user selected location where file will write to
        directory = sys.argv[1]
        # filter options
        state_checkboxes = json.loads(sys.argv[2])
        industry_checkboxes = json.loads(sys.argv[3])
        unlisted_industry = json.loads(sys.argv[4])
        unlisted_location = json.loads(sys.argv[5])
        unlisted_price = json.loads(sys.argv[6])
        sunbelt_network = json.loads(sys.argv[7])
        synergy = json.loads(sys.argv[8])
        minGross_revenue = changeListToInt(json.loads(sys.argv[9]))
        maxGross_revenue = changeListToInt(json.loads(sys.argv[10]))
        minCash_flow = changeListToInt(json.loads(sys.argv[11]))
        maxCash_flow = changeListToInt(json.loads(sys.argv[12]))
        minListing_price = changeListToInt(json.loads(sys.argv[13]))
        maxListing_price = changeListToInt(json.loads(sys.argv[14]))
        # create excel workbook and sheet
        outWorkbook = xlsxwriter.Workbook(f"{directory}//your_file.xlsx")
        outSheet = outWorkbook.add_worksheet()
        # write column headers
        outSheet.write("A1", "Name")
        outSheet.write("B1", "Price")
        outSheet.write("C1", "Cash Flow")
        outSheet.write("D1", "Gross Revenue")
        outSheet.write("E1", "Down Payment")
        outSheet.write("F1", "Financing")
        outSheet.write("G1", "Inventory")
        outSheet.write("H1", "Location")
        outSheet.write("I1", "Franchise")
        outSheet.write("J1", "Industry")
        outSheet.write("K1", "ID")
        outSheet.set_column('A:A', 75)
        outSheet.set_column('B:I', 15)
        outSheet.set_column('J:J', 160)
        row = 2
        # concatenates each data list from both scraper classes (this isnt permanent because there is options for which scraper is used) 
        all_data = vrscraper.data + sunbelt_scraper.data
        for biz in all_data:
            bizname = biz['name']
            asking_price = biz['askingprice']
            cash_flow = biz['cash_flow']
            gross_rev = biz['grossrev']
            down_payment = biz['down_payment']
            financing = biz['financing']
            inventory = biz['inventory']
            location = biz['location']
            franchise = biz['Franchise']
           # url = biz['industry']
            id = biz['ID']
            data = [bizname, asking_price, cash_flow, gross_rev, down_payment, financing, inventory, location, franchise, id] 
            outSheet.write_row(f"A{row}", data)
            row += 1
        outWorkbook.close()
    else:
        print("Insufficient arguments given.")
    
