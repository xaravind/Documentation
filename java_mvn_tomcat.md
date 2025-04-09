

# Deploying Java Application on Amazon Linux with Maven and Tomcat

This guide walks you through deploying a Java application using Maven, Amazon Corretto (Java 21), and Tomcat on Amazon Linux.

### Prerequisites
Make sure you have the following installed:
- Java
- Maven
- Tomcat
- Git

### 1. Log in to the EC2 instance and install required packages

First, connect to your Amazon Linux instance and install the necessary packages.

```bash
sudo yum update -y
sudo yum install git -y
sudo yum install java-21-amazon-corretto-devel.x86_64 -y
sudo yum install maven-amazon-corretto21.noarch -y
```

#### Check the versions:
```bash
# Check Git version
git --version
# Example output: git version 2.47.1

# Check Maven version
mvn --version
# Example output: Apache Maven 3.8.4 (Red Hat 3.8.4-3.amzn2023.0.5)
# Java version: 21.0.6, vendor: Amazon.com Inc.

# Check Java version
java --version
# Example output: openjdk 21.0.6 2025-01-21 LTS
```

### 2. Install Tomcat

Next, download and install Tomcat. Visit the [Tomcat download page](https://tomcat.apache.org/download-90.cgi), then copy the link for the desired version.

```bash
cd /opt
sudo wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.100/bin/apache-tomcat-9.0.100.zip
sudo unzip apache-tomcat-9.0.100.zip
```

### 3. Modify Tomcat Configuration Files

#### Edit `tomcat-users.xml` to create a user with roles:
```bash
cd /opt/apache-tomcat-9.0.100/conf/
sudo vi tomcat-users.xml
```
Uncomment the following lines and set the desired user and password:

```xml
<role rolename="manager-gui"/>
<role rolename="admin-gui"/>
<user username="admin" password="password" roles="manager-gui,admin-gui"/>
```

#### Modify `context.xml` files to allow external access (not just localhost):

```bash
find /opt/apache-tomcat-9.0.100 -name context.xml

# Edit the following files:
vi /opt/apache-tomcat-9.0.100/webapps/host-manager/META-INF/context.xml
vi /opt/apache-tomcat-9.0.100/webapps/manager/META-INF/context.xml
```

In both files, modify the `<Context>` element to look like this:

```xml
<Context docBase="..." path="/" reloadable="true" crossContext="true" />
```

### 4. Start the Tomcat server

Make sure the Tomcat scripts have the correct permissions and start the server:

```bash
cd /opt/apache-tomcat-9.0.100/bin
sudo chmod 755 *.sh
sudo ./startup.sh
```

Check that Tomcat started successfully:

```bash
ps -ef | grep tomcat
```

You should see an entry for Tomcat running like this:

```bash
root 27775 1 14 16:23 pts/1 00:00:03 /usr/bin/java ...
```

To check the open ports, use:

```bash
netstat -ntlp
```

You should see something like this:

```bash
tcp6 0 0 :::8080 :::* LISTEN 27775/java
```

### 5. Clone the Application Code

Navigate to your home directory and clone the application code from GitHub:

```bash
cd ~
git clone https://github.com/SergiiShapoval/CarRental.git
cd CarRental
```

### 6. Build the Application

Run Maven to build the application, which will generate a `.war` file in the `target/` directory.

```bash
mvn package
```

After the build completes, you should see something like this in the `target/` directory:

```bash
ls -l target/
# Example output:
# WebCarRental.war
# WebCarRental/
```

### 7. Deploy the Application to Tomcat

Copy the `.war` file to the `webapps` directory of your Tomcat installation:

```bash
sudo cp target/WebCarRental.war /opt/apache-tomcat-9.0.100/webapps/
```

### 8. Restart Tomcat

After copying the `.war` file, restart the Tomcat server:

```bash
cd /opt/apache-tomcat-9.0.100/bin
sudo ./shutdown.sh
sudo ./startup.sh
```

### 9. Access the Application

Once Tomcat has restarted, you can access the application at:

```
http://<EC2-Instance-IP>:8080/WebCarRental/
```

For example:

```
http://54.83.101.239:8080/WebCarRental/
```

### Additional Notes:
- Ensure that your security group for the EC2 instance allows inbound traffic on port `8080` (or whichever port your Tomcat server is using).
- If you encounter any issues, check the Tomcat logs located at `/opt/apache-tomcat-9.0.100/logs/`.
