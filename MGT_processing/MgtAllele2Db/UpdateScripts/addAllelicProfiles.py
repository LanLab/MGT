import sys
import re
from MGT_processing.MgtAllele2Db.UpdateScripts import getFromTableInOrgDb, readAppSettAndConnToDb, addToTableInOrgDb
from MGT_processing.MgtAllele2Db.UpdateScripts.genModelDefsForApsAndHgt import PGS_COL_LIMIT
import math


##################################### TOP_LVL
# def doAddAllelicProfiles(projectPath, projectName, appName, profile_dict):
#     """
#
#     :param projectPath:
#     :param projectName: Mgt
#     :param appName: Salmonella
#     :param fn_schemeToApMapping: file with MGTX \t MGTx_gene_profiles.txt
#     :param dir_allelicProfs: folder where above gene profiles can be found
#     :return:
#     """
#
#     # setting up the appClass
#
#
#     loadAndAddAps(organismAppClass, fn_schemeToApMapping, dir_allelicProfs, appName, projectPath)


##################################### AUX

# def loadAndAddAps(orgAppClass, fn_mapping, dir_apFiles, appName, projectPath):
#     with open(fn_mapping, 'r') as fh_:
#         for line in fh_:
#             line = line.strip()
#             [schemeName, fileName] = line.split("\t")
#
#             addApForScheme(orgAppClass, schemeName, dir_apFiles + fileName, appName, projectPath)

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

def addApForScheme(projectPath,projectName, appName, schemeName, profile_dict,st,dst,nodash_to_dash):
    readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
    orgAppClass = readAppSettAndConnToDb.importAppClassModels(appName)

    list_tableNameClass = getTableClasses(orgAppClass, schemeName, appName, projectPath)
    schObj = getFromTableInOrgDb.getScheme(orgAppClass, schemeName)
    lociNames_sorted = getLociNamesSorted(schObj)

    # print("HELLO",len(lociNames_sorted))
    # print(list_tableNameClass)

    locus_ids_list_o_lists = list(chunks(lociNames_sorted, 1000))

    alleles_ls = []
    for locuslis in locus_ids_list_o_lists:
        nlis = []
        for locus in locuslis:
            locus = nodash_to_dash[locus]
            nlis.append(profile_dict[locus])
        alleles_ls.append(nlis)

    # print("1")
    # for i in locus_ids_list_o_lists:
    #     print(len(i),i)
    # print("2")
    # for i in alleles_ls:
    #     print(len(i), i)

    #for addToDb() need lociNames_sorted = list of lists of loci ids = [[l1,l2,l3...][l1001,l1002....]]
    # also need equivalent list of allele assignments = alleles_ls = [[1,2,1,...][-1_1,4,....]]

    #TODO check when adding that allele + locus ids are used NOT unique allele id...

    # print("pre addToDb")
    # print(st, dst, locus_ids_list_o_lists)

    addToDb(list_tableNameClass, st, dst, locus_ids_list_o_lists, alleles_ls)
    # print("post addToDb")
    # isHeader = True
    # with open(pathAndFileName, 'r') as fh_:
    #     for line in fh_:
    #
    #         line = line.strip()
    #         arr = line.split("\t")
    #
    #         if isHeader == True:
    #             (col_st, col_dst, list_colNames) = getHeaderCols(arr, pathAndFileName)
    #
    #             isHeader = False
    #             continue
    #
    #         (st, dst) = getAlleleList(arr, col_st, col_dst)
    #
    #         # list_lociQueries = genQueryList(lociNames_sorted, list_colNames, arr)
    #         (list_namesSplit, list_alleleValsSplit) = splitTheLists(lociNames_sorted, list_colNames, arr)
    #         addToDb(list_tableNameClass, st, dst, list_namesSplit, list_alleleValsSplit)

        # print (list_lociQueries)


