#!/usr/bin/python

import cv, os, sys
import commands

# Chemin vers les cascades et les visages
path = "../haarcascades/"
corpus = "../faces/"
# cascades recherchees :
frontal_face = "haarcascade_frontalface_default.xml"
eyes = "haarcascade_eye.xml";
eyes2 = "haarcascade_eye_tree_eyeglasses.xml";
mouth = "haarcascade_mcs_mouth.xml";
nose = "haarcascade_mcs_nose.xml";
cascades_files = [frontal_face, eyes, eyes2, mouth, nose]
all_smiles = map( (lambda x : cv.Load(path+x)),cascades_files)

# cascade sourire
smile_1 = "smileD/smiled_01.xml"
smile_2 = "smileD/smiled_02.xml"
smile_3 = "smileD/smiled_03.xml"
smile_4 = "smileD/smiled_04.xml"
smile_5 = "smileD/smiled_05.xml" 
all_smiles_file = [ smile_1, smile_2, smile_3, smile_4, smile_5 ]
all_smiles = map( (lambda x : cv.Load(path+x)), all_smiles_file)

# BLEU VERT ROUGE !
bleu  = (255,0,0)
vert  = (0,255,0)
jaune = (0,255,255)
rose  = (255,186,185)
rouge = (0,0,255)
gris  = (128,128,128)
noir  = (0,0,0)
blanc = (255,255,255)
clair = (192,192,192)
sombre = (64,64,64)

                
# Automatisation du cadrage des visages sur les photos en .jpg (contenu dans le dossier)
def auto():
   liste = commands.getoutput("ls \""+ corpus+"\" | grep .jpg")
   liste = liste.split()
   #print liste
   return liste

#Function to detect and draw any faces that is present in an image
def detect_and_draw(liste):
   liste_sans_visage = []
   for image in liste:
      print image
      #img = cv.LoadImage(corpus + image, 1)
      #On extrait le visage
      
      liste = extracteur_de_visages(image,1)
      if liste == [] : liste_sans_visage.append(image)
      
      #extracteur_de_visage2(image)
      #On dessine le visage extrait
      #cv.Rectangle(img, (x,y), (x+w,y+h), bleu)
      #cv.SaveImage("../../result/face_"+image, img)
   for image in liste_sans_visage :
      print "Pas de visage VU dans " + image

# extrait les visages detecte d'une image
# USAGE : extracteur_de_visage(img, 0) renvoie les coordonnes
# USAGE : extracteur_de_visage(img, 1) renvoie la photo du visage extrait 
def extracteur_de_visages(image, boolean) :

      img_scale = 1
      src = cv.LoadImage(corpus+image, 1)
      img = cv.CreateImage( (src.width/img_scale, src.height/img_scale) , 8, 1)
      cv.CvtColor(src, img, cv.CV_BGR2GRAY )          
      faces = cv.HaarDetectObjects(img, face, cv.CreateMemStorage())

      liste = []
      
      for (x,y,w,h),n in faces: 
               tmp = cv.CreateImage( (w,h) , 8, 1)
               cv.GetRectSubPix(img, tmp, (float(x + w/2), float(y + h/2)))
               cv.EqualizeHist( tmp, tmp )
               
               #Detection oeil nez bouche :
               deyes = cv.HaarDetectObjects(tmp, ceye, cv.CreateMemStorage())
               deyes2 = cv.HaarDetectObjects(tmp, ceye2, cv.CreateMemStorage())
               dnoses = cv.HaarDetectObjects(tmp, cnose, cv.CreateMemStorage())
               dmouth = cv.HaarDetectObjects(tmp, cmouth, cv.CreateMemStorage())
               if ( len(dmouth) == 1 or len(deyes) + len(deyes2) >= 2 
                    or len(dnoses) == 1 ) : 
                    if(boolean) :
                        cv.SaveImage("../result/smallface_"+str(len(liste))+ image, tmp)
                    liste.append((x,y,w,h))
               detect_smile(image, tmp)
      return liste
      
def detect_smile(nom, img) :
   cpt = 0
   for smile in all_smiles :
      res = cv.HaarDetectObjects(img, smile, cv.CreateMemStorage())
      if len(res) >= 1 :
         cpt = cpt + 1     
   if cpt == len( all_smiles) :     
      cv.SaveImage("../result/smile/" + str(cpt) + "smile_" + nom, img)
           

def extracteur_de_visage2(image) :
    img_scale = 1
    src = cv.LoadImage(image, 1)
    img = cv.CreateImage( (src.width/img_scale, src.height/img_scale) , 8, 1)
    cv.CvtColor(src, img, cv.CV_BGR2GRAY )          
    faces = cv.HaarDetectObjects(img, face, cv.CreateMemStorage())
    
    cpt = 0
    for (x,y,w,h),n in faces: 
            cpt=cpt+1
            tmp = cv.CreateImage( (w,h) , 8, 1)
            cv.GetRectSubPix(img, tmp, (float(x + w/2), float(y + h/2)))
            cv.EqualizeHist( tmp, tmp )
            cv.SaveImage("../result/smallface_"+ str(cpt)+image, tmp)

def main():
        liste = auto()
        detect_and_draw(liste)

if __name__ == "__main__":
        main()

