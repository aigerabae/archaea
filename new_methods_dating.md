https://www.nature.com/articles/s41467-019-13443-4#Sec9            --- builds phylogeny of 10k prokaryotes (uses universal clock)
https://www.nature.com/articles/s41576-020-0233-0                  --- reviews methods for phylegeny (nature reviews)

1) We begin with the identification of orthologous genes (that is, genes whose relationships will reliably reflect species relationships) from sets of genome or transcriptome sequences.
2) We then discuss how to align orthologues from different species to account for insertions and deletions, and strategies for trimming unreliably aligned regions.
3) Finally, we discuss in detail the choice of inference methods and substitution models and consider potential errors as well as approaches to identify and avoid or mitigate them.


- **Orthology** is a special type of homology in which genes in different species have diverged from each other due to speciation15,16. As a result, orthologous genes recapitulate the relationships among the species they derive from (Fig. 2b). 
- Other forms of homology include **paralogy**, in which genes from two species are derived from gene duplications deeper in time than the common ancestor of the two species (Fig. 2c),   
- and **xenology**, where a gene in one species derives from a distantly related species through horizontal gene transfer (HGT).   

Paralogy and xenology do not reflect the relationships among species (Fig. 2c). Therefore, determining orthologous genes is an essential step for reconstructing species phylogenies16,17 (Fig. 1c). Gene duplications and losses in different lineages are common and may lead to paralogous relationships even among single-copy genes, posing a challenge to orthology identification.

We have to compare orthologues, and the right set of them because otherwise it will show how a gene might have duplicated and this gene diverged from that gene longer time than the species diverged or vice versa. We need to distinguish between paralogues and orthologues and not include paralogues into orthologues analysis

Approaches for de novo identification of orthologues fall into two main categories (Table 1): tree based and graph based18
1) tree based is conceptually corretc but prone to errors as go deeper. Gene family relationships may be further obscured if other processes causing gene-tree discordance are not accounted for such as incomplete lineage sorting, horizontal gene transfer, hybridization, introgression and non-allelic gene conversion22,24.
2) Graph-based orthology inference methods. Graph-based approaches are not immune to the problems described for tree-based methods, but they have the advantage of being computationally efficient and scaling well with large datasets27.

An alternative to de novo prediction is to use a set of **reference orthologues** and to identify their co-orthologues in newly sequenced species. Several dedicated databases offer orthologous sequences suitable for this cause, some spanning all domains of life, for example, OrthoDB29 and OMA35 and others focused on specific groups of organisms such as plants (Plaza36) and mammals (OrthoMam37). Several pipelines are available for automating this procedure (for example, ref.38) and there are two advantages in following this strategy. First, it is computationally cheaper than de novo inference and, second, it may alleviate errors associated with incomplete gene sampling. 

A final consideration for orthology prediction is the genetic fragment that is used as the unit. It is typical to use genes (entire or partial) as a means of identifying orthologous parts of a species’ genome. However, most genes consist of multiple domains and, through time, their order and number may change. In this context, it has been suggested that domains may be more suitable units for orthology and consequently for phylogenetic inference46,47.