def addToDb(list_tableNameClass, st, dst, list_namesSplit, list_alleleValsSplit):
    table_0_obj = None
    st = str(st)
    dst = str(dst)
    for i in range(0, len(list_tableNameClass)):
        if i == 0:
            # print("p1 pre")
            # print(st,dst)
            table_0_obj = addToTableInOrgDb.addAllelicProfileStrToTable(list_tableNameClass[i], list_namesSplit[i],
                                                                        list_alleleValsSplit[i], st, dst, None)


        else:
            # print("p2 pre")
            addToTableInOrgDb.addAllelicProfileStrToTable(list_tableNameClass[i], list_namesSplit[i],
                                                          list_alleleValsSplit[i], None, None, table_0_obj)



def splitTheLists(lociNames_sorted, header_colNames, arrVals):
    list_namesSplit = list()  # contains as many lists as tableNums # TODO: this is a bit redundant (needs only be done once) - can speed up script.

    list_alleleValsSplit = list()  # contains as many lists as table Num (values, in order, correspond to the namesSplit)

    list_tmpNames = list()
    list_tmpAlleleVals = list()

    tbNum = 0
    for i in range(0, len(lociNames_sorted)):
        newTbNum = math.floor(i / PGS_COL_LIMIT)
        if tbNum != newTbNum:
            # then add the temp lists to the overAll list

            list_namesSplit.append(list_tmpNames)
            list_alleleValsSplit.append(list_tmpAlleleVals)

            list_tmpNames = list()
            list_tmpAlleleVals = list()

            tbNum = newTbNum

        idx = getIndexForVal(header_colNames, lociNames_sorted[i])

        list_tmpNames.append(lociNames_sorted[i])
        list_tmpAlleleVals.append(arrVals[idx])

    list_namesSplit.append(list_tmpNames)
    list_alleleValsSplit.append(list_tmpAlleleVals)

    return (list_namesSplit, list_alleleValsSplit)


def getIndexForVal(header_colNames, lociName):
    return header_colNames.index(lociName)


def getLociNamesSorted(schObj):
    lociNames = list()

    lociObjs_sorted = getFromTableInOrgDb.getLociSortedInSchemeNoDb(schObj)

    for lociObj in lociObjs_sorted:
        lociName = re.sub("\_", "", lociObj.identifier)
        lociNames.append(lociName)

    return lociNames


def getAlleleList(arrLine, col_st, col_dst):
    if col_st > col_dst:
        st = arrLine.pop(col_st)
        dst = arrLine.pop(col_dst)
    else:  # dst > st
        dst = arrLine.pop(col_dst)
        st = arrLine.pop(col_st)

    return (st, dst)


def getHeaderCols(arrLine, pathAndFileName):
    col_st = -1
    col_dst = -1

    list_colNames = list()

    for i in range(0, len(arrLine)):
        if re.match("^st$", arrLine[i], flags=re.I):
            col_st = i
        elif re.match("^dst$", arrLine[i], flags=re.I):
            col_dst = i
        else:
            arrLine[i] = re.sub("\_", "", arrLine[i])
            list_colNames.append(arrLine[i])

    if (col_st == -1 or col_dst == -1):
        sys.exit("Error: file " + pathAndFileName + " header does not contain st or dst\n\n")

    return (col_st, col_dst, list_colNames)


def getTableClasses(orgAppClass, schemeName, appName, projectPath):
    tnObjs = getFromTableInOrgDb.getTabNamesSorted(orgAppClass, schemeName)
    list_tnClasses = list()

    for tnObj in tnObjs:
        # print(tnObj.table_name)

        tableClass = readAppSettAndConnToDb.importTableName(projectPath, appName, tnObj.table_name)
        list_tnClasses.append(tableClass)

    return list_tnClasses


##################################### MAIN
# def addSlashIfNotThere(dir_):
#     if not re.search(".*/$", dir_):
#         dir_ = dir_ + "/"
#
#     return dir_


# def main():
#     usage = "python3 script.py <projectPath> <projectName> <appName> <allelicProfileInfoFile> <allelicProfileCalculatedDir>"
#
#     if len(sys.argv) != 6:
#         sys.exit("Error: incorrect number of inputs\n" + usage + '\n\n')
#
#     sys.argv[1] = addSlashIfNotThere(sys.argv[1])
#     sys.argv[5] = addSlashIfNotThere(sys.argv[5])
#
#     doAddAllelicProfiles(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
#
#
# if __name__ == '__main__':
#     main()
