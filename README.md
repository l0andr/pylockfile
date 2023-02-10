# pylockfile
### Python implementation of Lock (.lock) and PID (.pid) file concepts

A <b>lock file</b> is a file used by various operating systems and programs to lock a resource, such as a file or device. A lock file is just a file, but if it exists, it signals to other processes that the resource is already in use. The <b><i>pylockfile.lockfile.LockFile</i></b> class can create lock files, delete them, and raise exceptions when attempts to lock it again. This class can be used as a Context Manager or Decorator for critical code sections or functions.

A <b>PID file</b> is a similar concept. It is a file that is created when a process starts and deleted when the process finishes. Usually, a PID file contains the process identifier number in its name. The <b><i>pylockfile.pidfile.PidFile</i></b> class can create a PID file when a process starts and delete it when it ends. It can also correctly handle SIGTERM and SIGINT signals and can work as a Context Manager.

Last but not least, the signal_dispatcher module contains the <b><i>pylockfile.signal_dispatcher.SignalDispatcher</i></b> class. This module allows for re-assignment or addition of new handlers for system signals such as SIGTERM or SIGINT. This module is used by other modules in the package, but it can also be used separately if you need to set your own handlers for system signals.

### Features:

* Can <b>LockFile</b> and <b>PidFile</b> can be used as Context Managers 
* Can <b>LockFile</b> and <b>PidFile</b> can be used as Decorators
* Available class <b>SignalPidFile</b>, it is singleton version of <b>PidFile</b>
* Available .lock \\ .pid file deleation by handling of SIGTERM \ SIGINT signals

### Example:

```
    import time
    import os
    from lockfile import LockFile
    from pidfile import SinglePidFile
    from lock_exceptions import AlreadyLocked

    with SinglePidFile(delete_lock_on_sigint=True):
        spf = SinglePidFile()
        while spf.is_locked():
            try:
                with LockFile(lockname="critical_code",delete_lock_on_sigint=True) as lockname:
                    print(f"I, process with PID={os.getpid()}, have caught this very critical resource")
                    # work with some critical resource
                    time.sleep(5)
            except AlreadyLocked:
                print(f"But I, process with PID={os.getpid()},can not caught this very critical resource")

            @LockFile(lockname="critical_function",delete_lock_on_sigint=True)
            def some_critical_function():
                time.sleep(3)
                print(f"Process with PID={os.getpid()},in some critical function")
            try:
                some_critical_function()
            except AlreadyLocked:
                print(f"Process with PID={os.getpid()},awaiting access to some critical function")
```
