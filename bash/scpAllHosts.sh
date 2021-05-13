while IFS= read -r dest; do
	scp <path to file> "$dest:<path to dest>"
done < destfile.txt
