
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
def affichage_corners(dcorners, img, diametre):
	for (x,y) in dcorners:
		cv.Circle(img, (x,y), diametre, rouge, -1)
def affichage(src, deyes, deyes2, dnose, dmouth, a=0, b=0):
	affichage_eyes(deyes, src, a,b)
	affichage_eyes2(deyes2, src, a,b)
	affichage_nose(dnose, src, a,b)
	affichage_mouth(dmouth, src, a,b)


