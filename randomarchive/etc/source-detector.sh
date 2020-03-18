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
                sed -i '9s/.*/    "GCS_BUCKET_NAME": "'"$RANDOMARCHIVE_BUCKET"'",/' config.json
        fi
        sleep 300
done
