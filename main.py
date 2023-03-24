import csv
from datetime import date
import os
import random

import configparser
import requests
from lxml import etree

from fake_useragent import UserAgent

def configInfo():
    '''Reads the configuration file "config.ini" to get the file path of the csv file that stores the vocabulary
    and the number of appearances of a word presented. Return in a tuple with these two values'''
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini')) #reads the configuration file
    return (config.get('FILES', 'the_file'),int(config.get('APPEARANCES', 'appearances'))) #return the two vales

def theDate(datePrompt, sep = " "):
    '''Used for acquiring a date from the user. Different prompt could be presented by modifying the argument
    "datePrompt", which must be a string. If there is no input, return the date of today. The default input format
      is "yyyy mm dd". Different separator may be specified by the argument sep.'''
    try: #return a date object if the input format is correct
        return (lambda x: date(*map(int, x.split(sep))) if x != "" else date.today())(input(datePrompt))
    except (TypeError, ValueError): #if format not correct, the user will be asked again
        print("The date format is not correct!\n")
        return theDate(datePrompt, sep)

def inputWords(inputWordsPrompt, sep = ","):
    '''Used to acquire the words that the user wants to store, and return a list with the words. The prompt and
    the separator can be modified.'''
    return [word.strip() for word in input(inputWordsPrompt).lower().split(sep)]

def inputDateAndWords(inputDate, inputWordList):
    '''Return the full list of a date and the words.'''
    return [inputDate] + inputWordList

def writeWords(dateWordsList, filePath):
    '''Writes the list with date and words to the csv file.'''
    with open(filePath, 'a', newline = '') as file:
        csv.writer(file).writerow(dateWordsList)

def file2Dict(filePath):
    '''Read the csv file into a dictionary with keys being the dates and values being the vocabulary.
    The file path should be given, and if the row is empty, it will be ignored.'''
    fileDict = {}
    [fileDict.setdefault(row[0], []).extend(row[1:]) for row in csv.reader(open(filePath, 'r')) if row]
    return fileDict

def lazyCaterer(appearances):
    '''Creating the lazy caterer sequence dictionary. The key is the show up count of the list, 
    and the value is the number of days of each appearances. The appearances is the number of 
    times a word would show up including the day that the word is being stored.'''
    forget = {-1:0, 0:1}
    for i in range(1, appearances): 
        forget[i] = i + forget[i-1]
    return forget

def datesToReview(appearances, reviewDate, filePath):
    '''Finds the dates that should be reviewed based on the date entered and the lazy caterer sequence, 
    and return them with a list.'''
    lazy = lazyCaterer(appearances)
    reviewDates = list(filter(lambda x: (reviewDate - date(*map(int, x.split("-")))).days in lazy.values(), list(file2Dict(filePath).keys())))
    return reviewDates

def listOfToday(appearances, reviewDate, filePath):
    '''Return the complete list of words to review! The sequence of the words were shuffled.'''
    todayList = [word for Date in datesToReview(appearances, reviewDate, filePath) for word in file2Dict(filePath)[Date]]
    random.shuffle(todayList)
    return todayList

def fakeUserAgent():
    '''Generate a fake user agent to pass the authenication process of the website.'''
    return UserAgent().random

def getDefinitions(word):
    '''This function indexes the definitions and example sentences of a given word on Cambridge Dictionary. They will be returned
     in the form of [(def1,sent1),(def2,sent2),(def3,sent3)]'''
    try: #using the fake user agent to request the website of Cambridge Dictionary
        url = f'https://dictionary.cambridge.org/dictionary/english-chinese-traditional/{word}'
        headers = {'user-agent': fakeUserAgent()}
        response = requests.get(url, headers = headers)
        html = response.text
        page = etree.HTML(html)
    except requests.exceptions.RequestException: #if request failed, return the following
        return [("No results found due to connection or request error!")*2]
    
    definitions = [] #if the request is successful, we need a list to contain the definitions and sentences
    ordinal = 1 #looping for all the definition and setences elements on the webpage
    
    while True:
        try:
            # english definition
            engDefXpath = f'//*[@id="page-content"]/div[2]/div[4]/div/div/div[{ordinal}]/div[3]/div/div[2]/div[1]/div[2]/div'
            engDefElements = page.xpath(engDefXpath)
            engDef = engDefElements[0].xpath('string(.)').strip()
            
            # english sentence
            engSentXpath = f'//*[@id="page-content"]/div[2]/div[4]/div/div/div[{ordinal}]/div[3]/div/div[2]/div[1]/div[3]/div[1]/span[1]'
            engSentElements = page.xpath(engSentXpath)
            if engSentElements: #Many words don't have example sentence.
                engSent = engSentElements[0].xpath('string(.)').strip()
            else:
                engSent = "No example sentence available!"
            definitions.append((engDef, engSent))
            ordinal += 2 #Use to find the next element with different definitions
        except IndexError: 
            if not definitions: #If no definition found
                definitions.append(("No definition found!", "No example sentence available!"))
            break #if there are no more definitions to be scooped
    return definitions

