WinUpdatesManager
=================

Series of scripts to manage MS DLC from KB913086 and others
* Support to process data through uif(JSON list) files, [MongoDB](https://www.mongodb.org/) or [SQLite](https://sqlite.org/).
* Collect data provided to *uif* (Updates Information) files that can be converted to MongoDB or SQLite through accompaniment tools *uif2MongoDB* and *uif2SQLite*.
* To work through MongoDB installing of [pymongo](https://pypi.python.org/pypi/pymongo/) required.
* For web UI installing of [cherrypy](https://pypi.python.org/pypi/CherryPy) required.

##Sample using

###Using getUif script for collect data
* Mount ```ISO-9660 DVD5 image``` with [security updates](http://support.microsoft.com/kb/913086/). To do so at Windows 8 and up right click on iso file and Open with Windows Explorer, for previous version of Windows you can use external application, for example [WinCDEmu](http://wincdemu.sysprogs.org/).
* Open cmd.exe, move to Python folder.
* Type and execute ```python getUif.py <path to mount point of image> <MMYY>```. Where MM is month of image (from 01 to 12) and YY is last two digits of image year, for example for 2015 it will be 15.
* List of update description in ```uif``` format (JSON list), so you can save to file, just add to command ```> file.uif```.
* For own created year edition of iso image required only path. All folders at root with name in form <MMYY> will be scanned.
* To import stored info into MongoDB type and execute ```python uif2MongoDB.py <file.uif or folder with *.uif> <database name> <table name> <address of server, for example mongodb://127.0.0.1:27017/> (optional, if not set using local)```. Names for database and table(collection) can be any, but while query used database ```win32``` and table ```updates``` so it required to set that names.
* To import stored info into SQLite type and execute ```python uif2SQLite.py <file.uif or folder with *.uif> <path to SQLite file, if not exist it will be created>```. Extension of SQLite file can be any except ```uif```.

###Using updates4Target(command line UI) or webUi to query information from collected data
* Open cmd.exe, move to Python folder.
* Depend of data storage running of ```updates4Target.py``` will be next:
   - ```python updates4Target.py <Path to uif file> or <Path to folder with uif files> <Os name> <Os type> <Os language> <Path to report file>(optional)```
   - ```python updates4Target.py <Path to MongoDB server, for example mongodb://127.0.0.1:27017/> <Os name> <Os type> <Os language> <Path to report file>(optional)```
   - ```python updates4Target.py <Path to SQLite file> <Os name> <Os type> <Os language> <Path to report file>(optional)```
* For running ```webUi.py``` you pass only source data(```<Path to uif file>```, ```<Path to MongoDB server>``` or ```<Path to SQLite file>```) and than open in web browser link [http://127.0.0.1:8080](http://127.0.0.1:8080) (by default configuration) where you can choose your target OS parameters and put required report.

###Using updates2Package to packing updates into folder tree that used in ISO-9660 DVD5 image with security updates
* For updates that do not located at regular iso images used manual download.
* Than you can automatic packing that files into folders' tree.
* Open cmd.exe, move to Python folder.
* Type and execute ```python updates2Package.py <Path to folder with downloaded updates>```.
* For example you downloaded:
   * Windows6.0-KBXXXXXXX-x64.msu
   * Windows6.0-KBXXXXXXX-x86.msu
   * Windows6.1-KBXXXXXXX-x64.msu
   * Windows6.1-KBXXXXXXX-x86.msu
   * Windows8.1-KBXXXXXXX-x64.msu
   * Windows8.1-KBXXXXXXX-x86.msu
   * Windows8-RT-KBXXXXXXX-x64.msu
   * Windows8-RT-KBXXXXXXX-x86.msu
   * WindowsServer2003-KBXXXXXXX-x64-ENU.exe
   * WindowsServer2003-KBXXXXXXX-x64-RUS.exe
   * WindowsServer2003-KBXXXXXXX-x86-ENU.exe
   * WindowsServer2003-KBXXXXXXX-x86-RUS.exe
* After executing updates2Package you got next file system tree:
├───Windows7
│   ├───x64
│   │   └───NEU
│   │           Windows6.1-KBXXXXXXX-x64.msu
│   │
│   └───x86
│       └───NEU
│               Windows6.1-KBXXXXXXX-x86.msu
│
├───Windows8
│   ├───x64
│   │   └───NEU
│   │           Windows8-RT-KBXXXXXXX-x64.msu
│   │
│   └───x86
│       └───NEU
│               Windows8-RT-KBXXXXXXX-x86.msu
│
├───Windows8.1
│   ├───x64
│   │   └───NEU
│   │           Windows8.1-KBXXXXXXX-x64.msu
│   │
│   └───x86
│       └───NEU
│               Windows8.1-KBXXXXXXX-x86.msu
│
├───WindowsServer2003
│   ├───x64
│   │   ├───ENU
│   │   │       WindowsServer2003-KBXXXXXXX-x64-ENU.exe
│   │   │
│   │   └───RUS
│   │           WindowsServer2003-KBXXXXXXX-x64-RUS.exe
│   │
│   └───x86
│       ├───ENU
│       │       WindowsServer2003-KBXXXXXXX-x86-ENU.exe
│       │
│       └───RUS
│               WindowsServer2003-KBXXXXXXX-x86-RUS.exe
│
└───WindowsVista
    ├───x64
    │   └───NEU
    │           Windows6.0-KBXXXXXXX-x64.msu
    │
    └───x86
        └───NEU
                Windows6.0-KBXXXXXXX-x86.msu

###Using batchGenerator(command line UI) or webUi to generate batch that installing updates
* Open cmd.exe, move to Python folder.
* Type and execute ```python batchGenerator.py <Path to file with path list from updates4Target>```
* For running ```webUi.py``` you pass only source data(```<Path to uif file>```, ```<Path to MongoDB server>``` or ```<Path to SQLite file>```) and than open in web browser link [http://127.0.0.1:8080](http://127.0.0.1:8080) (by default configuration) where you can generate your batch file by put required file list from queried section.

##Running tests with [coverage](https://pypi.python.org/pypi/coverage/)
* Open cmd.exe, move to Python folder.
* Adding <Python Path\Scripts> into the path, for example ```set PATH=%PATH%;C:\Python34\Scripts```
* Type and execute ```coverage_run.cmd```
* At Linux (in terminal(console) not at cmd.exe of course) you can set what version (depend of Python version) of coverage do you what to execute, for example:
   * ```bash coverage_run.sh coverage2```
   * ```bash coverage_run.sh coverage3```

=============

   Copyright 2013-2015 https://github.com/TheVice/

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
