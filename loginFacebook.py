import mechanize

def getToken(url):
    ans = url.split("access_token=")[1]
    i = 0
    token = ""
    while ans[i] != "&":
        token += ans[i]
        i += 1
    return token

def facebookLogin(browser, login, password):

    tries = 0
    success = False
    
    while not success:
        try:
            browser.open("http://m.facebook.com/")
            success = True
        except (mechanize.HTTPError, mechanize.URLError):
            tries += 1
            if tries >= 2:
                print (">>> HTTP error: check internet connection")
                return False
    browser.select_form(nr=0)
    browser.form['email'] = login
    browser.form['pass'] = password
    try:
        response = browser.submit()
    except (mechanize.HTTPError, mechanize.URLError):
        print (">>> HTTP error: check internet connection")
        return False
    if "login.php" in response.geturl():
        print(">>> Login error: login/password mismatch?")
        return False
    else:
        return True

def appAuth(browser, app_id, red_uri, scopes):
    request = ("https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=%s&response_type=token&display=page" %(app_id, red_uri, scopes))
    response = browser.open(request)
    if "access_token" in response.geturl():
        token = getToken(response.geturl())
        return token
    browser._factory.is_html = True
    browser.select_form(nr=0)
    browser.form.controls.pop(len(browser.form.controls)-2)
    response = browser.submit()

    if "error" in response.geturl():
        print ">>> App auth error: denied"
        return False
    elif "access_token" in response.geturl():
        token = getToken(response.geturl())
        return token
    else:
        print ">>> App auth error: unknown"
        return False

def doLogin(app_id="832365926851419", red_uri="https://www.facebook.com/connect/login_success.html", scopes="read_stream"):
    print
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@                                                    @")
    print("@           Facebook Login & App Auth Tool           @")
    print("@                                                    @")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print
    print("Esta ferramenta fara login em sua conta do Facebook")
    print("e solicitara autorizacao para que o aplicativo tenha")
    print("acesso as suas informacoes")
    print
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cookies = mechanize.CookieJar()
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Android; Mobile; rv:35.0) Gecko/35.0 Firefox/35.0')]
    login = raw_input(">>> Digite seu login do Facebook: ")
    password = raw_input(">>> Digite sua senha do Facebook: ")

    print ("    Realizando login...")
    if facebookLogin(browser, login, password):
        print ("    Login realizado com sucesso!")
    else:
        return False
    print("    ATENCAO: este aplicativo requer as seguintes permissoes:\n    %s" %scopes)
    confirm = raw_input(">>> Confirma a autorizacao? (s,n) ")
    if confirm == "s":
        print ("    Solicitando autorizacao...")
        token = appAuth(browser, app_id, red_uri, scopes)
        if not token:
            return False
        else:
            print ("    Autorizacao obtida com sucesso")
            return token
    else:
        return False
