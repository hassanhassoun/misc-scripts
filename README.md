# aws-multi-tier-vpc

# Usage

- Edit variable.tf. Default region is ca-central-1, default AZ ca-central-1a and ca-central-1b
- Apply will create a VPC with 3 tier subnet groups, every tier will have different subnets in every AZ
- elb and web tiers are public, db tier is private
- Creates ASG for web tier, ASG for worker tier
- Creates RDS and Redis Elasticache in DB Tier with connection settings passed to ASG instances during cloud-init
- Creates Default scale in and scale out policies based on cpu usage of 85 and 50 percent respectively
- Creates supporting SNS and S3 instances

```sh
$git clone git@github.com:hhassoun/aws-multi-tier-vpc
$cd aws-multi-tier-vpc
$terraform get
$terraform plan -var 'access_key=XXXXXXXXXXXXXXXX' -var 'secret_key=XXXXXXXXXXXXXXXX/CCCCCCCC' -var 'myip=66.66.67.68'
$terraform apply -var 'access_key=XXXXXXXXXXXXXXXX' -var 'secret_key=XXXXXXXXXXXXXXXX/CCCCCCCC' -var 'myip=66.66.67.68'
```
# misc-scripts
