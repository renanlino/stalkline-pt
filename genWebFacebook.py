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
    inputFile = openFile("output/webOutFacebook.json", "r")
    if inputFile == None:
        return None
    posts = json.load(inputFile)
    htmlOut = openFile("/var/www/facebook.html","w")

    htmlOut.write("<HTML><HEAD><TITLE>.:: Facebook Stalkline ::.</TITLE>")
    htmlOut.write("<style>body {background-color:#e9eaed} p {font-family:arial} h3 {color:#FFFFFF} </style></HEAD>")
    htmlOut.write("<BODY>")
    htmlOut.write("<p align='center'><TABLE bgcolor='#47639e' width='100%'><tr><td>")
    htmlOut.write("<p><b><h3>Facebook Stalkline</h3></b></p></td></tr></TABLE></p>")
    for i in range(len(posts)-1, -1, -1):
	post = posts[i]
        code = "<TABLE bgcolor='white' width=600 align='center'><tr>"
        code += ("<td><img src=%s></td>" %(post["profile_photo"]))
        code += ("<td><p>Because you're tracking '<b>%s</b>':</p>" %post["key"]).encode("ascii", "xmlcharrefreplace")
        code += ("<p><b>%s" %(post["from"][1].encode("ascii", "xmlcharrefreplace")))
        if post["to"][1] != "_":
            code += (" -></b> <b>%s</b>" %(post["to"][1].encode("ascii", "xmlcharrefreplace")) )
        else:
            code += ("</b>")
        code += ("<p>%s</p>" %(post["message"].encode("ascii", "xmlcharrefreplace")))
        if post["picture"] != "_":
            if post["link"] != "_":
                code += ("<a href=%s>" %post["link"])
            code += ("<p align='center'><img src=%s></p>" %(post["picture"]))
            if post["link"] != "_":
                code += "</a>"
        code += ("<p align='right' style='font-size:10px'><a href=http://www.facebook.com/%s>See this post at Facebook</a></p>" %(post["id"]))
        code += "</td></tr>"
        code += "</TABLE>"
        code += "<p></p>"
        htmlOut.write(code.encode("utf8"))

    htmlOut.write("</BODY></HTML>")
    htmlOut.close()
