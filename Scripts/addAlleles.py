import sys
import glob
import re
import readAppSettAndConnToDb
from Bio import SeqIO
import addToTableInOrgDb
import getFromTableInOrgDb

################################# TOP_LVL

def addAlleles(projectPath, projectName, appName, dir_alleleSeqs):

	# setting up the appClass
	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
	organismAppClass = readAppSettAndConnToDb.importAppClassModels(appName)

	# print (dir_seqsToSaveTo)
	dir_seqsToSaveTo = readAppSettAndConnToDb.importAlleleDirFromSettings(projectName)

	# for each file in the folder

	extractAndAddAlleles(organismAppClass, dir_alleleSeqs, projectPath, appName, dir_seqsToSaveTo)


def extractAndAddAlleles(organismAppClass, dir_alleleSeqs, projectPath, appName, dir_seqsToSaveTo):

	fns = glob.glob(dir_alleleSeqs + "*")

	for fn in fns:
		seqs_iterator = SeqIO.parse(fn, "fasta")

		for seqRec in seqs_iterator:
			[locusId, alleleId] = re.split(":", seqRec.id)

			# print (locusId, alleleId)
			if not doesAlleleExistInDb(organismAppClass, locusId, alleleId):
				seqFileLoc = appendSeqToFile(appName, dir_seqsToSaveTo, locusId, seqRec)

				# print (seqRec.seq)
				# print (len(seqRec.seq))
				addAlleleToDb(organismAppClass, locusId, alleleId, len(seqRec.seq), False, seqFileLoc)

			else:
				print("Allele already in db, not added: " + locusId + " " + alleleId)

			# print(locusId, alleleId)

def appendSeqToFile(appName, alleleSeqDirName, locusId, seqRec):
	arr = re.split("\:", seqRec.id)
	alleleName = arr[0]

	fn_ = alleleSeqDirName + appName + "/" + alleleName + ".fasta"
	print (fn_)
	# (seqRec.id)
	with open(fn_, 'a') as fh:
		SeqIO.write(seqRec, fh, "fasta")
		print("Seq. appended to: " + fn_)


	return fn_



def addAlleleToDb(organismAppClass, locusId, alleleId, seqLen, hasSnp, fileLocation):
	locusObj = getFromTableInOrgDb.getLocus(organismAppClass, locusId)

	addToTableInOrgDb.addAllele(organismAppClass, alleleId, locusObj, seqLen, hasSnp, fileLocation)



def doesAlleleExistInDb(organismAppClass, locusId, alleleId):

	set_allele = organismAppClass.models.Allele.objects.filter(locus=locusId, identifier=alleleId)

	if len(set_allele) == 0:
		# sys.stderr.write("Locus: " + locusId + ", Alelle: " + alleleId + " not found in db." + '\n')
		return False

	return True

	# except:
	# 	sys.stderr.write("Locus: " + locusId + ", Alelle: " + alleleId + " not found in db." + '\n')


################################# MAIN


def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_

def main():
	usage = "python3 scripty.py <projectPath> <projectName> <appName> <alleleSeqsFolder>"
	if len(sys.argv) != 5:
		sys.exit("Error: incorrect number of inputs\n" + usage + '\n\n')

	sys.argv[4] = addSlashIfNotThere(sys.argv[4])

	addAlleles(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
