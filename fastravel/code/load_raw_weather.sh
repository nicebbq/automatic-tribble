#!/bin/bash  
echo "Starting data loading"
echo
data_dir='/home/fastravel/raw_data/weather/'
api_key_file='/home/fastravel/keys/openweathermap_apikey.txt'
#cities_file='../raw_data/US_cities_sample.csv'
cities_file='/home/fastravel/raw_data/US_cities_final.csv'
apikey=$(cat "$api_key_file")
summary_file='/home/fastravel/raw_data/weather_summary.txt'
#start_date='2018-06-23'
start_date=$(date --date="next day" +"%Y-%m-%d")
echo $start_date

load_data(){
  file_name="${data_dir}$1_$5.txt"
  echo $file_name
  url="http://api.openweathermap.org/data/2.5/forecast?lat=$2&lon=$3&appid=${apikey}" #5d forecast
  #url="http://api.openweathermap.org/data/2.5/forecast/daily?lat=$1&lon=$2&cnt=10&appid=${apikey}" #16 day - for fee only
  curl -X GET "${url}" > $file_name
  wc -l $file_name >> $summary_file
}

mkdir -p $data_dir
cat $cities_file|while IFS=, read -r index name cid lat long code
  do
    if [ "$name" == "name" ]; then
        continue
    fi
    echo "$code $name $start_date"
    load_data $code $lat $long $cid $start_date
  done

echo
echo "Done data loading" 
