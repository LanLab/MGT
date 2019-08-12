from time import sleep as sl
import argparse
from pylatex import Document, Section, Subsection, Command, LongTabu, Tabu, MultiColumn, TikZ, Axis, Plot, Figure, SubFigure, FlushLeft, MiniPage
from pylatex.utils import italic, NoEscape, bold
import pandas as pd
from uuid import uuid1




import psycopg2

from os import path,remove
import sys

folder = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(folder)

from Mgt import settings

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

import matplotlib.gridspec as gridspec


"""
TODO

input limits on what should be reported

time range, country, continent, (my strains only - for user report)


Report structure so far:

Summary of input/settings

Number of isolates clustered at desired cutoff

graphs of clusters > X in size




"""



def country_standard():
    country_abbrev = {
        'Andorra': 'AN',
        'United Arab Emirates': 'AE',
        'Afghanistan': 'AF',
        'Antigua and Barbuda': 'AC',
        'Anguilla': 'AV',
        'Albania': 'AL',
        'Armenia': 'AM',
        'Angola': 'AO',
        'Antarctica': 'AY',
        'Argentina': 'AR',
        'American Samoa': 'AQ',
        'Austria': 'AU',
        'Australia': 'AS',
        'Aruba': 'AA',
        'Azerbaijan': 'AJ',
        'Bosnia and Herzegovina': 'BK',
        'Barbados': 'BB',
        'Bangladesh': 'BG',
        'Belgium': 'BE',
        'Burkina Faso': 'UV',
        'Bulgaria': 'BU',
        'Bahrain': 'BA',
        'Burundi': 'BY',
        'Benin': 'BN',
        'Saint Barthalemy': 'TB',
        'Bermuda': 'BD',
        'Brunei': 'BX',
        'Bolivia': 'BL',
        'Brazil': 'BR',
        'Bahamas': 'BF',
        'Bhutan': 'BT',
        'Bouvet Island': 'BV',
        'Botswana': 'BC',
        'Belarus': 'BO',
        'Belize': 'BH',
        'Canada': 'CA',
        'Cocos Islands': 'CK',
        'Democratic Republic of the Congo': 'CG',
        'Central African Republic': 'CT',
        'Republic of the Congo': 'CF',
        'Switzerland': 'SZ',
        'Ivory Coast': 'IV',
        'Cook Islands': 'CW',
        'Chile': 'CI',
        'Cameroon': 'CM',
        'China': 'CH',
        'Colombia': 'CO',
        'Costa Rica': 'CS',
        'Cuba': 'CU',
        'Cape Verde': 'CV',
        'Curacao': 'UC',
        'Christmas Island': 'KT',
        'Cyprus': 'CY',
        'Czech Republic': 'EZ',
        'Germany': 'GM',
        'Djibouti': 'DJ',
        'Denmark': 'DA',
        'Dominica': 'DO',
        'Dominican Republic': 'DR',
        'Algeria': 'AG',
        'Ecuador': 'EC',
        'Estonia': 'EN',
        'Egypt': 'EG',
        'Western Sahara': 'WI',
        'Eritrea': 'ER',
        'Spain': 'SP',
        'Ethiopia': 'ET',
        'Finland': 'FI',
        'Fiji': 'FJ',
        'Falkland Islands': 'FK',
        'Micronesia': 'FM',
        'Faroe Islands': 'FO',
        'France': 'FR',
        'Gabon': 'GB',
        'United Kingdom': 'UK',
        'England': 'UK',
        'Scotland': 'UK',
        'Wales': 'UK',
        'Grenada': 'GJ',
        'Georgia': 'GG',
        'French Guiana': 'FG',
        'Guernsey': 'GK',
        'Ghana': 'GH',
        'Gibraltar': 'GI',
        'Greenland': 'GL',
        'Gambia': 'GA',
        'Guinea': 'GV',
        'Guadeloupe': 'GP',
        'Equatorial Guinea': 'EK',
        'Greece': 'GR',
        'South Georgia and the South Sandwich Islands': 'SX',
        'Guatemala': 'GT',
        'Guam': 'GQ',
        'Guinea-Bissau': 'PU',
        'Guyana': 'GY',
        'Hong Kong': 'HK',
        'Heard Island and McDonald Islands': 'HM',
        'Honduras': 'HO',
        'Croatia': 'HR',
        'Haiti': 'HA',
        'Hungary': 'HU',
        'Indonesia': 'ID',
        'Ireland': 'EI',
        'Israel': 'IS',
        'Isle of Man': 'IM',
        'India': 'IN',
        'British Indian Ocean Territory': 'IO',
        'Iraq': 'IZ',
        'Iran': 'IR',
        'Iceland': 'IC',
        'Italy': 'IT',
        'Jersey': 'JE',
        'Jamaica': 'JM',
        'Jordan': 'JO',
        'Japan': 'JA',
        'Kenya': 'KE',
        'Kyrgyzstan': 'KG',
        'Cambodia': 'CB',
        'Kiribati': 'KR',
        'Comoros': 'CN',
        'Saint Kitts and Nevis': 'SC',
        'North Korea': 'KN',
        'South Korea': 'KS',
        'Kosovo': 'KV',
        'Kuwait': 'KU',
        'Cayman Islands': 'CJ',
        'Kazakhstan': 'KZ',
        'Laos': 'LA',
        'Lebanon': 'LE',
        'Saint Lucia': 'ST',
        'Liechtenstein': 'LS',
        'Sri Lanka': 'CE',
        'Liberia': 'LI',
        'Lesotho': 'LT',
        'Lithuania': 'LH',
        'Luxembourg': 'LU',
        'Latvia': 'LG',
        'Libya': 'LY',
        'Morocco': 'MO',
        'Monaco': 'MN',
        'Moldova': 'MD',
        'Montenegro': 'MJ',
        'Saint Martin': 'RN',
        'Madagascar': 'MA',
        'Marshall Islands': 'RM',
        'Macedonia': 'MK',
        'Mali': 'ML',
        'Myanmar': 'BM',
        'Mongolia': 'MG',
        'Macao': 'MC',
        'Northern Mariana Islands': 'CQ',
        'Martinique': 'MB',
        'Mauritania': 'MR',
        'Montserrat': 'MH',
        'Malta': 'MT',
        'Mauritius': 'MP',
        'Maldives': 'MV',
        'Malawi': 'MI',
        'Mexico': 'MX',
        'Malaysia': 'MY',
        'Mozambique': 'MZ',
        'Namibia': 'WA',
        'New Caledonia': 'NC',
        'Niger': 'NG',
        'Norfolk Island': 'NF',
        'Nigeria': 'NI',
        'Nicaragua': 'NU',
        'Netherlands': 'NL',
        'Norway': 'NO',
        'Nepal': 'NP',
        'Nauru': 'NR',
        'Niue': 'NE',
        'New Zealand': 'NZ',
        'Oman': 'MU',
        'Panama': 'PM',
        'Peru': 'PE',
        'French Polynesia': 'FP',
        'Papua New Guinea': 'PP',
        'Philippines': 'RP',
        'Pakistan': 'PK',
        'Poland': 'PL',
        'Saint Pierre and Miquelon': 'SB',
        'Pitcairn': 'PC',
        'Puerto Rico': 'RQ',
        'Palestinian Territory': 'WE',
        'Portugal': 'PO',
        'Palau': 'PS',
        'Paraguay': 'PA',
        'Qatar': 'QA',
        'Reunion': 'RE',
        'Romania': 'RO',
        'Serbia': 'RI',
        'Russia': 'RS',
        'Rwanda': 'RW',
        'Saudi Arabia': 'SA',
        'Solomon Islands': 'BP',
        'Seychelles': 'SE',
        'Sudan': 'SU',
        'South Sudan': 'OD',
        'Sweden': 'SW',
        'Singapore': 'SN',
        'Saint Helena': 'SH',
        'Slovenia': 'SI',
        'Svalbard and Jan Mayen': 'SV',
        'Slovakia': 'LO',
        'Sierra Leone': 'SL',
        'San Marino': 'SM',
        'Senegal': 'SG',
        'Somalia': 'SO',
        'Suriname': 'NS',
        'Sao Tome and Principe': 'TP',
        'El Salvador': 'ES',
        'Sint Maarten': 'NN',
        'Syria': 'SY',
        'Swaziland': 'WZ',
        'Turks and Caicos Islands': 'TK',
        'Chad': 'CD',
        'French Southern Territories': 'FS',
        'Togo': 'TO',
        'Thailand': 'TH',
        'Tajikistan': 'TI',
        'Tokelau': 'TL',
        'East Timor': 'TT',
        'Turkmenistan': 'TX',
        'Tunisia': 'TS',
        'Tonga': 'TN',
        'Turkey': 'TU',
        'Trinidad and Tobago': 'TD',
        'Tuvalu': 'TV',
        'Taiwan': 'TW',
        'Tanzania': 'TZ',
        'Ukraine': 'UP',
        'Uganda': 'UG',
        'United States': 'US',
        'United States of America': 'US',
        'USA': 'US',
        'Uruguay': 'UY',
        'Uzbekistan': 'UZ',
        'Vatican': 'VT',
        'Saint Vincent and the Grenadines': 'VC',
        'Venezuela': 'VE',
        'British Virgin Islands': 'VI',
        'U.S. Virgin Islands': 'VQ',
        'Vietnam': 'VM',
        'Vanuatu': 'NH',
        'Wallis and Futuna': 'WF',
        'Samoa': 'WS',
        'Yemen': 'YM',
        'Mayotte': 'MF',
        'South Africa': 'SF',
        'Zambia': 'ZA',
        'Zimbabwe': 'ZI',
        'Serbia and Montenegro': 'YI',
        'Netherlands Antilles': 'NT',
    }

    for long,short in country_abbrev.values():
        country_abbrev[short] = short
    return country_abbrev


