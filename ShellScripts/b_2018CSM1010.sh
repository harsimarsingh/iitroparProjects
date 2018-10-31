if [ "$(ls -A ~/Data)"  ] 
	then 
		rm -r ~/Data
fi
mkdir ~/Data 

while IFS=' ' read -r startyear endyear 
do 
	name=$startyear$endyear
	touch ~/Data/${name}.txt
	#echo $name
done < "Buckets.txt" 

while IFS=',' read -r a b c d e f g g1 h	
do 
	if [[ $d =~ (-) ]] 
	 	then echo "$a   " "    $d" >> ~/Data/questionb.txt   
	fi
	
done < "players_clean.csv"