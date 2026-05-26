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
```bash
# removing new line characters in fasta
name='supermatrix.fa'
printf "Converting "$name" into a one-line FASTA file\n"
chmod 775 ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/Tutorial_MCMCtree/src/*
perl ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/Tutorial_MCMCtree/src/one_line_fasta.pl $name 
onefa=$( echo $name | sed 's/\.fa/\_one\_line\.fa/' )
namefa=$( echo $name | sed 's/\.fa//' )
mv $onefa $namefa.fasta

# making phylips formatted file
aln_name=`ls *fasta`
a_noext=$( echo $aln_name | sed 's/\.fasta//' )
num=$( grep '>' $aln_name | wc -l )
len=$( sed -n '2,2p' $aln_name | sed 's/\r//' | sed 's/\n//' | wc -L )
~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/Tutorial_MCMCtree/src/FASTAtoPHYL.pl $aln_name $num $len

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
cp ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/Tutorial_MCMCtree/00_data_formatting/scripts/Include_calibrations.R /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces/mcmctree/

```

For the age estimates I read:
Marin et al. 2017 (Molecular Biology and Evolution, "The Timetree of Prokaryotes") — a large-scale prokaryote timetree built from 25 protein-coding genes across 218 species, which places crown Halobacteria in the ~1,000–1,200 Mya range
Battistuzzi et al. 2004 (BMC Evolutionary Biology, "A genomic timescale of prokaryote evolution") — estimates archaebacterial diversification broadly at 3.1–4.1 Ga, used as a sanity check for the root
TimeTree v5 (Kumar et al. 2022, MBE) — the community-consensus database, which aggregates published divergence time estimates

I decided to use TimeTree.org to get my calibrations:
Natronomonas - Halomarina = 455 MYA
Haladaptatus - Haladaptus = 314 MYA
Halomicrobium - Haloarcula = 151 MYA
Halobacterium - Natronorubrum = 314 MYA
Haloferax - Halohasta = 168 MYA

Haloferax - Halorubrum = 168 MYA
Haloferax - Natrialba = 279 MYA
Halobacterium - Haloarcula = 334 MYA

I will use node between Crown Halobacteria class: Natrialba_aegyptia_DSM_13077 and Haloferax_gibbonsii_ARA6 because they represent Natrialbales and Haloferacales orders, respectively =  279 MYA
Crown Haloferacales order: Haloferax_gibbonsii_ARA6 and Halorubrum_ezzemoulense_Fb21 = 168 MYA
Crown Halobacteriales order: Halobacterium_salinarum_KBTZ01 and Haloarcula_sp_KBTZ06_KBTZ06 = 334 MYA
As of 2021, Natrialbales contains one family, Natrialbaceae so I won't be seeing its last common ancestor between different families in that order

None of it makes sense. I will use the earliest roo date in timetree halobacteria class tree (even tho the tree itself makes no sense)
Name: no name
Rank: no rank
Clade Size: 65
Estimated Time: 413.7 MYA
Adjusted Time: 2400

name;tip1;tip2;MCMCtree
root_calib;Halobacteria 
Nah,this still makes no sense!

I need to find a reliable date for divergence of orders in Halobacteria but most importantly i need to find a reliable phylogeny
https://www.microbiologyresearch.org/content/journal/ijsem/10.1099/ijsem.0.006879 discusses halobacteria class
