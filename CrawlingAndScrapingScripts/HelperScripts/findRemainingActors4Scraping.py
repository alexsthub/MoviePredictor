#!/usr/bin/env python
# coding: utf-8



# In[14]:


import pandas

the3000WorkingWith = pandas.read_csv("./unique_actors.csv")
originalScrapePart1 = pandas.read_csv("./actorsINFO_1.csv")

remaining = []


# In[15]:


# print((originalScrapePart1.columns[0]))

# actors we already scraped:
actorsWehave = originalScrapePart1['actorName'].tolist()
# actorsWehave[1]

# actors we want to work with, for the "statistical analysis" trial:
targetedActors = the3000WorkingWith['actors'].tolist()

# saved arrays for actors we need to scrape and actors we have scraped. 
actsNeedToScrape = []
actsNotNeededToScrape = []

# for each actor we already scraped, add to new list (actorsRemaining)
for actor in targetedActors:        
    if actor not in actorsWehave:
        actsNeedToScrape.append(actor)
    else:
        actsNotNeededToScrape.append(actor)
        

  

print(len(actsNeedToScrape))
print(len(actsNotNeededToScrape)
      



actsNeedToScrape = pandas.DataFrame(actsNeedToScrape)
actsNeedToScrape.to_csv('./uniqueActorsLeft2.csv')
      
actsNeedToScrape.to_csv('./uniqueActorsLeft2.csv')


# In[ ]:





# In[ ]:




