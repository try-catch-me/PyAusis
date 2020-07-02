
#!/bin/bash
# Script for update Ausis

echo "
██╗░░░██╗██████╗░██████╗░░█████╗░████████╗███████╗██████╗░
██║░░░██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║░░░██║██████╔╝██║░░██║███████║░░░██║░░░█████╗░░██████╔╝
██║░░░██║██╔═══╝░██║░░██║██╔══██║░░░██║░░░██╔══╝░░██╔══██╗
╚██████╔╝██║░░░░░██████╔╝██║░░██║░░░██║░░░███████╗██║░░██║
░╚═════╝░╚═╝░░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝

        }+{ Author :: Umer Farid, Assasa Hussain }+{
         }+{   Email :: umerfarid53@gmail.com   }+{
           }+{Github :: github.com/MrRobot-hub}+{
";

git clone --depth=1 https://github.com/MrRobot-hub/PyAusis
sudo chmod +x PyAusis/setup.sh
bash PyAusis/setup.sh
