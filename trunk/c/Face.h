/*
 * Face.h
 *
 *  Created on: 11 oct. 2010
 *      Author: matthieu
 */
#ifndef FACE_H_
#define FACE_H_
#include <opencv/cv.h>

using namespace cv;
class Face
{
	
protected:
	Rect rect;
	
	bool eyesFound;
	bool mouthFound;
	bool noseFound;
	
	Rect leftEye;
	Rect rightEye;
	Rect mouth;
	Rect nose;
	
public:
	Face(Rect& faceRect);
	virtual ~Face();
	
	Rect& getRect();
	bool hasEyes();
	bool hasMouth();
	bool hasNose();
	
	void setLeftEye(Rect& r);
	Rect& getLeftEye();
	
	void setRightEye(Rect& r);
	Rect& getRightEye();
	
	void setMouth(Rect& r);
	Rect& getMouth();
	
	void setNose(Rect& r);
	Rect& getNose();
	
};
#endif /* FACE_H_ */

