#!/usr/bin/python

import images

def main():

	save = False

	#--- Normalisation --- #
	images.norm_loop("../../images/", "../../norm/")

	# --- Traitements --- #
	images.treatment_loop("../../norm/", "../../traitement/")

	# --- Arff --- #
	for i in range(8,16):
		images.arff_loop("../../traitement/", "fullcorpus_weka_div"+str(i), div=i)


if __name__ == "__main__":
	main()

