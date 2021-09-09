"""
@Author Hinux Chau
"""
#url: https://stuhealth.jnu.edu.cn

import json
import time
from requests import Session
from email.mime.text import MIMEText
import smtplib
import random

import requests


def dbg(n):
    print(n)
    exit(2)


#Log
def log(content,is_error:bool):
    with open("./log.txt","a+") as f:
        if is_error:
            f.writelines("**[{0}] ERROR: {1}\n".format(time.asctime(),content))
        else:
            f.writelines("[{0}] {1}\n".format(time.asctime(),content))

#You can customize this function for your email.
def sendmail(content,mail):
    """
    @param content Content to be sent
    @mail Mail address in "stuinfo"
    """
    with open('./sender_email','r+') as f:
        sender_info=json.load(fp=f)
        msg_from=sender_info["email"]                                 #Mailbox of sender
        passwd=sender_info["code"]                                      #Authentication code
    msg_to=mail                                                    #Mailbox of receiver                        
    subject="From:Hinux's Bot"                                     #Subject          　　                                          
    msg = MIMEText(content)                                        #Use the MIMEText to convert the content into correct form
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        #log("Mail has been sent",False)
        s.quit()
    except Exception as e:
        log(str(e),True)

if __name__ == "__main__":
    postData:dict = {
    "mainTable": {
        "passAreaC2": "",
        "passAreaC3": "",
        "passAreaC4": "",
        "leaveTransportationOther": "",
        "other": "",
        "way2Start": "",
        "language": "",
        "declareTime": "",
        "personNo": "",
        "personName": "",
        "sex": "",
        "professionName": "",
        "collegeName": "",
        "phoneArea": "",
        "phone": "",
        "assistantName": "",
        "assistantNo": "",
        "className": "",
        "linkman": "",
        "linkmanPhoneArea": "",
        "linkmanPhone": "",
        "personHealth": "",
        "temperature": "",
        "personHealth2": "",
        "schoolC1": "",
        "currentArea": "",
        "personC4": "",
        "otherC4": "",
        "isPass14C1": "",
        "isPass14C2": "",
        "isPass14C3": ""
    },
    "secondTable": {
        "other13": "",
        "other1": "",
        "other3": "",
        "other5": "",
        "other4": "",
        "other7": "",
        "other6": "",
        "other9": "",
        "other8": "",
        "other10": "",
        "other11": "",
        "other12": ""
    },
    "jnuid": ""
}
    mail_pot={}
    stu=Session()
    stuinfo={}
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Host':'stuhealth.jnu.edu.cn',
        'Origin':'https://stuhealth.jnu.edu.cn',
        'Referer':'https://stuhealth.jnu.edu.cn/',
        'Content-Type':'application/json'
    }

    try:
        with open("./mails","r+") as mails:
            mail_pot=json.load(mails)
    except Exception as e:
        sendmail("**[{0}] ERROR!!\n{1}".format(time.asctime(),str(e)),"1624339284@qq.com")

    for m in range(0,len(mail_pot[0])):      #m stands for index of each element
        try:
                
            with open("./stuinfo","r+") as f:
                stuinfo=json.load(f)

            login=stu.post(url="https://stuhealth.jnu.edu.cn/api/user/login",json={'username':stuinfo[m]['username'],'password':stuinfo[m]['password']},headers=headers)
            print(f" {stuinfo[m]['username']}:{login.json()['meta']['msg']}  jnuid={login.json()['data']['jnuid']}")
            #continue
            username = stuinfo[m]['username']           #student number
            jnuid = login.json()['data']['jnuid']       #encrypted student number

            #LOOKUP PREVIOUS DATA
            stucheckinUrl = "https://stuhealth.jnu.edu.cn/api/user/stucheckin"
            checkinInfo = stu.post(url=stucheckinUrl,json={'jnuid':jnuid},headers=headers).json()
            if checkinInfo['meta']['msg'] != "获取学生打卡记录成功":
                sendmail(f"URL:{stucheckinUrl},Response:{checkinInfo['meta']}","1624339284@qq.com")
            id = checkinInfo['data']['checkinInfo'][0]['id']
            previousId = checkinInfo['data']['checkinInfo'][1]['id']
            print(f"id:{id},previousId:{previousId}")
            reviewUrl = "https://stuhealth.jnu.edu.cn/api/user/review"
            reviewInfo = stu.post(url = reviewUrl, json={"id":previousId,"jnuid":jnuid},headers=headers).json()
            if "status" in reviewInfo:
                if reviewInfo["status"] != 200:
                    sendmail(reviewInfo,"1624339284@qq.com")
                    continue
            for k in postData:
                for sub in postData[k]:
                    if k != "jnuid":
                        postData[k][sub] = reviewInfo['data'][k][sub]
            postData["jnuid"] = jnuid


            if login.json()['meta']['msg']=='登录成功，今天已填写':
                print(f"{stuinfo[m]['username']}:登陆成功，今天已经填写")
                
                sendmail(f"Hey!User{stuinfo[m]['username']} \n{login.json()}",mail_pot[0][stuinfo[m]['username']])
                #log(login.json()['meta']['msg'],False)

            if login.json()['meta']['msg']=='登录成功，今天未填写':
                #log(login.json()['meta']['msg'],is_error=False)        
                postData["mainTable"]["declareTime"] = "{0}-{1}-{2}".format(
                    str(time.localtime().tm_year).zfill(2),
                    str(time.localtime().tm_mon).zfill(2),
                    str(time.localtime().tm_mday).zfill(2)
                )
                #location
                if postData["mainTable"]["other"]:
                    location = str(postData["mainTable"]["other"]).rsplit(",")
                    random.seed(time.asctime())
                    x = float(location[0])+(random.random()*(-1)**random.randint(a=0,b=99))
                    time.sleep(1)
                    y = float(location[1])+(random.random()*(-1)**random.randint(a=0,b=99))
                    postData["mainTable"]["other"]=f"{x},{y}"
                    #print(postData["mainTable"]["other"])

                    #
                    print(postData)
                    fill=stu.post(url="https://stuhealth.jnu.edu.cn/api/write/main",json=postData,headers=headers)
                    print(fill.json())
                    #print(f"{stuinfo[m]['username']}:{fill.json()['meta']['msg']}")
                    sendmail(f"Good morning!{stuinfo[m]['username']} \n{fill.json()}",mail_pot[0][stuinfo[m]['username']])
                    #log(fill.json()['meta']['msg'],False)
                    time.sleep(random.random()*10)

        except Exception as e:
            #log(str(e),True)
            sendmail("{0}**[{1}] ERROR!!\n{2}".format(stuinfo[m]['username'],time.asctime(),str(e)),"1624339284@qq.com")
            continue
    
    stu.close()
