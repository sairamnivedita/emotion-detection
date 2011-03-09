/*
 * Detection.h
 *
 *  Created on: 19 sept. 2010
 *      Author: matthieu
 */
#ifndef DETECTION_H_
#define DETECTION_H_
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <iostream>
#include <cstdio>
#include "Face.h"
using namespace std;
using namespace cv;
/**
 * Object detection in images
 */
class Detection
{
	
protected:
	CascadeClassifier cascadeFace;
	CascadeClassifier cascadeEyes;
	CascadeClassifier cascadeEyes2;
	CascadeClassifier cascadeMouth;
	CascadeClassifier cascadeNose;
	double scale;
	
public:
	Detection();
	virtual ~Detection();
	vector<Face*>* detectFaces(Mat& img);
	
protected:
	vector<Rect>* detectEyes(Mat& img);
	Rect* detectMouth(Mat& img);
	Rect* detectNose(Mat& img);
	
};
#endif /* DETECTION_H_ */
