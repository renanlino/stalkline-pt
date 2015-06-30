import urllib2
import json
import sys
import genWebFacebook


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
    

def getTimeline(token, output_path):
    """
    (str, str) -> int/None
    Recebe um token de acesso e um caminho para despejar o resultado
    de um request a Graph API do Facebook
    """

    request = "https://graph.facebook.com/v2.3/me/home?fields=id,message,from{id,name},to{id,name},likes{id,name},comments{id}" + "&access_token=" + token
    try:
        answer = urllib2.urlopen(request)
    except urllib2.URLError:
        print(">>> getTimeline Error: URL request error")
        return None

    output = openFile(output_path, "w")
    output.write( answer.read() )
    output.close()
    return 0

def searchWord(word, input_path):
    """
    (str, str) -> list
    Procura a ocorrencia da palavra "word" no arquivo "input_path" e
    retorna um vetor com os pontos de ocorrencia da palavra fornecida
    """
    inputData = openFile(input_path, "r")
    content = inputData.read()
    ocr = []
    for i in range(0, len(content), 1):
        if content[i : i + len(word)].upper() == word.upper():
            ocr.append(i)
    inputData.close()
    return ocr

def splitPosts(input_path):
    """
    (str) -> list
    Recebe um arquivo com a representacao em texto de uma estrutura JSON
    valida (do tipo fornecida pela Graph API do Facebook) e retorna uma
    matriz com as posicoes que delimitam um post na estrutura.
    [ [Inicio_Post1, Fim_Post1], [Inicio_Post2, Fim_Post2], ... , [Inicio_PostN, Fim_PostN] ]
    """
    inputData = openFile(input_path, "r")
    content = inputData.read()
    posts = []
    stack = []
    for i in range(1, len(content)-1, 1):
        if content[i] == "{":
            stack.append(i)
        elif content[i] == "}":
            if len(stack) == 1:
                posts.append( [stack[0], i + 1] )
            stack.pop()
    return posts

def detectOcrInPost(posts_vec, ocr):
    """
    (list, int) -> int
    Dada uma posicao "ocr" verifica a qual dos intervalos contidos na matriz
    "post_vec" (do tipo gerada pela funcao splitPosts() ) "ocr" pertence.
    Ex.
    Dada a posicao 456 e um vetor de limites [ [1,9], [10,200], [250,500], [673, 910] ]
    retorna "2" (elemento [2] do vetor de limites) pois 456 esta contido no intervalo [250,500]
    """
    for i in range(len(posts_vec)):
        postLimits = posts_vec[i]
        if ocr in range( postLimits[0], postLimits[1], 1):
            return i
    return None


def readSetup():
    configFile = openFile("userData/config.json", "r")
    if configFile is None:
        print (">>> readSetup error: please run 'python config.py' frist")
        sys.exit(0)
    try:
        settings = json.load(configFile)
    except ValueError:
        print(">>> readSetup error: bad format for JSON")
        configFile.close()
        return None
    configFile.close()
    return settings

def getDetail(postID, token, term):
    request = "https://graph.facebook.com/v2.3/" + postID + "?fields=id,message,from{id,name,picture},to{id,name},link,picture" + "&access_token=" + token
    try:
        answer = urllib2.urlopen(request)
    except urllib2.URLError:
        print(">>> getDetail Error: URL request error")
        return None
    postDict = {}
    jsonAns = json.load(answer)

    for key in ["id","message","from","to","link","picture"]:
        if key in jsonAns:
            if key is "from":
                postDict[key] = [jsonAns[key]["id"], jsonAns[key]["name"]]
                postDict["profile_photo"] = jsonAns[key]["picture"]["data"]["url"]
            elif key is "to":
                postDict[key] = [ jsonAns[key]["data"][0]["id"], jsonAns[key]["data"][0]["name"] ]
            else:
                postDict[key] = jsonAns[key]
        else:
            if key is "to":
                postDict[key] = ["_","_"]
            else:
                postDict[key] = "_"
        postDict["key"] = term
        postDict["source"] = "facebook"
    return postDict

def getFacebook():
    config = readSetup()
    if config is None:
        return None
    if "facebookToken" in config:
        if getTimeline(config["facebookToken"], "userData/facebookTimeline") is None:
            return None
    else:
        return None

    oldFile = openFile("output/webOutFacebook.json", "r")
    if oldFile != None:
        webOutput = json.load(oldFile)
        oldFile.close()
    else:
        webOutput = []
    if "trackUsers" in config:
        for user in config["trackUsers"]:
            print("    Rastreando %s..." %user)
            ocrs = searchWord(user, "userData/facebookTimeline")
            postsLimits = splitPosts("userData/facebookTimeline")
            posts = []
            for ocr in ocrs:
                position = detectOcrInPost(postsLimits, ocr)
                if position not in posts:
                    posts.append(position)
            content = openFile("userData/facebookTimeline", "r").read()
            ids = []
            for index in posts:
                post =  content[postsLimits[index][0]:postsLimits[index][1]]
                postDict = json.loads(post)
                if "id" in postDict:
                    ids.append(postDict["id"])
                for postID in ids:
                    postDict = getDetail(postID, config["facebookToken"], user)
                    if postDict is not None and postDict not in webOutput:
                        webOutput.append(postDict)
    if "trackTopics" in config:
        for topic in config["trackTopics"]:
            print("    Rastreando %s..." %topic)
            ocrs = searchWord(topic, "userData/facebookTimeline")
            postsLimits = splitPosts("userData/facebookTimeline")
            posts = []
            for ocr in ocrs:
                position = detectOcrInPost(postsLimits, ocr)
                if position not in posts:
                    posts.append(position)
            content = openFile("userData/facebookTimeline", "r").read()
            ids = []
            for index in posts:
                post =  content[postsLimits[index][0]:postsLimits[index][1]]
                postDict = json.loads(post)
                if "id" in postDict:
                    ids.append(postDict["id"])
                for postID in ids:
                    postDict = getDetail(postID, config["facebookToken"], topic)
                    if postDict is not None and postDict not in webOutput:
                        webOutput.append(postDict)

    outputFile = openFile("output/webOutFacebook.json", "w")
    if outputFile is None:
        return None

    outputFile.write(json.dumps(webOutput))
    outputFile.close()
    print(">>> Gerando HTML para o Facebook...")
    genWebFacebook.generate()
    return 0



                