def wordFirst(word, dic, _):
    '''If the user wants to view the word first, each time a definition pop up, they can choose whether to 
    view the definition by entering "s".'''
    print(word)
    for number,defSentPairs in enumerate(dic):
        input()
        print(f"def{number+1}: {defSentPairs[0]}")
        if input(">").lower() == "s": 
            print(f"sent{number+1}: {defSentPairs[1]}")

def defFirst(word, dic, numOfDef):
    '''If the user wants to view the definition first, when the word is presented, they can choose view the specific 
    definition by entering "s1", "s2", or view all the example sentences by entering "s".'''
    for number, (definition,_) in enumerate(dic): 
        print(f"def{number+1}: {definition}")
    input()
    print(word)
    def showSent(dic, numOfDef):
        '''The function managed the part of showing sentences.'''
        while True:
            sentCmd = input(">").lower()
            if sentCmd == "s": #the loop will end if the user choose to view all sentences 
                for number, (_, sentence) in enumerate(dic):
                    print(f"sent{number+1}: {sentence}")
                    input()
                    return 
            elif sentCmd.startswith("s") and sentCmd[1:].isdigit(): #the loop will not end if they view the specific sentences
                sentNum = int(sentCmd[1:])
                if 1 <= sentNum <= numOfDef: #the number after "s" must be in the range of the existing definitions
                    print(f"sent{sentNum}: {dic[sentNum-1][1]}")
                else:
                    print(f"Invalid input: there are only {numOfDef} sentences.")
            else: #the loop will end if entered nonsense
                return
    showSent(dic, numOfDef)

def displayWordList(appearances, reviewDate, filePath):
    '''This function will be called if the user wants to review the words. There are three choices: 
    viewing the word first, viewing the definition first, or in random order. '''
    #get the response of the user
    order = input("Do you want to see the word or the definition first?\nEnter 'w' for word first, 'd' for definition first, or any other key for random order.\n").lower()
    #two kinds of prompt for differnt scenarios
    wordFirstPrompt = "If you see '>', you can view the example sentence with corresponding definition by entering 's'.\n"
    defFirstPrompt = "If you see '>', you can view all the example sentences by entering 's', or you can view specific example sentence with corresponding definition by entering 's1','s2',etc.\n"
    if order == "w": 
        input(wordFirstPrompt)
    elif order == "d":
        input(defFirstPrompt)
    else:
        input(f"When the word presents prior to definitions:\n{wordFirstPrompt}\nWhen the definitions comes before the word:\n{defFirstPrompt}")
    for word in listOfToday(appearances,reviewDate,filePath): #displaying the words with separation lines between each word
        input("-" * 50)
        dic = getDefinitions(word)
        numOfDef = len(dic)
        if order == "w": 
            wordFirst(word, dic, numOfDef)
        elif order == "d": 
            defFirst(word, dic, numOfDef)
        else: 
            random.choice((wordFirst, defFirst))(word, dic, numOfDef)
    input("-" * 50)

def main():
    '''The function that put all the things together and underlying the two main functionalities: 
    adding words and reviewing.'''
    filePath, appearances = configInfo()
    continueLoop = True
    while continueLoop: #The user can choose to add words or to review. If neither, they will be asked whether they wants to continue.
        action = input("Do you want do add new vocabulary or review?\nEnter 'a' for adding new words, or enter 'r' to review.\n").lower()
        if action == "a": 
            writeWords(inputDateAndWords(theDate("Which date do you want to add words to?\nEnter 'yyyy mm dd' for a date or any other response for today.\n"),inputWords("Enter the words.\nUse ',' to separate them.\n")),filePath)
        elif action == "r": 
            displayWordList(appearances,theDate("Which date's word list do you want to review?\nEnter 'yyyy mm dd' for a date or any other response for today.\n"),filePath)
        askString = "Do you want to continue?\nEnter 'y' for continuing or enter 'n' to end.\n"
        ask = lambda x: True if x == "y" else False if x == "n" else ask(input(askString).lower())
        continueLoop = ask(input(askString).lower())
    input("Good work, bye!!\n")

if __name__ == '__main__':
    main()