#How to use program:
#Open up the console.  copy paste the entire code
#run the following:
#browser = webdriver.Chrome() #<======make sure the filepath is here
#get_data(browser) #<==== get_data should be changed based on what year you want
#then compile_stats()
import os
import glob
import time
import re
import csv
import selenium
import threading
from selenium import webdriver
import smtplib
from email.message import EmailMessage
import selenium.common.exceptions


thisyear = 2019
thisweek = 1

#took 40 mins

chromedrivepath = "C:\\Users\\donbran\\Desktop\\python\\webdriver\\chromedriver"
browser = webdriver.Chrome() #<======make sure the filepath is here

#Interval Time in seconds
days=7
waitinterval= 60 * 60 * 24 * days
ticker = threading.Event()

#to turn on emailing, set it to "yes"
emailing : str = "yes"

#emailling sender variables
sender : str= "brandonemailbot"
password : str= "somethingfornothing"

#add email address receivers here
#Email settings
contacts = ["@yahoo.com", "@gmail.com"]
subject :str = "PFF Scrape excel sheet"
message= EmailMessage()
message['Subject'] =subject
message['From'] = sender
message['To'] = contacts
message.set_content("")


GRADE_TYPES = ['offense','passing','rushing','receiving','defense']

GRADES_HEADERS = {'offense':['RANK', 'PLAYER', 'grade_type', '#', 'game_id', 'week', 'year', 'home_team', 'away_team', 'home_score', 'away_score', 'date', 'S', 'POS', 'TOT', 'PASS', 'PBLK', 'RUN', 'RBLK', 'OFF', 'PASS', 'PBLK', 'RUN', 'RBLK', 'PEN','TEAM'],
                  'passing':['RANK', 'PLAYER', '#','grade_type', 'game_id', 'week', 'year', 'home_team', 'away_team', 'home_score', 'away_score', 'date', 'S', 'POS', 'DB', 'ATT', 'COM', 'COM%', 'YDS', 'YPA', 'TD', 'INT', 'OFF', 'PASS', 'RUN', 'FUM', 'SK', 'BAT', 'DRP', 'TA', 'HAT', 'NFL', 'SCR', '1ST','TEAM'],
                  'rushing':['RANK', 'PLAYER', '#','grade_type', 'game_id', 'week', 'year', 'home_team', 'away_team', 'home_score', 'away_score', 'date', 'S', 'POS', 'SNP', 'OFF', 'RUN', 'FUM', 'RBLK', 'ATT', 'SCR', 'DYDS', 'SYDS', 'YDS', 'YPA', 'TD', '1ST', '10+', 'YCO', 'YCO/A', 'LNG', 'AVT', 'FUM', 'PEN','TEAM'],
                  'receiving':['RANK', 'PLAYER', '#','grade_type', 'game_id', 'week', 'year', 'home_team', 'away_team', 'home_score', 'away_score', 'date', 'S', 'POS', 'TGT', 'REC', 'REC%', 'YDS', 'TD', 'OFF', 'RECV', 'DROP', 'FUM', 'PBLK', 'Y/REC', 'YAC', 'YAC/REC', 'LNG', '1ST', 'DRP', 'INT', 'FUM', 'AVT', 'RTG', 'PEN','TEAM'],
                  'defense': ['RANK', 'PLAYER', '#','grade_type', 'game_id', 'week', 'year', 'home_team', 'away_team', 'home_score', 'away_score', 'date', 'S', 'POS', 'TOT', 'RDEF', 'PRSH', 'COV', 'DEF', 'RDEF', 'TACK', 'PRSH', 'COV', 'TOT', 'SK', 'HIT', 'HUR', 'BAT', 'TKL', 'AST', 'MIS', 'STOP', 'FFM', 'TGT', 'REC', 'REC%', 'YDS', 'Y/REC', 'YAC', 'LNG', 'TD', 'INT', 'PBU', 'NFL', 'PEN','TEAM']
                  }
URL_CHANGES = {'offense': 'offense' ,
                  'passing': 'offense/passing',
                  'rushing': 'offense/rushing',
                  'receiving': 'offense/receiving',
                  'defense': 'defense'
                  }





#Checks to see if the page is blank
def check_clear(browser):
    time.sleep(2)
    try:
        if browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]').text == '':
            return True
        else:
            return False
    except:
        return True

#when we get to the screen whatever grade it is, it make both teams into a CSV
def getBothTeams(browser, grade_type, game_number, week, year):

    home = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div[2]/div[2]/label[1]').text
    away = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div[2]/div[2]/label[2]').text
    score_home = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[2]/div/div[3]/div[1]/div').text
    score_away = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[2]/div/div[3]/div[3]/div').text
    date = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/span[2]').text

    browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div[2]/div[2]/label[1]').click()
    time.sleep(2)

    getGrades(browser, grade_type, game_number, week, year,home,away,score_home,score_away,date)

    browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div/div/div/div[2]/div[2]/label[2]').click()
    time.sleep(2)

    getGrades(browser, grade_type, game_number, week, year, home,away,score_home,score_away,date)
    # return

#feeds getBothTeams
def getGrades(browser, grade_type, game_number, week, year,home,away,score_home,score_away,date): #type can be keys from GRADES_HEADERS

    first_part = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[1]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/div').text.split('\n')
    number_of_players = int(len(first_part)/3)

    #arranges to table format
    table = []

    for k in range(0,number_of_players):
        templist = []
        player_1st = browser.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[1]/div[3]/div/div[1]/div[2]/div/div[1]/div/div[1]/div/div[' + str(k+1) + ']/div')
        player_2nd = browser.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[1]/div[3]/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[' + str(k+1) + ']/div')
        for element in player_1st:
            templist.append(element.text)
        templist.append(grade_type)
        templist.append(game_number)
        templist.append(week)
        templist.append(year)
        templist.append(home)
        templist.append(away)
        templist.append(score_home)
        templist.append(score_away)
        templist.append(date)
        for element in player_2nd:
            templist.append(element.text)
        table.append(templist)
    team = browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div[1]/div[1]/h1').text.split(' - ')[0]
    name = '%s_%s_%s_%s.csv' %(grade_type,year,week,team)
    convertCSV(name, table)

