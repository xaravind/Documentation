

## 💻 JavaScript Project Analysis (NPM + SonarScanner)

### 📥 Clone JS Project and Setup  
```bash
git clone https://github.com/<your-js-repo>.git
cd js_code/
npm install
npm install -g @sonar/scan
```
```bash
root@ip-172-31-26-213:~/Documentation/js_code# ll
total 208
drwxr-xr-x 4 root root   4096 Apr 13 09:33 ./
drwxr-xr-x 6 root root   4096 Apr 13 09:33 ../
drwxr-xr-x 3 root root   4096 Apr 13 09:33 dist/
-rw-r--r-- 1 root root 172684 Apr 13 09:33 package-lock.json
-rw-r--r-- 1 root root   1086 Apr 13 09:33 package.json
-rw-r--r-- 1 root root   6041 Apr 13 09:33 readme.md
drwxr-xr-x 4 root root   4096 Apr 13 09:33 src/
-rw-r--r-- 1 root root    322 Apr 13 09:33 tsconfig.json
-rw-r--r-- 1 root root   1317 Apr 13 09:33 webpack.config.js
```
![Image](https://github.com/user-attachments/assets/9ac205ef-08ba-4fa9-a0a5-c2250b2d4fc7)

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
