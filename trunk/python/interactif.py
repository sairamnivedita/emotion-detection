import sys
import cv

from pyfann import libfann
import face_detect
import images
import webcam

AN = 0
DI = 1
FE = 2
HA = 3
NE = 4
SA = 5
SU = 6
emo_name = ["AN","DI","FE","HA","NE","SA","SU"]
color_code = [images.rouge, images.vert, images.gris, images.jaune, images.noir, images.bleu, images.blanc]

def reco_et_detourage(img):
    # extrait des visages dans l'image
    faces = images.normalisation(img, webcam=True)
    for face,(x,y,w,h) in faces:
        cv.Rectangle(img, (x,y), (x+w,y+h), images.clair)
		# On cree ou on rempli le arff avec les images prise par la webcam
		images.webcam_arff(file_name="cam.arff", src, div=8):

    return img

if __name__ == "__main__":
    webcam.main_loop(reco_et_detourage)

