Frontend - Vue.JS (3 version) chat + socket.io
Backend - Python + Flask-socketIO + redis (cache) + postgresql (db)

<ul>Features:
<li>auto-add new users</li>
<li>auto-sort by last message</li>
<li>socketio send messages</li>
<li>send readinfo</li>
<li>muli-windows messages</li>
</ul>
<ul>TODO:
<li>lazy-load messages</li>
<li>send files</li>
<li>send smiless</li>
<li>multiusers chat</li>
<li>OAuth</li>
</ul>
<br />
Chat list

<ul>STEPS TO RUN

<li>sudo apt install postgresql redis python3-setuptools</li>
<li> install nodejs v17<br />
# Using Ubuntu<br />
curl -fsSL https://deb.nodesource.com/setup_17.x | sudo -E bash -<br />
sudo apt-get install -y nodejs<br />
</li>
<li>create postgres database chat</li>
<li>change db user postgres password to 'postgres'</li>
<li>cd frontend/</li>
<li>npm run build</li>
<li>cd ../backend/</li>
<li>pip3 install -r requirements.txt</li>
<li>python app.py</li>
</ul>




![image](https://user-images.githubusercontent.com/36193265/164279233-78ee8679-605c-4e15-8f73-0132542ec2f9.png)
