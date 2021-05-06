#!/bin/sh
sudo apt-get install -y jq
while true
do        
        RANDOMARCHIVELB_IP=$(gcloud compute forwarding-rules list --filter="NAME ~ randomarchive" --format=json | jq -r '.[] | .IPAddress')
        #echo "Current randomarchive loadbalancer ip is: $RANDOMARCHIVELB_IP"
        for i in $(seq 1 1800)
        do
                curl -I http://"$RANDOMARCHIVELB_IP"
                sleep 1
        done
done
