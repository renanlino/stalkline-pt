# -*- coding: utf-8 -*-
import loginTwitter
import loginFacebook
import json
import sys

PLAT_FACEBOOK = 1
PLAT_TWITTER = 2
PLAT_BOTH = 3

TRACK_PEOPLE = 1
TRACK_TOPIC = 2
TRACK_BOTH = 3

dicio = {}

def main():
    print("######################################################")
    print("#                                                    #")
    print("#               Stalkline Config Tool                #")
    print("#                                                    #")
    print("######################################################")
    print
    print("Bem-vindo ao assistente de configuracao do Stalkline!")
    print
    print("Nos proximos passos vamos definir o comportamento do")
    print("seu dispositivo")
    print
    go = raw_input(">> Pressione enter para comecar...")
    logins()
    trackMode()
    print("  Gravando as configuracoes...")
    try:
        configOut = file("userData/config.json", "w")
    except IOError:
        print("  Problemas na gravacao do arquivo!")
        sys.exit(0)
    configOut.write(json.dumps(dicio))
    configOut.close()
    return 0

def logins():
    print
    print("> Voce gostaria de utilizar o Stalkline em qual(is)")
    print("  plataforma(s)?")
    print("  Digite:\n  - 1 para Facebook apenas\n  - 2 para Twitter apenas\n  - 3 para ambos")
    platf = raw_input(">> Sua escolha: ")
    try:
        platf = int(platf)
    except:
        print("Por favor, escolha uma opcao valida")
        logins()
        return
    dicio["plats"] = str(platf)
    if platf == PLAT_FACEBOOK or platf == PLAT_BOTH:
        print
        print("Ok! Vamos configurar sua conta do Facebook!")
        facebookToken = loginFacebook.doLogin()
        if facebookToken is False:
            print("> Problemas ao obter o login/autorizacao do Facebook")
            logins()
            return
        dicio["facebookToken"] = facebookToken
        ## GRAVAR O TOKEN NO DICIONARIO ##
    if platf == PLAT_TWITTER or platf == PLAT_BOTH:
        print
        print("Agora vamos configurar sua conta do Twitter!")
        twitterToken, twitterToken_secret = loginTwitter.doLogin()
        if twitterToken is None or twitterToken_secret is None:
            print("> Problemas ao obter o login/autorizacao do Twitter")
            logins()
            return
        dicio["twitterToken"] = twitterToken
        dicio["twitterToken_secret"] = twitterToken_secret
        ## GRAVAR O TOKEN NO DICIONARIO ##
    if platf != PLAT_TWITTER and platf != PLAT_FACEBOOK and platf != PLAT_BOTH:
        print("Por favor, escolha uma opcao valida")
        logins()
        return

def trackMode():
    print
    print("> Agora vamos configurar o modo de vigilancia.")
    print("  Quem ou o que voce gostaria de vigiar?")
    print("  Digite:\n  - 1 para seguir uma pessoa\n  - 2 para seguir um assunto\n  - 3 para ambos")
    track = raw_input(">> Sua escolha: ")
    try:
        track = int(track)
    except:
        print("Por favor, escolha uma opcao valida")
        trackMode()
        return
    dicio["trackMode"] = str(track)
    if track == TRACK_PEOPLE or track == TRACK_BOTH:
        print
        print("> Indique quais sao os alvos que voce deseja marcar")
        print("  Insira as IDs dos perfis do Facebook e/ou os usuarios")
        print("  do Twitter que voce quer rastrear")
        print("  Voce pode indicar varios perfis, separando as IDs por virgula")
        print("  Exemplo: 100067998896,Ezequiel França,7987010001,renanlino,NDoug_")
        users = raw_input(">>> ")
        ## GRAVAR OS USUARIOS NO DICIONARIO ##
        dicio["trackUsers"] = users.split(",")
    if track == TRACK_TOPIC or track == TRACK_BOTH:
        print
        print("> Indique quais sao os topicos que voce deseja marcar")
        print("  Voce pode indicar varios topicos, separandos por virgula")
        print("  Exemplo: Dilma,Lula,PT,PSDB,Futebol,Netflix")
        topics = raw_input(">>> ")
        ## GRAVAR OS TOPICOS NO DICIONARIO ##
        dicio["trackTopics"] = topics.split(",")
    if track != TRACK_TOPIC and track != TRACK_PEOPLE and track != TRACK_BOTH:
        print("Por favor, escolha uma opcao valida")
        logins()
        return

main()
