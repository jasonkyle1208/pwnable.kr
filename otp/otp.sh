ulimit -f 0 && python2 -c "import os,signal; signal.signal(signal.SIGXFSZ,signal.SIG_IGN); os.system('./otp 0')"
