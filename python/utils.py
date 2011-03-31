#!/usr/bin/python
import cv, os, sys
import write_arff
import commands
import math
import copy

# Notre .arff est une variable global
arf = None

# taille en pixel : width et height des images normalisees
NORM_W = 128
NORM_H = 128

# chargement des paths
h_path = "../haarcascades/"
in_path = "../../images/"
#out_path = "../../result/"
treatment_path = "../../traitement/"
norm_path = "../../norm/"
path = ""
# cascades recherchees :
frontal_face = "haarcascade_frontalface_default.xml"
eyes = "haarcascade_eye.xml";
eyes2 = "haarcascade_eye_tree_eyeglasses.xml";
mouth = "haarcascade_mcs_mouth.xml";
nose = "haarcascade_mcs_nose.xml";

face_path = cv.Load(h_path+frontal_face)
eye_path = cv.Load(h_path+eyes)
eye2_path = cv.Load(h_path+eyes2)
mouth_path = cv.Load(h_path+mouth)
nose_path = cv.Load(h_path+nose)

# cascade sourire
s_0 = "smileD/smiled_01.xml"
s_1 = "smileD/smiled_02.xml"
s_2 = "smileD/smiled_03.xml"
s_3 = "smileD/smiled_04.xml"
s_4 = "smileD/smiled_05.xml" 
smile_files = [s_0, s_1, s_2, s_3, s_4]
smile_list = ["s_0", "s_1", "s_2", "s_3", "s_4"]
attr_list = ["eyes", "eyes2", "mouth"]
all_s = map( (lambda x : cv.Load(h_path+x)), smile_files)

# BLEU VERT ROUGE !
bleu  = (255,0,0)
vert  = (0,255,0)
jaune = (0,255,255)
rose  = (255,186,185)
rouge = (0,0,255)

# NOIR ET BLANC
gris  = (128,128,128)
noir  = (0,0,0)
blanc = (255,255,255)
clair = (192,192,192)
sombre = (64,64,64)

# Retourne la liste des fichiers dans le path entre en parametres
def jpg_list(path):
	res = []
	liste = commands.getoutput("ls -d "+path+"* | grep .jpg")
	liste = liste.split('\n')
	for line in liste:
		line = line.split('/')
		path = line[len(line)-2]+"/"+line[len(line)-1]
		#print path
		res.append(path)
	return res

"""
def display_loop(liste_norm):
	for image, image_n in zip(liste_images,liste_norm):
		display(image, image_n)
"""

# Renvoie l'emotion associee au nom de fichier : -
# AN -> anger
# DI -> disgust
# FE -> fear
# HA -> happiness
# NE -> neutral
# SA -> sad
# SU -> surprise
def emotion(file_name):
	try:
		return file_name.split(".")[2][:2]
	except:
		print "Erreur dans le nom du fichier (emotion incorrecte)"
		return None


