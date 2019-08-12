import sys
import re
import os
from Bio import SeqIO
import readAppSettAndConnToDb
import addToTableInOrgDb
import getFromTableInOrgDb

#################### CHANGE_IF_REQ.

ID = 0
POS_START = 1
POS_END = 2
ORIENTATION = 3
CHROMOSOME = 4


##################### TOP_LVL

def populateLoci(projectPath, projectName, appName, lociTabFile):

	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
	organismDjangoClass = readAppSettAndConnToDb.importAppClassModels(appName)


	dict_chrFileLocs = getChrSeqFilePaths(organismDjangoClass) # multiple paths due to being on multiple chromosomes
	# print(dict_chrFileLocs)

	# dirName_alleleSeqs = readAppSettAndConnToDb.getAlleleFolderName()

	dir_alleles = readAppSettAndConnToDb.importAlleleDirFromSettings(projectName)

	# dir_alleles = dir_alleles + appName + '/'
	# print (dir_alleles)


	dir_alleleSeqsBase = dir_alleles
	dir_alleleSeqsOrg = dir_alleleSeqsBase + appName + "/"
	print (dir_alleleSeqsOrg)

	createFolderIfDoesNotExist(dir_alleleSeqsBase)
	createFolderIfDoesNotExist(dir_alleleSeqsOrg);

	# print (dir_alleleSeqsOrg)
	extractSeqsAndWrite(dict_chrFileLocs, lociTabFile, dir_alleleSeqsOrg, organismDjangoClass)


def createFolderIfDoesNotExist(dirName):

	if not os.path.isdir(dirName):
		os.mkdir(dirName)

####################### AUXILLARY_SEQ_EXTRACTION

def getChrSeqFilePaths(appClass):

	chrs = appClass.models.Chromosome.objects.all()

	dict_chrFileLocs = dict()

	for chr in chrs:
		dict_chrFileLocs[chr.number] = str(chr.file_location)

		# print(dict_chrFileLocs[chr.number])

	return dict_chrFileLocs


def extractSeqsAndWrite(dict_chrFileLocs, lociTabFile, dir_alleleSeqsOrg, organismDjangoClass):

	numSeqsExtracted = 0

	for chrNum in dict_chrFileLocs:



		numSeqsExtracted = extractSeqsInChr(chrNum, dict_chrFileLocs[chrNum], lociTabFile, numSeqsExtracted, dir_alleleSeqsOrg, organismDjangoClass)


	if not areAllExtracted(numSeqsExtracted, lociTabFile):

		sys.exit("Error: not all sequences extracted!")


def areAllExtracted(numSeqsExtracted, lociTabFile):
	num_lines = sum(1 for line in open(lociTabFile))

	print("Total count: " + str(num_lines) + "\t" + str(numSeqsExtracted))

	if int(numSeqsExtracted) == int(num_lines):
		return True

	return False



def extractSeqsInChr(chrNum, chrFileLoc, lociTabFile, numSeqsExtracted, dir_alleleSeqsOrg, organismDjangoClass):
	genomeSeqObj = loadChromosomeForExtraction(chrFileLoc)

	chrObj = getFromTableInOrgDb.getChromosome(organismDjangoClass, chrNum)

	with open(lociTabFile, 'r') as fh_:
		for line in fh_:
			line = line.rstrip()

			arr = re.split("\t+", line)

			if int(arr[CHROMOSOME]) == int(chrNum):
				# get seq from genome and write to settings.ALLELES_DIR location
				loci_id = arr[ID] + ":1" # re.sub("\t+", "|", line)
				# print(loci_id)


				fn_seqSaved = getLocusObjAndWriteFasta(dir_alleleSeqsOrg, genomeSeqObj, arr[ID], int(arr[POS_START]), int(arr[POS_END]), arr[ORIENTATION], loci_id)


				# add loci obj to db
				locus = addToTableInOrgDb.addLocus(organismDjangoClass, arr[ID], arr[POS_START], arr[POS_END], arr[ORIENTATION], chrObj, None)


				# add allele obj with id 1 to db

				seq_length = int(arr[POS_END]) - int(arr[POS_START]) + 1
				allele = addToTableInOrgDb.addAllele(organismDjangoClass, 1, locus, seq_length, False, fn_seqSaved)

				numSeqsExtracted = numSeqsExtracted + 1

	return numSeqsExtracted


def getLocusObjAndWriteFasta(dir_alleleSeqsOrg, genomeSeqObj, loci_id, loc_start, loc_end, orientation, loci_seq_id):
	lociObj = getTheSeq(genomeSeqObj, loc_start, loc_end, orientation)

	lociObj.id = loci_seq_id

	print (lociObj.id)


	lociObj.name = ""
	lociObj.description = ""

	seqName = re.sub("\.+", "_", loci_id)

	fn_seqSaved = str(dir_alleleSeqsOrg) + seqName + ".fasta"

	SeqIO.write(lociObj, fn_seqSaved, "fasta")
	print("Seq. written to: " + fn_seqSaved)

	return fn_seqSaved



def getTheSeq(genomeSeqObj, locStart, locEnd, orientation):

	lociObj = genomeSeqObj[locStart-1:locEnd]

	# print(seq)
	if orientation == '-':
		# print("reversing")
		lociObj.seq = lociObj.seq[::-1].complement()
	# 	lociObj.seq

	return lociObj


def loadChromosomeForExtraction(chrFileLoc):
	obj = SeqIO.parse(chrFileLoc, "fasta")
	for genomeSeq in obj:
		return genomeSeq

################################ MAIN

def main():
	usage = "python3 script.py <projectPath> <projectName> <appName> <referenceInfoFile.json>\n\n"
	if (len(sys.argv) != 5):
		sys.exit("Error: incorrect number of inputs\n" + usage)


	populateLoci(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
