#!/bin/sh
while true
do        
        gcloud compute forwarding-rules list --filter="NAME=randomarchive-webapp-fe">loadbalancer.txt
        RANDOMARCHIVELB_IP=$(awk 'NR == 2 {print $3}' loadbalancer.txt)
        #echo "Current randomarchive loadbalancer ip is: $RANDOMARCHIVELB_IP"
        gcloud sql instances list --filter="NAME=randomarchive">privateip.txt
        RANDOMARCHIVESQL_IP=$(awk 'NR == 2 {print $6}' privateip.txt)
        #echo "Current randomarchive sql private ip is: $RANDOMARCHIVESQL_IP"
        ISBREAKAGEZERO=$(echo "SELECT is_active FROM breakage_scenario WHERE scenario=2;" | mysql -N --database=randomarchive --host="$RANDOMARCHIVESQL_IP" --user=root --password=CorrectHorseBatteryStaple)
        #echo "Is breakage scenario 3 running?: $ISBREAKAGEZERO"
        if [ $ISBREAKAGEZERO -eq 1 ] 
        then
                for i in $(seq 1 1800)
                do
                        curl -I http://"$RANDOMARCHIVELB_IP"
                done
        else
                for i in $(seq 1 12)
                do
                        curl -I http://"$RANDOMARCHIVELB_IP"/about
                        sleep 5
                done
        fi
done
