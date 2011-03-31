import sys
import cv

from pyfann import libfann
import face_detect
import webcam
import utils

AN = 0
DI = 1
FE = 2
HA = 3
NE = 4
SA = 5
SU = 6
emo_name = ["AN","DI","FE","HA","NE","SA","SU"]
color_code = [utils.rouge, utils.vert, utils.gris, utils.jaune, utils.noir, utils.bleu, utils.blanc]

multilayer_perceptron = libfann.neural_net()

def reco_et_detourage(img):
    # extrait des visages dans l'image
    faces = face_detect.find_faces_and_normalize(img)
    for face,(x,y,w,h) in faces:
        cv.Rectangle(img, (x,y), (x+w,y+h), utils.clair)

        print "Detection de trucs dans un visages trouves"
        Input = face_detect.detection_pour_classification(face)
        Input += face_detect.comptage_pixel_sur_image(face) # concat liste

        #detection d'emotion
        Output = multilayer_perceptron.run(Input)
        print Output
        # affichage :
        for emo in range(7):
            if Output[emo] > 0 :
                cv.Rectangle(img, (x-emo,y-emo), (x+w+emo,y+h+emo), color_code[emo])
                print "\nemotion detecte : " + emo_name[emo]
                
    return img

if __name__ == "__main__":
    multilayer_perceptron.create_from_file("./emo_detect.net")
    # 
    webcam.main_loop(reco_et_detourage)

