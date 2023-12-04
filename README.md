# Memorizing Vocabulary Using Forgetting Curve

## About

Memorizing words could be exasperating for those who wanted to prepare for tests. But it don't have to be. According to Ebbinghaus's
forgetting curve, we can memorize things better by manipulating the time interval of active recall: the more recently memorized words
should be reviewed more often. This program allows you to save words on a specific date and can presents the ones you need to review
on any date. Combining with web crawling, the definition and the word could be presented with both orders (The Cambridge Dictionary
web crawling part is modified from [mimiliaogo's cambridge-dictionary-crawler repo](https://github.com/mimiliaogo/cambridge-dictionary-crawler.git)). Example sentences 
could also be presented.

## Requirement

### Language

Python 3.x?

### Packages

`csv`
`datetime`
`os`
`random`

`configparser`
`requests`
`lxml`

`fake_useragent`

# Setup

1. Please make sure the config.ini and main.py are in the same directory.
2. Create a csv file, copy its absolute file path, and modify the file path in config.ini. For example: the_file = W:/Me/Vocabulary/vocab.csv
3. You can also change the number of appearances (in the course if the following days) of a word by changing the value of "appearances" in config.ini. Default setting allows you to see the words 6 times (days) including the day you add them.
4. All set! Run the file and follow the instructions.
