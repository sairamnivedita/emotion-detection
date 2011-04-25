#!/usr/bin/python
import sys
import cv
import commands

#java weka.classifiers.functions.MultilayerPerceptron -l model/mlp_all.model -T save_arff/prof.arff -p 0
#export CLASSPATH=$CLASSPATH/usr/share/java/weka.jar

from pyfann import libfann
import face_detect
import images
import webcam
import display
import random

AN = 0
DI = 1
FE = 2
HA = 3
NE = 4
SA = 5
SU = 6
emo_name = ["AN","DI","FE","HA","NE","SA","SU"]
color_code = [display.rouge, display.vert, display.gris, display.jaune, display.noir, display.bleu, display.blanc]
cv.NamedWindow('Photo')
cv.NamedWindow('Norm')
cv.NamedWindow('Percep')
cv.NamedWindow('Thres')
file_name ="cam" 
def reco_et_detourage(img):
    # extrait des visages dans l'image
    faces = images.normalisation(img)
    print "Faces : "
    print faces
    if faces :
        cv.ShowImage('Norm', faces[0][0])
        cv.ShowImage('Percep', images.ce_que_voit_le_perceptron(images.webcam_comptage_pixel(faces[0][0])))
        cv.ShowImage('Thres', images.treatments(faces[0][0]) )
        for face,(x,y,w,h) in faces:
            #cv.SaveImage("../../norm/test"+ str(random.random()) +".jpg" , face)
            cv.Rectangle(img, (x,y), (x+w,y+h), display.clair)
            # On cree ou on rempli le arff avec les images prise par la webcam
            images.webcam_arff(face, file_name, False, div=8)
            liste = commands.getoutput("java weka.classifiers.functions.MultilayerPerceptron -l model/mlp_seuil.model -T ./"+ file_name +".arff -p 0")
            print liste
        cv.ShowImage('Photo', img)
    return img

if __name__ == "__main__":
    webcam.main_loop(key_pressed = reco_et_detourage)

