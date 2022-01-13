# randomarchive
Simple flask blog site for integration with MySQL and Google Cloud Storage. Intended for SRE training on GCP.

# how to use
After completing a breakage scenario, run 
```
gcloud sql import sql randomarchive-sql gs://randomarchive-static-files/sql/sql_randomarchive_sql_export_healthy
``` 
from the command line to stop the scenario.

# setup
Step 0: Set Environment Variables \
```
CURRENT_PROJECT_ID=$(gcloud config list --format 'value(core.project)')
CURRENT_PROJECT_NUMBER=$(gcloud projects list --format 'value(PROJECT_NUMBER)' --filter="PROJECT_ID:$CURRENT_PROJECT_ID") 
```
////////////////////////////////////////// \
Step 1: Enable all APIs and Services: \
```
gcloud services enable compute.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable serviceusage.googleapis.com
gcloud services enable servicenetworking.googleapis.com
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 2: Create GCS bucket with any name. Populate with images from GitHub \
#Need to make the bucket uniform and grant allUsers Storage Object Viewer permission
```
gsutil mb -b -p $CURRENT_PROJECT_ID -c Standard -l US-CENTRAL1 gs://$CURRENT_PROJECT_NUMBER-randomarchive/

curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/gcs-assets/f3184b202f0f94d4.jpg' 
gsutil cp f3184b202f0f94d4.jpg gs://$CURRENT_PROJECT_NUMBER-randomarchive/

curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/gcs-assets/73b1072c2f219b33.jpg'
gsutil cp 73b1072c2f219b33.jpg gs://$CURRENT_PROJECT_NUMBER-randomarchive/

curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/gcs-assets/8dfdf38de52376dd.jpg'
gsutil cp 8dfdf38de52376dd.jpg gs://<BUCKET_NAME>/

curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/gcs-assets/RandomArchive%20Architecture.jpg'
gsutil cp RandomArchive%20Architecture.jpg gs://<BUCKET_NAME>/

curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/gcs-assets/default.jpg'
gsutil cp default.jpg gs://<BUCKET_NAME>/
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 3: Create CloudSQL MySQL database run the export code in GitHub user=root password=CorrectHorseBatteryStaple
```
gcloud --project=gcp-sre-training-stg beta sql instances create randomarchive \
       --network=default \
       --assign-ip \
       --tier=db-n1-standard-1 \
       --region=us-central1 \
       --version=MYSQL_5_7

gcloud sql users set-password root --host=% --instance randomarchive --password CorrectHorseBatteryStaple

curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/cloudsql-mysql-db/randomarchive_sql_export'
  
gcloud sql connect randomarchive --user=root --password=CorrectHorseBatteryStaple
mysql --user=root --password=CorrectHorseBatteryStaple --host=<'sql_public_ip'> < "randomarchive_sql_export"

#https://github.com/ragingrancher/randomarchive/blob/master/cloudsql-mysql-db/randomarchive_sql_export

#cloudsql-mysql-db/randomarchive_sql_export \
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 4: Create randomarchive-webapp-rule
```
gcloud compute --project=$CURRENT_PROJECT_ID firewall-rules create randomarchive-webapp-rule --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80,tcp:443 --source-ranges=0.0.0.0/0 --target-tags=allow-external-traffic
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 5: Create randomarchive-webapp-template \
```
gcloud beta compute --project=[PROJECT_ID] instance-templates create randomarchive-webapp-template --machine-type=n1-standard-1 --network=projects/gcp-sre-training-dev/global/networks/default --network-tier=PREMIUM --metadata=startup-script=cd\ /randomarchive/randomarchive/etc/$'\n'sh\ source-detector.sh --maintenance-policy=MIGRATE --service-account=[PROJECT_NUMBER]-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=allow-external-traffic,http-server,https-server --image=randomarchive-webapp-image --image-project=gcp-sre-training-dev --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=randomarchive-webapp-template --reservation-affinity=any
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 6: Create randomarchive-webapp-mig
```
gcloud compute --project=[PROJECT_ID] instance-groups managed create randomarchive-webapp-mig --base-instance-name=randomarchive-webapp-mig --template=randomarchive-webapp-template --size=1 --zone=us-central1-a

gcloud beta compute --project "[PROJECT_ID]" instance-groups managed set-autoscaling "randomarchive-webapp-mig" --zone "us-central1-a" --cool-down-period "60" --max-num-replicas "1" --min-num-replicas "1" --target-cpu-utilization "0.6" --mode "off"
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 7: Create randomarchive-webapp-lb7 \
Step 7a: Create randomarchive-webapp-be \
Step 7b: Create randomarchive-webapp-fe \

//////////////////////////////////////////

