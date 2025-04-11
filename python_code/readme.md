
# **Deploy Python Flask App with Gunicorn on Amazon Linux**

## **Prerequisites**

- Amazon Linux EC2 instance running
- Root/sudo access
- Python 3 and pip
- Git installed
- Flask app files with `requirements.txt`

---

## **1. Switch to Root and Update the System**

```bash
sudo -i
yum update -y
```

---

## **2. Check and Install Python 3**

Check if Python 3 is already installed:

```bash
yum list installed | grep -i python3
```

If not installed:

```bash
sudo yum install python3 -y
```

---

## **3. Install Required Packages**

```bash
yum install git -y
yum install python3-pip -y
```

---

## **4. Clone or Navigate to Flask App Directory**

Navigate to your Flask app directory:

```bash
git clone <git-url>
cd /root/example-voting-app/vote
```

---

## **5. Install Python Dependencies**

Install required packages:

```bash
pip3 install -r requirements.txt
pip3 install flask
pip3 install redis
pip3 install gunicorn
```

---

## **6. Create and Activate Virtual Environment**

Create a virtual environment under the ec2-user home directory
The following command creates the app directory with the virtual environment inside of it. You can change my_app to another name.
If you change my_app, then reference the new name in the remaining resolution steps:

```bash
python3 -m venv myenv
```

To activate the environment, source the activate file in the bin directory under your project directory:

```bash
source myenv/bin/activate
```
Your shell prompt should change, indicating you're in the virtual environment.

---

## **7. Run Flask App (Test in Dev Mode)**

Test the Flask app:

```bash
python3 app.py
```
you should see:

```bash
(myenv) [root@ip-172-31-24-252 vote]# python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:80
 * Running on http://172.31.24.252:80
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 138-173-870
```

---

## **8. Install and Test Gunicorn**

Gunicorn is a WSGI HTTP server for running Python web apps in production.

What is WSGI?
WSGI (Web Server Gateway Interface) is a standard interface that defines how Python web servers and applications communicate.
It allows Python web applications to be deployed on various web servers without modification, enhancing flexibility and portability.

Install Gunicorn:


```bash
pip3 install gunicorn
```

Run Gunicorn manually to test:

```bash
gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0
```

you should see successful startup logs and incoming requests in real time.

Now, the app is running as a front-end service
We need to convert this as a backend service, by creating a .service file 

---

## **9. Create systemd Service for Flask App**

Create a systemd service file:

```bash
vi /etc/systemd/system/vote.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/example-voting-app/vote
ExecStart=/root/example-voting-app/vote/myenv/bin/gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0
TimeoutStopSec=90
Restart=always
KillMode=mixed

[Install]
WantedBy=multi-user.target
```

---

## **10. Start and Enable the Flask Service**

Reload systemd:

```bash
systemctl daemon-reload
```

Start the Flask service:

```bash
systemctl start vote.service
```

Check service status:

```bash
systemctl status vote.service
```

```bash
(myenv) [root@ip-172-31-24-252 vote]# systemctl daemon-reload
(myenv) [root@ip-172-31-24-252 vote]# systemctl start  vote.service
(myenv) [root@ip-172-31-24-252 vote]# systemctl status  vote.service
● vote.service - Gunicorn instance to serve app1
     Loaded: loaded (/etc/systemd/system/vote.service; disabled; preset: disabled)
     Active: active (running) since Thu 2025-04-10 16:20:53 UTC; 8s ago
   Main PID: 27590 (gunicorn)
      Tasks: 5 (limit: 4656)
     Memory: 81.6M
        CPU: 566ms
     CGroup: /system.slice/vote.service
             ├─27590 /root/example-voting-app/vote/myenv/bin/python3 /root/example-voting-app/vote/myenv/bin/gunicorn app:app -b>
             ├─27591 /root/example-voting-app/vote/myenv/bin/python3 /root/example-voting-app/vote/myenv/bin/gunicorn app:app -b>
             ├─27592 /root/example-voting-app/vote/myenv/bin/python3 /root/example-voting-app/vote/myenv/bin/gunicorn app:app -b>
             ├─27593 /root/example-voting-app/vote/myenv/bin/python3 /root/example-voting-app/vote/myenv/bin/gunicorn app:app -b>
             └─27594 /root/example-voting-app/vote/myenv/bin/python3 /root/example-voting-app/vote/myenv/bin/gunicorn app:app -b>

Apr 10 16:20:53 ip-172-31-24-252.ec2.internal systemd[1]: Started vote.service - Gunicorn instance to serve app1.
Apr 10 16:20:53 ip-172-31-24-252.ec2.internal gunicorn[27590]: [2025-04-10 16:20:53 +0000] [27590] [INFO] Starting gunicorn 23.0>

```

Enable the service to start on boot:

```bash
systemctl enable vote.service
```

---

## **11. Access the Application**

Open your browser and visit:

```
http://<EC2_PUBLIC_IP>:80 or ex:- http://98.84.170.173/ or http://98.84.170.173:80
```

Replace `<EC2_PUBLIC_IP>` with your instance's public IP address.


![Image](https://github.com/user-attachments/assets/286193f1-5a77-4d2b-bcc8-dae980bb8cca)

used commands:

```bash
(myenv) [root@ip-172-31-24-252 vote]# history
    1  yum update -y
    2  yum install git -y
    3  git clone https://github.com/Ai-TechNov/example-voting-app
    4  cd example-voting-app/vote/
    5  ll
    6  cat requirements.txt
    7  yum install pip3 -y
    8  pip3
    9  yum install python3-pip -y
   10  pip3 install -r requirements.txt
   11  python3 -m venv my_app/env
   12  source env/bin/activate
   13  ll
   14  python3 -m venv myenv
   15  source myenv/bin/activate
   16  python3 main.py
   17  pip3 install flask
   18  python3 app.py
   19  pip3 install redis
   20  pip3 install gunicorn
   21  python3 app.py
   22  gunicorn app:app -b 0.0.0.0:80 --log-file - --access-logfile - --workers 4 --keep-alive 0
   23  pwd
   24  vi /etc/systemd/system/vote.service
   25  cat /etc/systemd/system/vote.service
   26  systemctl daemon-reload
   27  systemctl start  vote.service
   28  systemctl status  vote.service
   29  history

```
---

