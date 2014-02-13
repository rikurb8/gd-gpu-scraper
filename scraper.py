#!/usr/bin/env python
#-*- coding:UTF-8 -*-

#rikujjs


from bs4 import BeautifulSoup
import requests
from time import sleep

#column_headers array contains the names for the columns.
column_headers = ["Title", "Releasedate"]


class Scraper:

    #make the parsed soup in to a variable called "soup"
    def __init__(self, url):

        #initialize the datastorage[] dict
        #for header in column_headers:
        #   self.datastorage[header] = '-'
        self.datastorage = []

        #include possible spoofed header, and get the page
        header = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=header)

        #make some soup
        self.soup = BeautifulSoup(r.text.encode('utf-8', 'ignore'))


    def date_format(self, date):
        #Mar-2010 eg. -> 03-2010
        months_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

        modifieddate = ""


        if '-' in date:
            month = date.split('-')
            try:
                modifieddate += str(months_dict[month[0]])
            except KeyError:
                modifieddate += '1'


            modifieddate += '-'
            modifieddate += month[1]

            date = modifieddate
        else:
            return date

        return date

    #we go thru the datastorage[] dict and write the info to a string, separated with ';'
    def info_to_string(self):

        info_string = ""

        for spec in self.datastorage:
            info_string += ';'
            info_string += spec.strip().encode('utf-8', 'ignore').replace(";", '')


        #get rid of the first ;
        info_string = info_string.replace(";", "", 1)

        return info_string



    #do the actual scraping
    def get_pageinfo(self):

        #model
        model = self.soup.find("span", id="art_g_title").text
        self.datastorage.append(model)

        #get the rel. date and format it to MM-YYYY
        release = self.soup.find("div", "hDate")
        release = release.findAll('tr')

        if "Release period" in release[0].text:
            date = self.date_format(release[1].findAll('td')[2].text.strip())
            self.datastorage.append(date)


        #now for the actual specs
        specs = self.soup.find("div", id="systemRequirementsOuterBox").findAll("div", "systemRequirementsWrapBox")[0]

        spec_rows = specs.findAll("div", "systemRequirementsSmallerBox")

        for row in spec_rows:
            try:
                self.datastorage.append(row.find('span').text.strip())
            except AttributeError:
                self.datastorage.append('-')


        #after all the info is in the datastorage[] dictionary, we write it to a single string and return
        return self.info_to_string()

    #member variables
    soup = None
    datastorage = []



def model_getter(output, url):

    #include possible spoofed header, and get the page
    header = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=header)
    #make some soup
    soup = BeautifulSoup(r.text.encode('utf-8', 'ignore'))


    model_list = soup.find("div", "darkBox2013 componentListTable")
    rows = model_list.findAll("div", "hardwareRow")

    #every row has a separate model on it, find the url and go get specs
    for i in range( 0, len(rows)):
        model = rows[i].find("div", "hardwareDeriv").find('a')['href']
        url_end = model.split('/', 1)
        model_url =  "http://www.game-debate.com/" + url_end[1]
        model_url = model_url.replace(' ', '%20')


        #get the page, BS it, and get the pageinfo
        page_to_get = Scraper(model_url)
        page_info = page_to_get.get_pageinfo()

        #print page_info

        #write the info to a outputfile
        output.write(page_info)
        output.write("\n")

        sleep(1)


if __name__ == "__main__":

    #the page that has the links for model seriesis. "Desktop" in the end can be changed to "Laptop" for mobile gpus
    front_page = "http://www.game-debate.com/hardware/index.php?list=gfxDesktop"

    #insert the base of the url's we're going to scare
    baseurl = ""




    #the file we are gonna write the gotten info, the file has the starting_id in it, in case starting
    #from somewhere else than the begining.
    starting_id = 0
    output_file = "gd-gpu-starting_from{0}.csv".format(starting_id)
    output = open(output_file, 'w')


    #include possible spoofed header, and get the page
    header = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(front_page, headers=header)
    #make some soup
    soup = BeautifulSoup(r.text.encode('utf-8', 'ignore'))

    #print soup

    #all the 3 different parts (nvidia, amd, intel cpu gpus) can be found here
    gamebody = soup.find("div", id="gambody")

    #gpu_gategories[0] = nvidia, [1] = amd, [2] = intel integrated
    gpu_gategories = gamebody.findAll("div", "darkBox2013 componentListTable")

    for i in range(0, 3):

        #rows with the model families
        rows = gpu_gategories[i].findAll("div", "hardwareRow")

        #find out every model familys url, and call model_getter with the url
        for i in range( 0, len(rows)):
            model = rows[i].find("div", "hardwareModel").find('a')['href']

            url_end = model.split('/', 1)

            url =  "http://www.game-debate.com/" + url_end[1]
            url = url.replace(' ', '%20')

            print url

            model_getter(output, url)













