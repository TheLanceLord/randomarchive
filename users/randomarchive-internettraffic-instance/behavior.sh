#!/bin/sh
while true
do        
        gcloud compute forwarding-rules list --filter="NAME=randomarchive-webapp-fe">loadbalancer.txt
        RANDOMARCHIVELB_IP=$(awk 'NR == 2 {print $3}' loadbalancer.txt)
        #echo "Current randomarchive loadbalancer ip is: $RANDOMARCHIVELB_IP"
        for i in $(seq 1 1800)
        do
                curl -I http://"$RANDOMARCHIVELB_IP"
                sleep 1
        done
done