class Multistrain(Document):
    def __init__(self,fontclass):
        super().__init__()
        self.preamble.append(Command('usepackage', fontclass))
        self.preamble.append(NoEscape(r'\usepackage{float}'))

        # geometry_options = {
        #     "margin": "0.5in",
        #     "bottom": "0.6in",
        # }
        #
        # self.preamble.append(Command('geometry_options', "margin=0.5in"))

        self.preamble.append(NoEscape(r'\usepackage[margin = 0.5in, head = 1in, bottom = 1in]{geometry}'))
        self.preamble.append(NoEscape(r'\usepackage[export]{adjustbox}'))

        # self.preamble.append(NoEscape(r'\usepackage{geometry}\geometry{a4paper,total={170mm,257mm},left=20mm,top=20mm}'))
        self.preamble.append(Command('title', 'Multilocus Sequence Typing Report for multiple isolates'))
        # self.preamble.append(Command('author', 'Anonymous author'))
        self.preamble.append(Command('date', NoEscape(r'\today')))
        self.append(NoEscape(r'\maketitle'))

    def fill_document(self):
        """Add a section, a subsection and some text to the document."""
        with self.create(Section('A section')):
            self.append('Some regular text and some ')
            self.append(italic('italic text. '))

            with self.create(Subsection('A subsection')):
                self.append('Also some crazy characters: $&#{}')


