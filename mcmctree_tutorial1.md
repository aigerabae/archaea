Old tutorial

While I am waiting for optimal tree settings running with modeltest-ng, I will try to construct MCMTree time with 83 species using v2 tree made with raxml-ng and each gene as partition:
git clone https://github.com/abacus-gene/paml.git

```config (example)
seed = 2
seqfile = mtCDNApri123.txt
treefile = mtCDNApri.trees
mcmcfile = mcmc.txt
outfile = out.txt
ndata = 3
seqtype = 2 * 0 : nucleotides; 1: codons; 2: AAs
usedata = 2 * 0: no data; 1:seq; 2:approximation; 3:out.BV (in.BV)
clock = 2 * 1: global clock; 2: independent; and 3: correlated rates
RootAge = '<2.1' * safe constraint on root age, used if no fossil for root.
model = 0 * 0:JC69, 1:K80, 2:F81, 3:F84, 4:HKY85
alpha = 0 * alpha for gamma rates at sites
ncatG = 5 * No. categories in discrete gamma
cleandata = 0 * remove sites with ambiguity data (1:yes, 0:no)?
BDparas = 1 1 0.1 * birth, death, sampling
kappa_gamma = 6 2 * gamma prior for kappa
alpha_gamma = 1 1 * gamma prior for alpha
rgene_gamma = 2 20 1 * gammaDir prior for rate for genes
sigma2_gamma = 1 10 1 * gammaDir prior for sigma^2 (for clock=2 or 3)
finetune = 1: .1 .1 .1 .1 .1 .1 * auto (0 or 1) : times, rates, mixing...
print = 1 * 0: no mcmc sample; 1: everything except branch 2: ev...
burnin = 2000
sampfreq = 10
nsample = 20000
```

Another potentially useful took from https://www.cell.com/current-biology/fulltext/S0960-9822(21)00577-7 paper = MCScanX (for finding expansion/shribking of henome)

