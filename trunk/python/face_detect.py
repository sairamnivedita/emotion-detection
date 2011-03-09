#!/usr/bin/python

import cv, os, sys
import commands
import math
import write_arff

# Notre .arff est une variable global
arf = None

# taille en pixel : width et height des images normalisees
NORM_W = 128
NORM_H = 128

# chargement des paths
path = "../haarcascades/"
image_path = "../../images/"
norm_path = "../../norm/"
result = "../../result/"

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
all_s_file = [ s_0, s_1, s_2, s_3, s_4 ]
all_s = map( (lambda x : cv.Load(path+x)), all_s_file)

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
def auto(path):
	liste = commands.getoutput("ls "+path+" | grep .jpg")
	liste = liste.split()
	print liste
	return liste

# Boucle d'appel pour le traitement des images :
def norm_loop(liste):
	print "NORMALISATION"
	for image in liste:
		print image
		normalisation(image)
	print "FIN NORMALISATION"
# Affichage et arff sont des booleans pour savoir si on affiche et si l'on cree le fichier arff
def detect_loop(liste, affichage, boolean_arff):
	if boolean_arff:
		create_arff("premier_jet", "emotions")
	for image in liste:
		print image
		after_norm(image, affichage, boolean_arff)
	arf.no_more_data()
	print "Ecriture et fermeture du fichier arff terminees"

# Detection des yeux, nez et bouche
def detection_eye(img):
	eyes = cv.HaarDetectObjects(img, eye_path, cv.CreateMemStorage())
	return eyes
def detection_eye2(img):
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
	res['eyes'] = detection_eye(img)
	res['eyes2'] = detection_eye2(img)
	res['nose'] = detection_nose(img)
	res['mouth'] = detection_mouth(img)
	liste_s = sourires(img)
	res['s_0'] = liste_s[0]
	res['s_1'] = liste_s[1]
	res['s_2'] = liste_s[2]
	res['s_3'] = liste_s[3]
	res['s_4'] = liste_s[4]
	return res

def sourires(src):
	res = []
	img = cv.GetSubRect(src, (src.width*1/7, src.height*2/3, src.width*5/7, src.height/3)) 
	cpt = 0
	for s in all_s :
		temp = cv.HaarDetectObjects(img, s, cv.CreateMemStorage())
		res.append(len(temp))
	return res

def extracteur_de_sourires(nom, src):
	img = cv.GetSubRect(src, (src.width*1/7, src.height*2/3, src.width*5/7, src.height/3)) 
	cpt = 0
	for s in all_s :
		res = cv.HaarDetectObjects(img, s, cv.CreateMemStorage())
		if len(res) == 1 :
			cpt = cpt + 1     
		if cpt == len(all_s) :
			print "\tsourire vu dans "+nom
			cv.SaveImage(result+str(cpt)+"s_"+nom, img)

# Affichage des yeux, nez et bouche + correction 
def affichage_visage((x,y,w,h), img, a=0, b=0):
	cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), bleu)
def affichage_eyes(deyes, img, a=0, b=0):
	for (x,y,w,h),n in deyes:
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), vert)
def affichage_eyes2(deyes2, img, a=0, b=0):
	for (x,y,w,h),n in deyes2:
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), rouge)
def affichage_nose(dnose, img, a=0, b=0):
	for (x,y,w,h),n in dnose: 
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), rose)
def affichage_mouth(dmouth, img, a=0, b=0):
	for (x,y,w,h),n in dmouth: 
		cv.Rectangle(img, (x+a,y+b), (x+w+a,y+h+b), jaune)
def affichage(src, deyes, deyes2, dnose, dmouth, a=0, b=0):
	affichage_eyes(deyes, src, a,b)
	affichage_eyes2(deyes2, src, a,b)
	affichage_nose(dnose, src, a,b)
	affichage_mouth(dmouth, src, a,b)

def save(path, nom, img):
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