def get_merge_odclis(connection, odc, odclev,db,oldlev):
    # print(cc)

    conv = {"1": '1', "2": '2', "5": '3', "10": '4'}

    # odclev = conv[odclev]

    sqlquery = """ SELECT DISTINCT "cc2_{1}","cc2_{1}_merge" 
    FROM "{0}_view_apcc"
    WHERE ("cc2_{1}" in ('{2}') OR "cc2_{1}_merge" in ('{2}'));""".format(db, odclev, "','".join(odc))

    tuplelis = sqlquery_to_outls(connection, sqlquery)
    # print("tuplelis", tuplelis)
    tmpls = [x[0] for x in tuplelis] + [x[1] for x in tuplelis]
    # print("tmppls1",tmpls)
    tmpls = list(set(map(str, tmpls)))
    # print("tmppls2", tmpls)

    tmpls = [x for x in tmpls if x != "None"]

    if len(tmpls) == 0:
        sys.exit("There is no ODC {} for level {}".format(odc,oldlev))

    # print("tmppls3", tmpls)
    cclis = []
    for i in tmpls:
        if i not in cclis:
            cclis.append(i)

    # print(cclis)

    sqlquery = """ SELECT DISTINCT "cc2_{1}","cc2_{1}_merge" 
    FROM "{0}_view_apcc" 
    WHERE ("cc2_{1}" in ('{2}') OR "cc2_{1}_merge" in ('{2}'));""".format(db, odclev, "','".join(cclis))

    tuplelis = sqlquery_to_outls(connection, sqlquery)
    # print("tuplelis", tuplelis)
    tmpls = [x[0] for x in tuplelis] + [x[1] for x in tuplelis]
    # print("tmppls1",tmpls)
    tmpls = list(set(map(str, tmpls)))
    # print("tmppls2", tmpls)

    tmpls = [x for x in tmpls if x != "None"]

    # print("tmppls3", tmpls)
    cclis = []
    for i in tmpls:
        if i not in cclis:
            cclis.append(i)

    # print(cclis)

    cclis = ",".join(cclis)

    return cclis

def get_merge_cclis(connection, cc, level,db):
    """
    Gather all CCs that merge with the input CC then gather all CCs that merge with those CCs and return as list
    :param connection: sql connection
    :param cc: input clonal complex to check for merges
    :param level: MGT level
    :param db: database name (= args.psql)
    :return: comma joined list of clonal complexes of original and merges of input cc
    """
    #  Round one cc retreival - get any cc that input cc merges to or that merge to the input cc and store in list
    sqlquery = """ SELECT DISTINCT "identifier","merge_id_id" 
    FROM "{0}_cc1_{1}" 
    WHERE ("identifier" in ('{2}') OR "merge_id_id" in ('{2}'));""".format(db, level, "','".join(cc))

    tuplelis = sqlquery_to_outls(connection, sqlquery)
    # print(cc)
    # print(tuplelis)

    tmpls = [x[0] for x in tuplelis] + [x[1] for x in tuplelis]
    tmpls = list(set(map(str, tmpls)))
    tmpls = [x for x in tmpls if x != "None"]
    tmpls = [x for x in tmpls if x != ""]

    if len(tmpls) == 0:
        sys.exit("There is no CC {} for level {}".format(cc,level))



    cclis = []
    for i in tmpls:
        if i not in cclis:
            cclis.append(i)
    # print(cclis)
    #  Round two cc retreival - get any cc that round 1 ccs merges to or that merge to the round 1 ccs and store in list
    sqlquery = """ SELECT DISTINCT "identifier","merge_id_id" 
    FROM "{0}_cc1_{1}" 
    WHERE ("identifier" in ('{2}') OR "merge_id_id" in ('{2}'));""".format(db, level, "','".join(cclis))

    tuplelis = sqlquery_to_outls(connection, sqlquery)
    tmpls = [x[0] for x in tuplelis] + [x[1] for x in tuplelis]
    tmpls = list(set(map(str, tmpls)))
    tmpls = [x for x in tmpls if x != "None"]
    tmpls = [x for x in tmpls if x != ""]

    cclis = []
    for i in tmpls:
        if i not in cclis:
            cclis.append(i)
    # print(cclis)
    cclis = ",".join(cclis)

    return cclis

