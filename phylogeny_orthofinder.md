Generally speaking, protein input yields higher accuracy and more reliable phylogenetic trees than DNA input when you are looking at deeper evolutionary time scales (e.g., comparing different species, genera, or families). So I will be using protein input

I created a new folder phylogeny and copied fna and faa files into diff folders. I removed ref and wlsby files from both 

```bash
conda install bioconda::orthofinder

orthofinder -f ./faa -M msa
```

Didn't work. Not sure why



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

#### Unsuccessful attempts to get an alignment file that made me rerun OrthFinder with renamed protein ids:
Running MSA with this tutorial (to continue with RAXML-ng): https://biohpc.cornell.edu/doc/alignment_exercise3.pdf
Initially thought I might not run it because I already have MSA with famsa done in orthofinder but it turned out wrong so i ran alignment anew eventually
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
Didn't work.
I know the problem now. I have duplicate accessions for my species - i have 83 (as planned) samples but some of them are repeated several times. Probably they had the same accession number in NCBI. I need to map those repeating accessions back to species names

Turns out I had duplicate entries for proteins in closely related species. I will rename protein ids in faa files and re run orthofinder:
```bash
# For each .faa file, prepend a short species tag to every header
for f in ./*.faa; do
    tag=$(basename "$f" .faa)
    sed "s/^>/>${tag}|/" "$f" > "${tag}_renamed.faa"
done
mkdir renamed
mv *renamed.faa ./renamed/
conda activate archaea
orthofinder -f /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed
```

So the final results will be in /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May20/

Will wait for it to complte about 1.5 hours

Accidentally deleted results from 20th May; had to rerun on 21 May

MSA:
```bash
cd /mnt/harddisk/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May20/Single_Copy_Orthologue_Sequences
mkdir alignment
ls *.fa | xargs -I {} echo "mafft --thread 1 --amino --inputorder --quiet {} > ./alignment/aln_{} ; Gblocks ./alignment/aln_{} -t=p -b5=h" > msa.batch
parallel -j 20 < msa.batch
```

Changing format to fas and concatenating:
```bash
cd alignment
for f in *-gb.fa; do
    cp "$f" "${f%-gb.fa}.fas"
done
perl /home/aygera/tools/FASconCAT-G-master/FASconCAT-G_v1.06.1.pl -s -p 
```

	!FILE-ERROR!: Unknown character found in sequence Haladaptatus_caseinilyticus_ZJ1|WP_266074721.1 of file aln_OG0000247.fa.fas!
>Haladaptatus_caseinilyticus_ZJ1|WP_266074721.1
MLDTVVIATD GSESVERAVT VALDLARRFD AEVHTLYVVD TGEVESSPET LREELHTALE
SQGERALESI IVTAVREGDP AAEIREYARD HDADVVATGT RGRHGENRFL IGSVAERVVR
TCPTPVLTVR QL

This might be caused by spaces:
```bash
# Fix all alignment files at once
for f in aln_*.fas; do
    sed '/^>/! s/ //g' "$f" > "no_spaces_${f}"
done
mkdir no_spaces
mv no_spaces_* ./no_spaces
```

Running that perl script to get 1 file:
```bash
cd no__spaces
perl /home/aygera/tools/FASconCAT-G-master/FASconCAT-G_v1.06.1.pl -s -p 
```

Process killed error. IDK why

Finally:
```bash
perl /home/aygera/tools/catfasta2phyml-master/catfasta2phyml.pl no_spaces_aln_*.fa.fas --concatenate > supermatrix.txt 
```

Final results for Ortofinder are in ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/

Specifically RaxML-ng will ebe done in ~/biostar/archaea/phylogeny/ncbi_dataset_with_proper_names/only_selected/renamed/OrthoFinder/Results_May21/Single_Copy_Orthologue_Sequences/alignment/no_spaces

Ortofinder can identify horizontal gene transfer and the results are in Putative_Xenologs/. Need to take a look at that
