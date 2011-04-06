#!/usr/bin/python

import images

def main():

	save = False

	#--- Normalisation --- #
	#images.norm_loop("../../images/", "../../norm/")

	# --- Traitements --- #
	#images.treatment_loop("../../norm/", "../../traitement/")

	# --- Arff --- #
	images.arff_loop("../../traitement/", "weka", div=8)


if __name__ == "__main__":
	main()

