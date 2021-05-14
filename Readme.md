![N|Solid](https://images2.imgbox.com/5c/7f/1eNS6Ol7_o.png "VaxNotifier")
###### A Termux-tool to notify you when vaccine available in your region
### 
####
> *This tool will not auto register or schedule Vaccine doses for you. You have to do it yourself from the official CoWin Website.* 
## Features

- Notify you when any vaccine dose(s) is available in your desire region.
- Set notifier according to your desire location on the basis of Pin or district.
- Will check for available slot 24 x 7.
- Get public data.
- All available data will get logged on the console.

This tool is made to automate the task of checking vaccine availability so that you can focus on your task and schedule your vaccine dose at earliest.

## Installation

##### 1. Download and Install Essentials
- Head to Google Play Store or any App Store and download [Termux](https://play.google.com/store/apps/details?id=com.termux) and [Termux:API](https://play.google.com/store/apps/details?id=com.termux.api&hl=en)
![N|Solid](https://images2.imgbox.com/7d/e0/A5OllIiS_o.png "Install Termux")
![N|Solid](https://images2.imgbox.com/88/b3/gNXu13qi_o.png "Install Termux:API")
*Temux is needed to run this tool and Termux:API is needed to show notification and control device vibration*
##### 2. Open Termux and allow all permissions
- *The first time when you will open Termux, it will take some time to set-up. After that you will get an interface similar to the below image*
 ![N|Solid](https://images2.imgbox.com/48/85/ygqQu6uM_o.jpeg "Install Termux")
- Type the following command and hit enter, then allow the storage permission. We need this to move the script file to Termux's Home directory in order to execute it.
`termux-setup-storage`
##### 3. Download Main files and Setup
- You can download the zip/archive file from the release tab and Run the following command
  >*The below command is going to vary according to your download location. Most the device has the default download location as below. But, if you use third-party non-chromium browser then you may need to modify the below command to your download location.*
  
  ```sh 
   unzip storage/downloads/VaxNotifier_release.zip
   sh setup.sh
   ```
  *You may get prompt at 3-4 location during the installation
  First, At the beginning just press Enter on your Virtual Keyboard.
  Second and Third, Type 'Y' and press Enter.*

  *_During setup if you see any kind of error, then re-run the second and third command until you fix that. Also try to re-install Termux if error persists._
 
 ##### 4. Running the tool
 - After you restarted termux, everytime you want to run the tool, type the following command and you're good to go!
 
   `python VaxNotifier.py`
- Choose the desired options and set up the notifier according to your desire

  *__Do Not close termux from recent tab or notification panel or else, you will not get vaccine updates__*
  
 ## Screenshots
 ##### 1
 ![N|Solid](https://images2.imgbox.com/0b/c6/Dpq1fABG_o.jpeg "Screenshot-1")
 ##### 2
 ![N|Solid](https://images2.imgbox.com/83/f6/Lapq8tmK_o.jpeg "Screenshot-2 (Logs)")
 ##### 3
 ![N|Solid](https://images2.imgbox.com/8b/84/aW9A8o7n_o.jpeg "Screenshot-3 (Notification)")
 
 ### A Short Message
 __History says that, Humanity had faced a lot more bigger problems than this. During the time of World War. Different country tried to tear humanity appart but, we successfully overcame that situation because there is a hidden bond that connect us together. The bond that cannot be broken by some external Energy. But, During this pandemic we've have seen a BIG question mark on this bond. People are neglecting to serve the poor, the needy, people who are literally dying just because of hunger. Think about the people who used earn daily wages for their daily diet. The people who are used to be helpful and kind, are now fighting with each other just to get a single dose of vaccine. Rich ones leaving the county to protect their kind ones and poor ones just waiting for their turn to leave this world. People who can afford breads to the people who can't afford it, are neglecting to serve them just because of the fear of getting a positive result. But, at the same time these people can be found at hangouts, party etc...
 But, there are some people who are comming out of there comfy zone and pushing there capacity to max to help others. These are the people for which the word "Community" is not just a word in the dictionary.
 Please stay safe, avoid going outside for absoloute no good reason and follow all the Covid guildlines.__
 *Kill corona not Hummanity*
