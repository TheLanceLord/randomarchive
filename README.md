# important
If you aren't using our Qwiklabs, please make sure to delete your unused GCP projects when you are done. Sticker shock isn't fun for anyone!
And for students, try and avoid using the code in the randomarchive/users file as much as possible. The code there describes user behavior patterns, which won't be conveniently stored in an .sh file in a real world scenario.

# random archive
This is a simple flask blog site with integrations to MySQL and Google Cloud Storage. This application is intended for hands-on reliability training on the Google Cloud Platform, and is designed to be as lightweight to keep costs low for any users wishing to experiment with it or companies looking to use it as a baseline to build out their own internal training programs.

# how to use
For individuals, Qwiklabs.com will have self-service labs with this environment to help keep things simple. For teams, contact your GCP sales rep to get an instructor-led course with these labs.

# setup
![RandomArchive Architecture](https://user-images.githubusercontent.com/19802916/121415419-915d2500-c91c-11eb-9d0f-8b67958821db.jpg)
Nothing super complicated, you will need the following in GCP:
1 HTTP/HTTPS Load Balancer named "randomarchive"
1 Cloud SQL MySQL instance with Private IP enabled named "randomarchive"
1 GCS bucket with all of the static pictures saved to it
1 Default VPC
4 VMs (1 for each of the users: internettraffic, kendall, robin, and taylor; you can run these on n1-standard-1s or probably even our e2 CPUs). Use the code from randomarchive/users for these
1 VM for the webapp (running on an n1-standard-1). Use the code from randomarchive/randomarchive/ for this. 
3 Alerting policies (400 errors, 500 errors, and High CPU Utilization)

# breakage scenarios
Breakage scenarios are changes to the enviornment that result in the alerting policies being triggered. The goal of these scenarios is for users to practice triaging, mitigating, and then resolving the incident. These breakages can be implemented by importing the scripts in randomarchive/cloudsql-mysql-db/. Just run the "gcloud sql import sql" import command and point it to the scenario file you want to load and thing should start breaking in 5-10 minutes. The "healthy" returns the environment to its healthy state.

# breakage scenario #0
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! The rest of your team is out for today, and you are reading up on reliability best practices when you spot your boss hustling up to your desk.
“The site is having issues. Anyone visiting the site is greeted by an internal error message of ours. We need this fixed ASAP before we start losing customers.”

# breakage scenario #1
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! Today, you and your team are in a meeting room working through a Wheel of Misfortune, when there is an urgent knock at the door and your boss pops their head in. 
“Hey team, it looks like the site is completely down. We need it back up and running ASAP before we start losing users.”

# breakage scenario #2
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! Today, you and your team are working on the postmortem from your last incident when your boss walks up to your section. 
“Hey team, we are seeing a spike in 500 errors on the site. We haven’t heard many customer complaints, but we want to get this sorted before it turns into something big.”

# breakage scenario #3
You are a new hire with Random Archive Inc. a small blog site with hopes of making it big! Today, you and your team are updating your playbooks when your boss comes by and knocks on your desk. 
“So... we are seeing a spike in our site's CPU utilization. We haven’t heard any customer complaints, but we want to get this sorted before it turns into something big.”

# additional reading material
https://sre.google/books/ has free reading material to help you on your Site Reliability Engineering journey. It is strongly encouraged that you read these books to get the most out of these labs.

# thanks
@CoreyMSchafer for a killer flask tutorial youtube series that served as the base for Random Archive. https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

@prettyprinted for the tutorial on using Flask-MySQLDB. https://www.youtube.com/watch?v=51F_frStZCQ
