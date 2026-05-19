I created a new folder phylogeny and copied fna and faa files into diff folders. I removed ref and wlsby files from both 

```bash
conda install bioconda::orthofinder

orthofinder -f ./faa -M msa
```

Didn't work. Not sure why


Fron https://pmc.ncbi.nlm.nih.gov/articles/PMC11117635/ (good review of methods for phylogeny)
"Studies have reported that when using the same parameters and the same program, approximately 9% to 18% of single-gene phylogenetic trees cannot replicate the same topology [64]."
So using multiple genes is beneficial

Currently, there are two main methods for constructing multi-gene phylogenetic trees: 
- concatenation phylogeny (one tree given all genes) =  supermatrix method or total evidence
 In addition, the supermatrix method usually assumes that all genes have undergone the same evolutionary process, while there may be lineage sorting during the evolution of species, which can lead to conflicts between gene trees and species trees

- coalescence phylogeny (multiple trees for each gene, combined into 1) = supertree method or separate analysis
Studies across multiple data sets have shown that multi-species supertree models generally outperform concatenation models in phylogenetic inference [82]. However, because the supertree method directly operates on the phylogenetic tree and utilizes tree information summarized from various data sets, it often overlooks a significant amount of phylogenetic information [71].


Currently popular tree-building software includes PHYLIP [83], PAUP* [84], PhyML [85], MrBayes [86], MEGA [87], and Phylosuite [88].

However, due to the preset nature of software functionalities and options, it is often challenging to meet users’ flexible analysis needs. Processing large datasets with these software tools can be cumbersome and slow, leading to various inconveniences.

R offers a wide range of packages tailored for phylogenetic tree construction and analysis, including popular packages such as ape [92], phangorn [93], and dendextend [94].Notable examples include Treeio [95] and tidytree [96], which facilitate the manipulation of evolutionary trees and associated data within R.

Methods for inferring trees:
1) NJ = neighbor-joining: a representative method and one of the most popular distance-based methods
The NJ method has high accuracy and fewer assumptions when reconstructing phylogenetic trees. the advantages of the NJ method over the parsimony method and likelihood method become more evident, leading to its wide usage in analyzing large datasets

2) MP = maximum parsimony
Maximum parsimony is known for its straightforward mathematical approach and absence of a specific model. It is well suited for data types where designing appropriate evolutionary models is challenging, such as rare features based on genomic rearrangements or unique morphological traits. However, when applied to large datasets, it frequently generates numerous potential rooted trees, rendering comprehensive comparisons unfeasible [28].

3) ML = maximum likelihood
exhaustive searches are only suitable for phylogenetic inference based on a small number of taxa, and for inference based on more taxa, tree space searches are usually heuristic [49].Because likelihood methods have clear model assumptions, the probability of systematic errors (such as long-branch attraction artifacts) is lower than that of parsimony methods. greatly increase the computational burden

4) BI = Bayesian inference
The superiority of Bayesian inference lies in its ability to handle large datasets at a higher computational speed than maximum likelihood methods and to measure the confidence of trees through posterior probabilities.


To make orthofinder work I had to:
```bash
# Remove everything after the first space in headers
sed -i 's/ .*//' *.faa 

# Remove asterisks (stop codons) and dots which often cause Diamond errors
sed -i 's/[*.]//g' *.faa
```

Then 
```bash
orthofinder -f ./faa
```

Summary: 
 OrthoFinder assigned 146506 genes (93.6% of total) to 11624 orthogroups.       
 50% of genes were in orthogroups with 25 or more genes (G50 was 25) and were   
 contained in the largest 2114 orthogroups (O50 was 2114).                      
 There were 602 orthogroups with all species present and 453 of these consisted 
 entirely of single-copy genes. 


I will run all 272 species on server dell
```bash
conda create --name archaea
conda activate archaea
conda install bioconda::orthofinder
orthofinder -f ./all_faa_files

# didn't work with famsa so
conda install -c bioconda famsa
```

I tried running locally first but in 30 mins it barely finished a few percent. So i thought it might crash
This doesn't work. I'll leave it for now. The options are tp use a different older method or stop after creating dendrogroups

I will use -og fkag to stop the analysis after ortogroups:
```bash
orthofinder -f ./all_faa_files -og
```

