import mechanize
import requests
import tweepy
from requests_oauthlib import OAuth1
from urlparse import parse_qs

#Dados do aplicativo
client_key = '0t5gHmjCmed1qSUHFspKcuTRK'
client_secret = 'EGMD8fu3Vk0iDRM8CtSs0UEUj5hh3ge3EA1bQ8etU9EVBWhdWu'

def doLogin():
    print
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@                                                    @")
    print("@           Twitter Login & App Auth Tool            @")
    print("@                                                    @")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print
    print("Esta ferramenta fara login em sua conta do Twitter")
    print("e solicitara autorizacao para que o aplicativo tenha")
    print("acesso as suas informacoes")
    print
    login = raw_input(">>> Digite seu login do Twitter: ")
    password = raw_input(">>> Digite sua senha do Twitter: ")

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Android; Mobile; rv:35.0) Gecko/35.0 Firefox/35.0')]

    return appAuth(browser, login, password)

def appAuth(browser, login, password):

    request_token_url = 'https://api.twitter.com/oauth/request_token'

    print(">>> Solicitando Token...")
    oauth = OAuth1(client_key, client_secret=client_secret)
    r = requests.post(url=request_token_url, auth=oauth)
    credentials = parse_qs(r.content)
    if credentials.get('oauth_token') is None:
        return None, None
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]


    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorize_url = base_authorization_url + '?oauth_token='
    authorize_url = authorize_url + resource_owner_key
    
    browser.open(authorize_url)
    browser.select_form(nr=0)
    browser.form.controls.pop(len(browser.form.controls)-1)
    browser.form['session[username_or_email]'] = login
    browser.form['session[password]'] = password
    try:
        print(">>> Fazendo login e solicitando autorizacao...")
        response = browser.submit()
    except (mechanize.HTTPError, mechanize.URLError):
        print (">>> Login/auth error")
        return None, None
    content = response.get_data().split("<code>")[1]
    pin = ""
    for char in content:
        if char is not "<":
            pin += char
        else:
            break

    print(">>> Obtendo token do usuario...")
    oauth = OAuth1(client_key,
                   client_secret=client_secret,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=pin)

    access_token_url = 'https://api.twitter.com/oauth/access_token'

    r = requests.post(url=access_token_url, auth=oauth)

    credentials = parse_qs(r.content)
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    return resource_owner_key, resource_owner_secret




                

    
            
    
    

