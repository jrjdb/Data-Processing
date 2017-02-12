#!/usr/bin/env python
# Name: Jelle de Boer  
# Student number: 10540075  
'''
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
'''
import csv

from pattern.web import URL, DOM, plaintext
import re


TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    '''
    Extract a list of highest rated TV series from DOM (of IMDB page).

    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    '''
    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED TV-SERIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    series = []
    for serie in dom.by_class('lister-item'): 
        serieList = [None] * 5
        # Extracts the tv-serie title
        serieList[0] = re.findall(r'\.(.*?)\(',plaintext(serie.by_tag('h3')[0].content))[0]
        # Extracts the rating
        serieList[1] = plaintext(serie.by_class('ratings-imdb-rating')[0].content)
        # Extracts the genre
        serieList[2] = plaintext(serie.by_class('genre')[0].content)
        # Extracts the actors/actresses
        serieList[3] = plaintext(serie.by_tag('p')[2].content).replace('Stars:', '')
        # Extracts the runtime 
        serieList[4] = plaintext(serie.by_class('runtime')[0].content).replace('min', '')
        
        # Puts a list of serie-info in a dict for a certain serie - the key
        series.append(serieList)

    return series

def save_csv(f, tvseries):
    '''
    Output a CSV file containing highest rated TV-series.
    '''
    writer = csv.writer(f)
    writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])

    for tvs in tvseries: 
        writer.writerow([tvs[0].encode('utf8'), tvs[1].encode('utf8'), \
            tvs[2].encode('utf8'), tvs[3].encode('utf8'), \
            tvs[4].encode('utf8')])
    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE TV-SERIES TO DISK

if __name__ == '__main__':
    # Download the HTML file
    url = URL(TARGET_URL)
    html = url.download()

    # Save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # Parse the HTML file into a DOM representation
    dom = DOM(html)

    # Extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # Write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'wb') as output_file:
        save_csv(output_file, tvseries)