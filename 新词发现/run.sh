python findNewWords.py > res
python temp.py > res1
cat res1 t | sort | uniq -d  > file3
cat res1 file3 | sort | uniq -u > newwords