def mgt_from_assignments(args,conn,identifier=""):

    if identifier == "":
        identifier = args.identifier

    mgts = []

    if args.stlev:
        st = identifier
        level = args.stlev
        # print("st and level:",st,level)

        sqlq = """ SELECT "mgt_id","ap{1}_0_st" FROM "{0}_view_apcc" WHERE "ap{1}_0_st" = '{2}'; """.format(args.appname,level,st)


        res = sqlquery_to_outls(conn,sqlq)

        mgts = {str(x[0]):str(x[1]) for x in res}

        if len(mgts) == 0:
            sys.exit("There is no ST {} for level {}".format(st, level))

        ## get st,cc,odcs from "Salmonella_view_apcc" and get strain names from "Salmonella_isolate" by matching mgts

    elif args.cclev:
        cc = [identifier]

        level = args.cclev
        # print("cc and level:", cc, level)
        cclis = get_merge_cclis(conn,cc,level,args.appname).split(",")

        # print(cclis)

        sqlq = """ SELECT "mgt_id","cc1_{1}" FROM "{0}_view_apcc" WHERE "cc1_{1}" IN ('{2}'); """.format(args.appname, level, "','".join(cclis))

        res = sqlquery_to_outls(conn, sqlq)

        mgts = {str(x[0]):str(x[1]) for x in res}
        ## get st,cc,odcs from "Salmonella_view_apcc" and get strain names from "Salmonella_isolate" by matching mgts

    elif args.odclev:
        odc = [identifier]
        odclev = args.odclev
        # print("odc and level:",odc,odclev)

        conv = {"1": '1', "2": '2', "5": '3', "10": '4'}

        codclev = conv[odclev]

        odclis = get_merge_odclis(conn,odc, codclev,args.appname,odclev).split(",")

        # print(odclis)

        sqlq = """ SELECT "mgt_id","cc2_{1}" FROM "{0}_view_apcc" WHERE "cc2_{1}" IN ('{2}'); """.format(args.appname, codclev, "','".join(odclis))

        res = sqlquery_to_outls(conn, sqlq)

        mgts = {str(x[0]):str(x[1]) for x in res}
        ## get st,cc,odcs from "Salmonella_view_apcc" and get strain names from "Salmonella_isolate" by matching mgts


    sqlq = """ SELECT "identifier","mgt_id" FROM "{0}_isolate" WHERE "mgt_id" IN ('{1}') """.format(args.appname, "','".join(mgts.keys()))
    out = sqlquery_to_outls(conn, sqlq)

    mgtdict = {}
    ids = []
    for x in out:
        id = x[0]
        mgtid = str(x[1])
        mgtdict[id] = (mgtid,mgts[mgtid]) # (mgt_id, identifier matching that id for current analysis i.e. 34.2 for st or 6 for CC)
        ids.append(id)

    return ids,mgtdict

def parseargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a',
                       '--appname',
                       help="Name of the MGT app to use", default="Salmonella")


    parser.add_argument('-f',
                       '--file',
                       help="a file with strain names to examine, one per line. will be ignored if -i is set")

    parser.add_argument('-l',
                       '--list',
                       help="a comma separated list of isolate names i.e. strainA,strainB,strainC,will be ignored if -i is set")

    parser.add_argument('-i',
                       '--identifier',
                       help="comma separated list of one or more identifiers for st,cc or odc. i.e. 3 for ST 3 i MGT4 if --stlev 4.")
    time = parser.add_mutually_exclusive_group()
    time.add_argument("-r",
                        "--range",
                        help="range of dates in yyyy-mm-dd,yyyy-mm-dd format or one date in yyyy-mm-dd",
                        default="all")

    time.add_argument("-y",
                        "--year",
                        help="range of years yyyy,yyyy format or a single year in yyyy format",
                        default="all")

    parser.add_argument('--country',
                       help="Country the isolates should come from",
                       default="all")

    parser.add_argument('--continent',
                       help="Continent the isolates should come from",
                       default="all")

    parser.add_argument('--postcode',
                       help="list of postcode separates by , i.e. 2344,6134,1234",
                       default="all")

    parser.add_argument('--disease',
                       help="list of diseases , i.e. Salmonella gastroenteritis",
                       default="all")

    parser.add_argument('--source',
                       help="source of isolate, i.e. hominine,Miscellaneous Food,Avian",
                       default="all")

    parser.add_argument('--sourcetype',
                       help="type of source, either 'clinical' or 'environmental/other'",
                       default="all")

    parser.add_argument('--clustermin',
                       help="smallest cluster size to include in report",
                       default=2)

    parser.add_argument('--host',
                       help="host species, i.e. 'Gallus gallus', 'homo sapiens'",
                       default="all")

    parser.add_argument("--postgresdbname",
                        help="name of postgres database (warning may be different to website db option)",
                        default="salmonella")

    parser.add_argument("--port",
                        help="port for postgres connection",
                        default='5433')

    parser.add_argument("--postgresuser",
                        help="postgres user login",
                        default='postgres')

    parser.add_argument("--postgrespass",
                        help="Password for postgres database",
                        default="P8ppacre!")
                        # required=True)

    parser.add_argument("--postgreshost",
                        help="host adress for postgres access",
                        default="0.0.0.0")
                        # required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--stlev',
                       help="sequence type level. Mutually exclusive to --cc,--odc")
    group.add_argument('--cclev',
                       help="clonal complex level. Mutually exclusive to --seqtype,--odc")
    group.add_argument('--odclev',
                       help="odc cutoff. Mutually exclusive to --seqtype,--cc")


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

