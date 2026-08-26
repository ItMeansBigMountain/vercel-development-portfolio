
# PER USER - most interacted (likes ,RT, comments) tweets sorted for that day.
    # MOST LIKES
    # MOST RETWEETS
    # MOST COMMENTS
    # MOST INTERACTION (ALL)

# TOP INTERACTION USING KEYWORD - look up top interacted tweets sorted using keyword/phrase
    # MOST INTERACTED (likes ,RT, comments)
    # MOST POPULAR (twitters terms)



# HASHTAGS
# https://displaypurposes.com/hashtags/hashtag/elonmusk

import pprint


# TWITTER
import tweepy 
import datetime
import pytz
import random
utc=pytz.UTC

# TEXT TO SPEECH
from  gtts import gTTS


# IMAGE GENERATION
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import urllib.request
from textwrap import wrap
import warnings
warnings.filterwarnings("ignore")



# VIDEO OVERLAY EDITS
import os
from moviepy.editor import AudioFileClip, VideoFileClip ,  ImageClip , concatenate_videoclips


# DELETE TEMP MEDIA DIRS
import shutil





# GLOBAL VARIABLES
consumer_key = os.getenv("TWITTER_CONSUMER_KEY", "")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", "")
access_key = os.getenv("TWITTER_ACCESS_KEY", "")
access_secret = os.getenv("TWITTER_ACCESS_SECRET", "")


def require_twitter_credentials():
    missing = [
        name for name, value in {
            "TWITTER_CONSUMER_KEY": consumer_key,
            "TWITTER_CONSUMER_SECRET": consumer_secret,
            "TWITTER_ACCESS_KEY": access_key,
            "TWITTER_ACCESS_SECRET": access_secret,
        }.items() if not value
    ]
    if missing:
        raise RuntimeError("Missing Twitter/X credentials in environment: " + ", ".join(missing))


# TWITTER EXTRACT TWEETS
def get_all_tweets(screen_name):
    # AUTH tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # INIT populate alltweets with first set
    alltweets = []	
    new_tweets = api.user_timeline(screen_name = screen_name,count=200 ,  include_rts = False , tweet_mode='extended' )
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    # APPEND sets of historical data
    while len(new_tweets) > 0:
        # ITERATIVE PUSH
        print ("getting tweets before tweet.id: %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest ,  include_rts = False , tweet_mode='extended')
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    
    # outtweets = [tweet_text.text for tweet_text in alltweets]
    return alltweets
def get_lastWeek_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    startDate =  utc.localize(datetime.datetime.now() - datetime.timedelta(days=7))
    endDate =    utc.localize(datetime.datetime.now())
    tweets = []
    tmpTweets = api.user_timeline(screen_name=screen_name , include_rts=False , tweet_mode='extended' )
    for tweet in tmpTweets:
        if (tweet.retweeted) and ('RT @' in tweet.text): continue
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)
    return tweets

def topLikes(array):
    if len(array) < 2:
        return array
    low, same, high = [], [], []
    pivot = array[random.randint(0, len(array) - 1)].favorite_count
    for item in array:
        if item.favorite_count < pivot:
            low.append(item)
        elif item.favorite_count == pivot:
            same.append(item)
        elif item.favorite_count > pivot:
            high.append(item)
    return topLikes(low) + same + topLikes(high)
def topReTweets(array):
    if len(array) < 2:
        return array
    low, same, high = [], [], []
    pivot = array[random.randint(0, len(array) - 1)].retweet_count
    for item in array:
        if item.retweet_count < pivot:
            low.append(item)
        elif item.retweet_count == pivot:
            same.append(item)
        elif item.retweet_count > pivot:
            high.append(item)

    return topReTweets(low) + same + topReTweets(high)
def topInteractions(array):
    if len(array) < 2:
        return array
    low, same, high = [], [], []
    pivot = array[random.randint(0, len(array) - 1)].retweet_count + array[random.randint(0, len(array) - 1)].favorite_count
    for item in array:
        interactions = item.retweet_count + item.favorite_count
        if interactions < pivot:
            low.append(item)
        elif interactions == pivot:
            same.append(item)
        elif interactions > pivot:
            high.append(item)
    return topInteractions(low) + same + topInteractions(high)

