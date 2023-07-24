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
import datetime
from keybert import KeyBERT

# creates file in users appdata file where html data is stored
dir_path = '%s\\WJ\\' %  os.environ['APPDATA']
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# this dictionary is being used by the detect industry function. This uses fuzzy matching to try and figure out what industry a business is
# based on the name of the listing. Will be used when industry information is not present.
keyword_dict = {
    "Auto (Car, Motorcycle, Marine..)": [
        "Automotive", "Vehicles", "Dealership", "Powersports", "Motorcycles",
        "Boats", "Marine", "Watercraft", "Automobiles", "Cars", "Auto sales",
        "Car dealership", "Motorbike", "Vehicle sales", "Automotive industry",
        "Car rental", "Auto repair", "Vehicle maintenance", "Auto parts",
        "Car accessories", "Motorcycle dealership", "Motorbike sales",
        "Off-road vehicles", "Luxury cars", "Classic cars",
        "Electric vehicles", "Car leasing", "Car auctions",
        "Motorhome sales", "RV dealership", 
        "Boat repairs"
    ],
    "Marketing and Advertising": [
        "Marketing", "Advertising", "Sales", "Promotion", "Branding", "Campaigns",
        "Digital marketing", "Advertising agency", "Market research", "Social media marketing",
        "Content marketing", "Email marketing", "SEO", "SEM", "PPC advertising",
        "Online advertising", "Public relations", "Media planning", "Brand management",
        "Copywriting", "Graphic design", "Influencer marketing", "Event marketing",
        "Direct marketing", "Creative advertising", "Target audience", "Marketing strategy",
        "Brand awareness", "Customer engagement", "Advertising campaign", "Marketing analytics",
        "Brand positioning", "Product promotion", "Brand identity", "Market segmentation",
        "Consumer behavior", "Marketing communication", "Market trends", "Customer retention",
        "Sales funnel", "Lead generation", "Market penetration", "Competitive analysis",
        "Marketing ROI", "Marketing automation", "Customer relationship management"
    ],
    "Construction and Contractors": [
        "Construction", "Subcontractor", "Contractor", "Building", "Renovation",
        "Infrastructure", "Construction services", "Contracting", "Remodeling",
        "Construction management", "General contractor", "Construction project",
        "Construction site", "Construction company", "Residential construction",
        "Commercial construction", "Civil engineering", "Architectural design",
        "Structural engineering", "Construction materials", "Building codes",
        "Construction permits", "Construction labor", "Construction equipment",
        "Construction safety", "Excavation", "Demolition", "Concrete work",
        "Masonry", "Plumbing", "Electrical work", "Carpentry", "Roofing",
        "Flooring", "Painting", "HVAC", "Waterproofing", "Landscaping",
        "Site development", "Road construction", "Bridge construction",
        "Tunnel construction", "Environmental remediation", "Building maintenance",
        "Building restoration", "Project scheduling", "Budgeting and cost estimation",
        "Project management", "Quality control", "Sustainable construction",
        "Green building", "Renovation services", "Remodeling projects"
    ],
    "Distribution and Wholesale": [
        "Distribution", "Wholesale", "Supplier", "Logistics", "Supply chain",
        "Wholesaler", "Distribution center", "Inventory management", "Warehousing",
        "Shipping", "Order fulfillment", "Transportation", "Packing and labeling",
        "Inventory control", "Product sourcing", "Retail distribution",
        "E-commerce distribution", "Third-party logistics", "Inventory tracking",
        "Bulk purchasing", "Product distribution", "Wholesale pricing",
        "Vendor management", "Supply chain optimization", "Inventory replenishment",
        "Shipping and receiving", "Order processing", "Freight forwarding",
        "Warehouse management", "Cross-docking", "Stock management",
        "Product cataloging", "Last-mile delivery", "Reverse logistics",
        "Inventory forecasting", "Demand planning", "Order picking",
        "Packaging solutions", "Distribution network", "Value-added services",
        "Supply chain visibility", "Procurement", "Product inspection",
        "International trade", "Dropshipping", "Fulfillment services"
    ],
    "Dry Cleaning and Laundry": [
        "Laundry", "Drycleaning", "Clothes", "Textile", "Dry cleaning services",
        "Laundry service", "Fabric care", "Garment cleaning", "Stain removal",
        "Pressing", "Steam cleaning", "Clothing alterations", "Ironing",
        "Professional laundering", "Specialty cleaning", "Wash and fold",
        "Dry cleaning machines", "Dry cleaning chemicals", "Suede and leather cleaning",
        "Wedding dress cleaning", "Curtain cleaning", "Bedding cleaning",
        "Uniform cleaning", "Dry cleaning pickup and delivery", "Laundry supplies",
        "Wrinkle removal", "Color restoration", "Odor removal", "Garment storage",
        "Eco-friendly cleaning", "Launderette", "Fabric softening", "Laundry detergents",
        "Textile care", "Spot cleaning", "Delicate fabrics", "Washing machines",
        "Dryer machines", "Shirt laundering", "Dry cleaning equipment",
        "Laundry management", "Linen cleaning", "Clothing care tips"
    ],
    "Fast Food and Quick-Service Restaurants": [
        "Fast food", "Drive-thru", "Restaurant", "Quick-service", "Takeout",
        "Delivery", "Fast food chain", "Fast casual", "Quick bites",
        "Menu variety", "Burgers", "Fries", "Chicken", "Pizza", "Sandwiches",
        "Tacos", "Wraps", "Salads", "Breakfast items", "Combo meals",
        "Value meals", "Kids meals", "Beverages", "Soft drinks", "Coffee",
        "Desserts", "Ice cream", "Sweets", "Healthy options", "Vegetarian options",
        "Online ordering", "Mobile apps", "Contactless payments", "Drive-thru efficiency",
        "Order customization", "Fast order processing", "Quality ingredients",
        "Food safety standards", "Hygiene protocols", "Consistent taste",
        "Speed of service", "Customer satisfaction", "Franchise opportunities",
        "Brand recognition", "Marketing promotions", "Meal deals", "Limited-time offers",
        "Loyalty programs", "Restaurant design", "Seating arrangements",
        "Convenient locations", "Late-night hours", "Food delivery partnerships",
        "Staff training", "Kitchen equipment", "Food preparation"
    ],
    "Franchise Businesses, Resale, Existing and New Franchise Offers": [
        "Franchise", "Franchising", "Franchisee", "Franchisor",
        "Business opportunity", "Franchise resale", "Franchise opportunity",
        "Franchise development", "Franchise ownership", "Franchise system",
        "Franchise agreement", "Franchise disclosure", "Franchise fee",
        "Franchise training", "Franchise support", "Franchise branding",
        "Franchise marketing", "Franchise expansion", "Master franchise",
        "Multi-unit franchise", "Turnkey business", "Franchise financing",
        "Franchise consultant", "Franchise broker", "Franchise legal",
        "Franchise regulations", "Franchise success", "Franchise network",
        "Franchise territory", "Franchise royalties", "Franchise innovation",
        "Franchise standards", "Franchise growth", "Franchise management",
        "Franchise operations", "Franchise reseller", "Franchise showcase",
        "Franchise event", "Franchise exhibition", "Franchise seminar",
        "Franchise directory", "Franchise website", "Franchise blog",
        "Franchise magazine", "Franchise awards", "Franchise testimonials",
        "Franchise case studies", "Franchise opportunities", "Franchise listings"
    ],
    "Gas Stations and Car Washes": [
        "Gas station", "Gas", "Car wash", "Detailing", "Fuel", "Service station",
        "Automotive services", "Convenience store", "Fuel pumps", "Gasoline",
        "Diesel", "Fueling station", "Self-service pumps", "Full-service pumps",
        "Car wash services", "Car detailing", "Car vacuuming", "Car care",
        "Express car wash", "Touchless car wash", "Automatic car wash",
        "Hand car wash", "Car wash packages", "Car wash memberships",
        "Car wash equipment", "Car wash maintenance", "Car wash supplies",
        "Car wash accessories", "Car wash chemicals", "Car wash brushes",
        "Car wash drying systems", "Car wash waiting area", "Car wash loyalty programs",
        "Car wash promotions",
        "ATM", "Propane refill", "Air and water stations", "Car wash fundraising",
        "Car wash donation", "Car wash coupons", "Car wash gift cards"
    ],
    "Health Fitness Clubs, Gyms, Nutrition Food Stores": [
        "Gym", "Health", "Fitness", "Nutrition", "Exercise", "Wellness", "Sports",
        "Fitness center", "Health club", "Workout", "Sports nutrition",
        "Personal training", "Group fitness classes", "Cardio workouts", "Strength training",
        "Weightlifting", "Yoga", "Pilates", "Zumba", "CrossFit", "Cycling",
        "Functional training", "HIIT (High-Intensity Interval Training)", "Bootcamp",
        "Fitness equipment", "Gym membership", "Fitness assessment", "Body composition analysis",
        "Fitness goals", "Fitness programs", "Fitness challenges", "Fitness community",
        "Nutrition consultation", "Diet plans", "Supplements", "Protein powder",
        "Vitamins and minerals", "Healthy snacks", "Organic food", "Gluten-free products",
        "Vegan options", "Sports apparel", "Athletic shoes", "Fitness accessories",
        "Fitness trackers", "Wellness coaching", "Stress management", "Mindfulness",
        "Recovery and relaxation", "Massage therapy", "Sauna", "Steam room",
        "Health and fitness magazines", "Fitness events", "Fitness workshops",
        "Fitness seminars", "Fitness competitions", "Fitness influencers", "Fitness blogs"
    ],
    "Manufacturing and Assembly": [
        "Manufacturing", "Assembly", "Production", "Fabrication", "Manufacturing plant",
        "Assembly line", "Product assembly", "Mass production", "Custom manufacturing",
        "Prototype development", "Industrial manufacturing", "Manufacturing processes",
        "Manufacturing equipment", "Factory", "Manufacturing automation",
        "Quality control", "Supply chain management", "Logistics", "Inventory management",
        "Lean manufacturing", "Six Sigma", "Continuous improvement", "Efficiency",
        "Safety protocols", "Workplace safety", "Productivity", "Sustainability",
        "Material sourcing", "Raw materials", "Component manufacturing", "Final product",
        "Quality assurance", "Testing and inspection", "Packaging", "Shipping",
        "Warehousing", "Product maintenance", "Product lifecycle", "Industrial engineering",
        "Manufacturing software", "Robotics in manufacturing", "Industry 4.0",
        "Smart manufacturing", "Production planning", "Product scalability",
        "Value stream mapping", "Lean tools", "Process optimization"
    ],
    "Marine, Boat, Yacht, PWC, Watercraft": [
        "PWC", "Watercraft", "Marine", "Boat", "Yacht", "Sailboat", "Nautical",
        "Marina", "Boating", "Boat dealership", "Powerboat", "Cruiser",
        "Fishing boat", "Ski boat", "Wakeboard boat", "Pontoon boat",
        "Personal watercraft", "Jet ski", "Yacht charter", "Yacht brokerage",
        "Yacht maintenance", "Boat rental", "Boat club", "Marine accessories",
        "Marine electronics", "Boat engines", "Boat trailers", "Boat storage",
        "Boat insurance", "Boat financing", "Marine navigation", "Marine safety",
        "Marine supplies", "Marine maintenance", "Marine upholstery",
        "Boat detailing", "Boat repair", "Marine surveying", "Boat shows",
        "Marine events", "Boating magazines", "Boating blogs", "Boating communities",
        "Yachting lifestyle", "Water sports", "Sailing", "Cruising",
        "Yacht design", "Marine technology", "Boat building", "Marine engineering"
    ],
    "Media, Publishing, Newspaper, and Magazine": [
        "Media", "Publishing", "Newspaper", "Magazine", "Journalism", "Press",
        "Content", "News media", "Publishing house", "Print media", "Digital media",
        "Broadcasting", "Media production", "Media coverage", "Editorial",
        "Journalistic ethics", "Media distribution", "Media platforms", "Media advertising",
        "Media consumption", "Media trends", "Media industry", "Media professionals",
        "Media relations", "Media interviews", "Media monitoring", "Media analysis",
        "Media campaigns", "Media planning", "Media strategy", "Media outlets",
        "Media partnership", "Media sponsorship", "Media events", "Media coverage",
        "News reporting", "Investigative journalism", "Feature articles", "Opinion pieces",
        "Publishing industry", "Publishing process", "Publishing rights", "Book publishing",
        "Magazine publishing", "Newspaper publishing", "Print production",
        "Digital publishing", "Self-publishing", "Editorial services", "Copyediting",
        "Proofreading", "Graphic design", "Layout and formatting", "Print distribution",
        "Online publishing", "E-books", "E-publishing", "Newsstand", "Periodicals",
        "Media subscriptions", "Media readership", "Media audiences", "Media ratings",
        "Media analytics", "Media revenue", "Media monetization", "Media partnerships"
    ],
    "Professional Services, Consulting, CPA, Legal, and Financial Practices": [
        "Legal", "CPA", "Consulting", "Financial services", "Law", "Accounting",
        "Advisory", "Legal services", "Financial consulting", "CPA firm",
        "Tax services", "Audit", "Business consulting", "Management consulting",
        "Strategic consulting", "Financial planning", "Investment advisory",
        "Tax planning", "Tax preparation", "Bookkeeping", "Payroll services",
        "Corporate law", "Contract law", "Intellectual property law",
        "Employment law", "Real estate law", "Litigation", "Mergers and acquisitions",
        "Business law", "Estate planning", "Banking law", "Securities law",
        "Tax law", "Financial analysis", "Risk management", "Business valuation",
        "Forensic accounting", "Internal auditing", "Compliance", "Business advisory",
        "Financial reporting", "Budgeting and forecasting", "Financial modeling",
        "Financial strategy", "Debt management", "Cash flow management",
        "Business restructuring", "Business negotiations", "Legal consulting",
        "Corporate governance", "Due diligence", "Legal research", "Legal documentation",
        "Financial regulations", "Tax regulations", "Business contracts",
        "Financial statements", "Tax compliance", "Business compliance",
        "Financial controls", "Legal compliance", "Litigation support",
        "Investment management", "Retirement planning", "Estate administration",
        "Insurance advisory", "Wealth preservation", "Business succession planning"
    ],
    "Financial Investment, Credit, Insurance Services": [
        "Financial", "Credit", "Insurance", "Investment", "Wealth management",
        "Financial planning", "Investment services", "Insurance agency",
        "Credit services", "Asset management", "Portfolio management", "Retirement funds",
        "Financial advisory", "Financial consulting", "Risk assessment", "Risk mitigation",
        "Financial analysis", "Financial markets", "Stock market", "Bond market",
        "Mutual funds", "Hedge funds", "Private equity", "Venture capital",
        "Insurance coverage", "Life insurance", "Health insurance", "Auto insurance",
        "Property insurance", "Liability insurance", "Commercial insurance",
        "Underwriting", "Claims management", "Insurance policies", "Premiums",
        "Credit cards", "Loans", "Mortgages", "Credit scoring", "Credit reports",
        "Debt consolidation", "Credit counseling", "Credit monitoring",
        "Credit risk management", "Credit underwriting", "Credit analysis",
        "Creditworthiness", "Financial risk management", "Investment strategies",
        "Diversification", "Asset allocation", "Income planning", "Tax-efficient investing",
        "Estate planning", "Wealth preservation", "Retirement planning",
        "Financial education", "Financial literacy", "Financial empowerment",
        "Financial independence", "Financial security", "Financial well-being"
    ],
    "Retail Store": [
        "Retail", "Shop", "Store", "Merchandise", "Consumer goods", "Retailer",
        "Shopping", "Retail outlet", "Department store", "Boutique", "E-commerce",
        "Online shopping", "Brick-and-mortar", "Shopping center", "Mall",
        "Fashion", "Apparel", "Clothing", "Accessories", "Footwear",
        "Home goods", "Electronics", "Appliances", "Furniture",
        "Beauty products", "Cosmetics", "Personal care", "Health and wellness",
        "Grocery", "Supermarket", "Food and beverages", "Convenience store",
        "Discount store", "Variety store", "Specialty store", "Gift shop",
        "Bookstore", "Toy store", "Sporting goods", "Outdoor equipment",
        "Jewelry", "Watches", "Eyewear", "Department store", "Luxury goods",
        "Sales promotions", "Customer loyalty", "Point of sale", "Visual merchandising",
        "Inventory management", "Supply chain", "Logistics", "Retail analytics",
        "Omnichannel retail", "Customer experience", "Store layout",
        "Product assortment", "Retail marketing", "Advertising", "Retail branding",
        "Store signage", "Price optimization", "Retail technology", "POS systems",
        "E-commerce platforms", "Mobile commerce", "Digital marketing",
        "Social media marketing", "Customer reviews", "Online reviews",
        "Customer service", "Returns and exchanges", "Shopping carts",
        "Payment processing", "Retail security", "Loss prevention"
    ],
    "B2B Services": [
        "B2B services", "Business-to-business", "Corporate services",
        "Partnerships", "Business services", "B2B solutions", "B2B consulting",
        "Vendor management", "Supply chain management", "Outsourcing",
        "Professional services", "Business development", "Account management",
        "Strategic planning", "Market research", "Competitive analysis",
        "Sales and marketing", "Lead generation", "CRM solutions",
        "Business intelligence", "Data analytics", "IT services",
        "Software development", "Cloud computing", "Managed services",
        "Cybersecurity", "Digital transformation", "Process automation",
        "Logistics and transportation", "Fulfillment services",
        "Warehouse management", "Inventory control", "Distribution services",
        "Consulting services", "Financial consulting", "Legal consulting",
        "HR consulting", "Tax consulting", "Management consulting",
        "Marketing consulting", "Advertising services", "PR services",
        "Event planning", "Trade shows", "Exhibitions", "Business networking",
        "Accounting services", "Payroll services", "Bookkeeping",
        "Business planning", "Project management", "Quality assurance",
        "Risk management", "Sourcing and procurement", "Contract management",
        "Business process outsourcing", "Customer support", "Call center services",
        "Training and development", "Employee benefits", "Corporate wellness",
        "Sustainability services", "Green solutions", "Business analysis",
        "Process improvement", "Market expansion", "Financial management",
        "Risk assessment", "Supply chain optimization", "Strategic partnerships",
        "Digital marketing", "Content marketing", "Website development",
        "Search engine optimization", "Social media management",
        "Brand development", "Product development", "Market segmentation",
        "Sales strategy", "Customer relationship management",
        "Lead nurturing", "Product lifecycle management",
        "Business growth strategies", "Market penetration",
        "Business innovation", "Digital solutions", "Data management",
        "Data security", "Cloud services", "Cybersecurity solutions",
        "Network infrastructure", "IT consulting", "Application development",
        "IT support", "Data analytics solutions", "Business intelligence tools",
        "Supply chain analytics", "Inventory management systems",
        "Logistics optimization", "Fulfillment solutions",
        "E-commerce services", "Customer relationship management tools",
        "Training programs", "Employee engagement", "Team building",
        "Leadership development", "Performance management",
        "Workplace culture", "Employee retention"
    ],
     "B2C Services": [
        "B2C", "Business-to-consumer", "Customer services", "Retail services",
        "Consumer-oriented", "B2C solutions", "B2C consulting",
        "Customer experience", "Customer satisfaction", "Customer relationship",
        "Customer loyalty", "Retail operations", "Store management",
        "Product assortment", "Merchandising", "Point of sale", "E-commerce",
        "Online shopping", "Website design", "Mobile commerce",
        "Digital marketing", "Social media marketing", "Customer engagement",
        "Product recommendations", "Personalization", "Order fulfillment",
        "Delivery services", "Returns and exchanges", "Customer support",
        "Contact center", "Call center services", "Retail analytics",
        "Market research", "Competitive analysis", "Sales strategies",
        "Sales promotions", "Advertising campaigns", "Brand management",
        "Product branding", "Product packaging", "Price optimization",
        "Customer feedback", "User reviews", "Online ratings",
        "Social proof", "Consumer trust", "Customer loyalty programs",
        "Membership benefits", "Consumer education", "Consumer advocacy",
        "Consumer rights", "Consumer protection", "Retail trends",
        "Retail technology", "Point-of-sale systems", "Inventory management",
        "Supply chain management", "Logistics", "Order management",
        "Warehouse operations", "Delivery logistics", "Last-mile delivery",
        "Product quality", "Product safety", "Product regulations",
        "Consumer privacy", "Data protection", "Ethical business practices",
        "Sustainable products", "Fair trade", "Green initiatives",
        "Consumer empowerment", "Product innovation", "Market expansion",
        "Consumer behavior", "Consumer psychology", "Consumer insights"
    ],
    "Technology, Computing, ISP, and Networking services": [
        "Technology", "Software", "Computing", "Internet", "ISP", "Network",
        "WiFi", "IT services", "Tech solutions", "Software development",
        "Network infrastructure", "Cloud computing", "Cybersecurity",
        "Data analytics", "Artificial intelligence", "Machine learning",
        "Big data", "Internet of Things", "Blockchain", "Mobile applications",
        "Web development", "E-commerce solutions", "Database management",
        "Network security", "Wireless solutions", "IT consulting",
        "IT infrastructure", "System integration", "Hardware solutions",
        "Network monitoring", "Network administration", "Cloud services",
        "Managed services", "Virtualization", "Data center solutions",
        "Backup and recovery", "IT support", "Technical troubleshooting",
        "Software testing", "Quality assurance", "Software deployment",
        "IT project management", "IT governance", "Network design",
        "Network optimization", "Wireless networking", "Internet services",
        "Broadband solutions", "ISP management", "Network infrastructure",
        "Network maintenance", "Network troubleshooting", "WiFi deployment",
        "IT strategy", "IT solutions", "IT architecture", "Software engineering",
        "Web application development", "Mobile app development",
        "Cybersecurity solutions", "Data privacy", "Data management",
        "Data storage", "Cloud security", "IT risk management",
        "IT compliance", "Business continuity", "Disaster recovery",
        "Digital transformation", "IT automation", "Software as a Service (SaaS)",
        "Platform as a Service (PaaS)", "Infrastructure as a Service (IaaS)",
        "Network as a Service (NaaS)", "Internet Service Provider (ISP)",
        "Network security solutions", "IT training", "IT certifications",
        "Software licensing", "IT asset management", "IT procurement",
        "IT budgeting", "IT audit", "IT performance monitoring"
    ],
}