def build_query(args,isolatelist):

    if args.odclev:
        conv = {"1": '1', "2": '2', "5": '3', "10": '4'}
        levid = conv[args.odclev]

        if isolatelist != []:

            sqlflt = """  WHERE r.cc2_{lev} in (SELECT r.cc2_{lev} FROM r WHERE r.identifier in ('{isolates}'))""".format(
                lev=levid, appname=args.appname, isolates="','".join(isolatelist))

        else:
            sqlflt = ''

        sqlq = """ WITH r AS (SELECT * FROM "{appname}_isolate" FULL OUTER JOIN "{appname}_view_apcc" ON "{appname}_isolate".mgt_id = "{appname}_view_apcc".mgt_id) SELECT r.identifier,r.cc2_{lev} FROM r{filt}""".format(
            lev=levid, appname=args.appname, filt=sqlflt)


    elif args.cclev:

        if isolatelist != []:

            sqlflt = """  WHERE r.cc1_{lev} in (SELECT r.cc1_{lev} FROM r WHERE r.identifier in ('{isolates}'))""".format(
                lev=args.cclev, appname=args.appname, isolates="','".join(isolatelist))

        else:
            sqlflt = ''


        sqlq = """ WITH r AS (SELECT * FROM "{appname}_isolate" FULL OUTER JOIN "{appname}_view_apcc" ON "{appname}_isolate".mgt_id = "{appname}_view_apcc".mgt_id) SELECT r.identifier,r.cc1_{lev} FROM r{filt}""".format(
            lev=args.cclev, appname=args.appname, filt=sqlflt)



    elif args.stlev:

        if isolatelist != []:

            sqlflt = """  WHERE r.ap{lev}_0_st in (SELECT r.ap{lev}_0_st FROM r WHERE r.identifier in ('{isolates}'))""".format(lev=args.stlev, appname=args.appname, isolates="','".join(isolatelist))

        else:
            sqlflt = ''


        sqlq = """ WITH r AS (SELECT * FROM "{appname}_isolate" FULL OUTER JOIN "{appname}_view_apcc" ON "{appname}_isolate".mgt_id = "{appname}_view_apcc".mgt_id) SELECT r.identifier,r.ap{lev}_0_st FROM r{filt}""".format(
            lev=args.stlev, appname=args.appname, filt=sqlflt)


    return sqlq


def get_isolates(conn,isolatelist,args):
    """
    get isolates that match the filters supplied and are related to isolates in list by cutoff relatedness
    :param conn:
    :param isolatelist:
    :param args:
    :return:
    """
    ids = []
    out = {}
    # sql query to retrieve matching isolates
    if args.identifier: # get strains and mgt ids for isolates matching identifier and level IF identifier is defined
        if "," in args.identifier:
            for id in args.identifier:
                isolates, mgtdict = mgt_from_assignments(args, conn,id)
                out[id] = isolates
                ids+=isolates

        else:
            ids,mgtdict = mgt_from_assignments(args,conn)
            out[args.identifier] = ids
    else:

        sqlq = build_query(args,isolatelist)

        print(sqlq)

        sres = sqlquery_to_outls(conn, sqlq)
        odict = {}
        for res in sres:
            print(res)
            ids.append(res[0])
            if res[1] not in out:
                out[res[1]] = [res[0]]
            else:
                out[res[1]].append(res[0])


        # res = [x[0] for x in out]
        print(len(sres))
        # res = list(set(res))
        # by_ident = {}
        # for ident in res:
        #     ids, by_ident[ident] = mgt_from_assignments(args, conn,identifier=str(ident))

    return ids,out

def addSimpleFilter(arg,pgname):
    if "," in arg:
        argls = arg.split(",")
    else:
        argls = [arg]

    return """ AND "{pgname}" in ('{argls}')""".format(pgname=pgname,argls="','".join(argls))

def getMetaData(conn, isolates,idtoisolate,args):


    # sql = """ SELECT "identifier","date","year","country","continent" FROM "{appname}_isolate" INNER JOIN "{appname}_isolation" ON "{appname}_isolate".location_id = "{appname}_isolation".id INNER JOIN "{appname}_location" ON "{appname}_isolate".location_id = "{appname}_location".id WHERE "{appname}_isolate".identifier in ('{isolates}');""".format(appname=args.appname,isolates="','".join(isolates))
    # dat = pd.read_sql_query(sql, conn)
    # conn = None

    sqlFilterSection = """("{appname}_isolate".identifier in ('{isolates}')""".format(appname=args.appname, isolates="','".join(isolates))

    if args.country != 'all':
        sqlFilterSection += addSimpleFilter(args.country,"country")

    if args.continent != 'all':
        sqlFilterSection += addSimpleFilter(args.continent,"continent")

    if args.disease != 'all':
        sqlFilterSection += addSimpleFilter(args.disease,"disease")

    if args.postcode != 'all':
        sqlFilterSection += addSimpleFilter(args.postcode,"postcode")

    if args.source != 'all':
        sqlFilterSection += addSimpleFilter(args.source,"source")

    if args.host != 'all':
        sqlFilterSection += addSimpleFilter(args.host,"host")

    if args.sourcetype != 'all':
        sqlFilterSection += addSimpleFilter(args.sourcetype,"type")

    if args.year != 'all':
        if "," in args.year:
            year = args.year.split(",")

        elif "-" in args.year:
            year = args.year.split("-")
            year = list(map(int,year))
            if int(year[0]) <= int(year[1]):
                year = range(year[0],year[1]+1)
                year = list(map(str,year))
            else:
                sys.exit("Please enter years oldest first")
        else:
            year = [args.year]

        sqlFilterSection += """ AND "year" in ('{yr}')""".format(yr="','".join(year))
        # print(year)
        # new = dat[dat['year'].isin(year)]
        # dat = new

    if args.range != 'all':  # TODO currently only isolates with dates are returned, could include isolates with matching years, extracted from requested dates (may result in isolates outside window if large amount of year is not in date range.
        if "," in args.range:
            dates = args.range.split(",")
            sqlFilterSection += """ AND date::date >= '{d1}'::date AND date::date <= '{d2}'::date""".format(d1=dates[0],d2=dates[1])


    sqlFilterSection += ")"

    # print(sqlFilterSection)

    sql = """ SELECT "identifier","date","year","country","continent" FROM "{appname}_isolate" FULL OUTER JOIN "{appname}_isolation" ON "{appname}_isolate".location_id = "{appname}_isolation".id FULL OUTER JOIN "{appname}_location" ON "{appname}_isolate".location_id = "{appname}_location".id WHERE ({filt});""".format(
        appname=args.appname,filt=sqlFilterSection)

    # print(sql)

    dat = pd.read_sql_query(sql, conn,parse_dates=['date'])

    # print(dat.count())

    isolatetoid = {}

    for ident,strainl in idtoisolate.items():
        for strain in strainl:
            isolatetoid[strain] = ident


    # plt.figure(figsize=(16, 8))

    # with pd.option_context('display.max_rows', 10,'display.max_columns',100):
    #     # print(dat)

    dat['used_id'] = dat['identifier'].map(isolatetoid)


    summ = dat.groupby('used_id')['identifier'].count()==1

    summ2 = dat.groupby('used_id')['identifier'].count()[summ]


    # print(summ2)




    # dfnew = df.replace(not_top2, 'Other')


    # plt.show()

    # iso_to_df = pd.DataFrame(isolatetoid)
    # dat = pd.concat([iso_to_df,dat],axis=0).reset_index()


    # for i in dat['identifier']:
    #     print(i)

    outd = dat.set_index('identifier').to_dict()
    isolatels = dat.identifier.tolist()
    # print(outd)

    return outd,isolatels,dat

