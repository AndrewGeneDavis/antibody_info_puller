# -*- coding: utf-8 -*-
"""
Spyder Editor
Author = @Andrew Davis
Created 1/2/2025
Last updated 1/2/2025

Script to scrape common antibody manufacturer's websites for important antibody
information to add to laboratory inventories
"""

import requests
from bs4 import BeautifulSoup
import re

#%%
# Block for testing websites before adding to the main class
# Methods for pulling antibody names
def antibody_name_by_h1(soup):
    antibody_name = soup.h1.text.strip()
    return antibody_name



# Set list of websites to pull from
input_list = ["https://www.biolegend.com/de-at/products/alexa-fluor-488-anti-gfp-antibody-9584",
              "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv421-mouse-anti-human-cd4.565997?tab=product_details",
              "https://www.scbt.com/p/pecam-1-antibody-m-20"]
i = 1

# Check which website for formatting decisions
website = re.search("www\..+\.com",  input_list[i])[0]
company = website.strip(".com").strip("www.")

mfr_dict = {"biolegend":"BioLegend", "bdbiosciences":"BD Biosciences", "scbt":"Santa Cruz"}

# Load website Data
response = requests.get(input_list[i])
html_data = response.text

soup = BeautifulSoup(html_data, "html.parser")
name_test = antibody_name_by_h1(soup)
print(name_test)



#%%
# Write a class to hold all of the data and methods to scrape the websites
class antibody:
    """Antibody information storage"""
    mfr_list = ["biolegend", "bdbiosciences", "scbt"]
    mfr_name_method_dict = {"biolegend":"h1", "bdbiosciences":"h1", "scbt":"h1"}
    def __init__(self, link):
        self.link = link
        # pull company name url name
        website = re.search("www\..+\.com", self.link)[0]
        self.company = website.strip(".com").strip("www.")
        # Load and parse website data
        response = requests.get(self.link)
        html_data = response.text
        soup = BeautifulSoup(html_data, "html.parser")
        # check which website to choose which method to use
        if self.mfr_name_method_dict[self.company]=="h1":
            self.name = self.antibody_name_by_h1(soup)    
    def antibody_name_by_h1(self, soup):
        antibody_name = soup.h1.text.strip()
        return antibody_name

#%%

# Running antibody class
        
        
        
#        name, target, species_target, host, clonality, isotype, cat_no, company, 
# self.Name = name
#   Name has been added as h1 which works for all companies websites so far
        # self.target = target
        # self.species_target = species_target
        # self.host = host
        # self.clonality = clonality
        # self.isotype = isotype
        # self.cat_nono = cat_no
        # self.company = company
        

antibody_list = []
for link in input_list:
    antibody_list.append(antibody(link))
for antibody_item in antibody_list:
    print(antibody_item.company+": "+antibody_item.name)

