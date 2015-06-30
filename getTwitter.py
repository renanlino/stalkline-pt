import mechanize
import requests
import tweepy
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json
import genWebTwitter

def openFile(file_path, mode):
    """
    (str, srt) -> file object
    Funcao de abertura de arquivos com tratamento de erros
    """
    try:
        fileObj = open(file_path, mode)
    except IOError:
        print(">>> openFile error: %s" %file_path)
	return None
    return fileObj


def getTwitter():
    config = readSetup()
    if config is None:
        return None
    if "twitterToken" in config and "twitterToken_secret" in config:
        access_token, access_token_secret = config["twitterToken"], config["twitterToken_secret"]
        auth = tweepy.OAuthHandler('0t5gHmjCmed1qSUHFspKcuTRK', 'EGMD8fu3Vk0iDRM8CtSs0UEUj5hh3ge3EA1bQ8etU9EVBWhdWu')
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

	oldFile = openFile("output/webOutTwitter.json", "r")
	if oldFile != None:
	    lista_posts = json.load(oldFile)
	    oldFile.close()
	else:
	    lista_posts = []

        try:
            lista_timeline = api.home_timeline()
        except tweepy.TweepError:
            print(">>> getTwitter error")
            return None
            
        if "trackUsers" in config:
            for user in config["trackUsers"]:
                print("    Rastreando %s..." %user)
                lista = detectUser(api, user, lista_timeline)
                if lista is None:
                    return None
                for post in lista:
                    lista_posts.append(post)
        if "trackTopics" in config:
            for topic in config["trackTopics"]:
                print("    Rastreando %s..." %topic)
                lista = detectWord(api, topic, lista_timeline)
                if lista is None:
                    return None
                for post in lista:
                    lista_posts.append(post)
        outputFile = openFile("output/webOutTwitter.json", "w")
        if outputFile is None:
            return None
        print(lista_posts)
        outputFile.write(json.dumps(lista_posts))
        outputFile.close()
	print(">>> Gerando HTML para o Twitter...")
	genWebTwitter.generate()
        return 0
    else:
        return None
        

def readSetup():
    configFile = openFile("userData/config.json", "r")
    if configFile is None:
        print (">>> readSetup error: please run 'python config.py' first")
    try:
        settings = json.load(configFile)
    except ValueError:
        print(">>> readSetup error: bad format for JSON")
        configFile.close()
        return None
    configFile.close()
    return settings

def detectWord(api,trackedWord, lista_timeline):
    
    list_tweet_data = []
    
    for tweet in lista_timeline:
        tweet_data = {}
        tweet_data["message"] = tweet_data["from"] = tweet_data["to"] = tweet_data["id"] = tweet_data["profile_photo"] = tweet_data["picture"] = tweet_data["source"] = tweet_data["key"] = "."
        tweet_id = str(tweet.id)
        if (trackedWord.upper() in tweet.text.upper()):
            user = tweet.user.id
            try:
                u = api.get_user(user)
            except tweepy.TweepError:
                print (">>> detectWord error: API limit?")
                return None
            screen_name = str(u.screen_name)
            #print 'https://twitter.com/'+screen_name+'/status/'+tweet_id
            tweet_data["message"]       = tweet.text
            tweet_data["id"]       =     tweet_id
            tweet_data["from"]          = screen_name
            #tweet_data["datetime"]      = tweet.created_at
            tweet_data["profile_photo"] = tweet.user.profile_image_url.replace('_normal','_bigger')

            if 'media' in tweet.entities:
                for media in tweet.entities['media']:
                    tweet_data["picture"] =  media['expanded_url']              
                                       
            tweet_data["source"] = "twitter"
            tweet_data["key"] = trackedWord
            list_tweet_data.append(tweet_data)
    return list_tweet_data

def detectUser(api,trackedUser, lista_timeline):

    list_tweet_data = []
    
    for tweet in lista_timeline:
        tweet_data = {}
        tweet_data["from"] = tweet_data["to"] = tweet_data["id"] = tweet_data["profile_photo"] = tweet_data["picture"] = tweet_data["source"] = tweet_data["key"] = None
        tweet_id = str(tweet.id)
        user = tweet.user.id
        try:
            u = api.get_user(user)
        except tweepy.TweepError:
            print (">>> detectUser error: API limit?")
            return None
        screen_name = str(u.screen_name)
        if (screen_name == trackedUser):
            #print 'https://twitter.com/'+screen_name+'/status/'+tweet_id
            tweet_data["message"]       = tweet.text
            tweet_data["id"]       =     tweet_id
            tweet_data["from"]          = screen_name
            #tweet_data["datetime"]      = tweet.created_at
            tweet_data["profile_photo"] = tweet.user.profile_image_url.replace('_normal','_bigger')
            if 'media' in tweet.entities:
                for media in tweet.entities['media']:
                    tweet_data["picture"] =  media['expanded_url']
            tweet_data["source"] = "twitter"
            tweet_data["key"] = trackedUser
            list_tweet_data.append(tweet_data)
    return list_tweet_data
