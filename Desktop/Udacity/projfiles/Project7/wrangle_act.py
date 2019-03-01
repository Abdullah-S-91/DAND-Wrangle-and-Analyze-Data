#!/usr/bin/env python
# coding: utf-8

# ## Gathering Data
# 

# In[1]:


# Packages

import tweepy
import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Gather data from csv file 


archive = pd.read_csv('twitter-archive-enhanced.csv')

archive.head()


# In[3]:


# Download file from URL

URL= 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'

with open('image.tsv' , 'wb') as f:
    image_f = requests.get(URL)
    f.write(image_f.content)

image = pd.read_csv('image.tsv', sep='\t')

image.head()


# In[4]:


# Gather and store data from twitter API 

consumer_key = '******'
consumer_secret = '**********'
access_token = '382817036-********'
access_secret = '*******'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit= True, wait_on_rate_limit_notify= True)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#        print(tweet.text)
#tweet = api.get_status(id_of_tweet)
#print(tweet.text)


# In[5]:



#tweets= []
#deleted_tweets= []

#with open ('tweet_json.txt', 'w') as file:
#    for tweet_id in archive['tweet_id']:
#        try:
#            tweets.append(api.get_status(tweet_id, tweet_mode = 'extended')._json)
#        except Exception as e:
#            deleted_tweets.append(tweet_id)
#    file.write(json.dumps(tweets))

    
# Creating CSV file which have tweets thats not in api

#deleted_tweets = pd.DataFrame(deleted_tweets)
#deleted_tweets.to_csv('deleted_tweets.csv', sep = ',')


# In[6]:


#with open('tweet_json.txt') as jf:
#    tweets_info = pd.DataFrame(columns = ['tweet_id', 
#                                        'favorites', 
#                                        'retweets'])
#    for line in jf:
#        tweet = json.loads(line)
#        tweets_info = tweets_info.append({
#            'tweet_id': tweet['id'],
#            'favorites': tweet['favorite_count'],
#            'retweets': tweet['retweet_count']
#        }, ignore_index=True)
#
#tweets_info


# Read Json file 

with open('tweet_json.txt','r') as json_file:
    tweets = json.loads(json_file.read())
    
json_tweets = pd.DataFrame(tweets)


# In[ ]:





# In[ ]:





# ## Assess
# 
# In this section I will explore the data to improve evaluation of the data.

# In[7]:


archive.head()


# In[8]:


archive.info()


# In[9]:


archive.describe()


# In[10]:


image.head()


# In[11]:


image.info()


# In[12]:


image.describe()


# In[13]:


json_tweets.head()
#pd.set_option('display.max_colwidth', -1)


# In[14]:


json_tweets.info()


# In[15]:


json_tweets.describe()


# In[16]:


archive['name'].value_counts()


# In[17]:


image['jpg_url'].value_counts()
#image[image['jpg_url'] == 'https://pbs.twimg.com/media/CYLDikFWEAAIy1y.jpg']
#test= archive.query('tweet_id == "761750502866649088"')
#test


# In[18]:


archive.tweet_id.duplicated().sum()


# In[19]:


image.tweet_id.duplicated().sum()


# In[20]:


json_tweets.id.duplicated().sum()


# In[21]:


#archive.text.value_counts()
tweet_text= archive[archive.text.str.contains('&amp;')]
tweet_text.text.value_counts()

#source for this point is here:https://github.com/kdow/WeRateDogs

#twitter_archive_clean['text'] = twitter_archive_clean['text'].str.replace('&amp;', '&')


# ### Quality 
# 
# 
# 
# 
# 1- Missing values from images dataset which are 2075 rows and the archive are 2356.
# 
# 2- Retweets need to be removed
# 
# 3- Timestamp should be datetime instead of object (string)
# 
# 4- There are same jpg_url for more than one tweet_ids
# 
# 5- Incorrect dog names, The most popular name is 'a' which is not corrected name.
# 
# 6- Drop some columns which is not usefull for analysis.
# 
# 7- Some columns need to rename it to understandable name.
# 
# 8- Nulls represented as 'None' in columns 'name', 'doggo', 'floofer', 'pupper','puppo'.
# 
# 9- Some tweets have additional characters in the text which is not meaningful. 
# 
# 10- The numerator and denominator columns have invalid values "this is mentioned in Project Motivation but I cannot clean it because it will take time and I need to submit this project as soon as possible"
# 
# 
# 
# ### Tidiness
# 
# 1- Dog stage variable in different columns: doggo, floofer, pupper, puppo
# 
# 2- Marge 'json_tweets' and 'image' to 'archive' dataset
# 
# 
# 

# ## Cleaning 
# 
# 

# In[22]:


# make copies of datasets 

