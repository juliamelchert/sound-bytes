# Author: Julia Melchert
# Date: 2/22/22
# Description: A microservice that scrapes Wikipedia for company logos or general images, given a Wikipedia page's URL.

import requests, os, urllib.request, re, wikipedia
from bs4 import BeautifulSoup

def process_request(request):
    """
    Processes the given request and resets the signal file so it is ready for new requests.
    """
    print("Processing request...")
    # Splits the request type and URL/search into two separate list items (ex. ["logo", "www.example.com"])
    request = request.split("|")

    try:
        request_handled = search_for_content(request)

    finally:

        if request_handled is not True:
            print(f"The {request[0]} was not found.")

        # Erase the request that was just handled
        if os.path.exists('../signal.txt') is True:
            with open('../signal.txt', 'w') as outfile:
                outfile.write("")

def search_for_content(request):
    """
    Searches for the requested content (logo, image, or summary) and returns True if the request was successfully handled.
    """
    print(f"Searching for the {request[0]}...")
    request_handled = False

    if request[0] == "logo":
        request_handled = find_logo(request[1])
    elif request[0] == "image":         
        request_handled = find_image(request[1])
    elif request[0] == "summary":
        request_handled = find_summary(request[1])

    return request_handled

def find_logo(wikipedia_url):
    """
    Finds and saves a logo to '../output.png' given the Wikipedia URL for which the logo is found.
    Returns True if the request was successfully handled.
    """
    # Creates a BeautifulSoup object with the given URL
    page = requests.get(wikipedia_url)
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
        return True

def find_image(wikipedia_url):
    """
    Finds and saves the first image from a Wikipedia page's infobox to '../output.png' given 
    the Wikipedia page's URL. Returns True if the request was successfully handled
    """
    # Creates a BeautifulSoup object with the given URL
    page = requests.get(wikipedia_url)
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
        return True

def find_summary(artist):
    """
    Finds and writes the summary from the given music artist's Wikipedia page to '../output.txt'.
    Returns True if the request was successfully handled.
    """
    search_phrase = wikipedia.search(artist + " musician", results = 1)
    biography = wikipedia.summary(search_phrase, auto_suggest=False)

    with open('../output.txt', 'w') as output:
        output.write(biography)
        return True


# Runs infinitely in the background while waiting for requests to come in.
while True:

    with open('../signal.txt', 'r') as read_infile:

        request = read_infile.read()

        # Checks if a request has come in:
        if request != "":
            print(f"Received request: {request}")
            process_request(request)
            print("Finished processing request.")