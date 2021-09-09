# a_211_autoCheckIn  
A hand-free solution for automatic check-in on the Stuent Health System  

# Prerequisites  
Python3.x is required to be installed on your device  
If you are willing to create a crontab task (i.e. a periodic schedule) on a Linux server, please run pre-install.sh.  
The default time to check-in is at 11AM.  

# How to use  
Rewrite mails, sender_email and stuinfo with your content in the given form  
**NOTICE**: The "code" in sender_email refers to the POP3 SMTP Code of your email which has enabled such the function.  
This function is provided to achieve sending email automatically, which is highly depended by the code's email sending function.  
If you don't know how to get such the code, please refer to [here](https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256).  
