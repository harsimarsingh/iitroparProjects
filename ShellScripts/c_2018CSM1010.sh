if [ "$(ls -A ~/Data)"  ] 
	then 
		rm -r ~/Data
fi
mkdir ~/Data 

while IFS= read uniname
do 
	name=`echo $uniname | sed 's| | |g'`
	touch ~/Data/"$name.txt"		
done <"Univ.txt"

while read -r univcollege 
do
	while IFS=',' read -r a b c d e f g h collegename # we are separating using comma so it's pocking up comma of date  
	do
		if [ ! "$collegename" == "" ]
		then 	
			if [[ $univcollege == $collegename ]]
				then 
				difff=$(( c-b ))
				echo "$difff" "$a" "$b" "$c"  >> ~/Data/"temp$collegename.txt"
			fi
		fi
	done < "players_clean.csv"
done <"Univ.txt"


while IFS=',' read -r univcollege
do
	sort -k1 -r -n ~/Data/"temp$univcollege.txt" >> ~/Data/"tempsort$univcollege.txt"
	
done <"Univ.txt"

while IFS=',' read -r univcollege
do
	grep "" ~/Data/"tempsort$univcollege.txt" >> ~/Data/"last$univcollege.txt"
done <"Univ.txt"

while IFS=',' read -r univcollege
do
	while IFS=' ' read -r p q r s 
	do
		echo "$q $r $s" >> ~/Data/"$univcollege.txt"
	done < ~/Data/"last$univcollege.txt"
done <"Univ.txt"


while IFS=',' read -r univcollege
do
	rm ~/Data/"last$univcollege.txt"
	rm ~/Data/"temp$univcollege.txt"
	rm ~/Data/"tempsort$univcollege.txt"
done <"Univ.txt"