I made a new selection of species that includes all families DK used, 2 for each genus and 1 more for our KBTZ samples. i also renamed them to have strains encoded in the name for clarity. some geni were not present in my selection (Halobacteriales order, annotated genomes and complete assembly only) - for some reason when i downloaded it was 278 and now its 282; i suppose someone added more assemblies in the meantime
Do it on 83 species:
```bash
conda activate archaea
orthofinder -f /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected
```

Running MSA with this tutorial: https://biohpc.cornell.edu/doc/alignment_exercise3.pdf
Might not run it because I already have MSA with famsa done in orthofinder
```bash
conda install bioconda::mafft
conda install bioconda::gblocks

cd /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/OrthoFinder/Results_May19/Single_Copy_Orthologue_Sequences
ls *.fa | xargs -I {} echo "mafft --thread 1 --amino --inputorder --quiet {} > aln_{} ; Gblocks aln_{} -t=p -b5=h" > msa.batch
parallel -j 20 < msa.batch
```

After it's done:
```bash
head aln_OG0000599.fa-gb.fa
```

Concatenating all files together:
```bash
mkdir ../MSAdir
cp *fa-gb.fa ../MSAdir/
/home/aygera/tools/catfasta2phyml-master/catfasta2phyml.pl /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/OrthoFinder/Results_May19/MSAdir/*.fa > /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/OrthoFinder/Results_May19/out.phy > partitions.txt
```

Still the numbers don't allow me to make a single file. Why?
```bash
awk '!/^>/{print length($0)}' aln_OG0000512.fa-gb.fa | head -20
awk '/^>/{if(seq!=""){print length(seq), name} name=$0; seq=""} !/^>/{seq=seq$0} END{print length(seq), name}'  aln_OG0000512.fa-gb.fa | awk '{print $1}' | sort -u
for f in *.fa; do
    unique=$(awk '/^>/{if(seq!=""){print length(seq)} name=$0; seq=""} !/^>/{seq=seq$0} END{print length(seq)}' "$f" | sort -u | wc -l)
    [ "$unique" -gt 1 ] && echo "$f"
done
```

Generally speaking, protein input yields higher accuracy and more reliable phylogenetic trees than DNA input when you are looking at deeper evolutionary time scales (e.g., comparing different species, genera, or families). So I will be using protein input

To build a tree and get boostrapping values (with input in phy format & DNA model):
raxml-ng --all --msa prim.phy --model GTR+G --prefix D1

With input in fasta, amino acid model and 25 threads:
raxml-ng --all --msa merged.fasta --model LG+G4 --prefix D1 --threads 25

Ortofinder can identify horizontal gene transfer and the results are in Putative_Xenologs/. Need to take a look at that

First I need to get alignments of those 375 genes:
```bash
cd /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/OrthoFinder/Results_May19/Single_Copy_Orthologue_Sequences
ls > ../single_copy_list.txt
cd ../
mkdir -p MSA_single_copy
xargs -I {} cp MultipleSequenceAlignments/{} MSA_single_copy/ < single_copy_list.txt
```

I downloaded this script https://github.com/nylander/catfasta2phyml
/home/aygera/tools/catfasta2phyml-master/catfasta2phyml.pl /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/OrthoFinder/Results_May19/MSA_single_copy/*.fa > /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/OrthoFinder/Results_May19/out.phy > partitions.txt

catfasta2phyml.pl *.fas > out.phy 2> partitions.txt

This doesn't work because my alignment files have varying lengths. I don't know why. Something went wrong in the alignment process because for 275/375 genes it has varying length. I will run alignment as shown in the tutorial

I made alignment again but conversion still doesn't work even tho manual checking didn't detect any incnsistencies. I will use another tool for conversion: https://github.com/PatrickKueck/FASconCAT-G

```bash
for f in *-gb.fa; do
    cp "$f" "${f%-gb.fa}.fas"
done
perl /home/aygera/tools/FASconCAT-G-master/FASconCAT-G_v1.06.1.pl -s -p
```

I know the problem now. I have duplicate accessions for my species - i have 83 (as planned) samples but some of them are repeated several times. Probably they had the same accession number in NCBI. I need to map those repeating accessions back to species names
