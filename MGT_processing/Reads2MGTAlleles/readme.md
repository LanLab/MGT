Install
-----------
**1. Download latest miniKraken Database:**

Before setting up the pipeline for processing raw data reads into alleles, firstly download a minikraken database (warning is 2.9GB).

The MiniKraken DB can be accessed at https://ccb.jhu.edu/software/kraken/,
	
OR

	wget https://ccb.jhu.edu/software/kraken/dl/minikraken_20171019_4GB.tgz

	unzip archive


**2. Add database folder variable with:**

    export KRAKEN_DEFAULT_DB="/home/user/minikraken_db_folder"
    

**3. Install miniconda3:**

This pipeline requires you already have a miniconda3 installed.  
install miniconda3 -> https://conda.io/miniconda.html


**4. Create miniconda3 environment:**

Next a Miniconda3 environment will be created and will contain all the required dependencies for this pipeline.
The "fq_to_allele.yaml" has been provided to simply instruct Miniconda3 when creating an environment.
The environment will be named "deployable_fq_to_genome".

	conda env create -f /path_to_Reads2MGTAlleles/fq_to_allele.yaml -n deployable_fq_to_genome

**5. Users Permission**

Lastly, the user permissions for the shovill_cmd folder must be adjusted.

	chmod 755 /path_to_Reads2MGTAlleles/shovill_cmd

Run
---


**Activate conda environment**

    conda activate deployable_fq_to_genome

**For usage** 

    python /path/to/reads_to_alleles.py -h


    usage: reads_to_alleles.py [-h] [-s SPECIES] [--no_serotyping NO_SEROTYPING]
                               [-y SEROTYPE] [-t THREADS] [-m MEMORY] [-f]
                               [--min_largest_contig MIN_LARGEST_CONTIG]
                               [--max_contig_no MAX_CONTIG_NO]
                               [--genome_min GENOME_MIN] [--genome_max GENOME_MAX]
                               [--n50_min N50_MIN] [--kraken_db KRAKEN_DB]
                               ingenome refalleles reflocs outpath
    
    
    positional arguments:
      ingenome              Input genome
      refalleles            File path to MGT reference alleles file
      reflocs               File path to MGT allele locations file
      outpath               Path to ouput file name
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SPECIES, --species SPECIES
                            String to find in kraken species confirmation test
                            (default: Salmonella enterica)
      --no_serotyping NO_SEROTYPING
                            Do not run Serotyping of Salmonella using SISTR (ON by
                            default) (default: None)
      -y SEROTYPE, --serotype SEROTYPE
                            Serotype to match in SISTR, semicolon separated
                            (default: Typhimurium;I 4,[5],12:i:-)
      -t THREADS, --threads THREADS
                            number of computing threads (default: 4)
      -m MEMORY, --memory MEMORY
                            memory available in GB (default: 8)
      -f, --force           overwrite output files with same strain name?
                            (default: False)
      --min_largest_contig MIN_LARGEST_CONTIG
                            Assembly quality filter: minimum allowable length of
                            the largest contig in the assembly in bp (default for
                            salmonella) (default: 60000)
      --max_contig_no MAX_CONTIG_NO
                            Assembly quality filter: maximum allowable number of
                            contigs allowed for assembly (default for salmonella)
                            (default: 700)
      --genome_min GENOME_MIN
                            Assembly quality filter: minimum allowable total
                            assembly length in bp (default for salmonella)
                            (default: 4500000)
      --genome_max GENOME_MAX
                            Assembly quality filter: maximum allowable total
                            assembly length in bp (default for salmonella)
                            (default: 5500000)
      --n50_min N50_MIN     Assembly quality filter: minimum allowable n50 value
                            in bp (default for salmonella) (default: 20000)
      --kraken_db KRAKEN_DB
                            path for kraken db (if KRAKEN_DEFAULT_DB variable has
                            already been set then ignore) (default: )

Examples
--------

**example1:** 

running strain 1234 against salmonella typhimurium MGT with 8 cores and 30gb RAM

    python /path/to/reads_to_alleles.py 1234_1.fastq.gz,1234_2.fastq.gz MGT_alleles_file locus_position_file output_file_name --serotype "Typhimurium;I 4,[5],12:i:-" --species "Salmonella enterica" -t 8 -m 30

**example2:**

running strain abcd against vibrio cholerae MGT with 4 cores and 50gb RAM
(serotyping is currently only for Salmonella)

    python /path/to/reads_to_alleles.py abcd_1.fastq.gz,abcd_2.fastq.gz MGT_alleles_file locus_position_file output_file_name --no_serotyping --species "Vibrio cholerae" -t 4 -m 50
