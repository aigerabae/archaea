Gubbins on bacteriodales order:
I first downloaded all archeaea in the order (all complete assemblies). Then I renamed all files to have the name of the species as specified in data_summary.tsv; i then renamed faa and fna files to have names of the folders its in (commands did not save). I then copied them to getting_other_refs and manually added halobacterium sallinarium refseq files to it and named them ref.fna and ref.faa. I also manually added kbtz01 because it was in inside folder and i had to remove them.
I tried to run it like this with about 250 species but my computer clashed so i kept only those in the list provided by Dos.

I also extracted folders inside folders with
```bash
mv */*/ .
mv */*/ .
mv */*/ .
mv */*/ .

# did it a few times to extract all available foldes
#And renamed them accordingly

while read -r new_name old_name; do
    # Only proceed if the source directory actually exists
    if [ -d "$old_name" ]; then
        
        target="$new_name"
        counter=1
        
        # If the target name is already taken, increment the suffix
        while [ -e "$target" ]; do
            target="${new_name}_$counter"
            ((counter++))
        done
        
        mv -v -- "$old_name" "$target"
    else
        echo "Source directory '$old_name' not found. Skipping."
    fi
done < dict_rename.txt

# i renamed files as well
for dir in */; do
    (
        cd "$dir" || exit
        for file in *; do
            if [ -f "$file" ]; then
                # Renames file to "FolderName.extension"
                mv -- "$file" "${dir%/}.${file##*.}"
            fi
        done
    )
done
```

I want to either re-download it and do renaming again in a way that will conserve strain s well bc right now it doesn't save kbtz01, only as one of the halobacterium salinarium strains (unnamed)
I want to try using all 278 assemblies for phylogeny

I did that and i had one folder that wasn't renamed and it wasn't any of the kbtz samples so i removed it: GCF_002156705.1

I then copied all faa files into another folder all_faa_files
```bash
mkdir -p ../../all_faa_files
find . -name "*.faa" -exec cp {} ../../all_faa_files/ \;
```

and ran otherfinder again on all 277 assemblies
