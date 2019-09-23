# September-2019-Footbal-Scrapers
NFL birthdays, drafts, pff

Dependencies 
downloads
-chromedriver

python modules:
-Selenium
-xlwt
-smtplib
-email.message


------------------------
How they work
-------------------------
Drafts Scraper:

~Runthrough:
-Scraper goes to NFL site based on what the starting year is in startdraft()
-grabs the relevent data using grabdata(), compiles it into a string, then stores it in a global string list
-cycles to the next year until it hits currentyear

~Controls
-Set the interval for years you want to sift through with "startingyear" and "currentyear"

~Emailing
-to turn on emailing the excel file and error message emails, change "emailing" to yes
-I have put in a throw away gmail to use, you can change it in the "sender" variable. It has to be a gmail I'm pretty sure, it needs not
the @gmail.com in the string
-add the email addresses you want to send the messages/files to in the "contacts" list. These need the @address.com

~Functions
startdraft()
-starts loop that cycles through years from between [startingyear, currentyear]
-goes too each page based on the year
-calls grabdata()

grabdata(thisyear)
-counts all the players in the website's draft section
-collects each player row by row, storing their data into one string
-stores string into global list of strings

After the scraper finishes storing all the player data in the list, it parses through the list and puts it in the excel file


__________________________
Birthdays Scraper:
-Run-through
-Scrapes through every day of the year 
-functions scrape by month, each month has its own function, and startdob() is running all 12 
-each month loops through all the days of the month, calling grabbirths() on each day
-grabbirths grabs the data the same way grabdata does, but has an additional check to see if the row has data, because in the birthday site layout, there will be blank rows sometimes

~Controls
Choose which months you want to scrape through

~Emailing
same as Drafts

~Functions
-startdob() does every month
-each month does the same thing, but they all have varying days

~Note
-For currently unkown reasons, this program is prone to TimeoutExceptions. As of now, the program continues to run when these exceptions occur and will continue to scrape data. When the scraper does hit these exceptions, there will be duplicate entries. The duplicates are taken out by turning the list into a set and then back into a list again.

_____________________________________________________________________________________________________
PFF Scraper:
_____________________________________________________________________________________________________
~Basic Overview:
- running the program will execute whatever week it is set to now, and then begin a loop that sleeps the program for a week (set by waitinterval) and then scrapes the next week. 
- the program will run at most 16 scrapes
- if you want to add more scrapes out of the loop before it starts, call a complete scrape of the week, setupfolders(), and increment the thisweek by 1
-Error emails will be sent when they occur, but the program will continue to run and collect data. It will also still send the data of the week where the error occurred


~Control Variables:
- thisyear tells it what year to scrape
- thisweek tells you what week to start the scrape on
- waitinterval is the delay the program waits in seconds till the next scrape. It should be set on a week currently

~Functions
-get_data(), getGrades(), & getBothTeams() are all data collecting funtions. In the end they output csv files of each game
-converCSV() converts data into csvs
-compile_stats() takes all of the csvs created from the scrape and makes new ones with the compiled stats per category
-setupfolders() creates a newfolder with the current time on it, goes into it, then calls the scrape. At the end, it sends the emails and backs out of that folder
-sendemail() and erroremail() are for email handling

~Things that need to be changed before use
-contacts variable for who you want to send the emails to
-the webdriver path








