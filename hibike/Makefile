### DISCLAIMER
### This is an example Makefile and it MUST be configured to suit your needs.
### For detailed explanations about all the available options,
### please refer to https://github.com/sudar/Arduino-Makefile/blob/master/arduino-mk-vars.md

### PROJECT_DIR
### This is the path to where you have created/cloned your project

PROJECT_DIR       = $(PWD)

### AVR_GCC_VERSION
### Check if the version is equal or higher than 4.9
AVR_GCC_VERSION  := $(shell expr `avr-gcc -dumpversion | cut -f1` \>= 4.9)

### ARDMK_DIR
### Path to the Arduino-Makefile directory.
ARDMK_DIR         = $(PROJECT_DIR)/Arduino-Makefile

### ARDUINO_DIR
### Path to the Arduino application and resources directory.
ARDUINO_DIR       = /opt/arduino-1.8.1

ARDUINO_LIBS := Wire Servo

### USER_LIB_PATH
### Path to where your project's libraries are stored.
SKETCH_LIBS = hibike Adafruit_TCS34725 EEPROM SevenSeg TimerOne TimerThree FlexiTimer2 PID_v1 Encoder MFRC522 SPI NicoHID NicoHID/SingleReport
USER_LIB_PATH     :=  $(realpath $(PROJECT_DIR)/lib)

### BOARD_TAG & BOARD_SUB
### For Arduino IDE 1.0.x
### Only BOARD_TAG is needed. It must be set to the board you are currently using. (i.e uno, mega2560, etc.)
# BOARD_TAG         = mega2560
### For Arduino IDE 1.6.x
### Both BOARD_TAG and BOARD_SUB are needed. They must be set to the board you are currently using. (i.e BOARD_TAG = uno, mega, etc. & BOARD_SUB = atmega2560, etc.)
### Note: for the Arduino Uno, only BOARD_TAG is mandatory and BOARD_SUB can be equal to anything
BOARD_TAG         = micro
# BOARD_SUB         =


### MONITOR_BAUDRATE
### It must be set to Serial baudrate value you are using.
MONITOR_BAUDRATE  = 115200

### AVR_TOOLS_DIR
### Path to the AVR tools directory such as avr-gcc, avr-g++, etc.
AVR_TOOLS_DIR     = /opt/arduino-1.8.1/hardware/tools/avr

### AVRDUDE
### Path to avrdude directory.
AVRDUDE          = /opt/arduino-1.8.1/hardware/tools/avr/bin/avrdude
AVRDUDE_CONF		 = /opt/arduino-1.8.1/hardware/tools/avr/etc/avrdude.conf

### CFLAGS_STD
CFLAGS_STD        = -std=gnu11

### CXXFLAGS_STD
CXXFLAGS_STD      = -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -fno-devirtualize -fno-use-cxa-atexit

### CPPFLAGS
### Flags you might want to set for debugging purpose. Comment to stop.
CXXFLAGS         = -pedantic -Wall -Wextra

### If avr-gcc -v is higher than 4.9, activate coloring of the output
ifeq "$(AVR_GCC_VERSION)" "1"
    CXXFLAGS += -fdiagnostics-color
endif
### random uid
RANDOM := 0x$(shell head -c 8 /dev/urandom | xxd -p)
CXXFLAGS += -D UID_RANDOM=$(RANDOM)

CXXFLAGS += -D DESCRIPTOR=$(shell python escape_json.py $(PROJECT_DIR)/devices/$(DEVICE)/*.json)

LOCAL_CPP_SRCS := $(wildcard $(PROJECT_DIR)/devices/$(DEVICE)/*.cpp)

### MONITOR_PORT
### The port your board is connected to. Using an '*' tries all the ports and finds the right one.
# MONITOR_PORT      = /dev/ttyACM*

### Don't touch this
CURRENT_DIR       = $(shell basename $(CURDIR))

### OBJDIR
### This is were you put the binaries you just compile using 'make'
CURRENT_DIR       = $(shell basename $(CURDIR))
OBJDIR            = $(PROJECT_DIR)/bin/$(CURRENT_DIR)/$(BOARD_TAG)

### Path to Arduino.mk, inside the ARDMK_DIR, don't touch.
include $(ARDMK_DIR)/Arduino.mk
