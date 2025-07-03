#  Deploying an E-Commerce App on AWS EC2 with Load Balancer and Auto Scaling

## Real-Time Use Case
In a real-world scenario, online shopping platforms (like Amazon, Flipkart, or Shopify stores) must remain available, responsive, and scalable during peak sales, festive seasons, or flash deals. This project simulates such a setup by hosting a basic e-commerce web app on AWS using EC2 instances, distributing user traffic via an Application Load Balancer (ALB), and automatically scaling infrastructure based on CPU load using Auto Scaling. It ensures high availability, fault tolerance, and cost efficiency — just like in production-grade cloud environments.

## 📋 Agenda

1. Provision EC2 Security Group
2. Launch EC2 Instances and Deploy the App
3. Set Up Application Load Balancer (ALB)
4. Configure Auto Scaling with Launch Template
5. Validate Setup and Trigger Auto Scaling with Stress Test

##  AWS Services Used

* **EC2** – Virtual servers to host the application
* **Security Group** – Firewall to allow traffic
* **Application Load Balancer** – Distributes incoming traffic to multiple instances
* **Target Group** – Manages routing to EC2s registered in the load balancer
* **Launch Template** – Blueprint for launching EC2s with consistent settings
* **AMI (Amazon Machine Image)** – Snapshot of a configured EC2 instance
* **Auto Scaling Group** – Dynamically scales the number of EC2s based on load
* **CloudWatch** – Monitors resources and triggers alarms
* **SNS (Simple Notification Service)** – Sends alerts via email for scaling events

---

## 1.  Provision EC2 Infrastructure

###  Create a Security Group

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

###  Launch EC2 Instances

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

###  SSH into Each Instance and Deploy the App

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

###  Access the Application

Open your browser and access the app on both instances:

```
http://<public-ip-of-EC2-1A>:80
http://<public-ip-of-EC2-1B>:80
```
![Image](https://github.com/user-attachments/assets/357d5614-4451-47d6-870e-5a4ebdf7e1fc)

![Image](https://github.com/user-attachments/assets/ef02b9d4-8b2c-49de-98a9-a7ed1c1d26b6)

---

## 3.  Configure Load Balancer

###  Create Target Group

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

### Create Application Load Balancer (ALB)

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

![Image](https://github.com/user-attachments/assets/41e7250f-2813-4d5d-b532-4c7b7ffc283c)

###  Test Load Balancer

After provisioning status becomes **Active**, access the application using the DNS of the ALB:

![Image](https://github.com/user-attachments/assets/2f559cb0-4821-49bd-83db-7ac945a31788)

```
http://<load-balancer-dns>:80
```

![Image](https://github.com/user-attachments/assets/6257b8e1-61cb-4aea-b83f-0e62df27448e)

---

## 4.  Set Up Auto Scaling

###  Create an AMI from Existing Instance

1. Go to **EC2 > Instances**.
2. Select one of the deployed instances.
3. Click **Actions > Image and templates > Create image**.
4. Name the image as `EC2-AMI`.
5. Uncheck the **Reboot** option.
6. Click **Create image**.
7. Monitor the status under **EC2 > AMIs** until it shows **Available**.

###  Create a Launch Template

1. Navigate to **EC2 > Launch Templates > Create launch template**.

![Image](https://github.com/user-attachments/assets/18a7fc4f-1e2c-4f49-8b05-4864fda65cc2)

2. Set:

   * **Template name:** `EC2-LTEMP`
   * **AMI:** Select from “Owned by me” → choose `EC2-AMI`
   * **Instance type:** `t2.micro`
   * **Key Pair:** `ec2`
   * **Security Group:** `EC2-SG`
3. Click **Create launch template**.

![Image](https://github.com/user-attachments/assets/dd323e1c-1225-4285-986e-75d76d02d5e6)

![Image](https://github.com/user-attachments/assets/e70d3fb2-995a-43e6-b1e7-1862068afe42)

###  Create Auto Scaling Group

1. Go to **EC2 > Auto Scaling Groups > Create Auto Scaling group**.

![Image](https://github.com/user-attachments/assets/a1023d55-d837-4f72-b6e1-9ea0e1b4e835)

2. Name it: `EC2-ASG`.
3. Select **Launch Template:** `EC2-LTEMP`.
4. Select **Availability Zones:** `us-east-1a` and `us-east-1b`.
5. Attach the existing load balancer:

   * Choose the **Application Load Balancer**
   * Select the target group: `EC2-TG`

![Image](https://github.com/user-attachments/assets/5a05acda-ac0d-44ad-96e7-afdf29a3a12a)  

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
   * you will recieve a  confirmation mail and accept it

![Image](https://github.com/user-attachments/assets/fe317821-d3ea-445b-870a-16769f729aa5)

![Image](https://github.com/user-attachments/assets/32753e15-1ac5-49d7-9018-c8879deef9d0)

10. Click **Create Auto Scaling group**.


![Image](https://github.com/user-attachments/assets/187757c5-bd9f-4916-8ee8-81fda8e89763)

![Image](https://github.com/user-attachments/assets/42736e84-ac36-4dc9-8fe7-0cef25f61104)

---

## 5.  Validation

* Go to **EC2 > Instances** and verify new instances are created by Auto Scaling.
* Check **Target Group > Targets** for healthy status of the newly added instances.
* Confirm the application is accessible through the **Load Balancer DNS name**.

![Image](https://github.com/user-attachments/assets/c974b3cc-dac1-414b-b019-85f6cb11e3a4)

![Image](https://github.com/user-attachments/assets/c67a1203-428c-4250-90a9-a6e8c55ae0a9)


---

## 6.  Validate Auto Scaling with Stress Testing

###  Install Stress Tool on One EC2 Instance

SSH into one of the EC2 instances in the Auto Scaling Group and run:

```bash
sudo yum install stress -y
stress --cpu 1 --timeout 10000
```

###  Monitor Scaling Activity

1. Go to **CloudWatch > Alarms** and observe the scaling alarms triggered by high CPU usage.
2. The Auto Scaling group should launch additional EC2 instances based on the policy.
3. Check:

   * **New EC2 instances** in the console
   * **Target group health status** (new instances should show as healthy)
   * **SNS Email Notifications** for scaling activities

![Image](https://github.com/user-attachments/assets/40a4d1f7-92cf-4030-9cd2-e1bfacfef622)

![Image](https://github.com/user-attachments/assets/5c3834be-7011-4091-8db8-7869679f1b83)

![Image](https://github.com/user-attachments/assets/bd6a9b22-a506-4594-a680-1a5a36d97ca0)

![Image](https://github.com/user-attachments/assets/ad306fe7-29e9-402b-8416-028fdb93b46a)

**SNS Email Notifications** will send emails based on triggers like below whenever a new instance is created or terminated.

![Image](https://github.com/user-attachments/assets/23df4572-a614-4740-b1ba-fbad857d4823)

![Image](https://github.com/user-attachments/assets/52e2118d-709a-4b45-8db6-c66adbd927c9)

---


