
import sys
import cv
#import /usr/lib/pymodules/python2.6/cv.so
 
# le main_loop cree une fenetre et y affiche l'image de la webcam, apres traitement (fonction passe en parametre)
def main_loop(process = None, key_pressed = None):
    
    print "Press ESC to exit ..."
    # creation de la fenetre, redimensionnement automatique
    cv.NamedWindow('Camera')
 
    # webcam ou truc dans le genre
    ###device = -1 # n'importe laquelle
    capture = cv.CreateCameraCapture(0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)    
 
    # si pas de webcam...
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
 
    while 1: 
        # capture de l'image
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
 
        # simulation d'un mirroir
        cv.Flip(frame, None, 1)
        
        # traitement d'image
        if process :
            frame = process(frame)
 
        # display webcam image
        cv.ShowImage('Camera', frame)
 
        # handle events
        k = cv.WaitKey(10)
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            cv.DestroyAllWindows()
            break  
        if k == 0x20: # ESPACE
            print 'ESPACE pressed. Computing.'
            key_pressed(frame)
            break  

if __name__ == "__main__":
    main_loop()
