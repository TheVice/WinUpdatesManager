WinUpdatesManager
=================

Series of scripts to manage of MS DLC from KB913086 and others.

Using
=================
1)Mount ISO-9660 DVD5 image with security updates. 
2)Execute 'python main.py E:\ 1013'
Where E:\ mount point (e.g. for Windows case) and 1013 date in MMYY format.
3)List of update description in JSON format you can save to file,
just add to command '> file.json'.
4)After this you can import to data base that support JSON.
For e.g. on MongoDB this do like this 'mongoimport updates.JSON -d win32 -c updates'

=============

   Copyright 2013 https://github.com/TheVice/

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
