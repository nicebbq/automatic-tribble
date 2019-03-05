#!/bin/bash  
echo "Starting data loading"
echo
base_dir="/home/fastravel/"
data_dir="${base_dir}/raw_data/hotels/"
api_key_file="${base_dir}/keys/amadeus_apikey1.txt"
cities_file="${base_dir}/raw_data/US_cities_limited.csv"
#cities_file="${base_dir}/raw_data/US_cities_WAS.csv"
apikey=$(cat "$api_key_file")
summary_file="${base_dir}/raw_data/hotels_summary.txt"
radius=20 #in km
start_date=$(date --date="next day" +"%Y-%m-%d")

load_data(){
  file_name="${data_dir}$1_$4--$5.txt"
  url="https://api.sandbox.amadeus.com/v1.2/hotels/search-circle?apikey=${apikey}&latitude=$2&longitude=$3&radius=${radius}&check_in=${check_in_date}&check_out=${check_out_date}"
  #&all_rooms=true"
  curl -X GET "${url}" > $file_name
  wc -l $file_name >> $summary_file
}
  

mkdir -p $data_dir
cat $cities_file|while IFS=, read -r index name cid lat long code
  do
    if [ "$name" == "name" ]; then
        continue
    fi
    for i in {1..200}
    do
      check_in_date=$(date -I -d "$start_date + $i days")
      check_out_date=$(date -I -d "$check_in_date + 1 day")
      echo "$code $check_in_date $check_out_date"
      load_data $code $lat $long $check_in_date $check_out_date
    done
  done
  
echo
echo "Done data loading" 
