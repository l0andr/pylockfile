# pylockfile
### Python implementation of Lock (.lock) and PID (.pid) file concepts

A <b>lock file</b> is a file used by various operating systems and programs to lock a resource, such as a file or device. A lock file is just a file, but if it exists, it signals to other processes that the resource is already in use. The <b><i>pylockfile.lockfile.LockFile</i></b> class can create lock files, delete them, and raise exceptions when attempts to lock it again. This class can be used as a Context Manager or Decorator for critical code sections or functions.

A <b>PID file</b> is a similar concept. It is a file that is created when a process starts and deleted when the process finishes. Usually, a PID file contains the process identifier number in its name. The <b><i>pylockfile.pidfile.PidFile</i></b> class can create a PID file when a process starts and delete it when it ends. It can also correctly handle SIGTERM and SIGINT signals and can work as a Context Manager.

Last but not least, the signal_dispatcher module contains the <b><i>pylockfile.signal_dispatcher.SignalDispatcher</i></b> class. This module allows for re-assignment or addition of new handlers for system signals such as SIGTERM or SIGINT. This module is used by other modules in the package, but it can also be used separately if you need to set your own handlers for system signals.
