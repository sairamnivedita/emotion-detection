
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
def display_visage((x,y,w,h), img, a=0, b=0):
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