def searchRestrictionList(args):
    search_restictions = "\n"
    if args.continent != 'all':
        search_restictions += "Continent: {}\n".format(args.continent)
    if args.country != 'all':
        search_restictions += "Country: {}\n".format(args.country)
    if args.postcode != 'all':
        search_restictions += "Postcode: {}\n".format(args.postcode)
    if args.source != 'all':
        search_restictions += "Source: {}\n".format(args.source)
    if args.sourcetype != 'all':
        search_restictions += "Source type: {}\n".format(args.sourcetype)
    if args.host != 'all':
        search_restictions += "Host: {}\n".format(args.host)
    if args.disease != 'all':
        search_restictions += "Disease: {}\n".format(args.disease)
    if args.year != 'all':
        search_restictions += "Year: {}\n".format(args.year)
    if args.range != 'all':
        search_restictions += "Dates: {}\n".format(args.range)

    if search_restictions != '\n':
        search_restictions = " limited by:" + search_restictions

    return search_restictions


def make_year_prev_column(metaDf,complete):


    metaDf['Query isolates'] = metaDf["identifier"].isin(complete).astype(int)

    metaDf['Query isolates'] = metaDf['Query isolates'].replace([1, 0], ['Existing', 'Query'])

    print(metaDf)

    metaDf = metaDf.dropna(subset=["year"])

    metaDf.loc["year"] = pd.to_datetime(metaDf["year"].astype(int).astype(str), format="%Y")

    metaDf.loc["year"] = metaDf["year"].notna()

    yearls = metaDf["year"].unique()

    print(yearls)

    minyear = pd.to_datetime(yearls.min())
    maxyear = pd.to_datetime(yearls.max())
    yearrange = int(maxyear.strftime("%Y")) - int(minyear.strftime("%Y")) + 1

    pddaterange = pd.date_range(start=minyear, periods=yearrange, freq='A').to_period('Y')

    yearplot = metaDf[["year", 'Query isolates']]

    yearplot = yearplot.groupby([metaDf["year"].dt.to_period('Y'), 'Query isolates']).count()

    yearplot = yearplot.unstack(level=1)

    yearplot.columns = yearplot.columns.droplevel(level=0)

    yearplot = yearplot.reindex(pddaterange, fill_value=0)

    yearplot = yearplot.fillna(0)

    return yearplot


def makeplots(isolate_used_id,metaDf,newisolates,complete):

    # print(metaDf)

     # pie plot

    f = plt.figure(figsize=(10,4))

    if len(newisolates) > 0 and len(complete) > 0:

        gs1 = gridspec.GridSpec(1, 3)

        ax1 = f.add_subplot(gs1[0])


        values = [len(complete),len(newisolates)]

        ax1.pie(values,labels=["Existing Isolates","Query Isolates"],
                autopct=lambda p : '{:,.0f}'.format(int(round(p*sum(values)/100.0))))

        ax2 = f.add_subplot(gs1[1:])

        yearplot = make_year_prev_column(metaDf,complete)

        print(yearplot)

        yearplot.plot(kind='bar',ax=ax2,stacked=True)

        ax2.legend(title=None)



        # if int(yearrange) <= 2:
        #     ofinterest["year"].plot_date(kind="hist", ax=ax2)





        gs1.tight_layout(f)

    else:

        gs1 = gridspec.GridSpec(1, 1)

        ax1 = f.add_subplot(gs1[0])

        yearplot = make_year_prev_column(metaDf,complete)

        print(yearplot)

        yearplot.plot(kind='bar',ax=ax1,stacked=True)

        ax1.legend().remove()



    temp_fig = str(uuid1()) + "tmppie.pdf"

    f.savefig(temp_fig)
    plt.close()

    return temp_fig

    # print(isolate_used_id)
    # print(metaDf)
    # print(newisolates)
    # print(complete)
    # sys.exit("DONE")




