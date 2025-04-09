

# Deploying Java Application on Amazon Linux with Maven and Tomcat


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
[root@ip-172-31-17-119 bin]# ps -ef|grep tomcat
root       27775       1 14 16:23 pts/1    00:00:03 /usr/bin/java -Djava.util.logging.config.file=/opt/apache-tomcat-9.0.100/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djdk.tls.ephemeralDHKeySize=2048 -Djava.protocol.handler.pkgs=org.apache.catalina.webresources -Dsun.io.useCanonCaches=false -Dorg.apache.catalina.security.SecurityListener.UMASK=0027 -Dignore.endorsed.dirs= -classpath /opt/apache-tomcat-9.0.100/bin/bootstrap.jar:/opt/apache-tomcat-9.0.100/bin/tomcat-juli.jar -Dcatalina.base=/opt/apache-tomcat-9.0.100 -Dcatalina.home=/opt/apache-tomcat-9.0.100 -Djava.io.tmpdir=/opt/apache-tomcat-9.0.100/temp org.apache.catalina.startup.Bootstrap start
root       27811    2461  0 16:24 pts/1    00:00:00 grep --color=auto tomcat
```bash
root 27775 1 14 16:23 pts/1 00:00:03 /usr/bin/java ...
```

To check the open ports, use:
You should see something like this:
```bash
[root@ip-172-31-17-119 bin]# ps -ef|grep tomcat
root       27775       1 14 16:23 pts/1    00:00:03 /usr/bin/java -Djava.util.logging.config.file=/opt/apache-tomcat-9.0.100/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djdk.tls.ephemeralDHKeySize=2048 -Djava.protocol.handler.pkgs=org.apache.catalina.webresources -Dsun.io.useCanonCaches=false -Dorg.apache.catalina.security.SecurityListener.UMASK=0027 -Dignore.endorsed.dirs= -classpath /opt/apache-tomcat-9.0.100/bin/bootstrap.jar:/opt/apache-tomcat-9.0.100/bin/tomcat-juli.jar -Dcatalina.base=/opt/apache-tomcat-9.0.100 -Dcatalina.home=/opt/apache-tomcat-9.0.100 -Djava.io.tmpdir=/opt/apache-tomcat-9.0.100/temp org.apache.catalina.startup.Bootstrap start
root       27811    2461  0 16:24 pts/1    00:00:00 grep --color=auto tomcat
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

```
[INFO] Building war: /root/CarRental/target/WebCarRental.war
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.615 s
[INFO] Finished at: 2025-04-09T17:19:35Z
[INFO] ------------------------------------------------------------------------
[root@ip-172-31-17-119 CarRental]# ccd target/^C
[root@ip-172-31-17-119 CarRental]# cd target/
[root@ip-172-31-17-119 target]# ll
total 3932
drwxr-xr-x. 8 root root      82 Apr  9 17:19 WebCarRental
-rw-r--r--. 1 root root 4025158 Apr  9 17:19 WebCarRental.war
drwxr-xr-x. 3 root root     186 Apr  9 17:18 classes
drwxr-xr-x. 3 root root      25 Apr  9 17:18 generated-sources
drwxr-xr-x. 2 root root      28 Apr  9 17:19 maven-archiver
drwxr-xr-x. 3 root root      35 Apr  9 17:18 maven-status
[root@ip-172-31-17-119 target]# cp -r WebCarRental.war /opt/apache-tomcat-9.0.100/webapps/

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


```markdown
![Screenshot](https://raw.githubusercontent.com/xaravind/Documentation/main/Screenshot_29.png)
```



