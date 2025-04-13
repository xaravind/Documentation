
# 🧪 SonarQube Testing of Java, JS, and Python Code (Two-Server Setup)

## 🧠 Goal  
Set up **two separate servers**:  
- 🏗️ **Build Server**: for compiling code and running SonarQube analysis  
- 🧠 **SonarQube Server**: for hosting SonarQube and viewing results  

Test static analysis using SonarQube for a Java (Maven-based) project.

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
**http://18.232.140.167:9000**  
Login: `admin / admin`

---

## 🛠️ 2. Configure a SonarQube Project (Web UI)

1. Go to **Projects** → **Create Project**
2. Choose **Manually** (Local project)
3. Enter:
   - Project key (e.g., `java`)
   - Project name
4. Select **Use global settings**, then choose **Locally**
5. Generate a token:
   - Name: e.g., `java-token`
   - Click **Generate** → **Continue**

You’ll see a Maven command like:
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=java \
  -Dsonar.projectName='java' \
  -Dsonar.host.url=http://18.232.140.167:9000 \
  -Dsonar.token=sqp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 🧱 3. Build Server Setup

### 📦 Install Prerequisites  
```bash
apt update -y
apt install git -y
apt install openjdk-17-jre-headless -y
apt install maven -y
```

### 📥 Clone and Build a Java Project  
```bash
git clone https://github.com/Rahuldepp/Java-Blog.git
cd Java-Blog
mvn package
```

### 🧪 Run SonarQube Analysis  
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=java \
  -Dsonar.projectName='java' \
  -Dsonar.host.url=http://18.232.140.167:9000 \
  -Dsonar.token=sqp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

✅ Output will show SonarQube scanning and uploading results.

---

## 📊 4. View Results in SonarQube

Open browser → http://18.232.140.167:9000 → Go to your **project dashboard**  
✔️ Review:
- Code smells
- Bugs
- Vulnerabilities
- Coverage (if tests were run)

---

## ✅ Summary

| Component         | Purpose                          |
|------------------|----------------------------------|
| **SonarQube Server** | Hosts the SonarQube dashboard |
| **Build Server**     | Builds and analyzes project   |
| **Tools Used**       | Java, Maven, Git, SonarQube  |