#feeds getGrades
def convertCSV(name, data):
    with open(name, "w", newline='') as csvfile:
         writer = csv.writer(csvfile)
         writer.writerows(data)
    print('converted CSV',name)


def get_data(browser):
    #Page through Year
    #   Page through Week
    #       Page through Game
    #           Get Data

    homebase = ('https://premium.pff.com/nfl/games?season=%s&week=%s' % (str(thisyear), str(thisweek)))

    for i in range(1,17): #16 games max in a week 17
        try:
            browser.get(homebase)
            time.sleep(2)

            page_number = str(i)
            browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/div/div[%s]/div/div[3]/div[1]/button' %page_number).click()
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div[2]/div[1]/div/div[1]').click()
            time.sleep(2)

            game_number = browser.current_url.split('/')[5]
            week = browser.current_url.split('week=')[1][:2].replace('&', '')
            year = re.search('season=(.*)&week', browser.current_url).group(1)
            for grade_type in GRADE_TYPES:  # ALL THE GRADE TYPES
                url = 'https://premium.pff.com/nfl/games/%s/%s/summary?season=%s&week=%s' % (game_number, URL_CHANGES[grade_type], year, week)
                browser.get(url)
                time.sleep(2)

                # converts the stuff to CSV
                getBothTeams(browser, grade_type, game_number, thisweek, thisyear)
        except selenium.common.exceptions.NoSuchElementException as e:
            erroremail(str(e), homebase)
        #browser.close()
        #exit()


#---stats compile
def compile_stats():
    stats = ['defense', 'offense','rushing','passing','receiving']
    print("Start compile stats")
    #cycle through the different categories in stats
    for stat in stats:
        path = os.getcwd()
        print(os.listdir())
        print(path)

        fdata = []
        #print(str(glob.glob(path)))
        #if the csv's category matches up with the current stat category, then add it to the compiled csv
        for file in os.listdir():
            team : str = file.split('_')[-1].replace('.csv','')
            print(file)
            if str(file.split('_')[0]) == str(stat):
                with open(file) as csvfile:

                    reader = csv.reader(csvfile)

                    for row in reader:
                        temprow = row
                        temprow.append(team)
                        fdata.append(temprow)
        fdata.insert(0,GRADES_HEADERS[stat])
        name = '%s.csv' %stat
        convertCSV(name,fdata)

        #add the csv to attachments for the email
        with open(name, 'rb') as f:
            file_data = f.read()
            file_type = "csv"
            file_name = f.name
        message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
#---end stats compile

#auditing

def audit():
    stats = ['defense', 'offense','rushing','passing','receiving']
    # for stat in stats:
    stat = 'rushing'
    path = os.path.expanduser('~\Documents\GitHub\RIU_Studios\pff\%s*' %stat)
    i=0
    tdict = {}
    for file in glob.glob(path):
        for i in range(2003,2019):
            for j in range(1,22):
                string_part = ('%s_%s_' %(str(i),str(j)))
                if if_looper(string_part,file):
                    if string_part in tdict:
                        tdict[string_part]+=1
                    else:
                        tdict[string_part] = 1
    for a in tdict:
        print(a,tdict[a])
#utility for audit
def if_looper(condit, name):
    if condit in name:
        return True
    else:
        return False
#----end auditing

#rune the scraper and sets up folders to store the data in
def setupfolders():
    print("loop")
    #Using ctime to help label a new folder
    string : str = str(time.ctime())
    string : str = string.replace(':', '.')
    string : str = string.replace(' ', '_')
    string : str = "PFFScrape_" + string
    print(string)

    #go into that newly created folder
    os.mkdir(string)
    os.chdir(string)
    print(os.listdir())

    msg: str = "Collected at " + str(time.ctime() + "\nWeek:" + str(thisweek) + " of " + str(thisyear))
    message.set_content(msg)

    #scrape and compile
    get_data(browser) #<==== get_data should be changed based on what year you want
    compile_stats()



    #send email, clear the attachments, then back out of this folder into folder that houses PFFScraper
    sendemail()
    message.clear_content()
    os.chdir("..")
    print(os.listdir())

#sends the email when things go right
def sendemail():
    if emailing == "yes":
        print("Emailing")

        mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail.login(sender, password)
        mail.send_message(message)
        mail.close()

#sends the email when things go wrong
def erroremail(E, site):
    if emailing == "yes":
        print("Emailing the error")
        message.clear_content()
        msg : str ="An error has been detected on Week:"+ str(thisweek) + " Year:" + str(thisyear) + " the PFF Scraper\n" + str(E) + "\n" + str(site)
        message.set_content( msg )
        mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail.login(sender, password)
        mail.send_message(message)
        mail.close()


#does whatever week this is set to, then goes to the next week when the wait interval is done,
#runs to the end of the year
print("Wait Interval is "+ str(waitinterval) + " seconds" )

#1st week
#setupfolders()
#thisweek+=1

#2nd week
setupfolders()

#following weeks
while not ticker.wait(waitinterval):
    if thisweek >=17:
        break
    else:
        thisweek+=1
    setupfolders()


browser.close()
print("Year Finished")









