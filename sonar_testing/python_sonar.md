# 🧪 SonarQube Testing of python code with Two-Server Setup

## 🧠 Goal  
Set up **two separate servers**:  
- 🏗️ **Build Server**: for compiling code and running SonarQube analysis  
- 🧠 **SonarQube Server**: for hosting SonarQube and viewing results  

Test static analysis using SonarQube for Java, JavaScript, and Python projects.

---

## ⚙️ 1. SonarQube Server Setup

### 🖥️ OS Info  
```bash
uname -a
# Linux ip-172-31-20-239 ... x86_64 GNU/Linux
```
---

**Note:**  
Do **not** start SonarQube as the **root user**. Instead, use a **non-root user account** to run the application.  
Running SonarQube as root is **not supported** and can introduce **security risks**, lead to **permission issues**, and expose the system to **potential vulnerabilities**.  
Additionally, ensure that all SonarQube files and directories are **owned by the non-root user** to avoid access and permission errors during runtime.

---
### 📦 Install Prerequisites  
```bash
sudo apt update -y
sudo apt install -y unzip
sudo apt install openjdk-17-jre-headless -y
```

### 📥 Download and Extract SonarQube  
```bash
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-25.4.0.105899.zip
unzip sonarqube-25.4.0.105899.zip
```

### 🚀 Start SonarQube  
```bash
cd sonarqube-25.4.0.105899/bin/linux-x86-64
./sonar.sh start
./sonar.sh status
```

✅ Expected Output:
```
Starting SonarQube...
Started SonarQube.
SonarQube is running (PID)
```

### 🌐 Open SonarQube in Browser  
```bash
curl ifconfig.me
# Output: 18.232.140.167
```

Access SonarQube at:  
**http://44.202.193.53:9000**  
Login: `admin / admin`
Reset admin Password

---

## 🛠️ 2. Configure SonarQube Projects (Web UI)

For each language (Java / JS / Python):

Go to **Projects** → **Create Project** 
![Image](https://github.com/user-attachments/assets/d19c6015-ad88-42b8-8804-e132a7569dff)

choose **Local project** 

![Image](https://github.com/user-attachments/assets/1ba73e77-9c59-49cb-a88c-04ab34750f87)

give **Required details** 


Select **Use global settings**, then choose **Locally**

Choose **Locally** 
 Enter:
   - Project key (e.g., `java`, `js`, or `python`)
   - Project name
![Image](https://github.com/user-attachments/assets/3137a312-1b3f-476c-a4b2-01dc5bc07cfc)

![Image](https://github.com/user-attachments/assets/47d82a13-4c3c-4c5f-9825-9809c4d9637c)


Generate a token:
   - Click **Generate** → **Continue**

In 2. choose **the package/code** and **copy the code**


![Image](https://github.com/user-attachments/assets/1d6028ec-03ca-4516-a4d6-e84161a72b5a)

---

## 🧱 3. Build Server Setup
## 🐍 Python Project Analysis

### 📥 Prepare and Analyze Python Project  
```bash
cd python_code/
```

```bash

root@ip-172-31-26-213:~/Documentation/python_code# ll
total 20
drwxr-xr-x 3 root root 4096 Apr 13 09:33 ./
drwxr-xr-x 6 root root 4096 Apr 13 09:33 ../
drwxr-xr-x 4 root root 4096 Apr 13 09:33 app/
-rw-r--r-- 1 root root 6514 Apr 13 09:33 readme.md

```


### 🧪 Run SonarQube Scanner  
```bash
sonar-scanner \
  -Dsonar.projectKey=python \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://44.202.193.53:9000 \
  -Dsonar.token=sqp_e36b7c7b5af01a866631fd7a9dff62cf5b0c3c59
```

```bash
[INFO]  ScannerEngine: Analysis report compressed in 1475ms, zip size=11.1 MB
[INFO]  ScannerEngine: Analysis report uploaded in 160ms
[INFO]  ScannerEngine: ANALYSIS SUCCESSFUL, you can find the results at: http://18.232.140.167:9000/dashboard?id=java-1
[INFO]  ScannerEngine: Note that you will be able to access the updated dashboard once the server has processed the submitted analysis report
[INFO]  ScannerEngine: More about the report processing at http://18.232.140.167:9000/api/ce/task?id=d0ce00cc-7031-4b90-bcfb-c43b5f087224
[INFO]  ScannerEngine: Analysis total time: 1:19.266 s
[INFO]  ScannerEngine: SonarScanner Engine completed successfully
```
### If you get below error, follow below steps

```bash
sonar-scanner : command not found
```

## 🛠️ How to Install `sonar-scanner` on Ubuntu

###  1. Download SonarScanner

```bash
cd /opt
sudo wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
sudo unzip sonar-scanner-cli-5.0.1.3006-linux.zip
sudo mv sonar-scanner-5.0.1.3006-linux sonar-scanner
```

---

###  2. Add to PATH

Add SonarScanner to your shell’s path:

```bash
echo 'export PATH=$PATH:/opt/sonar-scanner/bin' >> ~/.bashrc
source ~/.bashrc
```

---

###  3. Confirm Installation

Run:

```bash
sonar-scanner -v
```

You should see the version output like:

```
SonarScanner 5.0.1.3006
```

---

###  4. Run the Scanner in Your Project

Now go to your project directory and run:

```bash
sonar-scanner
```

---

✅ Python code analysis will appear in the SonarQube dashboard, once analysis is completed.

![Image](https://github.com/user-attachments/assets/c56485aa-1c96-434c-8cf0-68e4f8a183ac)

---

## 📊 4. View Results in SonarQube

Open browser → http://18.232.140.167:9000 → Select your **project dashboard**

✔️ Review for each project:
- Code smells
- Bugs
- Vulnerabilities
- Test coverage (if applicable)

---

## ✅ Summary

| Language | Build Tool      | Analysis Command                                      |
|----------|------------------|------------------------------------------------------|
| Java     | Maven            | `mvn clean verify sonar:sonar ...`                  |
| JS       | NPM + Scanner    | `sonar-scanner` with `sonar-project.properties`     |
| Python   | Sonar Scanner    | `sonar-scanner -Dsonar.projectKey=...`              |

📡 All results are published to: **http://44.202.193.53:9000**

![Image](https://github.com/user-attachments/assets/e3216177-b412-47d8-9d1c-497fa4a2726a)
