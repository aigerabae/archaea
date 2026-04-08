Gubbins:
```bash
conda create --name archaea
conda activate archaea
conda config --add channels r
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
conda install gubbins
conda install -c bioconda ska2
```

Alignment:
```bash
for f in *fna; do echo -e "${f%.fna}\t${f}"; done > isolates.list
generate_ska_alignment.py --reference RMV4.fa --input PMEN3_isolates.list --out PMEN3.aln
```

run_gubbins.py [FASTA alignment]
run_gubbins.py --prefix PMEN1 --first-tree-builder rapidnj --first-model JC --tree-builder raxmlng --model GTR PMEN1.aln
