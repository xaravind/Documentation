Two server setup for Build and Release servers


what is Nexus?

Nexus is a repository manager(build repo) that centralizes the storage and management of software artifacts like binaries and packages. It supports formats such as Maven, npm, Docker, and more. Nexus integrates with CI/CD pipelines, helps enforce security policies, and ensures version control, making it easier to manage and deploy dependencies efficiently.

By using Nexus, organizations can:
Manage and version all artifacts in one centralized location.
Enforce security policies and control access to critical components.
Protect the software supply chain.
Maintain a reliable backup of all artifact versions.

In release server

Install and configure nexus repo in release server

-  min requirements for Nexus repo

Cores:- 2 cpu/4gb ram
port open :- 8081

Log in to your sever

update server

sudo apt update -y

install java

sudo apt install openjdk-17-jdk-headless
java --version

```bash
ubuntu@Release:~$ java --version
openjdk 17.0.14 2025-01-21
OpenJDK Runtime Environment (build 17.0.14+7-Ubuntu-124.04)
OpenJDK 64-Bit Server VM (build 17.0.14+7-Ubuntu-124.04, mixed mode, sharing)
```

Download Nexus

```bash
cd /opt
sudo wget https://download.sonatype.com/nexus/3/nexus-3.79.1-04-linux-x86_64.tar.gz
sudo tar -xvf nexus-3.79.1-04-linux-x86_64.tar.gz
```

Create user profile

```bash
sudo adduser nexus
```


```bash
ubuntu@Release:/opt$ sudo adduser nexus
info: Adding user `nexus' ...
info: Selecting UID/GID from range 1000 to 59999 ...
info: Adding new group `nexus' (1001) ...
info: Adding new user `nexus' (1001) with group `nexus (1001)' ...
info: Creating home directory `/home/nexus' ...
info: Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for nexus
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] y
info: Adding new user `nexus' to supplemental / extra groups `users' ...
info: Adding user `nexus' to group `users' ...
```
```bash
sudo chown -R nexus:nexus /opt/nexus
sudo chown -R nexus:nexus /opt/sonatype-work
```


```bash
ubuntu@Release:/opt$ ll
total 412244
drwxr-xr-x  4 root root      4096 Apr 16 07:09 ./
drwxr-xr-x 22 root root      4096 Apr 16 07:03 ../
drwxr-xr-x  7 root root      4096 Apr 16 07:08 nexus/
-rw-r--r--  1 root root 422117063 Apr 10 18:13 nexus-3.79.1-04-linux-x86_64.tar.gz
drwxr-xr-x  3 root root      4096 Apr 10 13:56 sonatype-work/
ubuntu@Release:/opt$ sudo chown -R nexus:nexus /opt/nexus
ubuntu@Release:/opt$ sudo chown -R nexus:nexus /opt/sonatype-work
```

Create a service file
```bash
sudo vi /etc/systemd/system/nexus.service
```

Add below content in service file
```bash
[Unit]
Description=nexus service
After=network.target

[Service]
Type=forking
LimitNOFILE=65536
ExecStart=/opt/nexus/bin/nexus start
ExecStop=/opt/nexus/bin/nexus stop
User=nexus
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

Start Nexus server

```bash
sudo systemctl daemon-reload
sudo systemctl enable nexus
sudo systemctl start nexus
sudo systemctl status nexus
```

```bash
ubuntu@Release:/opt$ sudo systemctl status nexus
● nexus.service - nexus service
     Loaded: loaded (/etc/systemd/system/nexus.service; enabled; preset: enabled)
     Active: active (running) since Wed 2025-04-16 07:11:19 UTC; 6s ago
    Process: 2353 ExecStart=/opt/nexus/bin/nexus start (code=exited, status=0/SUCCESS)
   Main PID: 2594 (java)
      Tasks: 32 (limit: 4674)
     Memory: 401.8M (peak: 402.1M)
        CPU: 12.896s
     CGroup: /system.slice/nexus.service
             └─2594 /opt/nexus/jdk/temurin_17.0.13_11_linux_x86_64/jdk-17.0.13+11/bin/java -server -Dnexus.installer.type=linux-x86->

Apr 16 07:11:19 Release systemd[1]: Starting nexus.service - nexus service...
Apr 16 07:11:19 Release nexus[2353]: /opt/nexus/bin/nexus: 155: [[: not found
Apr 16 07:11:19 Release nexus[2353]: Starting nexus
Apr 16 07:11:19 Release systemd[1]: Started nexus.service - nexus service.
```


Check and browse the nexus


check public IP and running port no:-

```bash
sudo apt install net-tools -y
curl ifconfig.me
netstat -ntpl
```

```bash
ubuntu@Release:/opt$ curl ifconfig.me
54.234.203.250
ubuntu@Release:/opt$ netstat -ntpl
(No info could be read for "-p": geteuid()=1000 but you should be root.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.54:53           0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:6010          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp6       0      0 :::8081                 :::*                    LISTEN      -
tcp6       0      0 ::1:6010                :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
```


Access URL in browser
```bash
http://<your-server-ip>:8081
```

Login with initial password, that will available in below file.

```bash
cat /nexus-data/admin.password
```
and reset the password

<image>

In Build server

login into build server,Update the server, install prerequisites

```bash
sudo apt update -y
sudo apt install openjdk-17-jdk-headless
sudo apt install git -y
sudo apt install maven -y
```

Clone the your java_code

```bash
cd ~
git clone  https://github.com/<your-repo>.git
```

go to your repo

```bash
cd <your-repo>
```

update pom.xml to add the nexus-repo details

add like below

```bash
    </dependencies>
    <distributionManagement>
        <repository>
            <id>repo-id</id>  <!-- Repository ID, used for authentication -->
            <url>http://<repo-ip>:8081/repository/maven-releases/</url>  <!-- Replace with your actual repository URL -->
        </repository>
    </distributionManagement>

    <build>

```

store nexus credentails in below file

```bash
vim /etc/maven/settings.xml
```

```
paste below content in file under <server> section

```bash
  <server>
      <id>maven-releases</id>
      <username>admin</username>
      <password>password</password>
  </server>
```

execute below command, it will deploy artifact in nexus

```
mvn deploy
```

Go to nexus browser ---> Browse --> maven-releases or (your component) ---> click on version no

<image>