def topical_popularity(topic):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    tweets = api.search_tweets(q=f'"{topic}"', result_type='popular' , include_entities = True  , tweet_mode='extended' )
    return tweets


# TEXT TO SPEECH
def text_speech(MYTEXT , file_name):
    MYTEXT =  MYTEXT.replace( "@" , " "  )
    language = 'en'
    say = gTTS(text = MYTEXT, lang = language , slow=False)
    say.save("%s.mp3" % os.path.join("tweet_media",file_name))


# IMAGE EDITOR
def generate_image(screen_name , tweet , photo=False, video=False, gif=False, counter=0):
    tweet_text = tweet.full_text.split("http")[0]

    # Set the font to be used
    FONT_USER_INFO = ImageFont.truetype("arial.ttf", 90, encoding="utf-8")
    FONT_TEXT = ImageFont.truetype("arial.ttf", 110, encoding="utf-8")
    # Image dimensions (pixels)
    WIDTH = 2376
    HEIGHT = 2024
    # Color scheme
    COLOR_BG = "white"
    COLOR_NAME = 'black'
    COLOR_TAG = (64, 64, 64)
    COLOR_TEXT = 'black'
    # Write coordinates
    COORD_PHOTO = (250, 170)
    COORD_NAME = (600, 185)
    COORD_TAG = (600, 305)
    COORD_TEXT = (250, 510)
    # Extra space to add in between lines of text
    LINE_MARGIN = 15


    # TWEET DETAILS
    user_name = tweet.user.name
    user_tag = screen_name
    text = tweet_text
    img_name = f"{screen_name}_{counter}"

    # DIMENTION DETAIL
    text_string_lines = wrap(text, 37)
    x = COORD_TEXT[0]
    y = COORD_TEXT[1]

    temp_img = Image.new('RGB', (0, 0))
    temp_img_draw_interf = ImageDraw.Draw(temp_img)

    line_height = [
        temp_img_draw_interf.textsize(text_string_lines[i], font=FONT_TEXT)[1]
        for i in range(len(text_string_lines))
    ]


    # IMAGE CREATION
    img = Image.new('RGB', (WIDTH, HEIGHT), color=  ( 200, 200, 200)  )
    draw_interf = ImageDraw.Draw(img)

    # DRAW USER DETAIL TEXT
    with Pilmoji(img) as pilmoji:
        pilmoji.text(COORD_NAME, user_name, font=FONT_USER_INFO, fill=COLOR_NAME)
        pilmoji.text(COORD_TAG, user_tag, font=FONT_USER_INFO, fill=COLOR_TAG)

    # DRAW TWEET TEXT
    for index, line in enumerate(text_string_lines):
        with Pilmoji(img) as pilmoji:
            pilmoji.text(  (x, y), line , font=FONT_TEXT, fill=COLOR_TEXT  )
        y += line_height[index] + LINE_MARGIN
    
    # DRAW LIKES AND RETWEETS
    interaction_stats = f"{tweet.retweet_count} RTs {tweet.favorite_count} Likes"
    with Pilmoji(img) as pilmoji:
        y += line_height[index] + (LINE_MARGIN * 2)
        pilmoji.text(  (x, y), interaction_stats , font=FONT_TEXT, fill=COLOR_TEXT  )


    # PROFILE PIC
    urllib.request.urlretrieve(tweet.user.profile_image_url , "tweet_media\\profilePic.png")
    user_photo = Image.open(  "tweet_media\\profilePic.png" , "r" ).convert("RGBA").resize((250,250))
    img.paste(user_photo, COORD_PHOTO, mask=user_photo)


    if photo:
        urllib.request.urlretrieve(  tweet.entities["media"][0]["media_url"]  , "tweet_media\\temp_media.png")
        media_photo = Image.open(  "tweet_media\\temp_media.png" , "r" ).convert("RGBA") 
        img.paste(media_photo, (x,y)  , mask=media_photo)
        print( img_name + " : photo" )

    elif video:
        print( tweet.entities['media'][0]['media_url'] ,  "video" )
    elif gif:
        print( tweet.entities['media'][0]['media_url'] ,  "gif" )

    # IMAGE OUTPUT
    # img.save(f'{img_name}.png')
    img.save("%s.png" % os.path.join("tweet_media",img_name))


