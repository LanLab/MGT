import re
import sys

import readAppSettAndConnToDb
import addToTableInOrgDb
import getFromTableInOrgDb


Fn_sql = "runOnDb.sql"
Fn_viewClass = "autoGenView"


################################# MAIN

def doGen(projectPath, projectName, appName, dbWebsiteUserName):
	readAppSettAndConnToDb.setupEnvPath(projectPath, projectName)
	appClass = readAppSettAndConnToDb.importAppClassModels(appName)

	doThePrinting(appClass, appName, dbWebsiteUserName)

################################# AUX

def doThePrinting(appClass, appName, dbWebsiteUserName):

	# getAllApTns
	# getAllCcTns

	qs_apTns = getFromTableInOrgDb.getApTns(appClass, 0)
	qs_ccTns = getFromTableInOrgDb.getCcTns(appClass)

	fh_sql = open(Fn_sql, "w+")
	printTheSqlFile(qs_apTns, qs_ccTns, appName, dbWebsiteUserName, fh_sql)
	fh_sql.close()

	fh_class = open(Fn_viewClass, "w+")
	printTheClassfile(fh_class, qs_apTns, qs_ccTns, appName)
	fh_class.close()


##################################### PRINT THE CLASS FILE
def printTheClassfile(fh_class, qs_apTns, qs_ccTns, appName):

	fh_class.write("class View_apcc(models.Model):\n")

	fh_class.write(tabs(1) + "mgt = models.OneToOneField(Mgt, primary_key=True, on_delete=models.DO_NOTHING)\n")

	for apTn in qs_apTns:
		fh_class.write(tabs(1) + apTn.table_name + " = " + intField() + "\n")
		fh_class.write(tabs(1) + apTn.table_name + "_st = " + intField() + "\n")
		fh_class.write(tabs(1) + apTn.table_name + "_dst = " + intField() + "\n")

	for apTn in qs_apTns:

		ccTnsInSch = getCcTnsForScheme(apTn.scheme, qs_ccTns)

		for ccTn in ccTnsInSch:
			fh_class.write(tabs(1) + ccFnForDjango(ccTn.display_table, ccTn.display_order) + " = " + intField() + '\n')

			fh_class.write(tabs(1) + cc_currForDjango(ccTn.display_table, ccTn.display_order) + " = " + intField() + '\n')


	fh_class.write('\n\n')
	fh_class.write(tabs(1) + "class Meta:\n")
	fh_class.write(tabs(2) + "managed = False\n")
	fh_class.write(tabs(2) + "db_table = " + viewTnInDb(appName) + '\n')



def intField():
	return "models.IntegerField()"


def tabs(num):
	tabStr = ""
	for i in range(0, num):
		tabStr = tabStr + "\t"

	return tabStr

##################################### PRINT THE SQL FILE

