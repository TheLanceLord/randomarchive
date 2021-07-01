#!/bin/sh
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
        for i in $(seq 1 60)
        do
                curl -I http://"$RANDOMARCHIVELB_IP"
                sleep 1
        done
done
