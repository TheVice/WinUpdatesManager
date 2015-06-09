WinUpdatesManager
=================

Series of scripts to manage MS DLC from KB913086 and others
* Support to process data through uif(JSON list) files, [MongoDB](https://www.mongodb.org/) or [SQLite](https://sqlite.org/)
* Collect data provided to *uif* (Updates InFormation) files that can be converted to MongoDB or SQLite through accompaniment tools *uif2MongoDB* and *uif2SQLite*
* To work through MongoDB installing of [pymongo](https://pypi.python.org/pypi/pymongo/) required
* For web UI installing of [cherrypy](http://www.cherrypy.org/) required

Sample using
=================

Collect data
------
* Mount ```ISO-9660 DVD5 image``` with [security updates](http://support.microsoft.com/kb/913086/)
* Execute ```python getUif.py <path> <MMYY>```
* List of update description in ```uif``` format (JSON list), so you can save to file, just add to command ```> file.uif```
* To import stored info into MongoDB type and execute ```python uif2MongoDB.py <file.uif>or<folder with *.uif> <database> <table> <address of server, for example mongodb://127.0.0.1:27017/>(optional, if not set using local)```. Names for database and table(collection) can be any, but while query used database ```win32``` and table(collection) ```updates```
* You can also convert data into SQLite database ```python uif2SQLite.py <file.uif>or<folder with *.uif> <path to SQLite file, if not exist it will be created>```. Extension of SQLite file can be any except ```uif```

Query
------
There are two types of query tool: through command line (*updates4Target*) or web (*webUi*)
* Depend of data storage running of ```updates4Target.py``` will be next:
   - ```python updates4Target.py <Path to uif file> or <Path to folder with uif files> <Os name> <Os type> <Os language> <Path to report file>(optional)```
   - ```python updates4Target.py <Path to MongoDB server, for example mongodb://127.0.0.1:27017/> <Os name> <Os type> <Os language> <Path to report file>(optional)```
   - ```python updates4Target.py <Path to SQLite file> <Os name> <Os type> <Os language> <Path to report file>(optional)```
* For running ```webUi.py``` you pass only source data (<Path to uif file>, <Path to folder with uif files>, <Path to MongoDB server> or <Path to SQLite file>) and than go through web browser to http://127.0.0.1:8080 where you can pass your target OS parameters with required report

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
