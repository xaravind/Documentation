
# 🧪 SonarQube Testing of Java, JS, and Python Code (Two-Server Setup)

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

![Image](https://github.com/user-attachments/assets/7d8031d4-3095-45ff-b26b-febafc850d29)

Select **Use global settings**, then choose **Locally**

Choose **Locally** 
 Enter:
   - Project key (e.g., `java`, `js`, or `python`)
   - Project name
![Image](https://github.com/user-attachments/assets/3137a312-1b3f-476c-a4b2-01dc5bc07cfc)

![Image](https://github.com/user-attachments/assets/47d82a13-4c3c-4c5f-9825-9809c4d9637c)


Generate a token:
   - Click **Generate** → **Continue**

![Image](https://github.com/user-attachments/assets/0d12a2ea-40b2-46ca-83ba-ccdda8e0ddf4)

![Image](https://github.com/user-attachments/assets/3d38afc9-81ca-4a56-a5c5-4ddf1a2bdbd7)

In 2. choose **the package/code** and **copy the code**

![Image](https://github.com/user-attachments/assets/7c6e4194-2dc0-4adf-a0e6-24ed0718c1c6)

---

## 🧱 3. Build Server Setup

### 📦 Install General Prerequisites  
```bash
apt update -y
apt install git -y
apt install openjdk-17-jre-headless -y
apt install maven -y
apt install npm -y
```

---

## ☕ Java Project Analysis (Maven)

### 📥 Clone and Build Java Project  
```bash
git clone https://github.com/Rahuldepp/Java-Blog.git
cd Java-Blog
mvn package
```
![Image](https://github.com/user-attachments/assets/9ac205ef-08ba-4fa9-a0a5-c2250b2d4fc7)
### 🧪 Run SonarQube Analysis  
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=java \
  -Dsonar.projectName='java' \
  -Dsonar.host.url=http://18.232.140.167:9000 \
  -Dsonar.token=sqp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

✅ Output will show analysis and upload to SonarQube.

---

## 💻 JavaScript Project Analysis (NPM + SonarScanner)

### 📥 Clone JS Project and Setup  
```bash
git clone https://github.com/<your-js-repo>.git
cd js_code/
npm install
npm install -g @sonar/scan
```

### 📄 Create `sonar-project.properties`
```bash
vi sonar-project.properties
```

Paste the following:
```properties
sonar.projectKey=js
sonar.projectName=js
sonar.projectVersion=1.0
sonar.sources=.
sonar.host.url=http://18.232.140.167:9000
sonar.login=sqp_ff83de42e0c3931f39f99357a83f4c0fa98efbc6
```

### 🧪 Run SonarQube Scanner  
```bash
sonar-scanner
```

✅ Results will be uploaded to the SonarQube server.

---

## 🐍 Python Project Analysis

### 📥 Prepare and Analyze Python Project  
```bash
cd python_code/
```

![Image](https://github.com/user-attachments/assets/1d6028ec-03ca-4516-a4d6-e84161a72b5a)

### 🧪 Run SonarQube Scanner  
```bash
sonar-scanner \
  -Dsonar.projectKey=python \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://44.202.193.53:9000 \
  -Dsonar.token=sqp_e36b7c7b5af01a866631fd7a9dff62cf5b0c3c59
```

✅ Python code analysis will appear in the SonarQube dashboard.

![Image](https://github.com/user-attachments/assets/7cd791c0-2228-4049-8f97-921d7da8067f)
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
