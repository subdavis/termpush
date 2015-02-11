# termpush
This is a project started by @subdavis for sending output from a console to the web in real time.  It will generate a link and feed all future output to that link (like pastebin)

###Uses:
```
~$ somecommand | termpush 
```
Watch page update in realtime as your terminal process runs.
```
~$ cat somefile | termpush 
```
Quick and easy way to publish a paste and get a link all in one command

###Planned Features:
* Feed any command line output to a webpage
* Generate a unique link for each feed session, and keep it live until the process ends
* Process event triggers like "process ended" and keyword triggers that the user sets.
* Nofity user via email when these events happen
* Expose API for getting JSON of entire feeds, most recent elements, or span from x to y
* Store all feeds in MongoDB
* Password protect pages.
* Allow users to "rebind" to pages they own and push more output.  
* Allow editing of pages
