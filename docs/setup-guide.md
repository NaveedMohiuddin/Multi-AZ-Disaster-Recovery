# Complete Setup Guide

## Prerequisites
- AWS Account with admin permissions
- Basic AWS knowledge (VPC, EC2, RDS)

## Step-by-Step Setup

### Phase 1: Network Infrastructure 
1. Create VPC (10.0.0.0/16)
2. Create 4 subnets (2 public, 2 private) in different AZs
3. Setup Internet Gateway and NAT Gateway
4. Configure Route Tables
5. Create Security Groups

### Phase 2: Database Setup 
1. Create DB Subnet Group
2. Launch RDS MySQL with Multi-AZ enabled
3. Note the database endpoint

### Phase 3: Application Setup 
1. Launch EC2 instance in private subnet
2. Install Python dependencies
3. Deploy application code
4. Setup database

### Phase 4: Load Balancer 
1. Create Target Group
2. Create Application Load Balancer
3. Test application access

## Testing Failover
1. Go to RDS Console
2. Select your database → Actions → Reboot
3. Check "Reboot with failover"
4. Monitor application - should see <2 second interruption

## Cleanup
To avoid charges, delete in this order:
1. ALB → Target Group → EC2 → RDS → NAT Gateway → VPC