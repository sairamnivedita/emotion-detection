/*
 * Webcam.cpp
 *
 *  Created on: 20 sept. 2010
 *      Author: matthieu
 */
#include "Webcam.h"
Webcam::Webcam() {
	capture = cvCaptureFromCAM(0);
}
Webcam::~Webcam() {
	cvReleaseCapture(&capture);
}
void Webcam::getImage(Mat& image) {
    Mat frame;
    IplImage* iplImg = cvQueryFrame(capture);
    frame = iplImg;
    if (frame.empty()) {
    	throw std::string("Error : No frame captured");
    }
    if (iplImg->origin == IPL_ORIGIN_TL) {
        frame.copyTo( image );
    }
    else {
        flip(frame, image, 0);
    }
}