def general_report(complete,fails,matchIsolates,metadata,metaDf,args):

    newisolates = list(set(matchIsolates).difference(set(complete)))

    plotcleanup = []

    """
    todo 
    input dict of id to isolates
    
    cclis = get_merge_cclis(conn,cc,level,args.appname).split(",")
    
    
    
    """

    doc = Multistrain('tgbonum')


    # Call function to add text
    # doc.fill_document()

    tp = ""
    lev = ""
    if args.stlev:
        tp = "ST"
        lev = args.stlev
    if args.cclev:
        tp = "CC"
        lev = args.cclev
    if args.odclev:
        tp = "ODC"
        lev = args.odclev

    search_restrictions = searchRestrictionList(args)

    # Add stuff to the document timerange="all",year="all",country="all",continent="all"postcode="all",source="all",sourcetype="all",host="all",disease="all"

    if not args.identifier: # if a particular ST, CC or ODC has not been assigned
        with doc.create(Section('Search Settings')):

            doc.append('Database was searched using {type} at level {lev}{restrict}'.format(type=tp,lev=lev,restrict=search_restrictions))

            if args.list or args.file:
                with doc.create(Subsection('Input Isolates')):
                    doc.append('Successfully processed isolates:\n {}\n'.format(", ".join(complete)))
                    doc.append('Failed isolates:\n')
                    if len(list(fails.keys())) != 0:

                        fmt = "X[l] X[l]"
                        with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:

                            header_row1 = ["Isolate","Failure Reason"]
                            data_table.add_row(MultiColumn(1, data=header_row1))
                            data_table.add_hline()
                            for reason in fails:
                                for isolate in fails[reason]:
                                    d = [isolate,reason]
                                    data_table.add_row(MultiColumn(2, data=d))
                    else:
                        doc.append('None\n')

            with doc.create(Subsection('Matching Isolates')):
                if len(newisolates) > 40:
                    doc.append(
                        'The above settings matched to {no} isolates \n'.format(no=len(newisolates)))
                else:
                    doc.append('The above isolates matched to the following {no} isolates \n'.format(no=len(newisolates)))
                    fmt = "X[l]X[l]"
                    with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:
                        search_level = tp+lev
                        header_row1 = ["Name",search_level]
                        data_table.add_row(MultiColumn(2, data=header_row1))
                        data_table.add_hline()
                        sorted_isolates = sorted(newisolates, key=lambda i: int(metadata['used_id'][i]))
                        # print(newisolates)
                        # print(sorted_isolates)

                        for i in sorted_isolates:
                            isolate_used_id = metadata['used_id'][i]
                            data = [i,isolate_used_id]
                            data_table.add_row(MultiColumn(2, data=data))

    else: # if a certain ST, CC or ODC was assigned
        with doc.create(Section('Search Settings')):
            doc.append('Database was searched using {type}={ident} at level {lev}{restrict}'.format(type=tp,ident=args.identifier,lev=lev,restrict=search_restrictions))

            if args.list or args.file:
                with doc.create(Subsection('Input Isolates')):
                    doc.append('Successfully processed isolates:\n {}\n'.format(", ".join(complete)))
                    doc.append('Failed isolates:\n')
                    if len(list(fails.keys())) != 0:

                        fmt = "X[l] X[l]"
                        with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:

                            header_row1 = ["Isolate","Failure Reason"]
                            data_table.add_row(MultiColumn(1, data=header_row1))
                            data_table.add_hline()
                            for reason in fails:
                                for isolate in fails[reason]:
                                    d = [isolate,reason]
                                    data_table.add_row(MultiColumn(2, data=d))
                    else:
                        doc.append('None\n')

            with doc.create(Subsection('Matching Isolates')):
                if len(newisolates) > 40:
                    doc.append(
                        'The above settings matched to {no} isolates \n'.format(no=len(newisolates)))
                else:
                    doc.append('The above settings matched to the following {no} isolates \n'.format(no=len(newisolates)))
                    doc.append(", ".join(newisolates))
                    fmt = "X[l]X[l]"
                    with doc.create(Tabu(fmt, spread="1pt", pos=["l"])) as data_table:
                        search_level = tp+lev
                        header_row1 = ["Name",search_level]
                        data_table.add_row(MultiColumn(2, data=header_row1))
                        data_table.add_hline()

                        sorted_isolates = sorted(newisolates, key=lambda i: int(metadata['used_id'][i]))
                        # print(newisolates)
                        # print(sorted_isolates)

                        for i in sorted_isolates:
                            isolate_used_id = metadata['used_id'][i]
                            data = [i,isolate_used_id]
                            data_table.add_row(MultiColumn(2, data=data))


    # TODO HERE years not carrying across properly, investigate later
    with doc.create(Section('Matching Isolate Summaries')):
        id_list = list(metaDf.used_id.unique())
        for ident in id_list:
            no_id_isolates = len(list(metaDf.loc[metaDf["used_id"] == ident,"identifier"]))
            if no_id_isolates >= args.clustermin:
                with doc.create(Subsection("MGT" + lev + ": " + tp + str(ident))):

                    with doc.create(Figure(position='H')) as plot:



                        id_isolates = metaDf[metaDf["used_id"]==ident]
                        new_id_isolates = list(id_isolates.loc[~id_isolates["identifier"].isin(newisolates),"identifier"])

                        exist_id_isolates = list(id_isolates.loc[id_isolates["identifier"].isin(newisolates),"identifier"])

                        # newisolates = list(set(id_isolates).difference(set(complete)))

                        # print("test")
                        #
                        # print(exist_id_isolates)
                        # print(new_id_isolates)

                        print(ident,exist_id_isolates,new_id_isolates)

                        plotpath = makeplots(metadata,id_isolates,new_id_isolates,exist_id_isolates)

                        plot.append(NoEscape(r'\includegraphics[width=\textwidth,height=5cm,left,keepaspectratio]{' + plotpath + '}'))

                        plotcleanup.append(plotpath)



                    # plot.append(Plot(name='estimate', coordinates=coordinates))
    # Generate data table with 'tight' columns


    # with doc.create(Center()) as centered:
    #     with centered.create(Tabu("X[r] X[r]", spread="1in")) as data_table:
    #         header_row1 = ["X", "Y"]
    #         data_table.add_row(header_row1, mapper=[bold])
    #         data_table.add_hline()
    #         row = [randint(0, 1000), randint(0, 1000)]
    #         for i in range(4):
    #             data_table.add_row(row)
    #
    # with doc.create(Center()) as centered:
    #     with centered.create(Tabu("X[r] X[r]", to="4in")) as data_table:
    #         header_row1 = ["X", "Y"]
    #         data_table.add_row(header_row1, mapper=[bold])
    #         data_table.add_hline()
    #         row = [randint(0, 1000), randint(0, 1000)]
    #         for i in range(4):
    #             data_table.add_row(row)



    doc.generate_pdf('MGT report', clean_tex=False) # make pdf
    # tex = doc.dumps() # make latex file

    for i in plotcleanup:
        remove(i)