archive_clean = archive.copy()
image_clean = image.copy()
json_tweets_clean = json_tweets.copy()

#json_tweets_clean.head(2)


# Issue:
# 
#     Some of tweets haven same jpg_url images 
# Define:
# 
#     Delete the duplicated jpg_url images

# In[23]:


#image_clean['jpg_url'].value_counts()


image_clean['jpg_url'] = image_clean['jpg_url'].drop_duplicates()

image_clean = image_clean[pd.notnull(image_clean['jpg_url'])]


# In[24]:


# test

image_clean.info()


# Issue:
# 
#     Some of these tweets haven't images, we want only the tweets with image 
# 
# Define:
# 
#     Delete the tweets which is haven't image from the dataset
#     

# In[25]:


# Delete tweets without Image 


#test= archive_clean.query('tweet_id == "685325112850124800"')
#test

image_id=image_clean[['tweet_id']]

#image_id

archive_clean=pd.merge(archive_clean,image_id,on='tweet_id')



# In[26]:


# For test 

archive_clean.info()
#archive.info()


# Issue:
# 
#     we want only the origen tweets not retweets 
# Define:
# 
#     Delete  retweets from the dataset
#     

# In[27]:


#Delete retweets 

archive_clean = archive_clean[pd.isnull(archive_clean['retweeted_status_id'])]


# In[28]:


# test

archive_clean.info()


# Issue:
# 
#     Datatype of timestamp
# Define:
# 
#     Convert timestamp to datetime data type.

# In[29]:


#Convert timestamp

archive_clean['timestamp'] =pd.to_datetime(archive_clean['timestamp'])


# In[30]:


# For test

archive_clean.info()


# Issue:
# 
#     Some columns not usefull in our datasets.
# Define:
# 
#     Delete these columns which is not usefull for analysis.
# 

# In[31]:


# Delete some columns 

#json_tweets_clean.info()
json_tweets_clean = json_tweets_clean.drop(json_tweets_clean.columns[[0, 1,2, 3,4,5,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,29,30,31]], axis=1)


# In[32]:


# For test 

json_tweets_clean.info()


# Issue:
# 
#     Some columns have difficult understandable name.
# Define:
# 
#     rename the columns to understandable name.
# 
# 

# In[33]:


# rename the columns 

json_tweets_clean.rename(columns={'favorite_count': 'favorite', 'id': 'tweet_id', 'retweet_count': 'retweet'}, inplace=True)

image_clean.rename(columns={'p1': 'prediction', 'p1_conf': 'confidence', 'p1_dog': 'Dog?',
                            'p2': 'prediction2', 'p2_conf': 'confidence2', 'p2_dog': 'p2_Dog?',
                            'p3': 'prediction3', 'p3_conf': 'confidence3', 'p3_dog': 'p3_Dog?'}, inplace=True)


# In[34]:


list(image_clean)
list(json_tweets_clean)


# In[35]:


# Delete some columns 

#archive_clean.info()
archive_clean = archive_clean.drop(archive_clean.columns[[6,7,8]], axis=1)


# In[36]:


# For test

archive_clean.info()


# Define:
# 
#        Marge the cleaned datasets together

# In[37]:


tweet_master = pd.merge(archive_clean, image_clean, how = 'left', on = ['tweet_id'] )

tweets_master = pd.merge(tweet_master, json_tweets_clean, how = 'left', on = ['tweet_id'])

#tweets_master.info()

tweets_master.to_csv('tweets_master.csv')


# In[38]:


#test

tweets_master.info()


# Define:
# 
#        Melt columnes ['doggo', 'floofer', 'pupper', 'puppo'] under stage column.

# In[39]:


idv = [x for x in list(tweets_master.columns) if x not in ['doggo', 'floofer', 'pupper', 'puppo']]

tweets_master = pd.melt(tweets_master, id_vars = idv , value_vars = ['doggo', 'floofer', 'pupper', 'puppo'],
                        var_name='stages', value_name = 'stage')

tweets_master = tweets_master.drop('stages', 1)

tweets_master = tweets_master.sort_values('stage').drop_duplicates('tweet_id', keep = 'last')




# In[40]:


# for test

#tweets_master.info()

tweets_master.stage.value_counts()


# In[41]:


tweets_master.info()
tweets_master.head(2)


# 
# Issue:
# 
#     Some dogs have incorrect name.
# Define:
# 
#     replace incorrect name to Nan.
# 
# 
# 

# In[42]:


#Replace incorrect name to Nan.

#tweets_master['name'].value_counts()

tweets_master['name']= tweets_master['name'].replace(['a', 'an', 'the'], np.nan)


# In[43]:


#test 

#tweets_master['name'].value_counts()

testname= tweets_master.query('name == "a"')
testname


