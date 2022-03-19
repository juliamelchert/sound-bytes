# Author: Julia Melchert
# Date: 2/22/22
# Description: A microservice that scrapes Wikipedia for company logos or general images, given a Wikipedia page's URL.

import requests, os, urllib.request, re, wikipedia
from bs4 import BeautifulSoup

# Runs infinitely in the background while waiting for a request to come in
while True:

    # Checks if any changes have been made to the signal.txt file (i.e. if a request has been made)
    with open('../signal.txt', 'r') as read_infile:
        # Clears the signal.txt file after reading its contents
        request = read_infile.read()
        
        # If a request has come in:
        if request != "":
            print("Received request: " + str(request))

            # Removes any current output files that were created in past requests
            if os.path.exists('../output.png') is True:
                os.remove('../output.png')

            # if os.path.exists('../output.txt') is True:
                # os.remove('../output.txt')

            # Splits the request type and URL/search into two separate list items (ex. ["logo", "www.example.com"])
            request = request.split("|")

            try:

                # If the request is for a logo:
                if request[0] == "logo":

                    # Creates a BeautifulSoup object with the given URL
                    page = requests.get(request[1])
                    soup = BeautifulSoup(page.content, "html.parser")

                    # Finds the appropriate HTML and converts it into an image address
                    logo = soup.find("table", class_="infobox vcard")

                    # Ensures that the BeautifulSoup object does not turn up as "None" throughout its search
                    if logo is not None:
                        logo = soup.find("table", class_="infobox vcard").find("td", class_="infobox-image logo")

                    if logo is not None:
                        logo = soup.find("table", class_="infobox vcard").find("td", class_="infobox-image logo").find("img")

                    if logo is not None:
                        # After locating the logo, its image address is generated
                        image_address = "https:" + logo['src']
                        
                        # Write image to output.png using the image address created above
                        urllib.request.urlretrieve(image_address, '../output.png')

                # If the request is for an image:
                elif request[0] == "image":         

                    # Creates a BeautifulSoup object with the given URL
                    page = requests.get(request[1])
                    soup = BeautifulSoup(page.content, "html.parser")

                    # Finds the appropriate HTML and converts it into an image address
                    # Finds the first HTML element with a class name that has the word "infobox" in it
                    image = soup.find("table", **{'class' : re.compile('.*infobox.*')})

                    # If there is an infobox, then looks for an image in the infobox
                    if image is not None:
                        image = soup.find("table", **{'class' : re.compile('.*infobox.*')}).find("img")

                    # If there was an image in the infobox, then the image address is generated and a file (output.png) is created
                    # with the image.
                    if image is not None:
                        image_address = "https:" + image['src']
                    
                        # Write image to output.png using the image address created above
                        urllib.request.urlretrieve(image_address, '../output.png')

                elif request[0] == "summary":

                    search_phrase = wikipedia.search(request[1] + " musician", results = 1)

                    with open('../output.txt', 'w') as output:
                        biography = wikipedia.summary(search_phrase, auto_suggest=False)
                        output.write(biography)

            finally:

                # If no logo/image was found, then "Image not found" is printed out.
                if (request[0] == "logo" or request[0] == "image") and os.path.exists('../output.png') is False:
                    print("Image not found.")

                # If no summary was found, then "Summary not found" is printed out.
                if request[0] == "summary" and os.path.exists('../output.txt') is False:
                    print("Summary not found.")

                # Erase the request that was just handled
                if os.path.exists('../signal.txt') is True:
                    with open('../signal.txt', 'w') as outfile:
                        outfile.write("")
