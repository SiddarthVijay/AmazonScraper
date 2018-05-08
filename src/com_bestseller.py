#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import csv

outputFile = open("../outputs/com_books.csv", "w")

with outputFile:
    csvWriter = csv.writer(outputFile)
    csvWriter.writerow(["Name", "URL", "Author", "Price", "No. of Ratings", "Rating"])

for pageNumber in range(1, 6):
    comAmazonURL = requests.get("https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg={0}".format(pageNumber))
    comAmazonData = BeautifulSoup(comAmazonURL.content, "lxml")

    bookCounter = 0

    for bookDataFull in comAmazonData.find_all('div', attrs={'class': 'a-section a-spacing-none p13n-asin'}):
        outputFile = open("../outputs/com_books.csv", "a")

        bookData = BeautifulSoup(str(bookDataFull), "lxml")
        if bookData.find('div', attrs={'class': 'p13n-sc-truncate p13n-sc-line-clamp-1'}) is None:
            bookName = "Not Available"
        else:
            bookName = bookData.find('div', attrs={'class': 'p13n-sc-truncate p13n-sc-line-clamp-1'}).get_text().strip()

        if bookData.find('a', attrs={'class': 'a-link-normal'}) is None:
            bookURL = "Not Available"
        else:
            bookLinkData = bookData.find('a', attrs={'class': 'a-link-normal'})
            if bookLinkData.get("href") is None:
                bookURL = "Not Available"
            else:
                bookLink = bookLinkData.get("href")
                bookURL = "https://www.amazon.in" + str(bookLink)

        if bookData.find('a', attrs={'class': 'a-size-small a-link-child'}) is None:
            bookAuthor = "Not Available"
        else:
            bookAuthor = bookData.find('a', attrs={'class': 'a-size-small a-link-child'}).get_text().strip()

        if bookData.find('span', attrs={'class': 'p13n-sc-price'}) is None:
            bookPrice = "Not Available"
        else:
            bookPrice = bookData.find('span', attrs={'class': 'p13n-sc-price'}).get_text().strip()

        if bookData.find('a', attrs={'class': 'a-size-small a-link-normal'}) is None:
            bookNoRatings = "Not Availble"
        else:
            bookNoRatings = bookData.find('a', attrs={'class': 'a-size-small a-link-normal'}).get_text().strip()
        if bookData.find('span', attrs={'class': 'a-icon-alt'}) is None:
            bookRating = "Not Available"
        else:
            bookRating = bookData.find('span', attrs={'class': 'a-icon-alt'}).get_text().strip()
            if bookRating == "Prime":
                bookRating = "Not Available"

        with outputFile:
            csvWriter = csv.writer(outputFile)
            csvWriter.writerow([bookName, bookURL, bookAuthor, bookPrice, bookNoRatings, bookRating])

        bookCounter += 1
        if(bookCounter == 20):
            break
