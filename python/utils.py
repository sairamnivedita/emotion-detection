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
out_path = "../../result/"
norm_path = "../../norm/"
traitement_path = "../../traitement/"

# cascades recherchees :
frontal_face = "haarcascade_frontalface_default.xml"
eyes = "haarcascade_eye.xml";
eyes2 = "haarcascade_eye_tree_eyeglasses.xml";
mouth = "haarcascade_mcs_mouth.xml";
nose = "haarcascade_mcs_nose.xml";

face_path = cv.Load(path+frontal_face)
eye_path = cv.Load(path+eyes)
eye2_path = cv.Load(path+eyes2)
mouth_path = cv.Load(path+mouth)
nose_path = cv.Load(path+nose)

# cascade sourire
s_0 = "smileD/smiled_01.xml"
s_1 = "smileD/smiled_02.xml"
s_2 = "smileD/smiled_03.xml"
s_3 = "smileD/smiled_04.xml"
s_4 = "smileD/smiled_05.xml" 
smile_files = [s_0, s_1, s_2, s_3, s_4]
smile_list = ["s_0", "s_1", "s_2", "s_3", "s_4"]
attr_list = ["eyes", "eyes2", "mouth"]
all_s = map( (lambda x : cv.Load(path+x)), smile_files)

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

# Boucle d'appel pour la normalisation des images
def norm_loop(liste):
	print "NORMALISATION"
	for image in liste:
		print "Normalisation de l'image "+str(image)+" en cours"
		normalisation(image)
	print "FIN NORMALISATION"

# Boucle d'appel pour le traitement des images
def traitement_loop(liste):
	print "TRAITEMENT"
	for image in liste:
		print "Traitement de l'image "+str(image)+" en cours"
		traitements(image)
	print "FIN TRAITEMENT"

# display et arff sont des booleans pour savoir si on affiche et si l'on cree le fichier arff
def arff_loop(liste_norm, liste_trait, file_name="fichier_arff", div=8):
	print "CREATION DU ARFF"
	create_arff(file_name, "emotions", div)
	for image_n, image_t in zip(liste_norm,liste_trait):
		after_norm(image_n, image_t, boolean_arff,div)
	arf.no_more_data()
	print "FIN ARFF"

"""
def display_loop(liste_norm):
	for image, image_n in zip(liste_images,liste_norm):
		display(image, image_n)
"""

# Detection des yeux, nez et bouche
def detection_eyes(img):
	eyes = cv.HaarDetectObjects(img, eye_path, cv.CreateMemStorage())
	return eyes
def detection_eyes2(img):
	eyes2 = cv.HaarDetectObjects(img, eye2_path, cv.CreateMemStorage())
	return eyes2
def detection_nose(img):
	nose = cv.HaarDetectObjects(img, nose_path, cv.CreateMemStorage())
	return nose
def detection_mouth(img):
	mouth = cv.HaarDetectObjects(img, mouth_path, cv.CreateMemStorage())
	return mouth
def detection(img):
	res = dict()
	res['eyes'] = detection_eyes(img)
	res['eyes2'] = detection_eyes2(img)
	res['nose'] = detection_nose(img)
	res['mouth'] = detection_mouth(img)
	l = smiles(img)
	for s in smile_list:
		res[s] = l[s]
	return res

def smiles(src):
	res = dict()
	img = cv.GetSubRect(src, (src.width*1/7, src.height*2/3, src.width*5/7, src.height/3)) 
	cpt = 0
	for s,smile in zip(all_s,smile_list) :
		temp = cv.HaarDetectObjects(img, s, cv.CreateMemStorage())
		res[smile] = len(temp)
	return res

# display des yeux, nez et bouche + correction 
def display_face((x,y,w,h), img, a=0, b=0):
	cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), bleu)
def display_eyes(deyes, img, a=0, b=0):
	for (x,y,w,h),n in deyes:
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), vert)
def display_eyes2(deyes2, img, a=0, b=0):
	for (x,y,w,h),n in deyes2:
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), rouge)
def display_nose(dnose, img, a=0, b=0):
	for (x,y,w,h),n in dnose: 
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), rose)
def display_mouth(dmouth, img, a=0, b=0):
	for (x,y,w,h),n in dmouth: 
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), jaune)
def display_corners(dcorners, img, diametre):
	for (x,y) in dcorners:
		cv.Circle(img, (x,y), diametre, rouge, -1)
def display(src, deyes, deyes2, dnose, dmouth, a=0, b=0):
	display_eyes(deyes, src, a,b)
	display_eyes2(deyes2, src, a,b)
	display_nose(dnose, src, a,b)
	display_mouth(dmouth, src, a,b)

def save(path, nom, img):
	print "Sauvegarde de l'image:"
	print path+nom
	cv.SaveImage(path+nom, img)

def best_mouth(mouth):
	res = ((0,0,0,0),0) 
	if len(mouth) > 0:
		val = 0
		for (x,y,w,h),n in mouth:
			if y+h > val:
				val = y+h
				res = ((x,y,w,h),n)
	return [res]

def pixels_count(img,div):

	res = []
	src = cv.LoadImageM(traitement_path+img, 1)
	largeur = NORM_W/div
	hauteur = NORM_H/div

	# div*div images de largeur NORM_W/div
	for l in range(0, NORM_W, largeur):
		for h in range(0, NORM_H, hauteur):
			nb_pixel = 0
			for l2 in range(largeur):
				for h2 in range(hauteur):
					# On prend le premier du pixel (niveau de gris => R=G=B
					#print src[l+l2,h+h2]
					if(src[l+l2,h+h2][0] > 128) : 
						nb_pixel += 1
			res.append(nb_pixel)
	return res

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
		return None


