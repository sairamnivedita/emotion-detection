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
all_s_file = [s_0, s_1, s_2, s_3, s_4]
smile_list = ["s_0", "s_1", "s_2", "s_3", "s_4"]
attr_list = ["eyes", "eyes2", "mouth"]
all_s = map( (lambda x : cv.Load(h_path+x)), all_s_file)

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
	for s in smile_list:
		res[s] = liste_s[s]
	return res

def sourires(img):
	res = dict()
	img = cv.GetSubRect(img, (img.width*1/7, img.height*2/3, img.width*5/7, img.height/3)) 
	cpt = 0
	for s,smiles in zip(all_s, smile_list) :
		res[smiles] = len(cv.HaarDetectObjects(img, s, cv.CreateMemStorage()))
	return res


# Retourne la liste des fichiers dans le path entre en parametres
def jpg_list(path):
	res = []
	print "le path est"+path
	liste = commands.getoutput("ls "+path+" | grep .jpg")
	liste = liste.split('\n')
	print liste
	for line in liste:
		print line
		res.append(line)
	return res

# Boucle d'appel pour le traitement des images :
def norm_loop(in_path, out_path):
	res = []
	jpegs = jpg_list(in_path)
	print "NORMALISATION"
	for img in jpegs:
		if(os.path.exists(out_path+"small."+img)):
			print "L'image "+img+" est deja normalisee"
		else:
			src = cv.LoadImage(in_path+img)
			print "Normalisation de l'image "+img+" en cours"
			normal = normalisation(src)
			if not normal == None:
				save(out_path, "small."+img, normal)
	print "FIN NORMALISATION"

# Boucle de traitements
def treatment_loop(in_path, out_path):
	res = []
	jpegs = jpg_list(in_path)
	print "TRAITEMENT"
	for img in jpegs:
		if(os.path.exists(out_path+"modif_"+img)):
			print "L'image "+img+" a deja ete traite"
		else:  
			src = cv.LoadImageM(in_path+img, cv.CV_LOAD_IMAGE_GRAYSCALE)
			print "Traitement de l'image "+img+" en cours"
			modif = treatments(src)
			save(out_path, "modif_"+img, modif)
	print "FIN TRAITEMENT"

# Boucle de creation du arff
def arff_loop(in_path, file_name="fichier_arff", div=8):
	create_arff(file_name, "emotions", div)
	jpegs = jpg_list(in_path)
	for img in jpegs:
		arff(in_path, img)	
	arf.no_more_data()
	print "Ecriture et fermeture du fichier arff terminees"

def webcam_comptage_pixel(img,div=8):

	src = treatments(img)
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

def webcam_arff(file_name="cam.arff", src, div=8):

	if not(os.path.exists(file_name)):
		create_arff(file_name, "verdict", div)
	else:
		arf = open(file_name, "w")
	# On copie l'image pour le traitement (en gris)
	gris = cv.CreateImage( (src.width, src.height) , cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(src, gris, cv.CV_BGR2GRAY )		
	cv.EqualizeHist(gris, gris)

	#Detection oeil nez bouche sur l'image source:
	d = detection(gris)

	c = webcam_comptage_pixel(img)
	fill_arff(d, img, c)	
	arf.no_more_data()

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

# Permet l'extraction des visages sur n'importe quelle photo et redimensionnent les visages trouves en NORM_W x NORM_H
def normalisation(src, webcam=False):

	res = []

	# On fait une copie l'image pour le traitement (en gris)
	gris = cv.CreateImage( (src.width, src.height) , cv.IPL_DEPTH_8U, 1)
	normal = cv.CreateImage((NORM_W,NORM_H), cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(src, gris, cv.CV_BGR2GRAY)		

	# On detecte les visages (objects) sur l'image copiee
	faces = cv.HaarDetectObjects(gris, face_path, cv.CreateMemStorage())

	for (x,y,w,h),n in faces: 
		tmp = cv.CreateImage( (w,h) , cv.IPL_DEPTH_8U, 1)
		cv.GetRectSubPix(gris, tmp, (float(x + w/2), float(y + h/2)))

		cv.EqualizeHist(tmp, tmp)
		cv.Resize(tmp, normal)

		#Detection oeil nez bouche sur l'image source:
		d = detection(tmp)

		# On detecte au moins 2 yeux "normaux", au moins un oeil avec lunette, au moins une bouche et au moins un nez
		if( (len(d['eyes'])>=2 or len(d['eyes2'])>=1) and len(d['mouth'])>=1 and len(d['nose'])>=1 ): 
			print "Visage detecte dans la photo"
			res.append((normal,(x,y,w,h)))
		if(webcam):
			return res
		else:
			return res[0]
			

# Traitement apres la normalisation (cad sur les images de visages en NORM_W x NORM_H)
def arff(in_path, img, div=8):

	src = cv.LoadImage(in_path+img)
	# On copie l'image pour le traitement (en gris)
	gris = cv.CreateImage( (src.width, src.height) , cv.IPL_DEPTH_8U, 1)
	cv.CvtColor(src, gris, cv.CV_BGR2GRAY )		
	cv.EqualizeHist(gris, gris)

	#Detection oeil nez bouche sur l'image source:
	d = detection(gris)

	c = comptage_pixel(in_path, img)
	fill_arff(d, img, c)	

def treatments(img):

	# --- Seuil --- #
	cv.AdaptiveThreshold(img,img,255, cv.CV_ADAPTIVE_THRESH_MEAN_C, cv.CV_THRESH_BINARY_INV, 7, 10)
	#cv.Erode(src,src,None,1)
	#cv.Dilate(src,src,None,1)
	return img

def comptage_pixel(in_path, img,div=8):

	res = []
	src = cv.LoadImageM(in_path+img, 1)
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

def create_arff(file_name, arff_name, div=8):
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
	for i in range(div*div):
		arf.add_attribute_numeric("cpt_"+str(i))
	arf.add_attribute_enum("emotion", ["AN", "DI", "FE", "HA", "NE", "SA", "SU"])
	print "Ouverture du fichier "+file_name+" reussie"

def fill_arff(d, img_name, c_pixels, div=8):

	dic = dict()
	try:
		e = emotion(img_name)
		dic["emotion"] = e
	except: 
		print "Nom de fichier non annote ou incorrect"

	for a in attr_list:
		dic[a] = len(d[a])
	for s in smile_list:
		dic[s] = d[s]
	for i in range(div*div):
		dic["cpt_"+str(i)] = c_pixels[i]
	print dic
	arf.add_instance(dic)        
	print img_name+" : "+e


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