# VIDEO GENERATION
def mp3PNGMerge(fileSaveName , audio_path , image_path):
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 1
    video_clip.write_videofile(  "clips\\" +   fileSaveName + '_CLIP.mp4')

def concat_videos(path):
    L = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)
    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile("output.mp4", fps=30, remove_temp=True)







def main():

    require_twitter_credentials()

    # INIT MP3 & PNG FOLDER
    if not os.path.exists('tweet_media'):
        os.makedirs('tweet_media')

    # INIT CLIP OUTPUT FOLDER
    if not os.path.exists('clips'):
        os.makedirs('clips')


    # USER MOST POPULAR TWEETS 
    screen_name = input('Type in Twitter handle you would like it look up: ')

    # TIME FRAME
    # User_Tweets = get_all_tweets(screen_name)
    User_Tweets = get_lastWeek_tweets(screen_name)


    # TWEET OUTPUTS
    # output = topReTweets(  User_Tweets )
    # output = topLikes(  User_Tweets )
    output = topInteractions(  User_Tweets )


    # IMAGE GENERATION
    for x in range(0,len(output),1):
        # TWEETS WITH NO TEXT
        if len(output[x].full_text.split("http")[0])<1: continue

        # CHECK FOR MEDIA IN TWEET
        if 'media' in output[x].entities:
            if "photo" in output[x].entities["media"][0]['type']:
                generate_image(screen_name=screen_name, tweet=output[x] , photo=True, counter = x)
            elif "video" in output[x].entities["media"][0]['type']:
                generate_image(screen_name=screen_name, tweet =output[x] , video=True, counter = x)
            elif "animated_gif" in output[x].entities["media"][0]['type'] :
                generate_image(screen_name=screen_name, tweet=output[x] , gif=True , counter = x)
        else:
            # PLAIN TEXT TWEET
            generate_image(screen_name=screen_name, tweet = output[x] , counter = x)

        # TEXT TO SPEECH
        text_speech( output[x].full_text.split("http")[0] , f"{screen_name}_{x}"  )



    # SORT FILES INTO CLIP DICTIONARY
    arr = os.listdir('tweet_media')
    clip_map = {}
    for x in range(0 , len(arr) , 1):
        if arr[x] == "profilePic.png" or arr[x] == "temp_media.png" : continue
        
        file_index_and_type = arr[x].split("_")[1].split(".")
        index = int(file_index_and_type[0])
        file_type = file_index_and_type[1]

        if index not in clip_map:
            clip_map[index] = [arr[x]]
        else:
            clip_map[index].append(arr[x])


    # VIDEO GENERATION
    for key in clip_map:
        mp3PNGMerge(  str(key) , 'tweet_media\\'+clip_map[key][0] , 'tweet_media\\'+clip_map[key][1]  )




    # CONCAT ALL CLIPS
    concat_videos("clips")





    # CLEANUP
    dir_paths = ('clips' , 'tweet_media')
    for path in dir_paths:
        shutil.rmtree(path)




    # PROGRAMMATICALLY UPLOAD YOUTUBE VIDEO
    if os.path.exists("output.mp4"):
        import subprocess, sys
        subprocess.check_call([
            sys.executable,
            "upload_output_to_youtube.py",
            "output.mp4",
            "--title",
            f"Top Tweets from @{screen_name}",
            "--description",
            f"Private tweet video generated from @{screen_name}. Review before making public.",
            "--tags",
            "tweets,automation,social media",
            "--privacy",
            "private",
        ])






    # TOPICAL POPULARITY [DEBUG]
    # topic = input('Type in Twitter topic you would like it look up: ')
    # output = topical_popularity( topic  )
    # text_speech( output[0].full_text.split("http")[0]  , f"{topic}"  )











if (__name__ == "__main__"):
    main()

