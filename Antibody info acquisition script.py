# -*- coding: utf-8 -*-
"""
Spyder Editor
Author = @Andrew Davis
Created 1/2/2025
Last updated 1/3/2025

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
input_list = ["https://www.biolegend.com/de-at/products/pe-mouse-igg2a-kappa-isotype-ctrl-1401", 
                "https://www.biolegend.com/de-at/products/apc-cyanine7-anti-human-cd3-antibody-1912", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv421-mouse-anti-human-cd4.565997?tab=product_details", 
                "https://www.biolegend.com/en-us/products/alexa-fluor-488-anti-gfp-antibody-9584", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bb515-rat-anti-cd11b.564455?tab=product_details", 
                "https://www.thermofisher.com/antibody/product/CD71-Transferrin-Receptor-Antibody-clone-OKT9-OKT-9-Monoclonal/17-0719-42", 
                "https://www.thermofisher.com/antibody/product/CD34-Antibody-clone-RAM34-Monoclonal/11-0341-81", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/apc-cy-7-rat-anti-mouse-ly-6a-e.560654?tab=product_details", 
                "https://www.biolegend.com/en-us/products/apc-anti-mouse-rat-cd29-antibody-3090", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/apc-rat-anti-mouse-cd44.561862?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/pe-rat-anti-mouse-cd34.551387?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/apc-rat-anti-mouse-cd45.561018?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/apc-rat-anti-mouse-cd45.561018?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/fitc-rat-anti-mouse-cd45.561088?tab=product_details", 
                "https://www.thermofisher.com/antibody/product/CD45-Antibody-clone-30-F11-Monoclonal/45-0451-80", 
                "https://www.thermofisher.com/antibody/product/CD45-2-Antibody-clone-104-Monoclonal/12-0454-82", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/pe-rat-anti-mouse-cd86.553692?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv421-rat-anti-mouse-f4-80.565411?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv421-rat-anti-mouse-cd19.562701?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/fitc-rat-anti-mouse-cd8a.561966?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/apc-rat-anti-mouse-ly-6g-and-ly-6c.561083?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/apc-rat-anti-mouse-cd3-molecular-complex.565643?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/pe-rat-anti-mouse-f4-80.565410?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/percp-cy-5-5-rat-anti-mouse-cd3-molecular-complex.560527?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv421-rat-anti-mouse-cd335.562850?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv510-rat-anti-mouse-ly-6g-and-ly-6c.563040?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/pe-cy-7-rat-anti-mouse-cd19.561739?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/bv605-hamster-anti-mouse-cd11c.563057?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/v450-mouse-anti-rat-cd45.561587?tab=product_details", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/pe-cy-7-mouse-anti-rat-cd11b-c.562222?tab=product_details", 
                "https://www.bdbiosciences.com/content/dam/bdb/products/global/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/554xxx/5548xx/554878_base/pdf/554878.pdf", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/pe-cy-7-mouse-anti-ki-67.561283?tab=product_details", 
                "https://www.thermofisher.com/antibody/product/CD8-alpha-Antibody-clone-5H10-Monoclonal/MCD0827", 
                "https://www.biolegend.com/en-us/products/fitc-anti-rat-cd11b-c-antibody-2391", 
                "https://www.thermofisher.com/antibody/product/CD86-B7-2-Antibody-clone-PO3-1-Monoclonal/12-0861-81", 
                "https://www.thermofisher.com/antibody/product/CD40-Antibody-clone-1C10-Monoclonal/12-0401-81", 
                "https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/fitc-rat-anti-mouse-i-a-i-e.553623?tab=product_details", 
                "https://www.scbt.com/p/pecam-1-antibody-m-20", 
                "https://www.biolegend.com/en-us/products/purified-anti-mouse-cd16-32-antibody-190", 
                "https://www.thermofisher.com/antibody/product/CD11c-Antibody-clone-N418-Monoclonal/11-0114-82"]
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
    mfr_name_method_dict = {"biolegend":"h1", 
                            "bdbiosciences":"h1", 
                            "scbt":"h1",
                            "thermofisher":"not h1"}
    mfr_url_name = {'biolegend': "BioLegend", 
                    "bdbiosciences":"BD Biosciences", 
                    "scbt":"Santa Cruz Biotechnology",
                    "thermofisher":"Thermo Fisher"}
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
        self.unhandled_extensions = [".pdf", ".txt", ".xls", ".xlsx", ".doc", ".docx"]
        # pull company name url name
        website = re.search("www\..+\.com", self.link)[0]
        self.company = website.strip(".com").strip("www.")
        # Load and parse website data
        response = requests.get(self.link)
        html_data = response.text
        soup = BeautifulSoup(html_data, "html.parser")
        # check which website to choose which method to use
        if self.mfr_name_method_dict[self.company]=="h1":
            # try to pull filetype extension from link and skip these with
            # a warning
############# this part is not working, and I don't know why.  It should catch
            # .pdf extensions, but it is being too greedy
            extension = re.search("\..+?$", link)
            print(extension)
            if extension in self.unhandled_extensions:
                self.cannot_handle(link, extension)
#############
            else:
            # if there is not a known filetype extension caught, try to parse
            # the data.  Failure to properly parse the data will usually
            # result in a TypeError exception.  Exception is handled by
            # printing the offending link
                try:
                    self.name = self.antibody_name_by_h1(soup)
                except TypeError:
                    print("exception with " + link)
                except AttributeError:
                    print("exception with " + link)
        else:
            self.name = "no name"
        if self.company == "biolegend":
            biolegend_data = self.biolegend_antibody(soup)
            self.isotype = biolegend_data[0]
            self.clonality = biolegend_data[1]
            self.host = biolegend_data[2]
            self.cat_no = biolegend_data[3]
    def cannot_handle(self, link, extension):
        '''Takes in self, link, and extension and fills in data for files
        that the program cannot handle.  Fills in dummy data for the entry
        so that the program can continue with other valid files later in the
        list'''
        print("cannot handle "+extension+" files")
        self.name = "cannot handle "+extension+" files"
        self.company = self.name
        self.isotype = self.name
        self.clonality = self.name
        self.host = self.name
        self.cat_no = self.name
        return "cannot handle "+extension+" files"
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
