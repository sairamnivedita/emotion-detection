/*
 * Face.cpp
 *
 *  Created on: 11 oct. 2010
 *      Author: matthieu
 */
#include "Face.h"
Face::Face(Rect& faceRect) {
	eyesFound = false;
	mouthFound = false;
	noseFound = false;
	rect = faceRect;
}
Face::~Face() {
}
Rect& Face::getRect() {
	return rect;
}
bool Face::hasEyes() {
	return eyesFound;
}
bool Face::hasMouth() {
	return mouthFound;
}
bool Face::hasNose() {
	return noseFound;
}
void Face::setLeftEye(Rect& r) {
	eyesFound = true;
	leftEye = r;
}
Rect& Face::getLeftEye() {
	return leftEye;
}
void Face::setRightEye(Rect& r) {
	eyesFound = true;
	rightEye = r;
}
Rect& Face::getRightEye() {
	return rightEye;
}
void Face::setMouth(Rect& r) {
	mouthFound = true;
	mouth = r;
}
Rect& Face::getMouth() {
	return mouth;
}
void Face::setNose(Rect& r){
 noseFound = true;
 nose = r;
}
Rect& Face::getNose(){
  return nose;
}