def printTheSqlFile(apTnObjs, ccTnObjs, appName, dbWebsiteUserName, fh_sql):

	counter_tNum = 1

	fh_sql.write('CREATE OR REPLACE VIEW' + '\n')
	fh_sql.write(viewTnInDb(appName) + ' AS' + '\n')
	fh_sql.write('WITH' + '\n')

	counter_apTns = 0

	for apTn in apTnObjs:
		# SELECT

		# print ap
		printSelect_ap(fh_sql, apTn.display_order, apTn.table_name)
		# print cc
		ccTnsInSch = getCcTnsForScheme(apTn.scheme, ccTnObjs)

		if len(ccTnsInSch) ==  1:
			ccTn = ccTnsInSch[0]

			printSelect_cc(fh_sql, ccTn.table_name, ccTn.display_table, ccTn.display_order)

			fh_sql.write('\n')

			# FROM
			fh_sql.write("FROM ")
			fh_sql.write(dbCcTn(appName, ccTn.table_name) + " " + ccTn.table_name + " " + rojoin() + " " + dbApTn(appName, apTn.table_name) + " " + apTn.table_name)

			fh_sql.write("\n")
			fh_sql.write("ON ")

			fh_sql.write(apsCcCol(apTn.table_name, ccTn.table_name)  + " = " + ccTn.table_name + ".identifier")

		else:


			for ccTn in ccTnsInSch:
				printSelect_cc(fh_sql, ccTn.table_name, ccTn.display_table, ccTn.display_order)

			fh_sql.write('\n')

			fh_sql.write("FROM ")
			fh_sql.write(dbApTn(appName, apTn.table_name)+ " " + apTn.table_name)

			dict_isSeenCcTn = dict()
			for ccTn in ccTnsInSch:
				if isInDictIfNotAdd(dict_isSeenCcTn, ccTn.table_name):
					continue
				fh_sql.write("\n" + lojoin() + " \"" + appName + "_" + ccTn.table_name + "\" " + ccTn.table_name)
				fh_sql.write("\nON " + apsCcCol(apTn.table_name, ccTn.table_name) +  " = " + ccTn.table_name + ".identifier")

		if counter_apTns < len(apTnObjs) - 1:
			fh_sql.write(")," + '\n')
		else:
			fh_sql.write(")" + '\n')


		counter_apTns = counter_apTns + 1

	fh_sql.write("select mgt.id mgt_id,\n")

	# SELECT PART 2.
	for apTn in apTnObjs:
		fh_sql.write(tNum(apTn.display_order) + "." + apTn.table_name + ", t" + str(apTn.display_order) + "." + apTn.table_name + "_st" + ", t" + str(apTn.display_order) + "." +  apTn.table_name + "_dst," + "\n")

	counter_ap = 0
	for apTn in apTnObjs:

		ccTnsInSch = getCcTnsForScheme(apTn.scheme, ccTnObjs)

		counter_cc = 0
		for ccTn in ccTnsInSch:
			fh_sql.write(tNum(apTn.display_order) + ".")

			fh_sql.write(ccFnForDjango(ccTn.display_table, ccTn.display_order))

			fh_sql.write(", ")
			fh_sql.write(tNum(apTn.display_order) + ".")
			fh_sql.write(cc_currForDjango(ccTn.display_table, ccTn.display_order))

			if counter_ap != len(apTnObjs) - 1 or counter_cc != len(ccTnsInSch) - 1:
				fh_sql.write(",\n")

			counter_cc = counter_cc + 1

		# sys.stdout.write("\n")
		counter_ap = counter_ap + 1

	fh_sql.write("\nfrom \"" + appName + "_mgt\" as mgt ")

	counter_ap = 0
	for apTn in apTnObjs:

		fh_sql.write(lojoin() + " " + tNum(apTn.display_order) + "\n")
		fh_sql.write("on " + "mgt." + apTn.table_name + "_id = "+ tNum(apTn.display_order) + "." + apTn.table_name)

		if counter_ap != len(apTnObjs) - 1:
			fh_sql.write("\n")
		else:
			fh_sql.write(";\n\n")

		counter_ap = counter_ap + 1

	printGrantAccess(fh_sql, appName, dbWebsiteUserName)

def printGrantAccess(fh_sql, appName, dbWebsiteUserName):
	fh_sql.write("grant select on " + viewTnInDb(appName) + " to " + dbWebsiteUserName + ";\n\n")



def isInDictIfNotAdd(dict_, ccTn):

	if ccTn in dict_:
		return True

	dict_[ccTn] = ""

	return False



def viewTnInDb(appName):
	return "\"" + appName + "_view_apcc\""

def apsCcCol(aptn, cctn):
	return aptn + "." + cctn + "_id"

def cc_currForDjango(tableNum, dispOrd):
	return ccFnForDjango(tableNum, dispOrd) + "_merge"

def ccFnForDjango(tableNum, dispOrd):
	return "cc" + str(tableNum) + "_" + str(dispOrd)

def dbApTn(appName, aptn):
	return "\"" + appName + "_" + aptn + "\""

def dbCcTn(appName, cctn):
	return "\"" + appName + "_" + cctn + "\""

def tNum(dispOrd):
	return ("t" + str(dispOrd))

def lojoin():
	return "LEFT OUTER JOIN"

def rojoin():
	return "RIGHT OUTER JOIN"



def printSelect_cc(fh_sql, tn, displayTab, displayOrd):
	fh_sql.write(", " + tn + ".identifier "  + "cc" + str(displayTab) + "_" + str(displayOrd) + ", " + tn + ".merge_id_id " + "cc" + str(displayTab) + "_" + str(displayOrd) + "_merge")


def printSelect_ap(fh_sql, tNum, tn):

	fh_sql.write('t' + str(tNum) +  ' as' + " (SELECT " + tn + ".id " + tn + ", " + tn + ".st " + tn + "_st, " + tn + ".dst " + tn + "_dst")


def getCcTnsForScheme(sch, ccTnObjs):

	list_ccObjsForSch = list()

	for ccTn in ccTnObjs:
		if ccTn.scheme == sch:
			list_ccObjsForSch.append(ccTn)

	return list_ccObjsForSch



################################# MAIN

def addSlashIfNotThere(dir_):
	if not re.search(".*/$", dir_):
		dir_ = dir_ + "/"

	return dir_


def main():

	usage = "python3 script.py <projectPath> <projectName> <appName> <dbMlstWebsiteUsername>"

	if len(sys.argv) != 5:
		sys.stderr.write("Error: incorrect number of input arguments\n" + usage + '\n\n')
		sys.exit()

	sys.argv[1] = addSlashIfNotThere(sys.argv[1])

	doGen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
