Location:
~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces


Generally speaking, protein input yields higher accuracy and more reliable phylogenetic trees than DNA input when you are looking at deeper evolutionary time scales (e.g., comparing different species, genera, or families). So I will be using protein input


RaXML-ng:
```bash
raxml-ng --all \
    --msa supermatrix.txt \
    --model LG+G4+F \
    --prefix v1 \
    --threads 25 \
    --bs-trees 1000 \
    --seed 12345
```

Started at 19:24, 21 May 2026
Still didn't finish bootstrapping on Monday 3PM; killed the process since the tree doesn't even look good - orthofinder's tree makes more sense. might need to change the model and limit number of bootstraps (until convergence takes too much time)

Some say the model should be chosen with some thinking. I will install the software and test it tomorrow if my run is still incomplete:
```bash
conda install bioconda::modeltest-ng
tail -n +2 supermatrix.txt > supermatrix_noheader.txt

modeltest-ng -d aa −i supermatrix_noheader.txt -o model_selection  -p 25 -r 42 −h uigfr −f ef -m DAYHOFF,LG,DCMUT,JTT,MTREV,WAG,RTREV,CPREV,VT,BLOSUM62,MTMAM,MTART,MTZOA,PMB,HIVB,HIVW,JTT-DCMUT,FLU,STMTREV,LG4M,LG4X,GTR
```

The reason this doesn't work is because it was it used the wrong kind of dashes. However, I suspect that my supermatrix is also wrong and that's why the results of RaxML-ng previous run were so bad. I wrote a custom script to create a supermatrix.fa (uploaded here)
```bash
python build_supermatrix.py --check 2>&1 | head -50                  # sanity check
python build_supermatrix.py
```

Rerunning modeltest on server (installed via conda the same way):
```bash
modeltest-ng -d aa -i supermatrix.fa -o model_selection  -p 25 -r 42 -h uigfr -f ef -m DAYHOFF,LG,DCMUT,JTT,MTREV,WAG,RTREV,CPREV,VT,BLOSUM62,MTMAM,MTART,MTZOA,PMB,HIVB,HIVW,JTT-DCMUT,FLU,STMTREV,LG4M,LG4X,GTR
```

Locally will rerun previous model and see if there any differences (previous results are in a separate folder) - i used slightly different model tho and only 100 bootstraps:
```bash
raxml-ng --all \
    --msa supermatrix.fa \
    --model LG+F+G \
    --prefix v2 \
    --threads 25 \
    --bs-trees 100 \
    --seed 12345
```

For now the orthofinder tree looks more sensible. potential reasons:
1. Gblocks is too aggressive (biggest culprit)
-b5=h is the most permissive Gblocks setting, but Gblocks in general throws away a lot of phylogenetically informative sites — sometimes 50-80% of your alignment. OrthoFinder by default uses a much gentler trimming (or none at all). With only 89,174 bp before trimming, you may be feeding RAxML a drastically reduced and biased subset. Try running without Gblocks entirely, or replacing it with trimAl -automated1 which is considered more appropriate for phylogenomics.
2. Single model for a partitioned dataset
You're fitting one LG+G4+F to the entire supermatrix concatenation of 375 genes. OrthoFinder uses a partitioned model (one model per gene). Forcing a single substitution model across genes with very different evolutionary rates can seriously distort branch lengths and topology. Use your partitions.txt file:
bashraxml-ng --all --msa supermatrix.fa --model partitions.txt --prefix v1 --threads 25 --bs-trees 1000 --seed 12345
3. MAFFT default settings may be suboptimal
mafft --amino --inputorder uses the default (FFT-NS-2) algorithm which is fast but less accurate. For phylogenomics, --maxiterate 1000 --localpair (L-INS-i) is much better for single-gene alignments, though slower.
4. OrthoFinder uses STAG + ASTRAL, not concatenation
This is conceptually important: OrthoFinder infers a species tree from individual gene trees (STAG algorithm + ASTRAL coalescence), which handles incomplete lineage sorting and gene tree discordance. Your pipeline does concatenation, which assumes all genes have the same history. For prokaryotes with potential HGT, the coalescence approach can be more accurate.
5. The supermatrix.txt from catfasta2phyml
You used catfasta2phyml.pl in your original pipeline but then switched to the Python script for supermatrix.fa. Make sure you're actually feeding RAxML the correct file and that the taxon names are clean (no |accession suffixes that could confuse it).
The quickest wins:

Drop Gblocks or replace with trimAl -automated1
Add the partition model (--model partitions.txt)
Consider using the OrthoFinder species tree directly if your goal is a reliable reference — it's genuinely hard to beat for prokaryotic phylogenomics
