# Memorizing Vocabulary Using Forgetting Curve

## About

Memorizing words could be exasperating for those who wanted to prepare for tests. But it doesn't have to be. According to Ebbinghaus's
forgetting curve, we can memorize things better by manipulating the time interval of active recall: the more recently memorized words
should be reviewed more often. This program allows you to save words on a specific date and can present the ones you need to review
on any date. 

For example, if a word is entered on the date 1/1, it will be shown in the word list 1 day after at 1/2, 2 days after at 1/3, 4 days after at 1/5, 7 days after at 1/8, etc.

Combining with web crawling, when the words are being reviewed, the definition and the word could be presented in both orders (The Cambridge Dictionary
web crawling part is modified from [mimiliaogo's cambridge-dictionary-crawler repo](https://github.com/mimiliaogo/cambridge-dictionary-crawler.git)). Example sentences 
could also be presented.

## Python Version

Python 3

## Requirements

﻿configparser==5.3.0
requests==2.28.1
lxml==4.9.2
fake-useragent==1.1.1

## Setup

1. Please make sure the config.ini and main.py are in the same directory.
2. Create a CSV file for storing the vocabularies. Copy its absolute file path, and paste it to the the_file variable in config.ini. For example: `the_file = W:/Me/Vocabulary/vocab.csv`
3. You can also change the number of appearances (in the following days) of a word by changing the value of "appearances" in config.ini. The default setting allows you to see the words 6 times (days) including the day you add them.
4. All set! Run the file and follow the instructions.

## Step by Step Guide

Before anything, please make sure you have installed all the required packages, and check for internet connection.

### Add words

1. Run the main.py file.

![image](/images/runMain.png)

2. Enter "a" for adding words.

![image](/images/enterAtoAdd.png)

3. Enter the date to add words. Pay attention to the format.

![image](/images/enterDateA.png)

4. Enter the words you want to add. The words should be separated by commas.

![image](/images/enterWords.png)

5. Done! The words are added to the CSV file.

6. (Optional) Add more words in the next day.

![image](/images/enterWords2.png)

### Review words

1. Run the main.py file. Or enter "r" if you are already in the main menu. Enter the date to review words.

![image](/images/enterRdateToReview.png)

3. Choose the reviewing option you want. You can choose the order of definition and words.

![image](/images/reviewOptions.png)

3. Start reviewing! Example sentences can be shown if you choose to. Note that the words in 6/13 and 6/14 are shown in the review date 6/15. Amazing isn't it?

![image](/images/reviewingWords.png)