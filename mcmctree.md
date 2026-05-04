In the meantime I will try to construct MCMTree time with 47 species:
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

Explanations:

Another potentially useful took from https://www.cell.com/current-biology/fulltext/S0960-9822(21)00577-7 paper = MCScanX (for finding expansion/shribking of henome)


Following tutorial in https://github.com/sabifo4/Tutorial_MCMCtree.git
(has all steps to get the right input files and run the analysis but only on 1 partition (one fasta file. i can cincatenate them into 1 but this will make it assume all genes had the same rate of evolution. but i dont know how to use multiple partitions yet)




I am giving up because it has no tutorials for multiple partitions. I will try another tool
