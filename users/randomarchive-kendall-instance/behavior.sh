#!/bin/sh
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
