INSTALL_DIR='/usr/local/bin'


echo "You wanna uninstall Ausis (y/n): ";
read -r mama
if [ "$mama" = "y" ]; then
        if [ "$TERMUX" = true ]; then
            rm -rf "$INSTALL_DIR"
        fi
fi