////////////////////////////////////////// \
Step 8: Create 400_error_threshold and 500_error_threshold alerting policies in Monitoring (requires project id) \
```
curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/stackdriver_alert_policies/400_error_threshold.json'
```
`# need to update the above file with your project id before proceeding
```
gcloud alpha monitoring policies create --policy-from-file="400_error_threshold.json"
```
``` 
curl \
  -O \
  -L 'https://github.com/ragingrancher/randomarchive/raw/master/stackdriver_alert_policies/500_error_threshold.json'
```
`# need to update the above file with your project id before proceeding
```
gcloud alpha monitoring policies create --policy-from-file="500_error_threshold.json" \
```
//////////////////////////////////////////

////////////////////////////////////////// \
Step 9: Create internettraffic, robin, taylor, and kendall instances
```
gcloud beta compute --project=<PROJECT_ID> instances create randomarchive-internettraffic-instance --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --metadata=startup-script=cd\ /user/$'\n'sh\ behavior.sh --maintenance-policy=MIGRATE --service-account=<PROJECT_NUMBER>-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/compute.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/devstorage.read_only --image=randomarchive-internettraffic-image --image-project=gcp-sre-training-dev --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=randomarchive-internettraffic-instance --reservation-affinity=any

gcloud beta compute --project=<PROJECT_ID> instances create randomarchive-kendall-instance --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --metadata=startup-script=cd\ /user/$'\n'sh\ behavior.sh --maintenance-policy=MIGRATE --service-account=<PROJECT_NUMBER>-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/sqlservice.admin,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/devstorage.read_only --image=randomarchive-kendall-image --image-project=gcp-sre-training-dev --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=randomarchive-kendall-instance --reservation-affinity=any

gcloud beta compute --project=<PROJECT_ID> create randomarchive-robin-instance --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --metadata=startup-script=cd\ /user/$'\n'sh\ behavior.sh --maintenance-policy=MIGRATE --service-account=<PROJECT_NUMBER>-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/sqlservice.admin,https://www.googleapis.com/auth/compute.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/devstorage.read_only --image=randomarchive-robin-image --image-project=gcp-sre-training-dev --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=randomarchive-robin-instance --reservation-affinity=any

gcloud beta compute --project=<PROJECT_ID> instances create randomarchive-taylor-instance --zone=us-central1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --metadata=startup-script=cd\ /user/$'\n'sh\ behavior.sh --maintenance-policy=MIGRATE --service-account=<PROJECT_NUMBER>-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/sqlservice.admin,https://www.googleapis.com/auth/compute.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/devstorage.read_only --image=randomarchive-taylor-image --image-project=gcp-sre-training-dev --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=randomarchive-taylor-instance --reservation-affinity=any
```
//////////////////////////////////////////


# breakage scenario #0
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! The rest of your team is out for today, and you are reading up on reliability best practices when you spot your boss hustling up to your desk.
“The site is having issues. Anyone visiting the site is greeted by an internal error message of ours. We need this fixed ASAP before we start losing customers.”

This scenario will take 30-60 minutes to complete.

Command line to run in cloud shell to start the breakage scenario: gcloud sql import sql randomarchive-sql gs://randomarchive-static-files/sql/sql_randomarchive_sql_export_breakage_0

# breakage scenario #1
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! Today, you and your team are in a meeting room working through a Wheel of Misfortune, when there is an urgent knock at the door and your boss pops their head in. 
“Hey team, it looks like the site is completely down. We need it back up and running ASAP before we start losing users.”

You will have ~3 hours to debug the issue. The instructor will call for breaks every 30 minutes to have teams share one thing that they have learned. 

Command line to run in cloud shell to start the breakage scenario: gcloud sql import sql randomarchive-sql gs://randomarchive-static-files/sql/sql_randomarchive_sql_export_breakage_1

# breakage scenario #2
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! Today, you and your team are working on the postmortem from your last incident when your boss walks up to your section. 
“Hey team, we are seeing a spike in 500 errors on the site. We haven’t heard many customer complaints, but we want to get this sorted before it turns into something big.”

You will have 3 hours to debug the issue. The instructor will call for breaks every 30 minutes to have teams share one thing that they have learned. 

Command line to run in cloud shell to start the breakage scenario: gcloud sql import sql randomarchive-sql gs://randomarchive-static-files/sql/sql_randomarchive_sql_export_breakage_2

# breakage scenario #3
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! Today, you and your team are updating your playbooks when your boss comes by and knocks on your desk. 
“So... we are seeing a spike in 400 errors on the site. We haven’t heard any customer complaints, but we want to get this sorted before it turns into something big.”

You will have 3 hours to debug the issue. The instructor will call for breaks every 30 minutes to have teams share one thing that they have learned. 

Command line to run in cloud shell to start the breakage scenario: gcloud sql import sql randomarchive-sql gs://randomarchive-static-files/sql/sql_randomarchive_sql_export_breakage_3

# Thanks
@CoreyMSchafer for a killer flask tutorial youtube series that served as the base for randomarchive. https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

@prettyprinted for the tutorial on using Flask-MySQLDB. https://www.youtube.com/watch?v=51F_frStZCQ
