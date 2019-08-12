from time import sleep as sl
import sys


def convert_from_enterobase(infile,inalleles,MGT1Call):
    """
    Parse metadata downloaded from enterobase
    :param infile: metadata file (can contain any number of isolate rows
    :param inalleles: alleles file use to get strain name from filename to match to metadata file
    :param MGT1Call: 7 gene MLST call
    :return: tab delimited string in MGT order
    """
    inf = open(infile,"r").read().splitlines()

    input_acc = inalleles.split("/")[-1].replace("_alleles.fasta","")

    #TODO make more flexible by matching enterobase headings to MGT headings

    outstringls = ["dbUsername"]

    for i in inf[1:]:
        col = i.split("\t")
        if col[2].startswith(input_acc):  # if the row isolate name matches the name derived from alleles file
            source_lab = col[23]
            Public = "Public"
            MGT_acc = input_acc
            Run_NCBI = input_acc
            MLST = MGT1Call
            if col[9] == "":
                date = ""
            else:
                if len(col[7]) == 4:
                    date = "{}/{}/{}".format(col[9],col[8],col[7][2:])
                else:
                    date = "{}/{}/{}".format(col[9], col[8], col[7])
            year = col[7]
            postcode = ""
            state = col[13]
            country = col[12]
            continent = col[11]
            isolation_source = col[4]
            isolation_source_cor = col[4]
            isolation_type = col[5]
            if col[4] == "Human":
                host = "Homo sapiens"
            else:
                host = ""
            hostdisease = ""
            original_experiment_id = col[1]
            outstringls += [source_lab,Public,MGT_acc,Run_NCBI,MLST,date,year,postcode,state,country,continent,isolation_source,isolation_source_cor,isolation_type,host,hostdisease,original_experiment_id]

    outstring = "\t".join(outstringls)
    return outstring

def convert_from_mgt(isolate_info, InputAllelesFile, MGT1Call):
    """
    Finds metadata line that matches name from alleles file
    """
    inf = open(isolate_info, "r").read().splitlines()
    input_acc = InputAllelesFile.split("/")[-1].replace("_alleles.fasta", "")

    for line in inf:
        if input_acc in line:
            return line



def convert_from_ncbi_pathogens():
    #TODO entrez query?
    print("todo")
