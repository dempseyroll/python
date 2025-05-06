import webbrowser
import subprocess
import time

# Applications desktop open.
subprocess.Popen(["xfce4-terminal", "--tab", "--execute", "bash"])
subprocess.run(["/opt/sublime_text/sublime_text"])

time.sleep(1)
# Chrome URLs open
webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("/usr/bin/firefox"))
c = webbrowser.get('firefox')

urls = [YOUR_URLS_LIST]
first = True

for url in urls:
	if first:
		c.open_new(url)
		first = False
	else:
		c.open_new_tab(url)
