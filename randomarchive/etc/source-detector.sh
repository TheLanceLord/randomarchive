#!/bin/sh
while true
do
        gcloud sql instances list --filter="NAME=randomarchive">privateip.txt
        RANDOMARCHIVESQL_IP=$(awk 'NR == 2 {print $6}' privateip.txt)
        if [ $RANDOMARCHIVESQL_IP != "" ]
        then
                sed -i '6s/.*/    "MYSQL_HOST": "'"$RANDOMARCHIVESQL_IP"'",/' config.json
        fi
        RANDOMARCHIVE_BUCKET=$(gsutil list)
        RANDOMARCHIVE_BUCKET=${RANDOMARCHIVE_BUCKET#'gs://'}
        RANDOMARCHIVE_BUCKET=${RANDOMARCHIVE_BUCKET%'/'}
        if [ $RANDOMARCHIVE_BUCKET != "" ] 
        then
                sed -i '9s/.*/    "GCS_BUCKET_NAME": "'"$RANDOMARCHIVE_BUCKET"'"/' config.json
        fi

        ISBREAKAGEZERO=$(echo "SELECT is_active FROM breakage_scenario WHERE scenario=0;" | mysql -N --database=randomarchive --host=$RANDOMARCHIVESQL_IP --user=root --password=CorrectHorseBatteryStaple)
        if [ $ISBREAKAGEZERO -eq 1 ] 
        then
                sed -i '4s/.*/    "MYSQL_USER": "elliott",/' config.json
                sed -i '5s/.*/    "MYSQL_PASSWORD": "Password123",/' config.json
        else
                sed -i '4s/.*/    "MYSQL_USER": "root",/' config.json
                sed -i '5s/.*/    "MYSQL_PASSWORD": "CorrectHorseBatteryStaple",/' config.json
        fi

        sudo supervisorctl reload
        sleep 300
done
