from selenium import webdriver
import xlwt
from selenium.common.exceptions import TimeoutException
import smtplib
from email.message import EmailMessage


#This needs to be changed per computer
chromedrivepath = "C:\\Users\\donbran\\Desktop\\python\\webdriver\\chromedriver"

#to turn on emailing, set it to "yes"
emailing : str = "yes"

#emailling sender variables
sender : str= "brandonemailbot"
password:str= "somethingfornothing"

#add email address receivers here
#Email settings
contacts = ["@yahoo.com", "@gmail.com"]
subject :str = "NFL Birthdays Scrape excel sheet"
message= EmailMessage()
message['Subject'] =subject
message['From'] = sender
message['To'] = contacts
message.set_content("")





browser = webdriver.Chrome(chromedrivepath)

#runs through every month, every month cycles through all the days in that month
def startdob():
    janbirths()
    febbirths()
    marbirths()
    aprbirths()
    maybirths()
    junbirths()
    julbirths()
    augbirths()
    sepbirths()
    octbirths()
    novbirths()
    decbirths()


def janbirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=1&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("January", str(x), dobs, dobsite)


def febbirths():
    for x in range(1, 30):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=2&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("February", str(x), dobs, dobsite)


def marbirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=3&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("March", str(x), dobs, dobsite)


def aprbirths():
    for x in range(1, 31):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=4&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("April", str(x), dobs, dobsite)



def maybirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=5&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("May", str(x), dobs, dobsite)


def junbirths():
    for x in range(1, 31):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=6&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("June", str(x), dobs, dobsite)


def julbirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=7&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("July", str(x), dobs, dobsite)


def augbirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=8&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("August", str(x), dobs, dobsite)


def sepbirths():
    for x in range (1,31):
        dobsite:str  ='https://www.pro-football-reference.com/friv/birthdays.cgi?month=9&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("September", str(x), dobs, dobsite)


def octbirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=10&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("October", str(x), dobs, dobsite)


def novbirths():
    for x in range(1, 31):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=11&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("November", str(x), dobs, dobsite)


def decbirths():
    for x in range(1, 32):
        dobsite :str = 'https://www.pro-football-reference.com/friv/birthdays.cgi?month=12&day=' + str(x)
        browser.get(dobsite)
        browser.implicitly_wait(5)
        grabbirths("December", str(x), dobs, dobsite)




def grabbirths(birthmonth,birthday, doblist,sitename):
    try:
        max :int = len(browser.find_elements_by_xpath('//*[@id="birthdays"]/tbody/tr'))
        #print(max)
        row :int =1
        for x in range(row, max + 1):
            rank = browser.find_element_by_xpath('//*[@id="birthdays"]/tbody/tr[' + str(row) + ']/th' or '//*[@id="birthdays_clone"]/tbody/tr[' + str(row) + ']/th').text
            if rank.isdigit():

                    playername : str = browser.find_element_by_xpath('//*[@id="birthdays"]/tbody/tr[' + str(row) + ']/td[1]/a' or '//*[@id="birthdays_clone"]/tbody/tr[' + str(row) + ']/td[1]/a').text
                    birthyear  : str = browser.find_elements_by_xpath('//*[@id="birthdays"]/tbody/tr[' + str(row) +']/td[3]' or '//*[@id="birthdays_clone"]/tbody/tr[' + str(row) + ']/td[3]')[0].text
                    string     : str = playername + "," + birthmonth + " " + birthday + "," + birthyear
                    print(string)
                    doblist.append(string)

                #    browser.refresh()
                #    browser.implicitly_wait(10)
                #    playername :str = browser.find_element_by_xpath('//*[@id="birthdays_clone"]/tbody/tr[' + str(row) + ']/td[1]/a' or '//*[@id="birthdays"]/tbody/tr[' + str(row) + ']/td[1]/a').text
                #    birthyear  :str = browser.find_elements_by_xpath('//*[@id="birthdays_clone"]/tbody/tr[' + str(row) + ']/td[3]' or '//*[@id="birthdays"]/tbody/tr[' + str(row) + ']/td[3]')[0].text
                #    string     :str = playername + "," + birthmonth + " " + birthday + "," + birthyear
                #    print(string)
                #    doblist.append(string)
            row += 1
    except TimeoutException as e:
        browser.get(sitename)
        browser.implicitly_wait(10)
        grabbirths(birthmonth,birthday,doblist,sitename)
    except Exception as e:
        if emailing == "yes":
            print("Emailing")
            text = "The scraper broke somehwere on " + sitename + "\n\n" + str(e)
            message.set_content(text)
            mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            mail.login(sender, password)
            mail.send_message(message)
            mail.close()
        print("Error detected and emails have been sent")
        exit()





#Start of program

dobs=[]
dobxl = xlwt.Workbook()
Birthdays=dobxl.add_sheet("Birthdays")


#excel header creation
#player, birth date, birth year
header = Birthdays.row(0)
header.write(0,"Player")
header.write(1,"Birthday")
header.write(2,"Birth year")


#initiate scrape here

startdob()
#janbirths()
#febbirths()
#marbirths()
#aprbirths()
#maybirths()
#junbirths()
#julbirths()
#augbirths()
#sepbirths()
#octbirths()
#novbirths()
#decbirths()

#cleans duplicates out
print(len(dobs))
duplicatescleaner = set(dobs)
dobs = list(duplicatescleaner)
print(len(duplicatescleaner))


#write to excel file from list of dobs
for x in range(0,len(dobs) ):
    thisrow= Birthdays.row(x+1)
    contents= dobs[x].split(',')
    thisrow.write(0, contents[0])
    thisrow.write(1, contents[1])
    thisrow.write(2, contents[2])



excelname  :str = "NFLbirthdays.xls"
dobxl.save(excelname)


browser.close()
browser.quit()

#sending the emails
if emailing == "yes":
    print("Emailing")
    files = [excelname]
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_type = "xls"
            file_name = f.name
    message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail.login(sender, password)
    mail.send_message(message)
    mail.close()
