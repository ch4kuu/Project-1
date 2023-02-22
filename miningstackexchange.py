from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import urlopen
import time

def getLinks():
    links = []
    link_string = "https://bitcoin.stackexchange.com"
    for page in range(1,3):
        url = f"https://bitcoin.stackexchange.com/questions?pagesize=50&sort=newest&page=%7Bpage%7D"
        time.sleep(2)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        questions  = soup.find_all('div',{'class': 's-post-summary'})
        for items in questions:
            title = items.find('a',{'class': 's-link'}).text
    
            title_id = items.find('a',{'class': 's-link'})['href']
            temp_string = link_string + title_id
            links.append(temp_string)
            time.sleep(2)
    return links

def extractQuestionData(bitcoin_url):
    response = requests.get(bitcoin_url)
    with urlopen (bitcoin_url) as url:
        soup = BeautifulSoup(url, "lxml")

        # to check if question is edited
        edited_check = soup.find('div', {'class': 'user-action-time'}).text
        if "edited" in edited_check:
          edited_flag = True

        else:
          edited_flag = False
   #   print(edited_flag)

      

        with open("bitcoin-questions.csv",'a') as csvfile:
            csvwriter = csv.writer(csvfile)
    
            row = []
            
            # get the title
            title = soup.find('a',{'class': 'question-hyperlink'}).text
            row.append(title)
            #print(title)
            
            # get the ID
            ques_id = soup.find('div',{'class': 'question js-question'})['data-questionid']
            row.append(ques_id)
            #print(ques_id)
            
            # get the author name
            author_name = soup.find('span', attrs={'itemprop': 'name'}).text
            row.append(author_name)
            #print(author_name)
            
            # get the author reputation
            author_rep = soup.find('span', attrs={'class': 'reputation-score'}).text
            row.append(author_rep)
            #print(author_rep)
                
            # get the time Time_Posted
            time_posted = soup.find('time')['datetime']
            row.append(time_posted)
            #print(time_posted)
                
            # get the question score
            ques_score = soup.find('div',{'itemprop': 'upvoteCount'}).text
            row.append(ques_score)
            #print(ques_score)
            
            
            
            csvwriter.writerow(row)
        time.sleep(2)

    
def extractAnswerData(bitcoin_url):
# =============================================================================
# Chanel
#   This function takes in a bitcoin stack exchange URL. 
#   	- The URL is for ONE question
#   After the URL is taken, the function extracts the answer data
#   	- the answer IDs, answer scores, author names, author reputations
#     		the number of comments, and whether the answer is accepted
# 	Finally this information is written into a .csv file
# 
# =============================================================================
  
    response = requests.get(bitcoin_url)
    with urlopen (bitcoin_url) as url:
        soup = BeautifulSoup(url, "lxml")
    
       # to check if question is edited
        edited_check = soup.find('div', {'class': 'user-action-time'}).text
        if "edited" in edited_check:
            edited_flag = True
    
        else:
            edited_flag = False
           #   print(edited_flag)

        with open("bitcoin-answers.csv",'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter = csv.writer(csvfile)
            
         

          # if the answer is accepted
            for accepted_answer in soup.findAll('div', {'class': 'answer js-answer accepted-answer js-accepted-answer'}):
                row = []
    
                  # gets answer id
                ans_id = accepted_answer['data-answerid']
                #  print("answer id: " + ans_id)
                row.append(ans_id)
    
                  # gets answer score
                ans_score = accepted_answer['data-score']
               #   print("answer score: " + ans_score)
                row.append(ans_score)
    
                  # gets author name
                ans_author_name = accepted_answer.find('span', attrs={'itemprop': 'name'}).text
               #   print("answer author: " + ans_author_name)
                row.append(ans_author_name)
    
                  # gets author rep
                ans_rep = accepted_answer.find('span', attrs={'class': 'reputation-score'}).text
                #  print(ans_rep)
                row.append(ans_rep)
    
                  # gets comment count, then checks if answer has no comments
                ans_com_count = accepted_answer.find('span', attrs={'itemprop' :'commentCount'}).text
                if not ans_com_count:
                    ans_com_count = "0"
               #   print("answer comment count: " + ans_com_count)
                    row.append(ans_com_count)            
    
                    accepted = True
                    row.append(accepted)
    
                # writes to csv
                csvwriter.writerow(row)
            time.sleep(2)

         
            for answer in soup.findAll('div', {'class': 'answer js-answer'}):
                row = []

                ans_id = answer['data-answerid']
             # print("answer id: " + ans_id)
                row.append(ans_id)

                ans_score = answer['data-score']
             # print("answer score: " + ans_score)
                row.append(ans_score)

                ans_author_name = answer.find('span', attrs={'itemprop': 'name'}).text
             # print("answer author: " + ans_author_name)
                row.append(ans_author_name)

                ans_rep = answer.find('span', attrs={'class': 'reputation-score'}).text
            #  print(ans_rep)
                row.append(ans_rep)

                ans_com_count = answer.find('span', attrs={'itemprop' :'commentCount'}).text
                if not ans_com_count:
                    ans_com_count = "0"
            #  print("answer comment count: " + ans_com_count)
                row.append(ans_com_count)

                accepted = False
            #  print(accepted)
                row.append(accepted)

                csvwriter.writerow(row)
            time.sleep(2)
#  NOTE: 
# each url should be one question. 
# this function should be ran in a for loop
# EXAMPLE:
# list_of_all_URLS = [SOME SHIT]
# for url in list_of_all_URLS:
#		extractAnswerData(url)
def main():
    links = getLinks()
    
    # fields is the column names in the csv
    aFields = ["Answer_ID", "Answer_Score", "Author_Name", "Author_Rep", 
    "Number_Of_Comments", "Answer_Accepted"]
             
    # fields is the column names in the csv
    qFields = ["title", "Ques_ID", "Author_Name", "Author_Rep", 
    "Time_Posted", "Ques_Score", "Num_Answers", "Ans_Accepted","" ]
    
    with open("bitcoin-questions.csv",'w', newline="") as qcsv:
        csvwriter = csv.writer(qcsv)
        csvwriter.writerow(qFields)
       
    
    with open("bitcoin-answers.csv",'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(aFields)
        
    
        
    for link in links:
        extractAnswerData(link)
        extractQuestionData(link)
        
    

main()