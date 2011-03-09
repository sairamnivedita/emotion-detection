/*
 * Detection.cpp
 *
 *  Created on: 19 sept. 2010
 *      Author: matthieu
 */
#include "Detection.h"
/**
 * Constructor
 */
Detection::Detection() {
	// Filename
	String cascadeNameFace = "../haarcascades/haarcascade_frontalface_alt.xml";
	String cascadeNameEyes = "../haarcascades/haarcascade_eye.xml";
	String cascadeNameEyes2 = "../haarcascades/haarcascade_eye_tree_eyeglasses.xml";
	String cascadeNameMouth = "../haarcascades/haarcascade_mcs_mouth.xml";
	String cascadeNameNose = "../haarcascades/haarcascade_mcs_nose.xml";
	scale = 1;
	// Load cascades
	if (! cascadeFace.load(cascadeNameFace)) {
		cerr << "ERROR: Could not load face cascade" << endl;
	}
	if (! cascadeEyes.load(cascadeNameEyes)) {
        cerr << "ERROR: Could not load eyes cascade" << endl;
	}
	if (! cascadeEyes2.load(cascadeNameEyes2)) {
        cerr << "ERROR: Could not load eyes cascade 2" << endl;
	}
	if (! cascadeMouth.load(cascadeNameMouth)) {
        cerr << "ERROR: Could not load mouth cascade" << endl;
	}
	if (! cascadeNose.load(cascadeNameNose)) {
        cerr << "ERROR: Could not load nose cascade" << endl;
	}
}
Detection::~Detection() {
}
/**
 * Detect faces inside the image
 */
vector<Face*>* Detection::detectFaces(Mat& img)
{
    vector<Rect> facesRect;
    vector<Face*>* faces = new vector<Face*>();
    Mat gray;
    Mat smallImg(cvRound(img.rows/scale), cvRound(img.cols/scale), CV_8UC1);
    // Prepare the image
    cvtColor( img, gray, CV_BGR2GRAY );
    resize( gray, smallImg, smallImg.size(), 0, 0, INTER_LINEAR );
    equalizeHist( smallImg, smallImg );

    // Detection
    cascadeFace.detectMultiScale( smallImg, facesRect,
        1.2, 3,
        0
        |CV_HAAR_FIND_BIGGEST_OBJECT
        //|CV_HAAR_DO_ROUGH_SEARCH
        //|CV_HAAR_SCALE_IMAGE
        ,
        Size(70, 70) );
    // For each face
    for (unsigned int i=0; i<facesRect.size(); i++)
    {
    	// Image of the face
    	Mat imgFace = smallImg(facesRect[i]);
    	
    	// Detect eyes in top half of the face
    	Rect eyesROIRect = Rect(
			0,
			facesRect[i].height/6,
			facesRect[i].width,
			facesRect[i].height/3
		);
    	Mat eyesROI = imgFace(eyesROIRect);
    	vector<Rect>* eyes = detectEyes(eyesROI);
    	
    	// Detect mouth in bottom third of the face
    	Rect mouthROIRect = Rect(
    		facesRect[i].width/5,
			facesRect[i].height*2/3,
			facesRect[i].width*3/5,
			facesRect[i].height/3
		);
    	Mat mouthROI = imgFace(mouthROIRect);
    	Rect* mouth = detectMouth(mouthROI);
    	
    	// Detect nose in middle fourth of the face
    	Rect noseROIRect = Rect(
    		facesRect[i].width/4,
			facesRect[i].height/4,
			facesRect[i].width/2,
			facesRect[i].height/2
		);
    	Mat noseROI = imgFace(noseROIRect);
    	Rect* nose = detectNose(noseROI);
    	
    	// Add to the face array
    	Face* f = new Face(facesRect[i]);
    	// Eyes
    	if (2 == eyes->size()) {
    		eyes->at(0).y += eyesROIRect.y;
    		eyes->at(1).y += eyesROIRect.y;
    		if (eyes->at(0).x < eyes->at(1).x) {
        		f->setLeftEye(eyes->at(0));
        		f->setRightEye(eyes->at(1));
    		} else {
        		f->setLeftEye(eyes->at(1));
        		f->setRightEye(eyes->at(0));
    		}
    	}
    	// Mouth
    	if (mouth != NULL) {
    		mouth->x += mouthROIRect.x;
    		mouth->y += mouthROIRect.y;
    		f->setMouth(*mouth);
    	}
    	// Nose
    	if (nose != NULL) {
    		nose->x += noseROIRect.x;
    		nose->y += noseROIRect.y;
    		f->setNose(*nose);
    	}
    	faces->push_back(f);
    }
    return faces;
}
/**
 * Detects eyes inside the image
 */
vector<Rect>* Detection::detectEyes(Mat& img)
{
    vector<Rect>* eyesRect = new vector<Rect>();
    // Detection
    cascadeEyes.detectMultiScale( img, *eyesRect,
        1.1, 2,
        0
        //|CV_HAAR_FIND_BIGGEST_OBJECT
        //|CV_HAAR_DO_ROUGH_SEARCH
        //|CV_HAAR_DO_CANNY_PRUNING
        |CV_HAAR_SCALE_IMAGE
        ,
        Size(30, 30) );
    if (2 != eyesRect->size())
    {
    	// Try to detect with the alternative cascade
        cascadeEyes2.detectMultiScale( img, *eyesRect,
            1.1, 2,
            0
            //|CV_HAAR_FIND_BIGGEST_OBJECT
            //|CV_HAAR_DO_ROUGH_SEARCH
            //|CV_HAAR_DO_CANNY_PRUNING
            |CV_HAAR_SCALE_IMAGE
            ,
            Size(30, 30) );
    	if (2 == eyesRect->size())
    	{
        	cout << "Eyes found with the alternative cascade" << endl;
        }
    }
	if (2 != eyesRect->size())
	{
    	cout << "Error eyes number : " << eyesRect->size() << endl;
    	eyesRect->empty();
    }
    return eyesRect;
}
/**
 * Detects the mouth inside the image
 */
Rect* Detection::detectMouth(Mat& img)
{
    vector<Rect>* mouthRect = new vector<Rect>();
    // Detection
    cascadeMouth.detectMultiScale( img, *mouthRect,
        1.1, 2,
        0
        //|CV_HAAR_FIND_BIGGEST_OBJECT
        //|CV_HAAR_DO_ROUGH_SEARCH
        //|CV_HAAR_DO_CANNY_PRUNING
        |CV_HAAR_SCALE_IMAGE
        ,
        Size(40, 30) );
    if (1 != mouthRect->size())
    {
    	cout << "Error mouth number : " << mouthRect->size() << endl;
    	return NULL;
    }
    return &mouthRect->at(0);
}
/**
 * Detects the nose inside the image
 */
Rect* Detection::detectNose(Mat& img)
{
    vector<Rect>* nosesRect = new vector<Rect>();
    // Detection
    cascadeNose.detectMultiScale( img, *nosesRect,
        1.1, 2,
        0
        //|CV_HAAR_FIND_BIGGEST_OBJECT
        //|CV_HAAR_DO_ROUGH_SEARCH
        //|CV_HAAR_DO_CANNY_PRUNING
        |CV_HAAR_SCALE_IMAGE
        ,
        Size(30, 30) );
    if (1 != nosesRect->size())
    {
    	cout << "Error nose number : " << nosesRect->size() << endl;
    	return NULL;
    }
    return &nosesRect->at(0);
}