state_dict = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
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

# this turns an address into a string representing the state its in. This is to make location filter possible for websites that post locations as addresses
def turnAddressToState(address):
    address_state = None
    address_words = address.split()
    for abbreviation, state in state_dict.items():
        if  abbreviation in address_words:
            address_state = state
            break

    return address_state

def find_industry(bizname):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(bizname)
    best_match_score = 0
    best_match_industry = None
    only_words = [x[0] for x in keywords]
    print(only_words)
    for industry, keywords in keyword_dict.items():
        for keyword in keywords:
            score = fuzz.ratio(only_words, keyword)
            if score > best_match_score:
                print(score)
                best_match_score = score
                best_match_industry = industry
    return best_match_industry

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
        self.makeDirectory()
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
                    biz_dict = {'name': name, 'askingprice': None, 'cash_flow': None, 'grossrev': None, 'industry': None, 'down_payment': None,
                                'Franchise': None,'financing': None, 'inventory': None , 'URL': url, 'location': None, 'ID': id, "source": "sunbelt"}
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
                                        biz_dict['askingprice'] = int(re.sub('[a-zA-Z\W_]', '', element[index - 2]))
                                    else:
                                        biz_dict['askingprice'] = int(re.sub('[a-zA-Z\W_]', '', element[index - 1]))
                                elif elt == 'Cash':
                                    biz_dict['cash_flow'] = int(re.sub('[a-zA-Z\W_]', '', element[index - 1]))
                                elif elt == 'URL':
                                    biz_dict['']
                                elif elt == 'Gross':
                                    if element[index - 1] == 'request':
                                        biz_dict['grossrev'] = 'On Request'
                                    else:
                                        biz_dict['grossrev'] =int(re.sub('[a-zA-Z\W_]', '',  element[index - 1]))
                                elif elt == 'Down':
                                    if element[index - 1] == 'request':
                                        biz_dict['down_payment'] = 'On Request'
                                    else:
                                        biz_dict['down_payment'] = int(re.sub('[a-zA-Z\W_]', '', element[index - 1]))
                                elif elt == 'YesFinancing':
                                    biz_dict['financing'] = 'Yes'
                                elif elt == 'NoFinancing':
                                    biz_dict['financing'] = 'No'
                                elif elt == 'Inventory':
                                    if element[index - 1] == 'request':
                                        biz_dict['inventory'] = 'On Request'
                                    else:
                                        biz_dict['inventory'] = int(re.sub('[a-zA-Z\W_]', '', element[index - 1]))
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
                    biz_dict['industry'] = find_industry(biz_dict['name'])
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
        self.makeDirectory()
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

    def scrapeVR(self):
        for filename in os.listdir(dir_path):
            file = os.path.join(dir_path, filename)
            opened_file = open(file, 'r', encoding='utf8')
            soup = turnToSoup(opened_file)
            try:
                # gets name from business page
                name = soup.find("span", {"id": "ContentPlaceHolder1_lblbusinessName"}).text.strip()
                # print(f"--------------------------_______________{name}_________________---------------------------------")
                biz_dict = {'name': name, 'askingprice': None, 'cash_flow': None, 'grossrev': None, 'industry': None, 'down_payment': None,
                                'Franchise': "Info Unavailable",'financing': None, 'inventory': None, 'URL': None, 'location': None, 'ID': id, "source": "vr"}
                information = soup.find('ul',  {"class": 'search-result-item-list'})

                # grabs all li objects that contain the information in a span tag
                reference_li = information.find('li', {"class": 'search-result-item-list__reference'})
                # location_li = information.find('li', {"class": 'search-result-item-list__location'})
                price_li = information.find('li', {"class": 'search-result-item-list__price'})
                amount_down_li = information.find('li', {"class": 'search-result-item-list__amountdown'})
                revenues_li = information.find('li', {"class": 'search-result-item-list__revenues'})
                earnings_li = information.find('li', {"class": 'search-result-item-list__earnings'})
                assets_li = information.find('li', {"class": 'search-result-item-list__assets'})
                
                # using this to get address to turn to a state
                address_div = soup.find('div', {'class': "oi_para"})

                # grabs the information we want from the span tags
                reference_id_a = reference_li.find("span", {"id": "ContentPlaceHolder1_lblListing"}, itemprop='availableAtorFrom').text.strip()
                # location = location_li.find("span", {"id": "ContentPlaceHolder1_lblLocation"}, itemprop='availableAtorFrom').text.strip()
                location_input_tag = address_div.find("input", type="hidden")
                location = location_input_tag.get('value')
                price = price_li.find("span", {"id": "ContentPlaceHolder1_lblPrice"}, itemprop="price").text.strip()
                amount_down = amount_down_li.find("span", {"id": "ContentPlaceHolder1_lblAmoutDown"}).text.strip()
                revenues = revenues_li.find("span", {"id": "ContentPlaceHolder1_lblRevenues"}).text.strip()
                earnings = earnings_li.find("span", {"id": "ContentPlaceHolder1_lblDiscretionaryEarnings"}).text.strip()
                assets = assets_li.find("span", {"id": "ContentPlaceHolder1_lblTotalAssets"}).text.strip()

                biz_dict['askingprice'] = int(re.sub('[a-zA-Z\W_]', '', price))
                biz_dict['location'] = turnAddressToState(location)
                biz_dict['down_payment'] = int(re.sub('[a-zA-Z\W_]', '', amount_down))
                biz_dict['industry'] = find_industry(biz_dict['name'])
                biz_dict['ID'] = reference_id_a
                biz_dict['grossrev'] = int(re.sub('[a-zA-Z\W_]', '', revenues))
                self.data.append(biz_dict)
            except:
                continue

