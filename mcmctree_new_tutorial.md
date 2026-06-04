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
