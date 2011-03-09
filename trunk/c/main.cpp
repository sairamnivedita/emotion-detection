/*
 * main.cpp
 *
 *  Created on: 14 sept. 2010
 *      Author: matthieu
 */
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
int main( int argc, const char** argv )
{
    Webcam * webcam = new Webcam();
    Mat img;
    Detection * detection = new Detection();
    // Creates the preview window
    cvNamedWindow( "result", 1 );
	for (;;)
	{
		webcam->getImage(img);
		// Detect faces
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
		// Show in window
		cv::imshow("result", img);
		// End
		if( waitKey( 10 ) >= 0 )
			goto _cleanup_;
	}
	// Release resources
	waitKey(0);
_cleanup_:
    cvDestroyWindow("result");
    return 0;
}

void detectAndDraw( Mat& img,
                   CascadeClassifier& cascade, CascadeClassifier& nestedCascade,
                   double scale)
{
    int i = 0;
    double t = 0;
    vector<Rect> faces;
    const static Scalar colors[] =  { CV_RGB(0,0,255),
        CV_RGB(0,128,255),
        CV_RGB(0,255,255),
        CV_RGB(0,255,0),
        CV_RGB(255,128,0),
        CV_RGB(255,255,0),
        CV_RGB(255,0,0),
        CV_RGB(255,0,255)} ;
    Mat gray, smallImg( cvRound (img.rows/scale), cvRound(img.cols/scale), CV_8UC1 );
    cvtColor( img, gray, CV_BGR2GRAY );
    resize( gray, smallImg, smallImg.size(), 0, 0, INTER_LINEAR );
    equalizeHist( smallImg, smallImg );
    t = (double)cvGetTickCount();
    cascade.detectMultiScale( smallImg, faces,
        1.1, 2, 0
        |CV_HAAR_FIND_BIGGEST_OBJECT
        //|CV_HAAR_DO_ROUGH_SEARCH
        //|CV_HAAR_SCALE_IMAGE
        ,
        Size(30, 30) );
    t = (double)cvGetTickCount() - t;
    printf( "detection time = %g ms\n", t/((double)cvGetTickFrequency()*1000.) );
    for( vector<Rect>::const_iterator r = faces.begin(); r != faces.end(); r++, i++ )
    {
        Mat smallImgROI;
        vector<Rect> nestedObjects;
        Point center;
        Scalar color = colors[i%8];
        int radius;
        center.x = cvRound((r->x + r->width*0.5)*scale);
        center.y = cvRound((r->y + r->height*0.5)*scale);
        radius = cvRound((r->width + r->height)*0.25*scale);
        circle( img, center, radius, color, 3, 8, 0 );
        if( nestedCascade.empty() )
            continue;
        smallImgROI = smallImg(*r);
        nestedCascade.detectMultiScale( smallImgROI, nestedObjects,
            1.1, 2, 0
            //|CV_HAAR_FIND_BIGGEST_OBJECT
            //|CV_HAAR_DO_ROUGH_SEARCH
            //|CV_HAAR_DO_CANNY_PRUNING
            |CV_HAAR_SCALE_IMAGE
            ,
            Size(30, 30) );
        for( vector<Rect>::const_iterator nr = nestedObjects.begin(); nr != nestedObjects.end(); nr++ )
        {
            center.x = cvRound((r->x + nr->x + nr->width*0.5)*scale);
            center.y = cvRound((r->y + nr->y + nr->height*0.5)*scale);
            radius = cvRound((nr->width + nr->height)*0.25*scale);
            circle( img, center, radius, color, 3, 8, 0 );
        }
    }
    cv::imshow( "result", img );
}
