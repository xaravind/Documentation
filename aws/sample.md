#  Deploying an E-Commerce App on AWS EC2 with Load Balancer and Auto Scaling

---

## 1.  Provision EC2 Infrastructure

### Step 1.1: Create a Security Group

1. Navigate to **EC2 > Security Groups**.
2. Click **Create security group**.
3. Provide the following:

   * **Name:** `EC2-SG`
   * **Description:** Security group for EC2 instances
4. Add **Inbound Rules**:

   * SSH (Port 22) — Source: Anywhere (IPv4)
   * HTTP (Port 80) — Source: Anywhere (IPv4)
5. Scroll down and click **Create security group**.

![Image](https://github.com/user-attachments/assets/cfdbcec4-bc5b-4a94-b3b8-58d0808e135c)

---

## 2.  Deploy the E-Commerce Application

### Step 2.1: Launch EC2 Instances

1. Navigate to **EC2 > Instances > Launch Instances**.
2. Create **two instances** named:

   * `EC2-1A` (in **us-east-1a**)
   * `EC2-1B` (in **us-east-1b**)
3. Use **Amazon Linux AMI**.
4. Select:

   * **Security Group:** `EC2-SG`
   * **Key Pair:** Create a new key pair named `ec2`
   * Leave all other settings as default.
   * 
![Image](https://github.com/user-attachments/assets/76323211-402d-493b-8db5-62eaf540d69c)

![Image](https://github.com/user-attachments/assets/300ce6ea-8493-4487-9c17-c39ded78399b)

![Image](https://github.com/user-attachments/assets/c0027c04-b729-43c0-89d8-5f09c70052c8)

### Step 2.2: SSH into Each Instance and Deploy the App

Run the following commands on both instances:

```bash
sudo yum update -y
sudo yum install git httpd -y
sudo systemctl start httpd
sudo systemctl enable httpd
sudo git clone https://github.com/Ai-TechNov/ecomm.git
sudo rm -rf /var/www/html/*
sudo cp -r ecomm/* /var/www/html
```

### Step 2.3: Access the Application

Open your browser and access the app on both instances:

```
http://<public-ip-of-EC2-1A>:80
http://<public-ip-of-EC2-1B>:80
```
![Image](https://github.com/user-attachments/assets/357d5614-4451-47d6-870e-5a4ebdf7e1fc)

---

## 3.  Configure Load Balancer

### Step 3.1: Create Target Group

1. Go to **EC2 > Target Groups**.
2. Click **Create target group**.
3. Select:

   * **Target type:** Instances
   * **Name:** `EC2-TG`
   * **Protocol:** HTTP
   * **Port:** 80
   * **VPC:** Choose your default VPC
4. Register both EC2 instances to the target group.
5. Click **Create target group**.

![Image](https://github.com/user-attachments/assets/8f76a630-9977-4787-944e-2a7119ca2558)

### Step 3.2: Create Application Load Balancer (ALB)

1. Navigate to **EC2 > Load Balancers > Create Load Balancer**.
2. Choose **Application Load Balancer**.
3. Set:

   * **Name:** `EC2-ALB`
   * **Scheme:** Internet-facing
   * **Listeners:** HTTP on port 80
   * **Availability Zones:** Select **us-east-1a** and **us-east-1b**
4. Assign **Security Group:** `EC2-SG`
5. Select **Target Group:** `EC2-TG`
6. Click **Create load balancer**.

### Step 3.3: Test Load Balancer

After provisioning status becomes **Active**, access the application using the DNS of the ALB:

```
http://<load-balancer-dns>:80
```

---

## 4.  Set Up Auto Scaling

### Step 4.1: Create an AMI from Existing Instance

1. Go to **EC2 > Instances**.
2. Select one of the deployed instances.
3. Click **Actions > Image and templates > Create image**.
4. Name the image as `EC2-AMI`.
5. Uncheck the **Reboot** option.
6. Click **Create image**.
7. Monitor the status under **EC2 > AMIs** until it shows **Available**.

### Step 4.2: Create a Launch Template

1. Navigate to **EC2 > Launch Templates > Create launch template**.
2. Set:

   * **Template name:** `EC2-LTEMP`
   * **AMI:** Select from “Owned by me” → choose `EC2-AMI`
   * **Instance type:** `t2.micro`
   * **Key Pair:** `ec2`
   * **Security Group:** `EC2-SG`
3. Click **Create launch template**.

### Step 4.3: Create Auto Scaling Group

1. Go to **EC2 > Auto Scaling Groups > Create Auto Scaling group**.
2. Name it: `EC2-ASG`.
3. Select **Launch Template:** `EC2-LTEMP`.
4. Select **Availability Zones:** `us-east-1a` and `us-east-1b`.
5. Attach the existing load balancer:

   * Choose the **Application Load Balancer**
   * Select the target group: `EC2-TG`
6. Configure the group size:

   * **Minimum capacity:** 2 instances
   * **Desired capacity:** 2 instances
   * **Maximum capacity:** 4 instances
7. Configure scaling policy:

   * Choose **Target tracking scaling policy**
   * **Metric type:** Average CPU Utilization
   * **Target value:** 70%
8. Enable CloudWatch group metrics collection.
9. (Optional) Set up notifications:

   * Create an SNS topic (e.g., `EC2-SNS`)
   * Provide your email to receive alerts
10. Click **Create Auto Scaling group**.

---

## 5. 🧪 Validation

* Go to **EC2 > Instances** and verify new instances are created by Auto Scaling.
* Check **Target Group > Targets** for healthy status of the newly added instances.
* Confirm the application is accessible through the **Load Balancer DNS name**.

---

