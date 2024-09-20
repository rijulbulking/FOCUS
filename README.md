
<h1 align="center">
  <br>
  <a href="https://github.com/rijulbulking/FOCUS"><img src="https://raw.githubusercontent.com/rijulbulking/FOCUS/refs/heads/master/ProjectPhotos/FOCUS.png" alt="FOCUS" width="900"></a>
  <br>
  <b> <u>
  🌧️ The FOCUS Framework 🌧️
  </b> </u>
  <br>
</h1>

<h4 align="center">A Malware prevention framework which integrates Machine Learning to reduce the risk of getting affected, Made with  <a href="https://www.python.org/" target="_blank">Python</a>.</h4>


</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> 
</p>

![screenshot](https://github.com/rijulbulking/FOCUS/blob/main/FOCUS.png)

<u>

## **✨Key Features**
</u>

* ### **Port Scanner 📡** 
- Quick, Fast and Efficient Port Scanner
  - Scans open ports on your local system and notifies the user about it.
* ### **Network Usage 📶**
- Monitor Upload/Download/Upload Speed/Download Speed.
  - [Beta Concept] Machine Learning can be implemented in this to detect a sudden network spike in the network, possibly a malicious attack.
* ### **Notifications 🔔**
- Get notified when Open Ports are detected and view the ports which are affected
* ### **Cross platform 🪟🍎🐧**
- Windows, macOS and Linux ready.

<b> <u>
## **✨How To Use**
</b> </u>
```bash
# Clone this repository
$ git clone https://github.com/rijulbulking/FOCUS

# Install the dependencies 
$ pip install -r requirements.txt 

# Go into the repository
$ cd FOCUS

# Run the Framework
$ python3 main.py
```
------------------------
<b> <u>
## **✨Project History**
</b> </u>
First Verion of the code focused primarily on developing a mechanism to scan all possible ports of the local system. However scan times would take much longer than anticipated:

<a href="https://github.com/rijulbulking/FOCUS"><img src="https://raw.githubusercontent.com/rijulbulking/FOCUS/refs/heads/master/ProjectPhotos/FirstScanTime.png" alt="First Test Result" width="300"> </a>

<br>
Scanning just 100 ports would take 204 Seconds, meaning scanning all 65535 ports would take approximately 36 hours.
However a method was found where multiple ports scans could be initialized in seperate threads. This tremendously reduced the scan time to seconds:

<a href="https://github.com/rijulbulking/FOCUS"><img src="https://raw.githubusercontent.com/rijulbulking/FOCUS/refs/heads/master/ProjectPhotos/SecondScanTest.png" alt="Second Test Result" width="300"> </a>
