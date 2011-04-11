import sys
import cv
#export CLASSPATH=$CLASSPATH/usr/share/java/weka.jar
#java weka.classifiers.functions.MultilayerPerceptron -l model/mlp_all.model -T save_arff/prof.arff -p

from pyfann import libfann
import face_detect
import images
import webcam
import display

AN = 0
DI = 1
FE = 2
HA = 3
NE = 4
SA = 5
SU = 6
emo_name = ["AN","DI","FE","HA","NE","SA","SU"]
color_code = [display.rouge, display.vert, display.gris, display.jaune, display.noir, display.bleu, display.blanc]

def reco_et_detourage(img):
    # extrait des visages dans l'image
    faces = images.normalisation(img, webcam=True)
    for face,(x,y,w,h) in faces:
        cv.Rectangle(img, (x,y), (x+w,y+h), display.clair)
        # On cree ou on rempli le arff avec les images prise par la webcam
        images.webcam_arff(img, div=8, file_name="cam.arff")

    return img

if __name__ == "__main__":
    webcam.main_loop(key_pressed = reco_et_detourage)

