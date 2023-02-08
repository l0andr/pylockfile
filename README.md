# pylockfile
### Implementation of concepts of .pid and .lock files.

<b>lockfile</b> is just a file that is created in the file system. If there is an attempt to create it again, an exception will be raised. It can be used to 
prevent simultaneous access to one resource from many processes.

<b>pidfile</b> is similar to a lockfile, but it is typically used for one process. It contains the process identification number and logic for handling SIGINT and 
SIGTERM signals.

#### pylockfile contain implementation of both concepts 
