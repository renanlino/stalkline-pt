import getFacebook
import getTwitter
import time
import sys
import tweepy


def main():
    sleepTime = 1*60

    print("Intervalo entre requests: %1.f segundos" %sleepTime)
    print
    while True:
        print(">>> Obtendo dados do Facebook...")
        getFacebook.getFacebook()
        print(">>> Obtendo dados do Twitter...")
        getTwitter.getTwitter()        
        print(">>> Aguardando %.1f segundos para continuar..." %sleepTime)
        time.sleep(sleepTime)
        print
        print
        """
        try:
            print(">>> Obtendo dados do Facebook...")
            getFacebook.getFacebook()
            print(">>> Obtendo dados do Twitter...")
            getTwitter.getTwitter()
            print(">>> Aguardando %.1f segundos para continuar..." %sleepTime)
            time.sleep(sleepTime)
            print
            print
        except tweepy.TweepError:
            print(">>> Aguardando %.1f segundos para continuar..." %sleepTime)
            time.sleep(sleepTime)
            print
            print
            continue
        """

main()
