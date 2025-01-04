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
    '''Takes the h1 element of the website and outputs it as text.  This
    seems to be common practice for antibody companies to use for the
    names of their antibodies on their store pages'''
    antibody_name = soup.h1.text.strip()
    return antibody_name
def biolegend_antibody(soup):
    '''Takes in soup object and outputs a list containing the
    isotype, clonality, host and catalog number(s) as text. All outputs 
    except the catalog numbers are outputted as text in a list; the
    catalog numbers are outputted as a sublist in the output list.
    Will only work on biolegend website.
    Last updated Jan 2025.'''
    info_tags = soup.find_all(name=["dl"])
    isotype = ""
    clonality = ""
    host = ""
    all_found = 0
    for tag in info_tags:
        if "Isotype" == tag.text.strip() and isotype == "":
            isotype = tag.find_next("dd").text.strip()
            all_found += 1
        if "Antibody Type" in tag.text and clonality == "":
            clonality = tag.find_next("dd").text.strip()
            all_found += 1
        if "Host Species" in tag.text and host == "":
            host = tag.find_next("dd").text.strip()
            all_found += 1
        if all_found == 3:
            break;
    cat_tags = soup.find_all(["thead", "tbody"])
    cat_no = []
    for tag in cat_tags:
        if "Cat #" in tag.text:
            cat_no.append(tag.find_next("tr").find_next("td").text.strip())
    return [isotype, clonality, host, cat_no]


# Set list of websites to pull from
input_list = ["https://www.biolegend.com/en-us/products/alexa-fluor-488-anti-gfp-antibody-9584",
              "https://www.biolegend.com/en-us/products/alexa-fluor-700-anti-mouse-cd45-antibody-3407",
              "https://www.biolegend.com/en-us/products/biotin-anti-human-il-1beta-antibody-10401",
              "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv421-mouse-anti-human-cd4.565997?tab=product_details",
              "https://www.scbt.com/p/pecam-1-antibody-m-20"]
i = 2

# Check which website for formatting decisions
website = re.search("www\..+\.com",  input_list[i])[0]
company = website.strip(".com").strip("www.")

# Establish list and dictionary of manufacturers
mfr_list = ["biolegend", "bdbiosciences", "scbt"]
mfr_dict = {"biolegend":"BioLegend", "bdbiosciences":"BD Biosciences", "scbt":"Santa Cruz"}

# Load website Data
response = requests.get(input_list[i])
html_data = response.text
soup = BeautifulSoup(html_data, "html.parser")

# Biolegend Parsing
name_test = antibody_name_by_h1(soup)
biolegend_test = biolegend_antibody(soup)

print(name_test+"\n"+
      biolegend_test[0]+"; "+
      biolegend_test[1]+"; "+
      biolegend_test[2]+"; ")
print(biolegend_test[3])




#%%
# Write a class to hold all of the data and methods to scrape the websites
class antibody:
    """Antibody information data and methods"""
    mfr_list = ["biolegend", "bdbiosciences", "scbt"]
    mfr_name_method_dict = {"biolegend":"h1", "bdbiosciences":"h1", "scbt":"h1"}
    mfr_url_name = {'biolegend': "BioLegend", "bdbiosciences":"BD Biosciences", "scbt":"Santa Cruz Biotechnology"}
    name = ""
    company = ""
    target = ""
    species_target = ""
    isotype = ""
    clonality = ""
    host = ""
    cat_no = ""
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
        if self.company == "biolegend":
            biolegend_data = self.biolegend_antibody(soup)
            self.isotype = biolegend_data[0]
            self.clonality = biolegend_data[1]
            self.host = biolegend_data[2]
            self.cat_no = biolegend_data[3]
    def antibody_name_by_h1(self, soup):
        '''Takes the h1 element of the website and outputs it as text.  This
        seems to be common practice for antibody companies to use for the
        names of their antibodies on their store pages'''
        antibody_name = soup.h1.text.strip()
        return antibody_name
    def biolegend_antibody(self, soup):
        '''Takes in self and soup object and outputs a list containing the
        isotype, clonality, host and catalog number(s) as text. All outputs 
        except the catalog numbers are outputted as text in a list; the
        catalog numbers are outputted as a sublist in the output list.
        Will only work on biolegend website.
        Last updated Jan 2025.'''
        info_tags = soup.find_all(name=["dl"])
        isotype = ""
        clonality = ""
        host = ""
        all_found = 0
        for tag in info_tags:
            if "Isotype" == tag.text.strip() and isotype == "":
                isotype = tag.find_next("dd").text.strip()
                all_found += 1
            if "Antibody Type" in tag.text and clonality == "":
                clonality = tag.find_next("dd").text.strip()
                all_found += 1
            if "Host Species" in tag.text and host == "":
                host = tag.find_next("dd").text.strip()
                all_found += 1
            if all_found == 3:
                break;
        cat_tags = soup.find_all(["thead", "tbody"])
        cat_no = []
        for tag in cat_tags:
            if "Cat #" in tag.text:
                cat_no.append(tag.find_next("tr").find_next("td").text.strip())
        self.cat_no = cat_no
        return [isotype, clonality, host, cat_no]

#%%

# Running antibody class

# Biolegend
    # Name - done
    # target - TODO if reasonably possible
    # species_target - TODO if reasonably possible
    # host - done
    # clonality - done
    # isotype - done
    # cat_no - done
    # company - done

# BD Biosciences
    # Name - done
    # target - TODO if reasonably possible
    # species_target - TODO if reasonably possible
    # host - TODO
    # clonality - TODO
    # isotype - TODO
    # cat_no - TODO
    # company - TODO

# Santa Cruz Biotechnology
    # Name - done
    # target - TODO if reasonably possible
    # species_target - TODO if reasonably possible
    # host - TODO
    # clonality - TODO
    # isotype - TODO
    # cat_no - TODO
    # company - TODO

        
#        name, target, species_target, host, clonality, isotype, cat_no, company, 
# self.Name = name
#   Name has been added as h1 which works for all companies websites so far
        # self.target = target
        # self.species_target = species_target
        # self.host = host
        # self.clonality = clonality
        # self.isotype = isotype
        # self.cat_no = cat_no
        # self.company = company
        

antibody_list = []
for link in input_list:
    antibody_list.append(antibody(link))
for antibody_item in antibody_list:
    print(antibody_item.company+": "+antibody_item.name+"\nIsotype: "+antibody_item.host)
    print(antibody_item.cat_no)