Following tutorial in https://github.com/sabifo4/Tutorial_MCMCtree.git
(has all steps to get the right input files and run the analysis but only on 1 partition (one fasta file. i can cincatenate them into 1 but this will make it assume all genes had the same rate of evolution. but i dont know how to use multiple partitions yet. i will run on one partition for now)

I copied supermatrix.fa and v2.raxml.bestTree into /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree and will do the rest here

I changed my mind and decided to it on server in /media/ds1821p_III/aserikzhan/archaea/v2
```bash
# removing new line characters in fasta
name='supermatrix.fa'
printf "Converting "$name" into a one-line FASTA file\n"
chmod 775 /media/ds1821p_III/aserikzhan/archaea/v2/Tutorial_MCMCtree/src/*
perl /media/ds1821p_III/aserikzhan/archaea/v2/Tutorial_MCMCtree/src/one_line_fasta.pl $name 
onefa=$( echo $name | sed 's/\.fa/\_one\_line\.fa/' )
namefa=$( echo $name | sed 's/\.fa//' )
mv $onefa $namefa.fasta

# making phylips formatted file
aln_name=`ls *fasta`
a_noext=$( echo $aln_name | sed 's/\.fasta//' )
num=$( grep '>' $aln_name | wc -l )
len=$( sed -n '2,2p' $aln_name | sed 's/\r//' | sed 's/\n//' | wc -L )
/media/ds1821p_III/aserikzhan/archaea/v2/Tutorial_MCMCtree/src/FASTAtoPHYL.pl $aln_name $num $len

# removing branch lengths from the tree
cp v2.raxml.bestTree tree_example_uncalib.tree
sed -i 's/:[0-9]*\.[0-9]*//g' tree_example_uncalib.tree
# NOTE: This regular expresion will work with that example
# file. You may have to use more complex regular expressions
# if you have `E-` or even bootstrap values that you need
# to get rid of!
#
# Add header
sed -i '1s/^/4 1\n/' tree_example_uncalib.tree

# adding calibrations
cp /media/ds1821p_III/aserikzhan/archaea/v2/Tutorial_MCMCtree/00_data_formatting/scripts/Include_calibrations.R ./
```

I will use v2 with this calibration:
```
name;tip1;tip2;MCMCtree
int_calib;Natronoarchaeum_mannanilyticum_JCM_16328;Halobacterium_salinarum_91_R6;'B(3.976,3.976,1e-300,0.025)'
```

I ran calculate_ratepriors and adjusted the prior distribution. now in ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree:
```bash
mkdir -p tmp/example_dating
cd tmp/example_dating 
num_aln=1
for i in `seq 1 $num_aln`
do
mkdir -p alignments/$i
mkdir -p Hessian/$i/prepare_baseml
mkdir -p trees/{uncalibrated/$i,calibrated/$i}
mkdir -p control_files/$i
done
mkdir -p pipelines_Hessian
mkdir scripts
```

populating those folders:
```bash
# Run from `tmp/example_dating`
# Copy alignment
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/supermatrix.phy alignments/1/
# Now, transfer calibrated tree
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/example_calib_MCMCtree.tree trees/calibrated/1
# Transfer uncalibrated tree
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/tree_example_uncalib.tree trees/uncalibrated/1
# Next, copy control file
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/prepbaseml.ctl control_files/1
# Last, copy the in-house bash scripts with our pipeline
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/Tutorial_MCMCtree/01_PAML/00_BASEML/scripts/*sh scripts/
cd ../
mv example_dating ../
cd ../
rm -r tmp
```

Getting Hessian and gradient:
```bash
# Run from `example_dating/scripts`
# Please change directories until
# you are there. Then, run the following
# commands.
chmod 775 *sh
# In this case, there are three alignments, so
# we can execute our script within a loop
num_aln=1
for i in `seq 1 $num_aln`
do
./generate_prepbaseml.sh $i
done
```

To make sure that all the paths have been properly extracted, you can run the following code snippet:
```sh
# Run from `example_dating/Hessian`
# Please change directories until
# you are there. Then, run the following
# commands.
grep 'seqfile' */prepare_baseml/*ctl
grep 'treefile' */prepare_baseml/*ctl
```

### Preparing input files

Now that we have the input files (alignment and tree files) and the instructions to run `BASEML` (control file) in `example_dating`, we will be manually running `MCMCtree` inside each `prepare_baseml` directory (see file structure above) in a special mode that launches `BASEML` for the sole purpose we want: to infer the vectors and matrix required to approximate the likelihood calculation.

```sh
# Run `MCMCtree` from
# `example_dating/Hessian/1/prepare_baseml`.
# Please change directories until
# you are in there.
# The first command to change directories 
# will work if you are still in 
# `main/Hessian`, otherwise ignore and 
# move to such directory with the command
# that best suits your current directory.
# If you had more than one alignment, you
# could write a `for` loop or access each
# dir individually.
mcmctree prepbaseml*ctl # You may have other aliases to run `MCMCtree`, 
                        # so run this command accordingly!
```

I had to change BDparas = 1 1 0.1 C because in new version they ask for this C flag

Also my tree was unrooted so i had to redo  it on the level of v2.raxml.bestTree and repopulate my example_dating folder:
```r
library(phytools)
tt_raxml <- read.tree("v2.raxml.bestTree")
is.null(tt_raxml$edge.length)  # should be FALSE
is.binary(tt_raxml)            # should be TRUE
tt_rooted <- midpoint.root(tt_raxml)
is.rooted(tt_rooted)           # should be TRUE
write.tree(tt_rooted, "v2.raxml.bestTree_rooted")
```

Re-running those things:
```bash
cp v2.raxml.bestTree_rooted tree_example_uncalib.tree
sed -i 's/:[0-9]*\.[0-9]*//g' tree_example_uncalib.tree
# NOTE: This regular expresion will work with that example
# file. You may have to use more complex regular expressions
# if you have `E-` or even bootstrap values that you need
# to get rid of!
#
# Add header
sed -i '1s/^/4 1\n/' tree_example_uncalib.tree

# adding calibrations - ran that IncludeCalibrations.R script but it has to be done in Rstudio rather than command line
cd ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/example_dating
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/example_calib_MCMCtree.tree trees/calibrated/1
# Transfer uncalibrated tree
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/tree_example_uncalib.tree trees/uncalibrated/1
```

My file aso had 41 instead of 83 1 in trees, i changd that manully 
I also changed in cluster files:
seqtype = 2    * 0: nucleotides; 1:codons; 2:AAs to have 2 (bc my data is aa)
model = 11    * changed for most common AA model = LG

I had to run BaseMl first
cp prepbaseml.ctl baseml.ctl
# in baseml.ctl i edited usedata = 1    * exact likelihood for Hessian calculation
# and outfile = out_baseml.txt
baseml baseml.ctl

None of it works. I think I should use a different version of mcmctree prepbaseml*ctl

conda install bioconda::paml==4.9
cp /home/aygera/anaconda3/pkgs/paml-4.9-hec16e2b_7/dat/lg.dat ./
when it asks for file i type lg.dat

I canceled the run as soon as it created temporary files and did the following
```
sed -i 's/method\ \=\ 0/method\ \=\ 1/' tmp0001.ctl
grep 'alpha' tmp0001.ctl   # You should see `fix_alpha = 0` and `alpha = 0.5`
grep 'ncatG' tmp0001.ctl   # You should see `ncatG = 4`
# the tutorial also says this: grep 'model' */*/tmp0001.ctl   # You should see `model = 3` (i.e., empirical+F model) but it won't work for my amino acid model so i skipped it
```

We have created a template bash script with flags (i.e., see script  `pipeline_Hessian_BASEML_template_PC.sh` in the [`scripts` directory](01_PAML/00_BASEML/scripts)), which will be replaced with the appropriate values by another bash script (i.e.,`generate_job_BASEML_PC.sh`, also saved in the [`scripts` directory](01_PAML/00_BASEML/scripts)). Please note that the second bash script will edit the template bash script according to the data alignment/s that will be analysed. We had already copied these scripts to the `example_dating` directory when setting our file structure. Therefore, we just need to execute the following code snippet there:
```sh
# Run from `example_dating` dir.
# Please change directories until
# you are there. Then, run the following
# commands.
home_dir=$( pwd )
cd scripts
chmod 775 *sh
num_aln=1
# Arg1: Number of alignments
# Arg2: Path to the pipeline directory
# Arg3: Name of the working directory (i.e., `example_dating` in this analysis)
# Arg4: Name of the executable file for BASEML. E.g., `baseml4.10.7`, `baseml`, etc.
# Arg5: Boolean, PAML exported to the path? `Y` or `N`.
#       If `N`, the executable file will be required to be in the home dirctory,
#       i.e., directory which name you type as `Arg3`.
./generate_job_BASEML_PC.sh $num_aln $home_dir/pipelines_Hessian example_dating baseml Y
```

Next, we will go to the `pipelines_Hessian` directory and run the script that will have been generated using the commands above:

```sh
# Run from `example_dating/pipelines_Hessian`.
# Please change directories until
# you are there. Then, run the following
# commands.
#
# If you list the content of this directory,
# you will see the pipeline you will need 
# to execute in a bash script called
# `pipeline_Hessian.sh`
ll *
# Now, execute this bash script
chmod 775 *sh
./pipeline_Hessian.sh & # Include the `&` to run this job in the background!

Again some damn error. I'm just gonna run MCMCMTree as is
seed = -1
   seqfile = mtCDNApri123.txt
  treefile = mtCDNApri.trees
  mcmcfile = mcmc.txt
   outfile = out.txt

     ndata = 3            * Number of partitions
   seqtype = 2            * 0: nucleotides; 1:codons; 2:AAs
   usedata = 2            * 2: approximate likelihood (requires an 'in.BV' file)
     clock = 2            * 1: global clock; 2: independent; 3: correlated rates

   RootAge = <24.0         * Constraint on root age

     model = 8            * 8: LG empirical amino acid model
     alpha = 0.5          * Alpha for gamma rates at sites (0.5 is standard for AAs)
     ncatG = 4            * No. categories in discrete gamma (4 is standard for AAs)

 cleandata = 0            * remove sites with ambiguity data (1:yes, 0:no)?

   BDparas = 1 1 0.1      * birth, death, sampling

* kappa_gamma and alpha_gamma are for nucleotides/codons and are ignored for AAs

rgene_gamma = 2 20 1      * gammaDir prior for rate for genes
sigma2_gamma = 1 10 1     * gammaDir prior for sigma^2 (for clock=2 or 3)

  finetune = 1: .1 .1 .1 .1 .1 .1

     print = 1            * 0: no mcmc sample; 1: everything except branch 2: ev...
    burnin = 2000
  sampfreq = 10
   nsample = 20000

nd this also needs more work. im gonna deal with it tomorow
