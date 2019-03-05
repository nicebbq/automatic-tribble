#!/bin/bash  
echo "Starting data loading"
echo
base_dir="/home/fastravel/"
data_dir="${base_dir}/raw_data/flights/"
api_key_file="${base_dir}/keys/amadeus_apikey1.txt"
cities_file="${base_dir}/raw_data/US_cities_limited.csv"
apikey=$(cat "$api_key_file")
summary_file="${base_dir}/raw_data/flights_summary.txt"
departure_date_start=$(date --date="next day" +"%Y-%m-%d")
departure_date_end=$(date -I -d "$departure_date_start + 180 day")
one_way='true'
direct='false'

load_data(){
  file_name="${data_dir}$1_$2_$3--$4.txt"
  echo $file_name
  #url="https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?apikey=${apikey}&origin=$1&destination=$2&one-way=true&direct=${direct}&aggregation_mode=DAY"
  url="https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?apikey=${apikey}&origin=$1&destination=$2&departure_date=$3--$4&one-way=true&direct=${direct}&aggregation_mode=DAY"
  curl -X GET "${url}" > $file_name
  wc -l $file_name >> $summary_file
}

check_if_file_exists(){
  substr="$1_$2"
  for file_name in "$data_dir"/*
  do
    if [[ $file_name = *"$substr"* ]]; then
      already_exists=1
    fi
  done
}

airports=()
#cat $cities_file|while IFS=, read -r index name cid lat long code
while IFS=, read -r index name cid lat long code
do
 if [ "$code" == IATA ]; then
  continue
 fi
 airports+=($code) 
done < <(cat $cities_file)
echo ${#airports[@]}

mkdir -p $data_dir
for airport1 in "${airports[@]}"
do
  for airport2 in "${airports[@]}"
    do
      if [ "$airport1" == "$airport2" ]; then
        continue
      fi
      already_exists=0
      check_if_file_exists $airport1 $airport2
      if [ $already_exists == 1 ]; then
        echo "Already exists:" $airport1 $airport2
        continue
      fi
      echo $airport1 $airport2 $departure_date_start $departure_date_end
      load_data $airport1 $airport2 $departure_date_start $departure_date_end
    done
done

echo
echo "Done data loading"  
