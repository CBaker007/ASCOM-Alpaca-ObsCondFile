# ASCOM-Alpaca-ObsCondFile
An ASCOM Alpaca Observing Conditions device that reads data from a Boltwood formatted file.

*********************************************
****  Process to Install and Use Driver  ****
*********************************************
<COMING SOON>


*********************************************
****  Process to Setup for Modding Code  ****
*********************************************

Download and install the latest ConformU tester for Windows (needed for testing Alpaca driver only):
- https://github.com/ASCOMInitiative/ConformU/releases
- Click on version like "Conform Universal v2.0.0+16486" at the top
- Scroll down to the bottom and select Windows installer (Conform...Setup.exe) 
- https://github.com/ASCOMInitiative/ConformU/releases/download/v2.0.0%2B16486/ConformU.2.0.0+16486.Setup.exe

Download and install Microsoft VS Code
Download and Install Python for Windows (https://phython.org)
Verify Python is installed and what version by:
  1) Open windows cmd prompt (search box, cmd)
  2) Type "py -3 --version".
  3) Should respond with Python <version>
Install Python extensions for VS Code by:
  1) In VS Code type ctrl+shift+x to bring up search extensions in marketplace.
  2) Search and install "Python Extension Pack"

Clone GitHub Repository by:
  1) Opening VS code, "Terminal -> New Terminal"
  2) CD to your VS Code Project folder (example: C:\user\<username>\VS Code\Projects)
  3) Clone to your machine: "git clone https://github.com/CBaker007/ASCOM-Alpaca-ObsCondFile Alpaca-ObsCond-File"
  4) CD into the clone folder "CD Alpaca-ObsCond-File"

Open the project folder in VS Code: 
  1) Open VS code
  2) "File -> Open Folder" select your "AplycaDevice" folder.

Create a virutal python environment (so the python options we use are isolated to this project):
  1) In VS Code, ctrl+shift+p and search for Python:Create Environment...
  2) Choose .venv
  3) Then your version of python (for example: Python 3.11.4 64-bit)

Install the dependencies needed:
  1) In VS Code, open a new terminal (terminal -> new)
  2) In the new terminal first type:
  3) Add Falcon: pip install falcon (should show installing ... installed)
  4) Add Toml: pip install toml (should show installing ... installed)

Verify the setting by:
  1) In VS Code, open <Your Project Folder>
  2) In the VS Code explorer on the left, find and open config.toml (verify IP, port, file location, etc. is OK)

Build and Run server:
  1) In VS Code, open <your project folder> (File->Open Folder)
  2) Open device/app.py  (Must choose thie main app.py file to build AND RUN the entire project.)
  3) Choose "Run" from the menu.
  4) Accept the Windows Firewall addition for your IP:Port if prompted.
  5) The app.py should be running.

Test Your Build:
  1) Run the ConformU you installed earlier.
  2) Choose "Select Device" and "Observing Conditions".
  3) It should automatically discover it.
  4) Select 127.0.0.1 version (assuming you are running both locally)
  5) Start test.
  6) Should run through all the tests with OK or INFO/ERRORS.

Debugging:
  1) In ConformU: Can also check protocol which is helpful when debugging.
  2) In VS Code: Can stop debugging, modify logging level to DEBUG in config.toml.  Re-run with debugging.
  3) Can view the logs in project folder with the latest being observingconditions.log
 
NOTE:  Might want to create your own Project Folder and do the above setup and keep the original clean for reference.
