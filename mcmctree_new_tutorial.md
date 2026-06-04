Following this tutorial designed for amino acid alignments:

I copied files supermatrix.phy, v2.raxml.bestTree_rooted, example_calib_MCMCtree.tree (changed the format to match the provided example), v2.raxml.bestTreeinto into ~/biostar/archaea/mcmctree
I also cloned this repo and will do all work in designated folders inside it

https://github.com/abacus-gene/paml-tutorial

I will use class node calibration from timetree:
Name: Halobacteria
Rank: class
Clade Size: 177
Estimated Time: 455.3 MYA
Adjusted Time: 2400
CI: n/a
NCBI Link: Halobacteria

Using rooted tree i will remove branch lengths:
sed 's/:[0-9]*\.[0-9]*//g' v2.raxml.bestTree_rooted > no_branch_lengths.tree

I used Claude to add root calibration to it into Calibnodes_haloarchaea.tree

The rest was as shown here: https://github.com/abacus-gene/paml-tutorial/blob/main/mcmctree-approxlnL-aa/README.md

I am currently on this step: codeml *ctl > log_CODEML.txt to calculate branch lengths, the gradient, and the Hessian; the process is running locally 
This finished and now I am moving on

Because it's my data I need to run priors first:
```bash
## Run from 02_PAML
cd 01_MCMCtree
home_dir=$( pwd )
for i in `seq 1 6`
do
  cd $home_dir/00_prior/NODAT/$i
  printf "[[ Running MCMCtree for chain "$i" | prior ]]\n"
  mcmctree *ctl 2>&1 | tee log_mcmc$i"_prior.txt"
done
cd $home_dir
```

The priors are looking good. I will run the rest now:
```bash
## Run from `02_PAML`
cd 01_MCMCtree
home_dir=$( pwd )
for i in `seq 1 6`
do
  printf "[[ Running MCMCtree for chain "$i" | posterior (ILN) ]]\n"
  cd $home_dir/01_posterior/ILN/$i
  mcmctree *ctl 2>&1 | tee log_mcmc$i"_postILN.txt"
  printf "[[ Running MCMCtree for chain "$i" | posterior (GBM) ]]\n"
  cd $home_dir/01_posterior/GBM/$i
  mcmctree *ctl 2>&1 | tee log_mcmc$i"_postGBM.txt"
done
cd $home_dir
grep 'Species tree for FigTree' -A1 00_prior/NODAT/1/out.txt | sed -n '2,2p' > 00_prior/node_tree.tree
```
