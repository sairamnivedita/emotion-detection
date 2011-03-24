#!/usr/bin/python
import utils

class treatments:

	def __init__(self, img)
		self.img = img

	def normalisation():	

		# On fait une copie l'image pour le traitement (en gris)
		gray = cv.CreateImage( (img.width, img.height) , cv.IPL_DEPTH_8U, 1)
		normal = cv.CreateImage((utils.NORM_W,utils.NORM_H), cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(img, gray, cv.CV_BGR2GRAY)		

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
	def corners():
		eig_img = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
		temp_img = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
		corners = cv.GoodFeaturesToTrack(dst, eig_img, temp_img, 100, 0.04, 1.0, useHarris = True)
		#utils.affichage_corners(corners, img, 2) 
		return dst

	# --- Laplace --- #
	def laplace():
		dst = cv.CreateImage(cv.GetSize(src), cv.IPL_DEPTH_16S, 3)
		cv.Laplace(img, dst)
		return dst

	# --- Seuil --- #
	def threshold():

		gray = cv.CreateImage( (img.width, img.height) , cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(img, gray, cv.CV_BGR2GRAY)		
		cv.AdaptiveThreshold(gray,gray,255, cv.CV_ADAPTIVE_THRESH_MEAN_C, cv.CV_THRESH_BINARY_INV, 7, 10)
		#src = cv.LoadImageM(img, cv.CV_LOAD_IMAGE_GRAYSCALE)
		return gray

