# Code and instruction for setting up your own MGT database

Detailed (and perhaps complementary) instructions can also be found at [MGT-docs](https://mgt-docs.readthedocs.io/).

1. Download this code.

2. Assuming you want to set up the database now for your organism called NewBacteria, then run the following two commands:

```bash
 find . -type f -exec sed -i.bak “s/Salmonella/NewBacteria/g” {} ;
 find . -type f -exec sed -i.bak “s/salmonella/newBacteria/g” {} ;
```

Make sure you type the cases correctly.

3. Create two databases:

  1. A 'default' database for storing information of users that sign up.
  2. A 'newBacteria' (note the case) database for storing the species specific MGT information.

4. Define your Loci and Schemes and add to the database by following instructions in Scripts/readme.md


5. Then update the various variables in Mgt/settings.py. Some ones to pay special attention to are:

  * SECRET_KEY - a unique combination of characters only known to your we application.

  * MY_URL - your website's url

  * DATABASES - your databases connection information.

  * EMAIL_HOST_USER - your notification systems username

  * EMAIL_HOST_PASSWORD - your notification systems password

  * DEFAULT_FROM_EMAIL - your notification systems address

  * SUBDIR_REFERENCES = 'location/to/References/'

  * SUBDIR_ALLELES = 'location/to/Alleles/'

  * MEDIA_ROOT = "location/to/Uploads/"

6. Update registration templates in Home/templates/django_registration and Home/templates/registration if you want different messages to appear. Alternatively you can also turn off registration in the Mgt/settings.py file by setting REGISTRATION_OPEN=FALSE

7. Now you can run a local testing server as:

```
python3 manage.py runserver
```

8. In script MgtAllele2Db/Allele_to_mgt_db.py, update dbUsername to your database username.

isolate_info = ["dbUsername",args.project,"Public",input_acc,input_acc,"","","","","","","","","","","","","","A"]

9. In script MgtAllele2Db/convert_metadata.py, update dbUsername to your database username.

```
outstringls = ["dbUsername"]
```

10. In script Scripts/bioentrezMetadataGet.py, update "yourRegisteredEntrezEmailId", note that the email you use has to be one you used to register with NCBI.

```
Entrez.email = "yourRegisteredEntrezEmailId"
```
11. Finally, to automate the process of extracting alleles and assigning MGT, you can use set up a cron job.
