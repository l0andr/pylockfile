# pylockfile
### Python implementation of Lock (.lock) and PID (.pid) file concepts

A <b>Lock file</b> is a file used by various operating systems and programs to lock a resource, such as a file or a
device. <b>Lock file</b> it is just a file, but if it exists it's signal to another processes that some resource
already in use.
class <i>pylockfile.lockfile</i>: create lock file, delete them and raise exceptions in attempts to lock it again.
This class can be used as Context Manager or Decorator for some critical code sections or functions

A <b>Pid file</b> is a similar concepts, this is file that created when some process started and deleted when 
this process finished. Usually PID file contains Process Indeficator number in his name.  
class <i>pylockfile.pidfile</i>: can create pid file on start of process and delete on the end, also can correct handle
SIGTERM and SIGINT signals, can work as Context Manager.

#### pylockfile contain implementation of both concepts 
