#*******************ques 1***************************



if [ "$(ls -A ~/Data)"  ] 
	then 
		rm -r ~/Data
fi
mkdir ~/Data 

while IFS=' ' read -r startyear endyear 
do 
	name=$startyear$endyear
	touch ~/Data/${name}.txt
done < "Buckets.txt"

while IFS=',' read -r player playerstart c d e f g h collegename # we are separating using comma so it's pocking up comma of date
do
	while IFS=' ' read -r startyear endyear 
 		do
 			if [ $playerstart -ge $startyear ] && [ $c -le $endyear ]
 			then 
 				echo "$player            " "$collegename" >> ~/Data/$startyear$endyear.txt
 				fi

 		done <"Buckets.txt"

done < "players_clean.csv"


#*******************ques 2***************************