# Introduction

​    This is a part of the google chrome extesion project. This sub project is specifically design for mac system. With this program, the chrome new tab is changed to a dashboard which shows different kinds of plugins. Right now, we provided a software update checking plugin, which will check all the softwares' version installed on you computer and compare them to the softwares' version listed on our software whitelist. And show the user which softwares are out of date. 

# How to use it

### 1.Setup chrome extension

1. Go to chrome://extensions/ on chrome
2. Select load unpacked extensions
3. Select this frameWorkExtension package
4. Confirm

### 2.Setup local server

1. Install PM2 globally using NPM (npm install pm2 -g)
2. Start this script in localApp folder with pm2 (pm2 start app.js)
3. generate an active startup script (pm2 startup) NOTE: pm2 startup is for startting the PM2 when the system reboots. PM2 once started, restarts all the processes it had been managing before the system went down.
4. In case you want to disable the automatic startup, simply use pm2 unstartup**



# How does it work

​    First of all, the framework html(showing the dashboard) in the extension program has four iframe. Each of the iframe is like a plugin, they can display different local html pages. Thus, the dashboad can display an software update checking plugin, a fishpool plugin, a chat bot plugin and a new plugin at the same time. Also, it's very easy to change plugins. All the developer has to do is to change the href tag in the framework html page. Also there's a google search bar in the middle of the dashboard for the convience of the user. 

​    Second, regarding how the software update checking plugin works is a little complicated. First, it has to use server to scrape the software information of our desired softwares from the website "softpedia".  To elaborate a little more about the desired softwares mentioned above, they are the softwares that we have to defined by ourself because the name of software varies a lot. Thus we have to establish a map for the names of the software to the names on "softpedia" to correctly scrape the right data. After that, the local server on the user's computer will get the softwares installed on their computer and compare them with the scraped data. Last, the local server will push these data to the chrome extension and display it. Note that there is another function just for mac, the update function. The local server can also check the apps that are installed through appstrore,  get the correct update information and update them. This function right now is disabled for the sake of demo, but it can be easily reimplemented. More detail is written in app.js file.

​    Third, we use pm2 to run the local server for the sake of consisency. Pm2 will let the server to run in the background and it will start the server every time the user's computer activates.

### Author

Adrian Chang(adrian.aa.chang.aa@gmail.com)

Junting Chen

Ting Lu



# 



