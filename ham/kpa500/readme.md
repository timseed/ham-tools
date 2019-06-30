# Installing

You will need python, preferable3 - as I have not tested it on anything else !

# Python Modules 

Should be straightforward

   pip install -r requirements.txt

Occasionally yaml can be a little strange to install  - fingers crossed.

# Configuration


There are 2 places we need to change things - the first is a simple port name.

## Port Name

Edit the file called **config.yaml** and update the device to the KPA500's serial connection name. 

## Ip Address

The webpka.py starts a web server, which listens on an IP address (this should be in a config file). So please edit the webkpa.py file and replace *192.168.1.163* with your IP Address.

Please note the IP Address and the Serial Portname are on the machine where the KPA500 is connected to.

# Starting the Server

Assuming all the Configuration changes are done

    python webpka.py

You can make this a detached process if you need - but to start with it may be best to see what the program is outputting.


To connect to the Web screen open up a browser and enter the IP Address you set about 8 lines above.  i.e.   192.168.1.163:8000

*Note* the Ip Address must have the port number (by default 8000, again you can change this in case you have other web services running).

Any issues - please drop me a line.

Please note: There is minimal error checking - so if you enter something totally stupid there is a possibility this will have an unpleasant consequence on your KPA. Simple steps please !!

de Tim, A45WG