# Issue:
# 
#        Nulls represented as 'None'.
#        
# Define:
# 
#        replace None to Nan in the datasets.
#  

# In[44]:


# replace None 

tweets_master['name']= tweets_master['name'].replace(['None'], np.nan)
tweets_master['stage']= tweets_master['stage'].replace(['None'], np.nan)


# In[45]:


# test
#tweets_master['name'].value_counts()


#t1 = tweets_master.query('name == "None"')
#t2 = tweets_master.query('stage == "None"')
tweets_master.stage.value_counts()


#print (t1, t2)


# Issue:
# 
#        Additional characters in tweet text .
# Define:
# 
#        Remove the Additional characters in tweet text.

# In[46]:



tweets_master['text'] = tweets_master['text'].str.replace('&amp;', '&')


# In[47]:


#FOr test 


tweet_text= tweets_master[tweets_master.text.str.contains('&amp;')]
tweet_text.text.value_counts()


# Define:
# 
#        Reorder the columns and drop the additional columns to make the dataset easy to read.

# In[48]:


#Reorder the columns

#list(tweets_master.columns.values)


tweets_master = tweets_master[['tweet_id','text','retweet','favorite','name','stage','rating_numerator','rating_denominator',
                               'timestamp','prediction','confidence','Dog?','jpg_url','source','in_reply_to_status_id','in_reply_to_user_id','expanded_urls',
                               'img_num','prediction2','confidence2','p2_Dog?','prediction3','confidence3','p3_Dog?']]


# In[49]:


#drop the additional columns


tweets_master = tweets_master.drop(tweets_master.columns[[14,15,17,18,19,20,21,22,23]], axis=1)


# In[50]:


#for test

tweets_master.tail(2)


# ### Storing
# 
# Storing cleaned master dataset:
# 

# In[51]:


#Storing


tweets_master.to_csv('twitter_archive_master.csv')


# ### Analyzing and Visualizing Data

# In[52]:


# make copy for analyzing

tweets_data= pd.read_csv('twitter_archive_master.csv')

tweets_data.info()


# ### Famous and lovely Dogs at WeRateDogs
# 
# * Let's see who are the famous dogs in WeRateDogs which have a top retweet.
# 
# * Also we will see who are the lovely dogs that the pepole like it by display dogs favorite.
# 
# 
# #### Top 10 of Famous Dogs:
# 

# In[59]:


#top_dog_retweets= tweets_data.groupby('prediction')["retweet"].sum().sort_values(ascending=False)

#top_dog_retweets.head()

top_dog_retweets = tweets_data.sort_values(by='retweet',ascending =False ).head(10)

top_dog_retweets[['name','stage','retweet','text','jpg_url']]
#pd.reset_option('display.max_rows')

#pd.set_option('display.max_colwidth', -1)


# In[55]:


from PIL import Image
import requests
from io import BytesIO


response = requests.get('https://pbs.twimg.com/ext_tw_video_thumb/744234667679821824/pu/img/1GaWmtJtdqzZV7jy.jpg')
img = Image.open(BytesIO(response.content))

img


#sources "https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python"


# **Hi there, I am the top one Famous Dog in WeRateDogs, I have more than 83K retweet, my stage is doggo, I will not tall you my name right now**
# 

# #### Top 10 of Lovely Dogs:

# In[62]:


top_dog_favorite = tweets_data.sort_values(by='favorite',ascending =False ).head(10)

top_dog_favorite[['name','stage','retweet','favorite','text','jpg_url']]


# **As we see from the list above, The top one retweet dog have top favorite also, that's mean there is correlation between retweets and favorites.**
# 
# 
# #### The relationship between the variables

# In[67]:


#Correlation map
f,ax = plt.subplots(figsize=(14, 14))
sns.heatmap(tweets_data.corr(), annot=True, linewidths=1, fmt= '.1f',ax=ax)
plt.title('Correlation')
plt.show();


# **From the correlation map there is a strong correlation between favorites and retweets.** 

# ### Top dog breeds in the tweets based on prediction data:

# In[79]:


#Top dog breeds in the tweets based on prediction data 

top_dog_breeds= tweets_data['prediction'].value_counts().head(20)

top_dog_breeds.plot(kind='bar', title='Top 20 dog breeds')
plt.show();


# **The top one on Dog breeds is golden_retriever then Labrador_retriever**

# ### Popular stage on the tweets 
# 

# In[81]:


#Popular stage 

dog_stage= tweets_data['stage'].value_counts()

dog_stage.plot(kind='pie', title='Popular stage')
plt.show();


# **Pupper represent the big number of the pie**

# In[82]:


from subprocess import call
call(['python','-m','nbconvert','wrangle_act.ipynb'])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