def check_success(args,conn,isolatelist):
    sqlq = """ SELECT "identifier","server_status","assignment_status" FROM "{appname}_isolate" WHERE "identifier" in ('{isolates}')""".format(appname=args.appname,isolates="','".join(isolatelist))
    out = sqlquery_to_outls(conn, sqlq)
    res = [x for x in out]
    # print(out)
    fails = {}
    complete = []

    for match in out:
        id = match[0]
        server = match[1]
        assign = match[2]
        if server != "C":
            print(server)
            #sys.exit("Still running")
        else:
            if assign != "A":
                if assign == "L":
                    print(assign)
                    # sys.exit("Still running")
                if assign not in fails:
                    fails[assign] = [id]
                else:
                    fails[assign].append(id)
            else:
                complete.append(id)
    # print(complete)
    return complete,fails




def main_pipe(conn,isolatelist,args):

    # print(isolatelist)

    complete,fails = check_success(args,conn,isolatelist)

    matchingisolates,idtoisolate = get_isolates(conn,complete,args)

    # print(len(matchingisolates))
    #
    # for id in idtoisolate:
    #     print(id,len(idtoisolate[id]))


    ## mgtids in format {identifier:{isolate:(mgt_id, identifier)}}

    # print(matchingisolates)

    #TODO START HERE - currently have search with st,cc,odc or isolate lists working producing list of strain names and
    # dict of {strain_name : mgt_id}
    # next filter results by input filters (isolate metadata)
    # get alleles online db and add meta here - maybe add sophies data for tests

    metadata,metafiltered_isolates,metaDf = getMetaData(conn,matchingisolates,idtoisolate,args)

    general_report(complete,fails,metafiltered_isolates,metadata,metaDf,args)

    # print(matchingisolates)
    # print(mgtids)


def reportstarterargs():
    args = parseargs()

    DbConString = "dbname='{0}' host='{1}' port='{2}' user='{3}' password='{4}'".format(args.postgresdbname,args.postgreshost,args.port,args.postgresuser,args.postgrespass)  ## connection info for Db - assign new user that can only do what is needed for script

    conn = psycopg2.connect(DbConString)
    conn.autocommit = True
    isolatelist = []
    if args.file:
        isolatelist += open(args.file,"r").read().splitlines()
    if args.list:
        isolatelist += args.list.split(",")
    if len(isolatelist) == 0 and not args.identifier:
        print("Examining strains based on an strain lists from -l and of -f. If neither get all.")

    main_pipe(conn,isolatelist,args)

def reportstarter(appname="Salmonella",isolatelist=[],timerange="all",year="all",country="all",continent="all",cutoff="2",stlev="",cclev="",odclev="",identifier="",alliso="",postcode="all",source="all",sourcetype="all",host="all",disease="all",clustermin=2):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()
    args.appname = appname
    args.country = country
    args.range = timerange
    args.year = year
    args.continent = continent
    args.stlev = False
    args.odclev = False
    args.cclev = False
    args.identifier = False
    args.all = False
    args.list = False
    args.file = False
    args.postcode = postcode
    args.source = source
    args.sourcetype = sourcetype
    args.host = host
    args.disease = disease
    args.clustermin = clustermin
    if stlev != "":
        args.stlev = stlev
        print("Examining Sequence type at level {}".format(stlev))
    if odclev != "":
        args.odclev = odclev
        print("Examining Outbreak detection cluster at level {}".format(odclev))
    if cclev != "":
        args.cclev = cclev
        print("Examining Clonal Cluster at level {}".format(cclev))

    if stlev == "" and cclev == "" and odclev == "":
        sys.exit("one of stlev, cclev or odclev must be specified")

    if identifier != "":
        args.identifier = identifier
        print("Examining strains based on an identifier rather than strain list (-l and -f will be ignored)")
    else:
        print("Examining strains based on an strain lists from -l and of -f. If neither get all.")

    if isolatelist != []:
        args.list = True



    database = settings.APPS_DATABASE_MAPPING[appname]

    psql_details = settings.DATABASES[database]

    DbConString = "dbname='{0}' host='{1}' port='{2}' user='{3}' password='{4}'".format(psql_details['NAME'],psql_details['HOST'],psql_details['PORT'],psql_details['USER'],psql_details['PASSWORD'])  ## connection info for Db - assign new user that can only do what is needed for script

    conn = psycopg2.connect(DbConString)
    conn.autocommit = True

    main_pipe(conn,isolatelist,args)
    print("hello")

if __name__ == '__main__':
    # reportstarter(country="United Kingdom",odclev="5",clustermin=20)
    reportstarter(identifier='17', odclev="5",clustermin=10)
    # reportstarter(identifier="32", stlev='3')
    # reportstarterargs()