import json
import cgi

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

def generate():
    inputFile = openFile("output/webOutTwitter.json", "r")
    if inputFile == None:
        return None
    posts = json.load(inputFile)
    htmlOut = openFile("web/twitter.html","w")

    htmlOut.write("<HTML><HEAD><TITLE>.:: Twitter Stalkline ::.</TITLE>")
    htmlOut.write("<style>body {background-color:#c0deed} p {font-family:arial} h3 {color:#0184b4} </style></HEAD>")
    htmlOut.write("<BODY>")
    htmlOut.write("<p align='center'><TABLE bgcolor='#FFFFFF' width='100%'><tr><td>")
    htmlOut.write("<p><b><h3>Twitter Stalkline</h3></b></p></td></tr></TABLE></p>")
    for i in range(len(posts)-1, -1, -1):
	post = posts[i]
        code = "<TABLE bgcolor='white' width=600 align='center'><tr>"
        code += ("<td><img src=%s></td>" %(post["profile_photo"]))
        code += ("<td><p>Because you're tracking '<b>%s</b>':</p>" %post["key"]).encode("ascii", "xmlcharrefreplace")
        code += ("<p><b>%s" %(post["from"].encode("ascii", "xmlcharrefreplace")))
        code += ("</b>")
        code += ("<p>%s</p>" %(post["message"].encode("ascii", "xmlcharrefreplace")))
        code += ("<p align='right' style='font-size:10px'><a href=http://www.twitter.com/%s/status/%s>See this post at Twitter</a></p>" %(post["from"],post["id"]))
        code += "</td></tr>"
        code += "</TABLE>"
        code += "<p></p>"
        htmlOut.write(code.encode("utf8"))

    htmlOut.write("</BODY></HTML>")
    htmlOut.close()

