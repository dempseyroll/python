import webbrowser
import os
import time

# Applications desktop open.
os.system("open -a Terminal .")
os.system("open /Applications/Sublime\ Text.app")


time.sleep(3)
# Chrome URLs open
c = webbrowser.get('chrome')

c.open('https://google.com/')
time.sleep(2)

os.system("open -na \"Google Chrome\" --args --incognito \"https://chatgpt.com/\"")
os.system("open -na \"Google Chrome\" --args  --incognito \"https://web.whatsapp.com/\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://mail.google.com/\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://www.udemy.com/\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://github.com/login\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://translate.google.com/\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://www.linkedin.com/\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://medium.com/\"")
os.system("open -na \"Google Chrome\" --args --incognito \"https://www.awseducate.com/\"")
