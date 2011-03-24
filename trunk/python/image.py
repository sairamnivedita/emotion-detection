#!/usr/bin/python
import utils

class image: 

	def __init__(self, img):

		self.img = img
		# Attributs 
		self.eyes = detection_eyes(img)
		self.eyes2 = detection_eyes2(img)
		self.nose = detection_nose(img)
		self.mouth = detection_mouth(img)
		self.l = smiles(img)

	def normalisation(self):	

		# On fait une copie l'image pour le traitement (en gris)
		gray = cv.CreateImage( (self.img.width, self.img.height) , cv.IPL_DEPTH_8U, 1)
		normal = cv.CreateImage((utils.NORM_W,utils.NORM_H), cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(self.img, gray, cv.CV_BGR2GRAY)		

		# On detecte les visages (objects) sur l'image copiee
		faces = cv.HaarDetectObjects(gray, utils.face_path, cv.CreateMemStorage())

		for (x,y,w,h),n in faces: 
			tmp = cv.CreateImage( (w,h) , cv.IPL_DEPTH_8U, 1)
			cv.GetRectSubPix(gris, tmp, (float(x + w/2), float(y + h/2)))

			cv.EqualizeHist(tmp, tmp)
			cv.Resize(tmp, normal)

			#Detection oeil nez bouche sur l'image source:
			d = utils.detection(tmp)

			if( (len(d['eyes'])>=2 or len(d['eyes2'])>=1) and len(d['mouth'])>=1 and len(d['nose'])>=1 ): 
				return normal

	# --- Corners --- #
	def corners(self):
		eig_img = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
		temp_img = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
		corners = cv.GoodFeaturesToTrack(dst, eig_img, temp_img, 100, 0.04, 1.0, useHarris = True)
		#utils.affichage_corners(corners, img, 2) 
		return dst

	# --- Laplace --- #
	def laplace(self):
		dst = cv.CreateImage(cv.GetSize(src), cv.IPL_DEPTH_16S, 3)
		cv.Laplace(img, dst)
		return dst

	# --- Seuil --- #
	def threshold(self):
		gray = cv.CreateImage( (img.width, img.height) , cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(img, gray, cv.CV_BGR2GRAY)		
		cv.AdaptiveThreshold(gray,gray,255, cv.CV_ADAPTIVE_THRESH_MEAN_C, cv.CV_THRESH_BINARY_INV, 7, 10)
		#src = cv.LoadImageM(img, cv.CV_LOAD_IMAGE_GRAYSCALE)
		return gray


	# Detection des yeux, nez et bouche
	def detection_eyes(self):
		eyes = cv.HaarDetectObjects(self.img, eye_path, cv.CreateMemStorage())
		return eyes
	def detection_eyes2(self):
		eyes2 = cv.HaarDetectObjects(self.img, eye2_path, cv.CreateMemStorage())
		return eyes2
	def detection_nose(self):
		nose = cv.HaarDetectObjects(self.img, nose_path, cv.CreateMemStorage())
		return nose
	def detection_mouth(self):
		mouth = cv.HaarDetectObjects(self.img, mouth_path, cv.CreateMemStorage())
		return mouth

	def smiles(self):
		res = []
		image = cv.GetSubRect(self.img, (self.img.width*1/7, self.img.height*2/3, self.img.width*5/7, self.img.height/3)) 
		cpt = 0
		for s in all_s:
			temp = cv.HaarDetectObjects(self.img, s, cv.CreateMemStorage())
			res.append(len(temp))
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

	def best_mouth(mouth):
		res = ((0,0,0,0),0) 
		if len(mouth) > 0:
			val = 0
			for (x,y,w,h),n in mouth:
				if y+h > val:
					val = y+h
					res = ((x,y,w,h),n)
		return [res]

	def save(path, nom):
		print "Sauvegarde de l'image:"
		print path+nom
		cv.SaveImage(path+nom, self.img)

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