# Permet l'extraction des visages sur n'importe quelle photo et redimensionnent les visages trouves en NORM_W x NORM_H
def normalisation(img) :

	print image_path+img
	src = cv.LoadImage(image_path+img)

	# On fait une copie l'image pour le traitement (en gris)
	gris = cv.CreateImage( (src.width, src.height) , cv.IPL_DEPTH_8U, 1)
	normal = cv.CreateImage((NORM_W,NORM_H), cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(src, gris, cv.CV_BGR2GRAY)		

	# On detecte les visages (objects) sur l'image copiee
	faces = cv.HaarDetectObjects(gris, face_path, cv.CreateMemStorage())
	
	cp = 0
	for (x,y,w,h),n in faces: 
		tmp = cv.CreateImage( (w,h) , cv.IPL_DEPTH_8U, 1)
		cv.GetRectSubPix(gris, tmp, (float(x + w/2), float(y + h/2)))

		cv.EqualizeHist(tmp, tmp)
		cv.Resize(tmp, normal)
		
		#Detection oeil nez bouche sur l'image source:
		d = detection(tmp)
		d['mouth2'] = best_mouth(d['mouth'])
		
		if( (len(d['eyes'])>=2 or len(d['eyes2'])>=1) and len(d['mouth'])>=1 and len(d['nose'])>=1 ): 
			
			print "VISAGE dans la photo : "+ img
			# ----- Affichage visage ----- #
			affichage_visage((x,y,w,h), src)
			# ----- Affichage de toute les bouches ----- #
			#affichage(src, d['eyes'], d['eyes2'], d['nose'], d['mouth'], x, y)
			# ----- Affichage de la bouche la plus basse (en general la bonne) ----- #
			#affichage(src, d['eyes'], d['eyes2'], d['nose'], d['mouth2'], x, y)

			save(norm_path, "smallface_"+str(cp)+img, normal)
			save(result, "face_"+img, src)
			cp = cp +1

# Traitement apres la normalisation (cad sur les images de visages en NORM_W x NORM_H)
def after_norm(img, affichage, boolean_arff):

	#print norm_path+img
	src = cv.LoadImage(norm_path+img)

	# On copie l'image pour le traitement (en gris)
	gris = cv.CreateImage( (src.width, src.height) , cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(src, gris, cv.CV_BGR2GRAY )		
	cv.EqualizeHist(gris, gris)
	
	#Detection oeil nez bouche sur l'image source:
	d = detection(gris)
	d['mouth2'] = best_mouth(d['mouth'])

	# On detecte sans lunettes

	if affichage:
		# ----- Affichage de toute les bouches ----- #
		affichage(src, d['eyes'], d['eyes2'], d['nose'], d['mouth'])
		# ----- Affichage de la bouche la plus basse (en general la bonne) ----- #
		#affichage(src, d['eyes'], d['eyes2'], d['nose'], d['mouth2'])
	if boolean_arff:
		fill_arff(d, img)	

	#extracteur_de_sourires(img, tmp)
	save(norm_path, img, src)

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
		return file_name.split(".")[1][:2]
	except:
		return None

def create_arff(file_name, arff_name):
	global arf
	arf = write_arff.ArfFile(file_name, arff_name)
	arf.add_attribute_numeric("eyes")
	arf.add_attribute_numeric("eyes2")
	arf.add_attribute_numeric("mouth")
	arf.add_attribute_numeric("s_0")
	arf.add_attribute_numeric("s_1")
	arf.add_attribute_numeric("s_2")
	arf.add_attribute_numeric("s_3")
	arf.add_attribute_numeric("s_4")
	arf.add_attribute_enum("emotion", ["AN", "DI", "FE", "HA", "NE", "SA", "SU"])
	print "Ouverture du fichier "+file_name+" reussie"

def fill_arff(d, file_name):
	try:
		dic = dict([("eyes", len(d['eyes'])),("eyes2", len(d['eyes2'])), ("mouth", len(d['mouth'])),
			("s_0", d['s_0']), ("s_1", d['s_1']),("s_2", d['s_2']),("s_3", d['s_3']),("s_4", d['s_4']),
			("emotion", emotion(file_name))])
		arf.add_instance(dic)        
	except: 
		print "Nom de fichier non annote ou incorrect"

def main(image = "../../images/", norm = "../../norm/", res = "../../result/"):
    global image_path
    global norm_path
    global result
    image_path = image
    norm_path = norm
    result = res   

    liste = auto(image_path)
    norm_loop(liste)
    #liste_norm = auto(norm_path)
    #detect_loop(liste_norm, False, True)

if __name__ == "__main__":
	main()
