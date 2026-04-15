### Gubbins:
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
I decided to use RefSeq reference sequence for Halobacterium salinarum from https://www.ncbi.nlm.nih.gov/datasets/taxonomy/2242/ for alignment

```bash
for f in *fna; do echo -e "${f%.fna}\t${f}"; done > isolates.list
generate_ska_alignment.py --reference GCF_004799605.1_ASM479960v1_genomic.fna --input isolates.list --out kbt.aln
```

Gubbins:
```bash
run_gubbins.py --prefix kbt kbt.aln --filter-percentage 90 # doesn't work because 3 sequences is too little for iterative algorithm
run_gubbins.py --tree-builder fasttree --filter-percentage 90 kbt.aln
```

Result without fasttree:
```result
Filtering input alignment...
Excluded sequence KBTZ01 because it had 51.62675743307761 percentage missing data while a maximum of 25.0 is allowed
Excluded sequence KBTZ05 because it had 83.74308550920286 percentage missing data while a maximum of 25.0 is allowed
Excluded sequence KBTZ06 because it had 84.53590596292516 percentage missing data while a maximum of 25.0 is allowed
Not enough sequences are left after removing duplicates.Please check you input data.

With fasttree (conclusions):
1. Relationship and Ancestry (The Phylogeny)
The GFF file reveals the structure of the evolutionary tree Gubbins reconstructed:

Node 1 is the most recent common ancestor (MRCA) of your strains KBTZ01 and KBTZ06.

The last row identifies a recombination event occurring on the branch from Node 2 to Node 1. This means the ancestor of both KBTZ01 and KBTZ06 acquired a piece of DNA (at coordinates 675,652–675,700) via horizontal transfer before they diverged into separate strains.

KBTZ01 and KBTZ06 then diverged and independently acquired their own unique horizontal transfers.

2. Strain-Specific Horizontal Gene Transfer
The file lists "recombination predictions," which are blocks of DNA imported from external sources.

KBTZ01: Has at least 5 unique horizontal transfer events shown here. These range in size from very small (10 bp at ~479kb) to moderate (61 bp at ~1.86Mb).

KBTZ06: Appears significantly more "recombinant" than KBTZ01 in this snippet, with 8 unique events. Several of these involve much larger blocks of DNA (e.g., 460 bp at ~1.05Mb and 455 bp at ~1.95Mb).

KBTZ05: This strain is absent from this recombination list. This suggests that either KBTZ05 did not undergo detectable horizontal transfer since it diverged from the others, or it is the "outgroup" that lacks the specific markers identified in this run.

3. Key Evolutionary Events
Shared History: The event on the branch Node_2->Node_1 is a "shared" horizontal transfer. Both KBTZ01 and KBTZ06 carry this 9-SNP signature because they inherited it from their shared parent.

Divergence Drivers: The unique blocks for KBTZ06 at positions ~1.05Mb and ~1.95Mb are significant. Since each contains 12 SNPs, these imports introduced a relatively high amount of genetic variation in a single event, which may have contributed to KBTZ06 developing unique traits compared to KBTZ01.

Recombination "Hotspots": There is a potential hotspot around coordinate 1.72Mb. Both KBTZ01 and KBTZ06 have unique recombination events overlapping this region (1,721,527 for KBTZ01 and 1,721,538 for KBTZ06). This often suggests a specific gene in that area is frequently exchanged or under high selective pressure.

Summary of the "Direction" of Transfer
While Gubbins doesn't name the "donor" species, it shows the direction of inheritance:

Ancestral Transfer: DNA moved from an unknown source into the common ancestor (Node 1).

Recent Transfer: DNA moved from unknown sources into the individual lineages of KBTZ01 and KBTZ06 after they split.
```


Following archeae paper: https://www.nature.com/articles/s41598-020-77723-6#Sec10  
get homologues art tutorial at https://eead-csic-compbio.github.io/get_homologues/tutorial/pangenome_tutorial.html#3_analysis_of_bacterial_pan-genomes

Estimating completeness and annotation
```bash
conda install bioconda::checkm-genome
checkm lineage_wf -t 28 -x fna ~/biostar/archaea/input ~/biostar/archaea/checkm # might want to do this on server bc my computer keeps clashing; i should have all the metrics in ncbi anyways
```

Clustering:
```bash
conda install bioconda::get_homologues
# i copied files faa and fna for eacg if the 3 strains into get_homologues_input
# ## 1 Compute orthologous gene clusters with default settings with BDBH

get_homologues.pl -d ./get_homologues_input -n 20
cd get_homologues_input_homologues/kbtz01_f0_alltaxa_algBDBH_e0_/

# list contents (orthologous gene clusters) and count them
ls && ls | wc
# # 1426 gene clusters

# 1.7 how many genes does each orthologous cluster contain?
grep -c '>' *faa

 # clusters that contain inparalogues (in this case over 3)
grep -c '>' *faa | grep -v ':3'

# OCML
get_homologues.pl -d ./get_homologues_input -M -D -t 0 -A -P -c 

get_homologues.pl -d ./get_homologues_input -D -n 20
```


Gubbins on bacteriodales order:
I first downloaded all archeaea in the order (all complete assemblies). Then I renamed all files to have the name of the species as specified in data_summary.tsv; i then renamed faa and fna files to have names of the folders its in (commands did not save). I then copied them to getting_other_refs and manually added halobacterium sallinarium refseq files to it and named them ref.fna and ref.faa. I also manually added kbtz01 because it was in inside folder and i had to remove them.
I tried to run it like this with about 250 species but my computer clashed so i kept only those in the list provided by Dos.


Not present:
Halobiforma  
Halogranum  
Halomicroarcula  
Halonotius  
Natronobacteria  
Natronolimnobius  
Natronolimnohabitans  
Salinirubrum  

I saved all items in list (1 for each genus) to_keep.tsv - this resulted in 39 entries
