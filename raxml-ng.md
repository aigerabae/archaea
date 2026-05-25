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
