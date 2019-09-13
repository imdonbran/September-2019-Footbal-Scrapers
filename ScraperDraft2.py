from selenium import webdriver
import xlwt
import smtplib
from email.message import EmailMessage


#This path needs to be changed for your computer
chromedrivepath = "C:\\Users\\donbran\\Desktop\\python\\webdriver\\chromedriver"

#1985 was the original starting year
startingyear:int = 2019
currentyear:int = 2019

#to turn on emailing, set it to "yes"
emailing : str = "no"

#emailling sender variables
sender : str= "brandonemailbot"
password:str= "somethingfornothing"

#add email address receivers here
#Email settings
contacts = ["@yahoo.com", "@gmail.com"]


subject :str = "NFL Drafts Scrape excel sheet"
message= EmailMessage()
message['Subject'] =subject
message['From'] = sender
message['To'] = contacts
message.set_content("")


#cycle through site based on year
def startdraft():
    for x in range(startingyear, currentyear+1):
        year : int =x
        draftsite: str = "https://www.pro-football-reference.com/years/" + str(year) + "/draft.htm"
        try:
            browser.get(draftsite)
            grabdata(year)
        except Exception as e:
            if emailing == "yes":
                print("Emailing")
                text= "The scraper broke somehwere on "+ draftsite +  "\n\n" +  str(e)
                message.set_content(text)
                mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                mail.login(sender, password)
                mail.send_message(message)
                mail.close()
            print("Error detected and emails have been sent")
            exit()
        browser.implicitly_wait(5)

        #for debugging
        #if x==1985:
        #    break


#grab all the draft data we need per site
def grabdata(thisyear):
    row : int = 1
    max : int = len( browser.find_elements_by_xpath('//*[@id="drafts_clone"]/tbody/tr') )

    for x in range(row, max+1):

        round :str = browser.find_element_by_xpath('//*[@id="drafts_clone"]/tbody/tr[' + str(row) + ']/th').text
        if str(round) != "Rnd":
            playername :str =   browser.find_element_by_xpath('//*[@id="drafts"]/tbody/tr[' + str(row) + ']/td[3]').text
            position   :str =   browser.find_element_by_xpath('//*[@id="drafts"]/tbody/tr[' + str(row) + ']/td[4]').text
            pick       :str =   browser.find_element_by_xpath('//*[@id="drafts_clone"]/tbody/tr[' + str(row) + ']/td[1]').text
            string     :str =   playername + ","+ position  + "," +  str(thisyear)  + "," + str(round)+","+ str(pick)
            list.append(string)
            print(string)
        row+=1

        #for debugging
        #if row==15:
        #    break

    #for x in list:
        #print(x)





browser = webdriver.Chrome(chromedrivepath)
list=[]
draftxl= xlwt.Workbook()
Drafts=  draftxl.add_sheet("Drafts")


#create headers for xml
#player, position,draftyear,draftround, draftnumber
header= Drafts.row(0)
header.write(0,"Player")
header.write(1,"Position")
header.write(2,"Draft Year")
header.write(3,"Draft Round")
header.write(4,"Draft Pick Number")

#This starts the scrape
startdraft()


#write to excel everything fromlist
for x in range(0,len(list)):
    thisrow= Drafts.row(x+1)
    contents=list[x].split(',')
    thisrow.write(0, contents[0])
    thisrow.write(1, contents[1])
    thisrow.write(2, contents[2])
    thisrow.write(3, contents[3])
    thisrow.write(4, contents[4])

print(len(list))
print(list)

excelname :str = "NFLdrafts" + str(startingyear) + "-" + str(currentyear) + ".xls"
draftxl.save(excelname)

browser.close()
browser.quit()
print(excelname)

#send out the xls in the email
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




