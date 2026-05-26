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

Claude suggests this calibration:
name;tip1;tip2;MCMCtree
root_calib;Haloferax_gibbonsii_ARA6;Halostagnicola_larsenii_XH_48_XH_48;'ST(2.791,0.05,0.112,109.124)'
haloferacales_calib;Haloferax_gibbonsii_ARA6;Halohasta_litchfieldiae_tADL;'B(1.0,2.5,1e-300,0.025)'
halobacteriales_calib;Halobacterium_salinarum_91_R6;Haloarcula_halobia_XH51;'B(1.0,2.5,1e-300,0.025)'

This is what it says about making a calibratiobns file yourself:
Great question. Here's the complete mental model:

---

## What a calibration row actually means

Each row in the CSV tells MCMCtree: *"the ancestor of these two species lived at approximately this time."* That ancestor is whatever internal node in your tree is the MRCA of your two chosen tips. So the entire exercise is: **pick a node you want to constrain → find two species that "point to" it → look up when they diverged → translate that into a prior.**

---

## Step 1: Decide which nodes to calibrate

You want to calibrate **well-separated, unambiguous nodes** — ideally the root plus 1–2 deep internal splits. In your tree there are three natural choices:

| Node | What it represents |
|---|---|
| Root | Crown Halobacteria — when all three orders last shared a common ancestor |
| Crown Haloferacales | When the 19-taxon Haloferacales clade started diversifying |
| Crown Halobacteriales s.s. | When the 41-taxon Halobacteriales clade started diversifying |

---

## Step 2: Choose your tip pairs on TimeTree

For each node, you need **one tip from each side of that split.** The MRCA of the two tips you pick must land exactly on the node you want — not above it, not below it.

**Root** — you need one species from Haloferacales and one from Natrialbales (the two deepest branches). Search:
- *Haloferax volcanii* vs *Natrialba magadii*

**Crown Haloferacales** — you need two species from opposite ends of that 19-taxon clade. The deepest split inside it is Haloferacaceae (*Haloferax*) vs Halorubraceae (*Halorubrum*, *Halohasta*). Search:
- *Haloferax volcanii* vs *Halorubrum lacusprofundi*

**Crown Halobacteriales s.s.** — deepest split inside the 41-taxon clade is Halobacteriaceae (*Halobacterium*) vs Haloarculaceae (*Haloarcula*). Search:
- *Halobacterium salinarum* vs *Haloarcula marismortui*

Use the most well-known type strains when searching TimeTree — they have the most published studies behind them, so you get more data points and tighter confidence intervals.

---

## Step 3: What numbers TimeTree gives you

For each search TimeTree returns:
- **Time** — the divergence time in Mya (this is your key number)
- One or more studies with individual estimates
- Sometimes a CI or range across studies

The **mean/consensus time** is what you use. If multiple studies are listed, TimeTree averages them — use that average.

---

## Step 4: Convert to MCMCtree units

MCMCtree works in **units of 100 Mya**. So:

```
MCMCtree value = Mya ÷ 100

Examples:
  279 Mya → 2.79
  200 Mya → 2.00
  150 Mya → 1.50
   50 Mya → 0.50
```

---

## Step 5: Choose your prior type and fill the parameters

There are two prior types you'll use:

### For the root → use `ST` (skew-t, soft prior)
```
'ST(mean, sigma, shape, scale)'
```
- **mean** = your TimeTree value converted to MCMCtree units
- **sigma** = uncertainty. Use `0.05` if TimeTree gave you one study, `0.1` if estimates varied a lot across studies
- **shape and scale** = keep `0.112` and `109.124` (these are standard values from the tutorial — don't change them)

Example: TimeTree says 279 Mya → `ST(2.79,0.05,0.112,109.124)`

### For internal nodes → use `B` (hard bounds)
```
'B(lower,upper,1e-300,0.025)'
```
- **lower** = TimeTree value minus ~20–30% converted to MCMCtree units (your minimum age)
- **upper** = TimeTree value plus ~20–30% converted to MCMCtree units (your maximum age)
- `1e-300` and `0.025` are standard tail probabilities — don't change them

Example: TimeTree says 200 Mya → lower = 160 Mya = 1.60, upper = 240 Mya = 2.40 → `B(1.60,2.40,1e-300,0.025)`

The ±20–30% window reflects the uncertainty around a single point estimate. If TimeTree gives you a confidence interval directly, use those bounds instead.

---

## Step 6: Sanity check — the bounds must be nested

Before running, verify that your calibrations respect the tree topology:

```
lower(root) > upper(any internal node)   ← root must always be oldest
lower(internal) < upper(root)            ← internal must fit inside root bounds
```

In your case: root = 279 Mya, so both internal calibrations must have their upper bound below 279 Mya (i.e., upper < 2.79).

---

## Complete worked example using your tree

| Search on TimeTree | Result (Mya) | MCMCtree units | Prior |
|---|---|---|---|
| *Haloferax* vs *Natrialba* | 279 | 2.79 | `ST(2.79,0.05,0.112,109.124)` |
| *Haloferax* vs *Halorubrum* | e.g. 180 | 1.80 | `B(1.26,2.16,1e-300,0.025)` |
| *Halobacterium* vs *Haloarcula* | e.g. 160 | 1.60 | `B(1.12,1.92,1e-300,0.025)` |

Then plug those into your CSV:
```
name;tip1;tip2;MCMCtree
root_calib;Haloferax_gibbonsii_ARA6;Halostagnicola_larsenii_XH_48_XH_48;'ST(2.79,0.05,0.112,109.124)'
haloferacales_calib;Haloferax_gibbonsii_ARA6;Halohasta_litchfieldiae_tADL;'B(1.26,2.16,1e-300,0.025)'
halobacteriales_calib;Halobacterium_salinarum_91_R6;Haloarcula_halobia_XH51;'B(1.12,1.92,1e-300,0.025)'
```

The tip names in `tip1`/`tip2` must always be **exact names from your tree file** — those are just used by the R script to find the node. The TimeTree search can use any well-known strain of that genus.

There arr trees https://www.nature.com/articles/s41598-020-77723-6/figures/4 and https://www.microbiologyresearch.org/content/journal/ijsem/10.1099/ijsem.0.006879
