'''
        NOTE : there is no 'alt' key or 'Windows' key due to security purposes.
        for example anyone can press alt + f4 and your game will quit...


        -> Make sure you paste the pop-out chat link below
'''

from selenium import webdriver
import time
import os
from getkeys import key_check
from directkeys import PressKey, ReleaseKey, keyList
import sys
import tkinter as tk
from tkinter import messagebox

#Globul
readDelay = 0.2
keyStack = []
MaxKeyDelay = 3
MaxInputKeys = 2
refreshRate = 10000
paused = True
root = 0
chatThread = 0
isExit = False

#Setting up browser
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(os.path.join(os.getcwd(),'chromedriver.exe'),chrome_options=options)

#Removing emojis
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def processKey(messageString,gameloop,delay):
    global keyStack
    requests = messageString.split(',')
    keyDuration = 0
    
    if len(requests) > MaxInputKeys:
        return 0
    
    for request in requests:
        keyData = request.split(' ')
        keyName = keyData[0]
        keyName = keyName.lower()
        
        if len(keyData) > 1:
            if keyData[1].isdigit():
                if int(keyData[1]) <= MaxKeyDelay :
                        keyDuration = gameloop + int(int(keyData[1])/delay)

        if keyName in keyList and len(keyStack) <= 10:
            keyStack.append([keyList[keyName],keyDuration])

def closeBrowser():
    browser.quit()
    quit()

def readChat(link='https://www.youtube.com/live_chat?is_popout=1&v=0Ku4f56pj-U'):
    global readDelay,keyStack,paused,refreshRate,browser,root,isExit

    #Parameters
    msgID = [0]
    actualMsg = "Null"
    gameLoop = 0
    newMsg = []
    newMsgId = 0
    
    #Loading the page
    browser.get(link)
    
    print("\n\n[!] Script is Paused By Default\n- To Resume the script Press '1','2' and '3' at the same time\n- To Quit Press '4','5','6' at the same time\n")
    print(">> Script Paused <<")

    #Main Loop
    while True:
        gameLoop += 1

        if not paused:
            #Extracting Latest chat message
            try:
                msgs = browser.find_elements_by_css_selector('yt-live-chat-text-message-renderer')
                newMsg = msgs[len(msgs)-1]
                actualMsg = deEmojify(newMsg.find_element_by_id('message').text)
                newMsgId = newMsg.id
            except :
                pass

            print(actualMsg)

            #Differentiating new message
            if newMsgId != msgID[len(msgID)-1]:
                msgID.append(newMsgId)

                #Processing The Keys
                processKey(actualMsg,gameLoop,readDelay)

            #Processing the Key Stack
            for index,keyData in enumerate(keyStack):
                if keyData[1] >= gameLoop:
                    PressKey(keyData[0])
                else:
                    PressKey(keyData[0])
                    ReleaseKey(keyData[0])
                    keyStack.remove(keyData)
        
            #For Popular live-streamers :P
            time.sleep(readDelay)

        else:
            time.sleep(readDelay)

        #Pausing The Loop
        #To pause the script press 1,2,3,4 all together
        keys = key_check()
        if '1' in keys and '2' in keys and '3' in keys:
            paused = not paused
            if paused:
                print(">> Script Paused <<")
            if not paused:
                print(">> Script Unpaused <<")
        elif '4' in keys and '5' in keys and '6' in keys:
            isExit = True

        #Saving From overflow
        if len(msgID) % refreshRate == 0:
            msgID = [0]
            browser.get(link)
            print("--------------- Refreshed --------------")

        if isExit:
            closeBrowser()
            break

def checkLink(link):
    browser.get(link)

def startRead(linkEntry):
    global root
    link = linkEntry.get()
    #Link checking.. Important
    try:
        checkLink(link)
    except:
        messagebox.showerror("Invalid Link","Entered Link is invalid or doesn't exists. Please paste the full link including 'http' or 'https'")
        return
    root.destroy()

    noticeRoot = tk.Tk()
    noticeRoot.title("Note")
    noticeRoot.iconbitmap(os.path.join(os.getcwd(),'tubeplayLogo.ico'))
    noticeRoot.resizable(0,0)

    def final():
        noticeRoot.destroy()
        readChat(link=link)

    label = tk.Label(noticeRoot,text="[!] Script is paused by default.\n- To unpause/pause the script, press '1','2' and '3' at the same time\n- To Quit Press '4','5','6' at the same time.").pack()
    okbutton = tk.Button(noticeRoot,text="Ok",command=final).pack(fill=tk.X,padx=5,pady=5)

    noticeRoot.mainloop()

def main():
    global root
    root = tk.Tk()
    root.iconbitmap(os.path.join(os.getcwd(),'tubeplayLogo.ico'))
    root.focus_force()

    #Configuring Window GUI
    root.title("Tube Play")
    root.geometry("600x80")
    root.resizable(0,0)
    
    root.columnconfigure(0,weight=1)
    root.columnconfigure(1,weight=2)
    root.columnconfigure(2,weight=2)
    root.columnconfigure(3,weight=2)

    #Building GUI
        #Link
    linkLabel = tk.Label(root,text="Pop-out Chat Link : ")
    linkLabel.grid(row=0,column=0)
    
    linkEntry = tk.Entry(root)
    linkEntry.insert(tk.END,'https://www.youtube.com/live_chat?is_popout=1&v=0Ku4f56pj-U')
    linkEntry.grid(row=0,column=1,columnspan=3,padx=5,pady=5,sticky="news")
    
    startReadingButton = tk.Button(root,text="Start Reading",command=lambda:startRead(linkEntry))
    startReadingButton.grid(row=1,column=1,padx=5,pady=5,sticky="nwes")

    root.mainloop()

if __name__ == "__main__":
    main()