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
