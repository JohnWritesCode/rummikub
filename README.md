# rummikub
A set of tools for winning at the game of rummikub

This a tool to find the legal rummikub play that uses the most tiles


The convenient to use functions are defined within search.py 
searchPrimitives.py has the somewhat hairier recursive tools. 

The command line tool is rummikub.py, to get a sense of how it works run
python rummikub.py samples/sampleTable1.txt samples/sampleRack1.txt 


The biggest shortcoming currently is that it does not handle wild cards. 
A nice UI would also be a good step. In addition it will completely 
reshuffle the table on every turn. Other human players would find this
annoying, so it would be nice to find the solutoin that also minimizes
table churn. 
