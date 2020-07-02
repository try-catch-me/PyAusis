# PyAusis

    Author: Umer Farid, Assasa Hussain
Speech Interactive System in Python (PyAusis) developed for UNIX (Linux, MACOS) and Windows.

# How to install
    git clone github.com/MrRobot-hub/PyAusis.git
    cd PyAusis
    chmod +x setup.sh
    bash setup.sh

# PyAusis Commands Interepretation 

# AusisAPI(self, ausis) 

It's an interface for skills or plugins in AUSIS and recieved values from the second parameter(ausis) during execution function. Moreover this class implements a stateless function which cannot be implemented in packages that is related to Ausis. Some functions of AusisAPI are

# Say

    AusisAPI.say(self, text, color='', speak=True)

This function of the class AusisAPI gives an ability to the print out the text on screen any speak that text when the sound is enabled. If parameter speak has a value False (speak=False) then it only prints the text from the text parameter.

# String Input 

    AusisAPI.input(self, prompt='', color='')

This function is used to take an input as a text from the user and printed on the console. We didn't use input() method to take an input from the user because it doesn't works properly with color codes on window's cmd so we used sys library for input.

# Input Number
    AusisAPI.input_number(self, prompt='', color='', rtype=<class 'float'>, rmin=None, rmax=None)
    
This method takes an input as a numeric value from the user and return that numeric value to the method. If user entered incoorect number it will ask user to enter it again.

# Enable Voice

    AusisAPI.enable_voice(self)
    
Enable voice method is capable of speaking text in voice that was passed as a parameter to Ausis.say() method.

# Disable Voice

    AusisAPI.disable_voice(self)
    
Disable voice is a method of AusisAPI class that is used to stop text to speech output for every text that was passed to Ausis.say() method.

# Is Voice Enabled

    AusisAPI.is_voice_enabled(self)
    
in case of checking voice is enabled or disabled. This method invoked and returned True or False if voice is anabled or disabled while default voice is disabled.

# Get Data

    AusisAPI.get_data(self, key)

It takes some keys from the memory to attain online data such as news, time, weather forecast by using user's current location and country information.

# Add Data

    AusisAPI.add_data(self, key, value)
    
Ausis requires some keys to get online data from different sources such as news, time etc. This method is used to get value and key and stored that into a memory with .json extension inside memory directory for future achievements.

# Update Data

    AusisAPI.update_data(self, key, value)
    
In case of changing sources location for news and different online stuff, keys must be updated with the help of this update_data() method.

# Delete Data

    AusisAPI.del_data(self, key)
    
In case of deleting keys from the memory this method is here to help in deleting that keys from the memory  immediately. 

# Exit

    AusisAPI.exit(self)
    
This function of the class AusisAPI will exit from the Ausis interface immediately and return to the main console

# Skills/Plugins

Pre-installed skills are present in skills directory while skills which are created by yourself will be saved in custom directory. Ausis has ability to search and load plugins from both of the directories.

    from plugin import plugin

    @plugin("hello world")
    def hello_world(ausis, s):
        ausis.say("Hello World!")

    or it can be used as a callable class:

    from plugin import plugin

    @plugin("hello world")
    class hello_world:
        """Prints \"hello world!\""""
        def __call__(self, ausis, s):
            ausis.say("Hello World!")

# Init

If a class Plugins has a function init(self, ausis) this method will be avoked at the initialization state of the execution.

    from plugin import plugin

    @plugin
    class HelloWorld:

        def init(self, ausis):
            ausis.say("INIT HelloWorld!!!")

        def require(self):
            pass

        def complete(self):
            pass

        def alias(self):
            pass

        def run(self, ausis, s):
            ausis.say("Hello world!")

# Features

@alias, @require and @complete are the decorators by which plugins can be modified. These decorators can be used in any order or several times. @plugin must be declared because it is the name of the command by which action of that command would be called.

# Alias

    from plugin import plugin, alias

    @alias("hello", "cmd")
    @plugin("helloCmd")
    def helloWorld(ausis, s):
       pass
       
hello and cmd are the alias of the plugin helloCmd. An alias is just like copy and pasting the whole plugin with the new name.

# Require

@require decorator has all compatiability constraints to check which plugins are compatiable with the system. Those plugins which are not compatable with that system will not be displayed.

# Requirements

> Network connection
> Python(plugin.python2, plugin.python3)
> Platform (plugin.Linux, plugin.MACOS, plugin.Windows)
> Native (string)

# Example

    from plugin import plugin, require, PYTHON3, LINUX, WINDOWS


    @require(platform=[LINUX, WINDOWS], python=python3, network=True, native=["firefox", "curl"])
    @plugin("helloCmd")
    def helloWorld(ausis, s):
        pass

In case of plugin incompatible because of missing native binary ($PATH) a notification will be saved in status of the plugins and will not be counted in loaded plugins during execution.

# Auto Complete Command

Ausis has the feature of auto completion (@complete) of the commands by using TAB button from the keyboard when ausis in text mode.

    from plugin import plugin, complete

    @complete("complete0", "complete1")
    @plugin
    def helloWorld(ausis, s):
        pass

# Multi Word Commands

It's better to create two separate plugins for multi word commands that works with @alias decorator e.g. check ram, check weather.

    @plugin("check weather")
    check_weather(ausis, s):
        pass

    @alias("info ram")
    @plugin("check ram")
    check_ram(ausis s):
        pass
