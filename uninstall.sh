clear

echo "
██╗░░░██╗██╗███╗░░██╗░██████╗████████╗░█████╗░██╗░░░░░██╗░░░░░███████╗██████╗░
██║░░░██║██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░░░░░██╔════╝██╔══██╗
██║░░░██║██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░░░░██║░░░░░█████╗░░██████╔╝
██║░░░██║██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░░░░██║░░░░░██╔══╝░░██╔══██╗
╚██████╔╝██║██║░╚███║██████╔╝░░░██║░░░██║░░██║███████╗███████╗███████╗██║░░██║
░╚═════╝░╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝

              }+{ Author :: Umer Farid, Assasa Hussain }+{
               }+{   Email :: umerfarid53@gmail.com   }+{
                 }+{Github :: github.com/MrRobot-hub}+{

";


INSTALL_DIR='/usr/local/bin'

if [ -e "$INSTALL_DIR/Ausis" ]; then
	echo "[!] Do you wanna uninstall Ausis (y/n): ";
	read -r mama

    if [ "$mama" == "y" ]; then
        sudo rm -f "$INSTALL_DIR/Ausis"
        echo "[+] Uninstalled Successfully"
    elif [ "$mama" == "n" ]; then
        	
  		echo "[+] Thanks for using Ausis!"
    
    fi
else
	echo "[+] No Installation found!"
fi