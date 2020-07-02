#!/bin/bash
clear
echo "
██╗███╗░░██╗░██████╗████████╗░█████╗░██╗░░░░░██╗░░░░░███████╗██████╗░
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░░░░░██╔════╝██╔══██╗
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░░░░██║░░░░░█████╗░░██████╔╝
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░░░░██║░░░░░██╔══╝░░██╔══██╗
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║███████╗███████╗███████╗██║░░██║
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝

              }+{ Author :: Umer Farid, Assasa Hussain }+{
               }+{   Email :: umerfarid53@gmail.com   }+{
                 }+{Github :: github.com/MrRobot-hub}+{"

echo -e "[\e[32m1\e[97m]. Install Ausis \n[\e[32m2\e[97m]. Uninstall Ausis \n[\e[32m3\e[97m]. Update Ausis \n[\e[32m4\e[97m]. Exit";
read -r mama
if [ "$mama" == '1' ]; then

	cd $(dirname $0)

	if python --version; then
		python installer
	elif python3 --version; then
		python3 installer
	elif python2 --version; then
		python2 installer
	else
		echo "Could not find Python installation"
	fi
elif [ "$mama" == '2' ]; then
    #statements
    cd $(dirname $0)
    sudo chmod +x uninstall.sh
    sudo ./uninstall.sh

elif [ "$mama" == '3' ]; then
    cd $(dirname $0)
    sudo chmod +x update.sh
    sudo ./update.sh
else
    echo "Good Bye!"
fi