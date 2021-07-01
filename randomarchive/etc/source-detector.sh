#!/bin/sh
# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
while true
do
        gcloud sql instances list --filter="NAME ~ randomarchive">privateip.txt
        RANDOMARCHIVESQL_IP=$(awk 'NR == 2 {print $6}' privateip.txt)
        if [ $RANDOMARCHIVESQL_IP != "" ] && [ $RANDOMARCHIVESQL_IP != "-" ]
        then
                sed -i '6s/.*/    "MYSQL_HOST": "'"$RANDOMARCHIVESQL_IP"'",/' config.json
        fi
        # Use the first bucket found as our image bucket
        RANDOMARCHIVE_BUCKET=$(gsutil list)
        RANDOMARCHIVE_BUCKET=${RANDOMARCHIVE_BUCKET#'gs://'}
        RANDOMARCHIVE_BUCKET=$(echo $RANDOMARCHIVE_BUCKET | cut -f1 -d"/")
        if [ $RANDOMARCHIVE_BUCKET != "" ] && [ $RANDOMARCHIVE_BUCKET != "-" ]
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
