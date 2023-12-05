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


