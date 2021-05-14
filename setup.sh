echo "\033[38;5;226mGoing to have a full system update and need to download some packages!\033[0m"
echo ' '
echo "\033[38;5;145mPress Enter to Start\033[0m" && read REPLY
echo "\033[38;5;46mUpdating Termux...\033[0m"
apt update -y
echo "\033[38;5;46mUpgrading system...\033[0m"
apt upgrade -y
echo "\033[38;5;46mDownloading API Package...\033[0m"
pkg install termux-api -y
echo "\033[38;5;46mInstalling Essentials...\033[0m"
apt-get install python -y
apt-get install pip -y
echo "\033[38;5;46mDownloading Packages...\033[0m"
pip install requests
termux-notification -t "System ready to run Notifier!" -content "Now, You can setup notifier and check for vaccine availability..."
echo "\033[38;5;196mRestart Termux and type python VaxNotifier.py to run the tool\033[0m"
rm setup.sh
