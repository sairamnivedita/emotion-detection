/*
 * Webcam.h
 *
 *  Created on: 20 sept. 2010
 *      Author: matthieu
 */
#ifndef WEBCAM_H_
#define WEBCAM_H_
#include <opencv/cv.h>
#include <opencv/highgui.h>
using namespace cv;
class Webcam {
public:
	Webcam();
	virtual ~Webcam();
	void getImage(Mat& image);
protected:
	CvCapture* capture;
};
#endif /* WEBCAM_H_ */
