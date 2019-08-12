from time import sleep as sl
import argparse

from addIsolates import addInfo
import psycopg2
import csv
import sys
from os import path
import os
import shutil

folder = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(folder)

from Mgt.Mgt import settings

sys.path.remove(folder)


"""
Col_username = 0
Col_projectName = 1
Col_privStatus = 2
Col_isolateId = 3

## Meta data fields

Col_date = 6 # file isolate_metadata_.txt
Col_year = 7
Col_postcode = 8 # file isolate_info.txt
Col_state = 9 # file isolate_info.txt
Col_country = 10 # file isolate_info.txt
Col_continent = 11 # file isolate_info.txt

Col_source = 13 # file isolate_metadata_.txt
Col_type = 14 # file isolate_metadata_.txt
Col_host = 15 # file isolate_metadata_.txt
Col_hostDisease = 16 # file isolate_metadata_.txt


"""

def parseargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i","--inmeta", help="input tsv file in mgt format")
    parser.add_argument("-r","--readsfolder",
                        help="Folder containing reads (*_1.fastq.gz and *_2.fastq.gz) where *=Col_isolateId in inmeta",
                        required=True)
    parser.add_argument("--appname", help="App name", default="Salmonella")
    parser.add_argument("--projectPath", help="Path to project folder")
    parser.add_argument("--projectName", help="Name of project",
                        default="Mgt")


    args = parser.parse_args()


    return args

def sqlquery_to_outls(con, query):
    """
    Run sql query string with supplied connection and return results as a list of tuples
    :param con: psycopg2 sql connection object
    :param query: sql query string
    :return: sql query results (which are in a list of tuples)
    one tuple for each row returned and each tuple with the selected columns
    """
    cur = con.cursor()  # generate cursor with connection
    cur.execute(query)  # execute the sql query
    res = cur.fetchall()  # get results and save to res as list
    cur.close()  # close cursor
    return res


def get_isolate_info(args,conn,strainname):
    reads_query = """ SELECT "id","identifier","project_id" FROM "{}_isolate" WHERE "identifier" = '{}'; """.format(
        args.appname,strainname)
    res = sqlquery_to_outls(conn, reads_query)

    idno = res[0][0]
    projno = res[0][2]

    return idno,projno



def add_reads(args,conn,uploads):

    reader = open(args.inmeta, 'r').read().splitlines()

    for line in reader[1:]:
        col = line.split("\t")
        strain_id = col[3]
        user_id = col[0]

        fq1 = args.readsfolder + "/" + strain_id + "_1.fastq.gz"
        fq2 = args.readsfolder + "/" + strain_id + "_2.fastq.gz"


        idno,projno = get_isolate_info(args,conn,strain_id)

        fqbase = "/{}/{}/{}/{}/".format(args.appname, user_id, projno, idno)

        if path.exists(fq1) and path.exists(fq2):

            if not path.exists(uploads + fqbase):
                os.makedirs(uploads + fqbase)

            newf1 = uploads + fqbase + "/" + strain_id + "_1.fastq.gz"
            newf2 = uploads + fqbase + "/" + strain_id + "_2.fastq.gz"

            if not path.exists(newf1):
                shutil.copy2(fq1, newf1)
            else:
                os.remove(newf1)
                shutil.copy2(fq1, newf1)

            if not path.exists(newf2):
                shutil.copy2(fq2, newf2)
            else:
                os.remove(newf2)
                shutil.copy2(fq2, newf2)

            f1db = "{}{}_1.fastq.gz".format(fqbase, strain_id)
            f2db = "{}{}_2.fastq.gz".format(fqbase, strain_id)

            reads_query = """ UPDATE "{0}_isolate" SET "server_status" = 'U' WHERE "identifier" = '{1}';
                              UPDATE "{0}_isolate" SET "file_forward" = '{2}' WHERE "identifier" = '{1}';
                              UPDATE "{0}_isolate" SET "file_reverse" = '{3}' WHERE "identifier" = '{1}';""".format(
                args.appname, strain_id, f1db, f2db)
            print(strain_id, "read paths added, status set to U")

            cur = conn.cursor()  # generate cursor with connection
            cur.execute(reads_query)
            cur.close()
        else:
            print("1 or more reads for isolate {} missing or not in correct format (name_1.fastq.gz)".format(strain_id))



def main():
    args = parseargs()

    uploads = settings.MEDIA_ROOT.replace("..","/") + "/"

    database = settings.APPS_DATABASE_MAPPING[args.appname]

    args.database = database

    psql_details = settings.DATABASES[database]

    args.psqldb = psql_details['NAME']

    DbConString = "dbname='{0}' host='{1}' port='{2}' user='{3}' password='{4}'".format(psql_details['NAME'],psql_details['HOST'],psql_details['PORT'],psql_details['USER'],psql_details['PASSWORD'])  ## connection info for Db - assign new user that can only do what is needed for script

    conn = psycopg2.connect(DbConString)
    conn.autocommit = True


    addInfo(args.projectPath, args.projectName,args.appname,args.inmeta)

    add_reads(args,conn,uploads)


if __name__ == '__main__':
    main()
