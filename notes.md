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



I will use the oldest node in timetree.org when looking up Halobacteria class which is
Name: no name
Rank: no rank
Clade Size: 65
Estimated Time: 413.7 MYA
Adjusted Time: 2400

If I look at the paper i see this but for that I would have to use an outgroup and re-run the analysis:
Archaeoglobus/Haloferax split (3240 Ma)	node 8
Methanosarcina/Haloferax split (2740 Ma)

And the second timetree.org split i can use is Halobacterium and Halarchaeum = Halobacterium_salinarum_KBTZ01 and Halarchaeum_sp_CBA1220_CBA1220
Name: no name
Rank: no rank
Clade Size: 2
Estimated Time: 140.8 MYA
Adjusted Time: 168
CI: n/a

but then my tree doesn't match with halomarina being the outgroup... might use just 1 calibration? either way i will wait for the new model to finish first


If I use v2 then the outgroup is Nanoarchaeum and Halobacterium and they diverged 3976 MYA
Natronoarchaeum_mannanilyticum_JCM_16328 and Halobacterium_salinarum_91_R6



If I use v3 i can compare Natrinem and Halobacterium 314 MYA
