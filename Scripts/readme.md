# scripts to set up the database:
-1. First make sure an empty database exists. In psql can do this to create one:

```CREATE DATABASE salmonella";```

0. Script to read and load settings.py from supplied project location (uses the django model system for db access). & scripts to get and add to tables.

```readAppSettAndConnToDb.py```
```addToTableInOrgDb.py```
```getFromTableInOrgDb.py```

Run migrations:

```python3 manage.py makemigrations Salmonella```

```python3 manage.py migrate --database=salmonella```

(is used directly, as required by the scripts below).


1. Set up the chromosome and reference.

```python3 populateReference.py ../ Mgt Salmonella Files/refFileInfo.json ```

(Location of chromosomes must be supplied in refFileInfo, which will be used to move them to the locations in SETTINGS.py)

2.  Script to extract loci, add to db, and add allele with id 1 to db.

```python3 populateLoci.py ../ Mgt Salmonella Files/lociLocationsInRef.txt```

Header:
lociName	startPos	endPos	dir	chrNum


3. Script to add schemes

```python3 populateSchemes.py ../ Mgt Salmonella Files/schemesInfo.txt Files/Schemes```

Header:
schemeName	uncertainty_th	fn_lociList	displayName	description(optional)

Old: ~~ schemeName	orderNum	uncertainty_th	fn_lociList	description(optional) ~~



4. Script to set up clonal_complex tables code and add to Tables_cc:

```python3 setUpCcs.py ../ Mgt Salmonella Files/tables_ccs.txt > autoGenCcs```

(Copy and paste the output to Salmonella/autoGenCcs and rerun migrations on the app).

Header (1 row for 1 table):

schemeName	tableNum	tableDisplayOrder	displayName
e.g.
stmcgMLST	2	4	"stmcgmlst 10 allele"

e.g. (when the same value is to appear in multiple tables)
stmcgMLST	1,2	10,1	"stmcgmlst 1 allele","stmcgmlst 1 allele"


5. Script to generate allelic_profile tables + the MGT table

```python3 setUpApsAndMgt.py ../ Mgt Salmonella Files/tables_aps.txt > autoGenAps```

(Copy and paste the output to Salmonella/autoGenAps and rerun migrations on the app).

Header:
schemeName	display_order


6. Add alleles:
```python3 addAlleles.py ../ Mgt Salmonella Files/Alleles/```


7. Add snps:

```python3 addSnps.py ../ Mgt Salmonella Files/snpMuts.txt```

Header:

locusId:alleleId	snpMut1,snpMut2...,snpMutN|<empty>

(snpMuts col in standard mutations format)


8. Populate allelic_profile tables above: # TODO

[# TODO: add checks (if exists in db; & after adding that all three added properly)]

```python3 addAllelicProfiles.py ../ Mgt Salmonella Files/schemeToApMapping.txt Files/AllelicProfiles```

Header:
schemeName	alellicProfilesFileName

[Note: ] Always check if allele exists before adding to allelic_profile tables. (as script does not check it)

cut -f1,2 MGT9_gene_profiles.txt | sort | uniq -c | sort

mgt6
2 1159	0
2 3224	0
2 3619	0
2 3671	0
2 3784	0
2 3873	0
2 4331	0
2 4967	0
mgt7
2 3341	0
2 4543	0
2 4590	0


9. Populate clonal_complex tables and assign them to allelic profiles:

```python3 addClonalComplexes.py ../ Mgt Salmonella  Files/ccInfo.txt Files/ClonalComplexes```

Header (of ccInfo.txt):
schemeName	ccAssignmentToAp	ccMerges	tableNum_orderNum(ccInfo)

Header (of a ccFile):
st	dst	ccOrig


10. Register for an account on the web-app.
(Can set up a dummy local email server as:)
	```python -m smtpd -n -c DebuggingServer localhost:25```


11. Populate isolate tables: # FIXME: as isolate metadata info becomes more certain, update me (missing the manually adding of the isolation date).
```python3 addIsolates.py ../ Mgt Salmonella Files/isolate_info.tab```

Header:
userName	projectName	privacy_status	isolateId	METADATA(cols_tabbed)

(Specify column names of metadata in script).



12. Populate Hst tables, and assign isolates to hsts:
```python3 addMgts.py ../ Mgt Salmonella Files/hgt_annotations.tab```

Header:
username	projectName	isolateName	schName1	schName2	schName3	...	schNameN


13. Script to generate the ap_cc view table: + (sql code for running directly on the sql server).

```python3 genViewSqlAndClass.py ../ Mgt Salmonella mlstWebsite```

Two files are written out:
1. "runOnDb.sql" : run the two sql statements in postgresSql (can follow the method in 14.).
2. "autoGenView" : copy and paste this to autoGenViews.py in the models folder.

14. Run postgres commands from file:
```psql -U <dbUsername> -d salmonella50 -a -f runOnDb.sql```
