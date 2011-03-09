

#define CV_NO_BACKWARD_COMPATIBILITY
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <iostream>
#include <cstdio>
using namespace std;
using namespace cv;
#include "Webcam.h"
#include "Detection.h"
#include "Face.h"

int main()
{
    //On déclare "un pointeur vers une structure IplImage" :
    //En gros, on "déclare une image".
    IplImage *img2;
    Mat *img;
    //On charge notre image depuis un fichier.
    img2= cvLoadImage("./img.jpg");
    img= Mat(img, true);
    
    vector<Face*>* faces = detection->detectFaces(img);
    
		// Add info in image
		for (vector<Face*>::const_iterator face = faces->begin(); face != faces->end(); face++ )
		{
			Point center;
			Scalar colorFace = CV_RGB(150,150,150);
			Scalar colorEye = CV_RGB(10,200,10);
			Scalar colorMouth = CV_RGB(200,10,10);
			Scalar colorNose = CV_RGB(10,10,200);
			int radius;
			Rect faceRect = (*face)->getRect();
			center.x = cvRound(faceRect.x + faceRect.width*0.5);
			center.y = cvRound(faceRect.y + faceRect.height*0.5);
			radius = cvRound((faceRect.width + faceRect.height)*0.25);
			circle(img, center, radius, colorFace, 2, 8, 0);
			// Eyes
			if ((*face)->hasEyes()) {
				// Left
				Rect& eye = (*face)->getLeftEye();
				eye.x += faceRect.x;
				eye.y += faceRect.y;
	            rectangle(img, eye, colorEye, 1);
	            // Right
	            eye = (*face)->getRightEye();
				eye.x += faceRect.x;
				eye.y += faceRect.y;
	            rectangle(img, eye, colorEye, 1);
			}
			// Mouth
			if ((*face)->hasMouth()) {
				Rect& mouth = (*face)->getMouth();
				mouth.x += faceRect.x;
				mouth.y += faceRect.y;
	            rectangle(img, mouth, colorMouth, 1);
			}
			// Nose
			if ((*face)->hasNose()) {
				Rect& nose = (*face)->getNose();
				nose.x += faceRect.x;
				nose.y += faceRect.y;
	            rectangle(img, nose, colorNose, 1);
			}
		}
    
    //On crée une fenêtre intitulée "Hello World", 
    //La taille de cette fenêtre s'adapte à ce qu'elle contient.
    cvNamedWindow("Hello World", CV_WINDOW_AUTOSIZE);
    
    //On affiche l'image dans la fenêtre "Hello World".
    cvShowImage("Hello World", img);
    
    //On attend que l'utilisateur appuie sur une touche (0 = indéfiniment).
    cvWaitKey(0);
    
    //Destruction de la fenêtre.
    cvDestroyWindow("Hello World");
    
    //Libération de l'IplImage (on lui passe un IplImage**).
    //cvReleaseImage(&img);

    //Fini ^^
    return 0;

}

