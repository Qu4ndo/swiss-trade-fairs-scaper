from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv


#grab all basic informations from the website_container
def get_buffer():

    page_number_max = 100   #increase if not all pages are scraped
    page_number = 1         #first page to start

    filename = "buffer.csv"
    b = open(filename, "w")
    headers = "link; company_name"
    b.write(headers)

    for x in range(0, page_number_max):
        myurl = "https://guide.swissbau.ch/de/aussteller?page=" + str(page_number)
        page_number += 1

        #connencting to site and grabbing content
        uClient = uReq(myurl)
        page_html = uClient.read()
        uClient.close()

        #html parser
        page_soup = soup(page_html, "html.parser")

        #grabs each object
        containers = page_soup.findAll("li", {"class":"ngn-content-box ngn-content-box-horizontal ngn-bookmark-button-visible"})

        #loop container to get infos and safe to csv
        for container in containers:
            #name of the company
            company_name = container.div.picture.img["alt"]
            #link to profile page
            link = "https://guide.swissbau.ch" + container.div.a["href"]
            b.write("\n" + link + ";" + company_name)
            print(company_name + ", " + link)

    b.close()


#grab all detailed inforamtion from the website
def get_details():

    filename = "buffer.csv"
    b = open(filename, "r+")
    data = csv.reader(b, delimiter=';')

    #ignore header row
    headers = next(data)

    #write to new CSV file
    filename = "index_exhibitors.csv"
    f = open(filename, "w")
    headers = "link; company_name; adress; postal; city; country; phone; website; contact_name; contact_position; contact_link"
    f.write(headers)

    for row in data:
        print(row[1])
        myurl = row[0]
        company = row[1]

        #connencting to site and grabbing content
        uClient = uReq(myurl)
        page_html = uClient.read()
        uClient.close()

        #html parser
        page_soup = soup(page_html, "html.parser")

        #grabs each object
        container_details = page_soup.findAll("div", {"class":"ngn-box__content"})
        container_contact = page_soup.findAll("div", {"class":"media-object-section"})

        adress = ""
        postal = ""
        city = ""
        country = ""
        phone = ""
        website = ""
        contact_name = ""
        contact_position = ""
        contact_link = ""

    #get full adress info
        try:
            #adress
            adress_container = container_details[1].find("span", {"itemprop":"streetAddress"})
            adress = adress_container.get_text().strip()

            #postalcode
            postal_container = container_details[1].find("span", {"itemprop":"postalCode"})
            postal = postal_container.get_text().strip()

            #city
            city_container = container_details[1].find("span", {"itemprop":"addressLocality"})
            city = city_container.get_text().strip()

            #country
            country_container = container_details[1].find("span", {"itemprop":"addressCountry"})
            country = country_container.get_text().strip()

        except AttributeError:
            try:
                #adress
                adress_container = container_details[0].find("span", {"itemprop":"streetAddress"})
                adress = adress_container.get_text().strip()

                #postalcode
                postal_container = container_details[0].find("span", {"itemprop":"postalCode"})
                postal = postal_container.get_text().strip()

                #city
                city_container = container_details[0].find("span", {"itemprop":"addressLocality"})
                city = city_container.get_text().strip()

                #country
                country_container = container_details[0].find("span", {"itemprop":"addressCountry"})
                country = country_container.get_text().strip()
            except:
                pass

        except:
            pass


    #get phone and website
        try:
            #phone
            phone_container = container_details[2].a["href"]
            phone = phone_container.replace("tel:", "")

            #website
            website_container = container_details[3].a["content"]
            website = website_container

        except IndexError:
            try:
                #phone
                phone_container = container_details[1].a["href"]
                phone = phone_container.replace("tel:", "")

                #website
                website_container = container_details[2].a["content"]
                website = website_container
            except:
                pass

        except:
            pass

    #get full contact info
        try:
            #contact_name
            contact_name_container = container_contact[2].img["alt"]
            contact_name = contact_name_container

            #contact_position
            contact_position_container = container_contact[3].div.find("div", {"itemprop":"jobTitle"})
            contact_position = contact_position_container.get_text().strip()

            #contact_link
            contact_link_container = container_contact[2].div.a["href"]
            contact_link = "https://guide.swissbau.ch" + contact_link_container

        except IndexError:
            try:
                #contact_name
                contact_name_container = container_contact[3].img["alt"]
                contact_name = contact_name_container

                #contact_position
                contact_position_container = container_contact[4].div.find("div", {"itemprop":"jobTitle"})
                contact_position = contact_position_container.get_text().strip()

                #contact_link
                contact_link_container = container_contact[3].div.a["href"]
                contact_link = "https://guide.swissbau.ch" + contact_link_container
            except:
                pass

        except:
            pass


        f.write("\n" + myurl + ";" + company + ";" + adress + ";" + postal + ";" + city + ";" + country + ";" + phone + ";" + website + ";" + contact_name + ";" + contact_position + ";" + contact_link)

    b.close()
    f.close()
