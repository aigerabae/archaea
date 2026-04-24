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
