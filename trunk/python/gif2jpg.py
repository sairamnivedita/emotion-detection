#!/usr/bin/python

import cv, os, sys
import commands

def main():        
        os.system("mv jpg ../faces/")
        liste = commands.getoutput("ls | grep subject")
        liste = liste.split()
        for fic in liste :
            os.system("convert " + fic + " " + fic +".jpg")
        os.system("mv *.jpg ../faces/")

if __name__ == "__main__":
        main()
