'''
NOTES
https://www.cisco.com/c/en/us/products/eos-eol-listing.html
Holds all the data containing router models.
<div class="eol-listing-cq">


/////////////Cisco serial numbers////////////
The serial number will be in the format: 'LLLYYWWSSSS';
'YY' is the year of manufacture 
'W' is the week of manufacture.  
DATE DECODE TABLE - https://community.cisco.com/t5/switching/cisco-serial-number-lookups/td-p/1375234
///////////////////////////////////////////////


___________________________________________________________________________________________________
Get model name and check all eol-listing-cq classes if model name string in any of the rows. 
if true, group found and test name. 
we need to make sure that they match directly. if they are matching loose, then we need to make sure we test the number against all and not just return the first find
____________________________________________________________________________________
it would be cool to add a serial number and check the name of the model but ill need to log into cisco
to use their schecker website 

< 3tiermargin > are the groups with multiple in them 
'''

# grab EOL list
import requests
from bs4 import BeautifulSoup

# email
import smtplib

import pprint




# returns categories , links , and texts of all model names 
def getEOL_list():
    # go on the website
    page = requests.get('https://www.cisco.com/c/en/us/products/eos-eol-listing.html')
    soup = BeautifulSoup(page.content, 'html.parser')

    # get most recent updated html
    title = soup.find_all(class_="contentBold")
    contentLink = soup.find_all(class_="contentLink")
    content_NO_LINK = soup.find_all(class_="contentContent")

    # filter lower cased text <---- TITLE
    Clean_titles = []
    for x in title:
        clean_data = x.text.lower() 
        Clean_titles.append(clean_data)

    # filter lower cased text <---- LINKS
    Clean_links = []
    for x in contentLink:
        clean_data = x.text.lower() 
        Clean_links.append(clean_data)

    # filter lower cased text <---- TEXT ONLY
    Clean_text = []
    for x in content_NO_LINK:
        clean_data = x.text.lower() 
        Clean_text.append(clean_data)

    # print(len(Clean_titles))
    # print(len(Clean_links))
    # print(len(Clean_text))

    print( f"There are {len(Clean_links)  + len(Clean_text) } routers that are End-Of-Life."  )

    return Clean_titles , Clean_links , Clean_text








# constantly grab an EOL List and then save it. go onto next iteration, subtract diff of lengths , if < 0 notify with an email   --- make sure to add email list param
# add new updated routers into the email. TODO
def ConstantChecker_EOL():
    prev_titles = 0
    prev_links = 0
    prev_texts = 0
    while True:
        curr_title , curr_links , curr_texts = getEOL_list()

        if ( prev_titles - len(curr_title) ) < 0:
            print('new categories email')
            send_Email()

        if ( prev_links - len(curr_links) ) < 0:
            print('new items email')
            send_Email()

        if ( prev_texts - len(curr_texts) ) < 0:
            print('new items email')
            send_Email()

        prev_titles = len(curr_title)
        prev_links = len(curr_links)
        prev_texts = len(curr_texts)




def send_Email():
    content = 'Subject: Cisco EOL Service Update\n\n Please check to see if your device is not supported anymore.'
    mail = smtplib.SMTP("smtp.gmail.com" , 587)
    mail.ehlo()
    mail.starttls()
    emailAddress = "laflametoast@gmail.com"
    password = "YOUR_EMAIL_PASSWORD"
    mail.login(emailAddress , password)
    
    # TODO add email list here 
    mail.sendmail("laflametoast@gmail.com" , "affan.fareed@gmail.com", content )








# Search for model 
def UserModel_Checker(user_model):
    user_model = user_model.lower()

    EOL_titles , EOL_links , EOL_texts = getEOL_list()

    output = {
        "titles" : [],
        "routers" : [],
        "texts" : [],
    }

    for x in EOL_titles:
        if user_model in x:
            output['titles'].append(x)
            print(x)

    for x in EOL_links:
        if user_model in x:
            output['routers'].append(x)
            print(x)

    for x in EOL_texts:
        if user_model in x:
            output['texts'].append(x)
            print(x)

    return output




def main():
    print("Welcome to Cisco EOL Support\n")
    print("1 - Constant Checker")
    print("2 - Search EOL for specific model")
    options = input("Please choose an option: ")

    if options == '1':
        ConstantChecker_EOL()
    
    elif options == '2':
        model_Name = input("\nPlease enter a model name: \n>> ")
        output = UserModel_Checker(model_Name)

    else:
        print("Inavalid option\n\n")





# calling functions down here
# main()
all_end_of_life_routers = getEOL_list()