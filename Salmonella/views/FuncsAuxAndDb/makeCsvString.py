
from Salmonella.models import Isolate, View_apcc, Tables_ap, Tables_cc
from Salmonella.views.FuncsAuxAndDb import constants as c
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def makeCsv(isolates,isAuth):
    """
    Make tab separated string from search results so return to user through ajax
    :param isolates:
    :return:
    """

    if isAuth:
        mgtColInfo = dict(c.MgtColsPv[0])
        apstart = mgtColInfo["apStart"]
        apEnd = mgtColInfo["apEnd"]
        ccStart = mgtColInfo["ccStart"] - 1
        ccEnd = mgtColInfo["ccEnd"]
        epiStart = mgtColInfo["epiStart"] - 1
        epiEnd = mgtColInfo["epiEnd"]
    else:
        mgtColInfo = dict(c.MgtColsPu[0])
        apstart = mgtColInfo["apStart"]
        apEnd = mgtColInfo["apEnd"]
        ccStart = mgtColInfo["ccStart"] - 1
        ccEnd = mgtColInfo["ccEnd"]
        epiStart = mgtColInfo["epiStart"] - 1
        epiEnd = mgtColInfo["epiEnd"]



    header = ['Strain']

    # add MGT levels for ST headers
    qs_tablesAp = Tables_ap.objects.filter(table_num=0).order_by('display_order').values('table_name',
                                                                                         'scheme__display_name')
    for i in qs_tablesAp:
        header.append(i['scheme__display_name'])

    # add MGT_CC for CC headers
    qs_tablesCc = Tables_cc.objects.filter(display_table=1).values('table_name', 'display_name').order_by(
        'display_order')
    for i in qs_tablesCc:
        header.append(i['display_name'] + "_CC")

    #add ODC names as headers
    qs_tablesEpi = Tables_cc.objects.filter(display_table=2).values('table_name', 'display_name').order_by(
        'display_order')
    for i in qs_tablesEpi:
        header.append(i['display_name'])

    #add location info header
    locheader = []
    locpos = []

    if isAuth:
        for i in c.IsoMetaLocInfoPv:
            locheader.append(i['display_name'])
            locpos.append(i["db_col"])
    else:
        for i in c.IsoMetaLocInfoPu:
            locheader.append(i['display_name'])
            locpos.append(i["db_col"])

    #add isolation header
    isoheader = []
    isopos = []
    if isAuth:
        for i in c.IsoMetaIslnInfoPv:
            isoheader.append(i['display_name'])
            isopos.append(i["db_col"])
    else:
        for i in c.IsoMetaIslnInfoPu:
            isoheader.append(i['display_name'])
            isopos.append(i["db_col"])

    header += locheader
    header += isoheader

    #start output variable string
    returnstring = "\t".join(header) + "\n"


    for isolate in isolates:
        if len(isolate) > 1 and isolate[2] == "C" and isolate[3] == "A":

            #add isolate name
            isolateout = []
            isolatename = isolate[1]
            isolateout.append(isolatename)

            # add ST assignments as ST.dST
            sts = list(zip(isolate[apstart+1:apEnd+1:3], isolate[apstart + 2:apEnd+1:3]))

            outsts = [str(x[0]) + "." + str(x[1]) for x in sts]

            isolateout += outsts

            # add CC assignments (if isolate has merge cc add that, otherwise if merge is null return cc id
            ccs = list(zip(isolate[ccStart:ccEnd:2], isolate[ccStart + 1:ccEnd:2]))

            outcc = []

            for ccpair in ccs:
                if ccpair[1]:
                    outcc.append(str(ccpair[1]))
                else:
                    outcc.append(str(ccpair[0]))

            isolateout += outcc

            # Add odcs with same merges as CCs
            odcs = list(zip(isolate[epiStart:epiEnd:2], isolate[epiStart + 1:epiEnd:2]))

            outodc = []

            for odcpair in odcs:
                if odcpair[1]:
                    outodc.append(str(odcpair[1]))
                else:
                    outodc.append(str(odcpair[0]))

            isolateout += outodc

            # add location metadata
            for p in locpos:
                # print(p)
                if not isolate[p]:
                    isolateout.append("")
                else:
                    isolateout.append(str(isolate[p]))

            # add isolation metadata
            for p in isopos:
                # print(isolate,p)
                if not isolate[p]:
                    isolateout.append("")
                else:
                    isolateout.append(str(isolate[p]))

            # final string
            returnstring += "\t".join(isolateout) + "\n"


    return returnstring
