import subprocess
import time
import os
import datetime

# Applications desktop open.
subprocess.Popen(["xfce4-terminal", "--tab", "--execute", "bash"])
subprocess.Popen(["/opt/sublime_text/sublime_text"])
subprocess.Popen(["keepassxc"])

time.sleep(2)

log_file = "/tmp/firefox_autostart_test.log"

try:
    urls = [LIST_URLS]

    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now()}] Intentando lanzar Firefox...\n")
        subprocess.Popen(["/usr/bin/firefox", "--new-instance", "--no-remote", "--url"] + urls)
        #subprocess.Popen(["/usr/bin/firefox", "-P", "autostart", "--no-remote","--url"] + urls)

except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now()}] Error: {str(e)}\n")
