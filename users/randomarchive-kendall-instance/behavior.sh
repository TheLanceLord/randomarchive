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
#####################################################################################################################
# IMPORTANT - READ BEFORE YOU PROCEED!!!!                                                                                
# If you are doing this breakage lab as part of an instructor-led training, we ask that you don't look through the 
# user behavior code, as in a real world scenario you wouldn't have a convenient script readily available that
# tells you what a user is doing. If you have questions about a users behavior feel free to ask your instructor!
# If you are doing this breakage lab as a self-paced training on Qwiklabs and if no user context is provided, then
# proceed if you feel stuck, or if you would feel that talking with this user would be the next rational step
#####################################################################################################################
sudo apt-get install -y jq
while true
do
        RANDOMARCHIVELB_IP=$(gcloud compute forwarding-rules list --filter="NAME ~ randomarchive" --format=json | jq -r '.[] | .IPAddress')
        #echo "Current randomarchive loadbalancer ip is: $RANDOMARCHIVELB_IP"
        gcloud sql instances list --filter="NAME ~ randomarchive">privateip.txt
        RANDOMARCHIVESQL_IP=$(awk 'NR == 2 {print $6}' privateip.txt)
        #echo "Current randomarchive sql private ip is: $RANDOMARCHIVESQL_IP"
        ISBREAKAGEZERO=$(echo "SELECT is_active FROM breakage_scenario WHERE scenario=1;" | mysql -N --database=randomarchive --host="$RANDOMARCHIVESQL_IP" --user=root --password=CorrectHorseBatteryStaple)
        #echo "Is breakage scenario 1 running?: $ISBREAKAGEZERO"
        if [ $ISBREAKAGEZERO -eq 1 ] 
        then
                gcloud compute firewall-rules list --filter="NAME ~ randomarchive-network-security-rule">firewall.txt
                [ -s /user/firewall.txt ]
                if [ $? -eq 1 ]
                then
                        RANDOMARCHIVEPROJECT_ID=$(gcloud config list project --format 'value(core.project)')
                        gcloud compute --project="$RANDOMARCHIVEPROJECT_ID" firewall-rules create randomarchive-network-security-rule --direction=INGRESS --priority=999 --network=default --action=DENY --rules=tcp:80 --source-ranges=35.191.0.0/16,209.85.152.0/22,209.85.204.0/22 --target-tags=allow-external-traffic
                fi
                for i in $(seq 1 12)
                do
                        curl -I http://"$RANDOMARCHIVELB_IP"/about
                        sleep 5
                done
        else
                gcloud compute firewall-rules list --filter="NAME ~ randomarchive-network-security-rule">firewall.txt
                [ -s /user/firewall.txt ]
                if [ $? -eq 0 ]
                then
                        yes | gcloud compute firewall-rules delete randomarchive-network-security-rule
                fi
                for i in $(seq 1 12)
                do
                        curl -I http://"$RANDOMARCHIVELB_IP"/about
                        sleep 5
                done
        fi
done
