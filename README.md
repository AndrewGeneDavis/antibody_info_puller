# antibody_info_puller
A quick web scraper that will take useful information from the proteintech website and output in csv format for entry into a local database.  Built initially to help with data entry of a large number of antibodies that are being used for an antibody screen.  We purchased the antibodies from proteintech, but I would like to expand to most major antibody retailers (abcam, sigma/millipore, santa cruz, etc.).

# 1/3/2025
Added python version still in development.  Dependencies are "requests", "BeautifulSoup", and "re".

# 04/26/2022
Currently I have a prototype version (Scraping_in_R) that will pull relevant info from Proteintech based on a given url or sets of urls.  Proteintech's website generation and antibody information entry is not uniform across its antibodies, so I need to add more conditioning to handle a range of cases.
The csv is example output, there is currently a problem with the grep pulling the wrong line, which ends with incorrect information in the "reactivity" field.
I've also added a graph of the line lengths of their HTML to illustrate the ridiculousness on their webpage, specifically that several of their webpages' lines have over 20k characters in a single line.