# gets time stamp from a file
def getFileTimeStamp(filename):
    path = filename
    time = os.path.getmtime(path) / 86400 # amount of seconds in a day, this converts epoch time from seconds to days 
    return time

# this function takes a file time stamp in epoch time in days, then checks if a week has passed
def check3WeekPassed(file_time):
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
                if check3WeekPassed(time):
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

if __name__ == "__main__":
    vrscraper = VRScraper()
    sunbelt_scraper = sunbeltScraper()
    if len(sys.argv) >= 14:
        # user selected location where the excel file will be stored
        directory = sys.argv[1]
        # filter options for businesses
        state_checkboxes = json.loads(sys.argv[2])
        industry_checkboxes = json.loads(sys.argv[3])
        unlisted_industry = json.loads(sys.argv[4])
        unlisted_location = json.loads(sys.argv[5])
        unlisted_price = json.loads(sys.argv[6])
        sunbelt_network = json.loads(sys.argv[7])
        vr = json.loads(sys.argv[8])
        minGross_revenue = json.loads(sys.argv[9])
        maxGross_revenue = json.loads(sys.argv[10])
        minCash_flow = json.loads(sys.argv[11])
        maxCash_flow = json.loads(sys.argv[12])
        minListing_price = json.loads(sys.argv[13])
        maxListing_price = json.loads(sys.argv[14])
        
        if checkAllFilesTime():
            deleteAllFiles()
            sunbelt_scraper.parallelDownloadAllHTML()
            vrscraper.parallelDownloadAllHTML()
            
        #  check which scraper has been turned on
        if sunbelt_network == 1:
            sunbelt_scraper.scrapeSunbelt()
        if vr == 1:
            vrscraper.scrapeVR()
            
        current_datetime = datetime.datetime.now()
        filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        # create excel workbook and sheet
        outWorkbook = xlsxwriter.Workbook(f"{directory}//{filename}.xlsx")
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
        outSheet.set_column('J:J', 100)
        row = 2
        # concatenates each data list from both scraper classes
        all_data = vrscraper.data + sunbelt_scraper.data
        for biz in all_data:
            try:
                bizname = biz['name']
                asking_price = biz['askingprice']
                cash_flow = biz['cash_flow']
                gross_rev = biz['grossrev']
                down_payment = biz['down_payment']
                financing = biz['financing']
                inventory = biz['inventory']
                location = biz['location']
                franchise = biz['Franchise']
                industry = biz['industry']
                id = biz['ID']
                source = biz['source'] # this is hardcoded into each scrapers data dictionary.easy way to manage the information from dif sites
                data = [bizname, asking_price, cash_flow, gross_rev, down_payment, financing, inventory, location, franchise, industry, id]
                
                # figuring this out
                
                if unlisted_industry == 0:
                    if industry not in industry_checkboxes:
                        continue
                elif unlisted_industry == 1:
                    if industry != None:
                        if industry not in industry_checkboxes:
                            continue
                
                if unlisted_location == 0:
                    if location not in state_checkboxes:
                        continue
                elif unlisted_location == 1:
                    if location != None:
                        if location not in state_checkboxes:
                            continue
                
                if gross_rev < minGross_revenue:
                    continue
                if gross_rev > maxGross_revenue:
                    continue
                
                if unlisted_price == 0:
                    if asking_price > maxListing_price:
                        continue
                    if asking_price < minListing_price:
                        continue
                elif unlisted_price == 1:
                    if asking_price != None:
                        if asking_price > maxListing_price:
                            continue
                        if asking_price < minListing_price:
                            continue
                # this checks if the data is coming from vr brokers. 
                # The reason for this is because there is no cash flow listed on vr, so 
                # it breaks when making a None comparison.
                if source != 'vr':  
                    if cash_flow > maxCash_flow:
                        continue
                    if cash_flow < minCash_flow:
                        continue
                    
                outSheet.write_row(f"A{row}", data)
                row += 1
            except:
                continue
        outWorkbook.close()
    else:
        print("Insufficient arguments given.")