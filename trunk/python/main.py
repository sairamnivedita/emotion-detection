#!/usr/bin/python

import images

def main():

	save = False

	#--- Normalisation --- #
	#images.norm_loop("../../images/", "../../norm/")

	# --- Traitements --- #
	images.treatment_loop("../../norm/", "../../traitement/")

	# --- Arff --- #
<<<<<<< .mine
	#for i in range(8,16):
	#	images.arff_loop("../../traitement/", "fullcorpus_weka_div"+str(i), div=i)
=======
	for i in range(2,8):
		images.arff_loop("../../traitement/", "fullcorpus_weka_div"+str(i), div=i)
>>>>>>> .r56


if __name__ == "__main__":
	main()

