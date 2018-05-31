## Overview of Local Server on Windows 

For the backend part, we need to do two jobs:

1. Get the version numbers of local softwares.

2. Check if a local software has update.

The brief process of our program is:

- Get the list of installed softwares and their version numbers with Powershell command line

- Launch a local server that listens to a certain port.

- When user opens a new tab, the frontend (Chrome extension) will send a packet to local server.

- Once the local server catches the packet, it will start to check which installed softwares are in the white list. For installed softwares in the white list, the local server will scrape their latest version numbers online (from Softpedia.com) and check which softwares have updates.

- The local server generates a packet including softwares and update info and send it back to our Chrome extension.

## Files Details  

==== `data`    # directory to store white list file, local softwares info

======== `fetch_version_info.bat` # a wrapper to get installed software info

​							   \# and launch local host

======== `fetch_version_info.ps1` # get installed software info with Powershell command line

======== `localhost.py` # code of local host

======== `response_gen.py` # methods to generate a response packet (softwares have updates)

======== `Software_wrapper.py` # code of class `Software`

## Usage 

Simply run `fetch_version_info.bat` (double click in Windows). 

It will store installed softwares info in `data` directory and launch a local server. There are two files (`version1.csv` and `version2.csv`) since 32-bit softwares and 64-bit softwares are separately stored in Windows registry. 

If you have already installed our Chrome extension, once you open a new tab, wait for a while and you will see updates info. 

## Further work

Since scraping data from webpages costs a lot of time, we should scrape data when Windows boots and store it into a database. When a user opens a new tab, the local server should check latest version info in the database instead of do runtime scraping, which will save a lot of time in practice. 