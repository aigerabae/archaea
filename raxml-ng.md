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
```
