# **Modem AT command testing**
## Description

This script is used to automaticaly test AT commands on different routers via SSH or serial

## Content

1. <a href=#arguments style="color: White;">Arguments</a>
   * <a href=#terminal-arguments style="color: White;">Terminal arguments</a>
   * <a href=#config-arguments style="color: White;">Config arguments</a>  
     * <a href=#ssh-arguments style="color: White;">SSH arguments</a>
     * <a href=#serial-arguments style="color: White;">Serial arguments</a>
2. <a href=#how-to-edit-configuration-file-to-your-needs style="color: White;">Configuration file</a>
3. <a href=#how-to-start-this-script style="color: White;">Script start</a>
4. <a href=#modules style="color: White;">Modules</a>
5. <a href=#output-file style="color: White;">Output</a>

---
## Arguments

### Terminal arguments

```bash
    -h, --help  show this help message and exit
    -IP         Devices SSH connection IP address
    -u          Devices SSH connection username
    -psw        Devices SSH connection password
    -b          Devices Serial connection baud rate
    -port       Devices connection port
```

### Config arguments

#### SSH arguments
```jsonc
    "authentication": {
        "type" : "SSH",
        "default_address" : "192.168.1.1",  //Devices default IP address to use if address lower is not written and is not given as argument starting script for SSH connection
        "default_username" : "root",        //Devices default user to use if username lower is not written and is not given as argument starting script for SSH connection
        "default_password" : "Admin123",    //Devices default password to use if password lower is not written and is not given as argument starting script for SSH connection
        "default_port" : "/dev/ttyUSB3",    //Devices default port to use if port lower is not written and is not given as argument starting script for AT commands
        "address" : "192.168.2.1",          //Configured IP address credentials for SSH connection starting script
        "username" : "",                    //Configured username for SSH credentials for SSH connection starting script
        "password" : "",                    //Configured password credentials for SSH connection starting script
        "port" : ""                         //Configured port for AT commands starting Serial connection
    }, 
```

#### Serial arguments
```jsonc
    "authentication": {
        "type" : "serial",                  
        "default_port" : "/dev/ttyUSB3",    //Devices default port to use if port lower is not written and is not given as argument starting script for serial connection
        "default_baud_rate" : "115200",     //Devices default baud rate to use if baud_rate lower is not written and is not given as argument starting script for serial connection
        "port" : "",                        //Configured port for serial connection starting script
        "baud_rate" : ""                    //Configured baud rate for serial connection starting script
    },
```
---
## How to edit configuration file to your needs

### Example of how router to connect via Serial configuration should be written

```jsonc
{
   "TRM240": {
      "authentication": {
         "type" : "serial",
         "default_port" : "/dev/ttyUSB3",
         "default_baud_rate" : "115200",
         "port" : "",
         "baud_rate" : ""
      },
      "commands": [
         {
            "command": "ATE1",
            "arguments": [
               ""
            ],
            "expects": "OK"
         }
      ]
   }
}
```

### Example of how router to connect via SSH configuration should be written

```jsonc
{
    "RUTX11": {
        "authentication": {
            "type" : "SSH",
            "default_address" : "192.168.1.1",
            "default_username" : "root",
            "default_password" : "Admin123",
            "default_port" : "/dev/ttyUSB3",
            "address" : "",
            "username" : "",
            "password" : "",
            "port" : ""
        },
        "commands": [
            {
                "command": "ATE1",
                "arguments": [
                ""
                ],
                "expects": "OK"
            }
        ]
    }
}
```

### Example of how multiple routers should be written

```jsonc
{
   "TRM240": {
      "authentication": {
         "type" : "serial",
         "default_port" : "/dev/ttyUSB3",
         "default_baud_rate" : "115200",
         "port" : "",
         "baud_rate" : ""
      },
      "commands": [
         {
            "command": "ATE1",
            "arguments": [
               ""
            ],
            "expects": "OK"
         }
      ]
   },
   "RUTX11": {
        "authentication": {
            "type" : "SSH",
            "default_address" : "192.168.1.1",
            "default_username" : "root",
            "default_password" : "Admin123",
            "default_port" : "/dev/ttyUSB3",
            "address" : "",
            "username" : "",
            "password" : "",
            "port" : ""
        },
        "commands": [
            {
                "command": "ATE1",
                "arguments": [
                ""
                ],
                "expects": "OK"
            }
        ]
    }
}
```

### Example of how command should be written

```jsonc
    "commands": [
         {
            "command": "ATE1",
            "arguments": [
               ""
            ],
            "expects": "OK"
         }
    ]
```

### Example of how multiple commands should be written

```jsonc
    "commands": [
         {
            "command": "ATE1",
            "arguments": [
               ""
            ],
            "expects": "OK"
         },
         {
            "command": "AT",
            "arguments": [
               ""
            ],
            "expects": "OK"
         }
    ]
```

### Example of how arguments should be written

```jsonc
    "commands": [
         {
            "command": "AT+CMGS=\"+3706XXXXXXX\"",
            "arguments": [
               "TRM240",

            ],
            "expects": "OK"
         }
    ]
```

### What expects can be written

- ERORR
- OK
- NO CARIER

### <span style="color:red">Warning!</span>

Added routers, commands or arguments to configuration file should be in line with other routers, commands or arguments otherwise it will not work

### <a href=#example-to-add-commands style="color: Green;">Click to see example of how it should be</a>

### <span style="color:red">Example of how it shouldn't be</span>

```jsonc
    "commands": [
         {
            "command": "ATE1",
            "arguments": [
               ""
            ],
            "expects": "OK"
         },
    {
        "command": "AT",
        "arguments": [
            ""
        ],
        "expects": "OK"
    }
    ] 
```
---
## How to start this script

### To start script use this command

```bash
    python3 script.py <arguments> <device name>
```

### Example

```bash
    python3 script.py -IP 192.168.1.1 -u root -psw admin01 -port /dev/ttyUSB3 rutx11
```
---
## Modules

### configuration_handler

- This module is used to read config file to variable that could be accessed similarly as dictionary

### initializer

- This module is used to make SSH or serial connection between computer and router to variable

### resulter

- This module is used to print text to console and add lines to result list

### tester

- This module is used to send AT commands to router, read response and send it to resulter module

### write_to_file

- This module is used to create new csv file with router name, todays date and time and to write result list to it
---
## Output file

### What information is shown in the output file

- Columns: Executed command, expects for response, response and test passed or failed

### Example of output file

 Command   | Expected | Response | Test   
-----------|----------|----------|--------
 ATE1      | OK       | OK       | Passed 
 AT        | OK       | OK       | Passed 

