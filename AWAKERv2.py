import pyautogui
import keyboard
import numpy as np
import pytesseract
import cv2

from PIL import ImageGrab
import matplotlib.pyplot as plt

import time


print('running')

def getAwakeData(x, y):
  
    # Path of tesseract executable
    pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'
  
    # ImageGrab-To capture the screen image in a loop. 
    # Bbox used to capture a specific area.
    cap = ImageGrab.grab(bbox =(x-25, y-80, x+200, y-20))
    #cap.show()

    cap = np.asarray(cap)
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    # Define range of greens values in HSV
    lower_g = np.array([40, 40, 40])
    upper_g = np.array([70, 255, 255])

    # Create mask
    mask = cv2.inRange(cap_hsv, lower_g, upper_g)
    # Mask image
    cap_masked = cv2.bitwise_and(cap, cap, mask=mask)
    # Convert BGR to RGB
    cap_rgb = cv2.cvtColor(cap_masked, cv2.COLOR_BGR2RGB)
  
    

    # Converted the image to monochrome for it to be easily 
    # read by the OCR and obtained the output String.
    #tesstr = pytesseract.image_to_string(cap, lang ='eng')
    tesstr = pytesseract.image_to_string(cap_rgb, lang ='eng')
    x = tesstr.splitlines()
    res = ""
    for awake_line in x:
        k = awake_line.split('+')
        if len(k) > 1:
            res += k[0] + '|' + k[1] + '|'
    x = res.split('|')
    x = [s.replace("%", "") for s in x]
    for i in range(len(x)):
        if i % 2 == 0:
            x[i] = x[i].replace(' ', '')
        else:
            if x[i] != '':
                try:
                    x[i] = int ( ''.join(filter(str.isdigit, x[i]) ) )
                except ValueError:
                    pass
    x.pop()

    awake_stats = []

    if len(x) == 2:
        awake_stats.append(x[0])
        awake_stats.append(x[1])
    elif len(x) == 4:
        awake_stats.append(x[0])
        item_stat = x[1]
        
        if x[0] == x[2]:
            item_stat += x[3]
        else:
            awake_stats.append(x[1])
            awake_stats.append(x[2])
            item_stat=x[3]
        awake_stats.append(item_stat)

    elif len(x) == 6:


        awake_stats.append(x[0])
        awake_stats.append(x[1])       
        for i in range(2,6,2):

            is_found = False
            for index in range(0, len(awake_stats), 2):
                if x[i] == awake_stats[index]:
                    awake_stats[index+1] += x[i+1]
                    is_found = True
                    break
            if not is_found:
                awake_stats.append(x[i])
                awake_stats.append(x[i+1])

        


    #plt.figure()
    #plt.imshow(cap_rgb) 
    #plt.show()  # display it

    desired_stats = ['STA', 'STR', 'INT', 'DEX', 'PvEDamageIncrease', 'DecreasedCastingTime', 'AttackSpeed',
    'CriticalChance', 'ADOCH', 'IncreasedAttack', 'Max,MP', 'Speed', 'IncreasedHP']

    desiredAwake = [100, 100, 100, 100, 20, 60, 60, 60, 50, 20, 1500, 36, 20]

    print(awake_stats)

    for i in range(0,len(awake_stats),2):

        #find 
        for index in range(len(desired_stats)):
            if awake_stats[i] == desired_stats[index]:
                #print(desired_stats[index], ' +',desiredAwake[index]) 
                if awake_stats[i+1] >= desiredAwake[index]:
                    print('GOODSHIT')
                    return True
    return False
                



def awake():
    is_goodshit = False
    while not is_goodshit:


        if keyboard.is_pressed('ctrl'):  # if key 'q' is pressed 
            print('quit')
            break  # finishing the loop

        x, y = pyautogui.position()

        pyautogui.click(x+36, y, clicks=2)
        #time.sleep(0.1)
        pyautogui.click(x, y)
        #time.sleep(0.1)
        pyautogui.click(x-36, y, clicks=2)
        #time.sleep(0.1)
        pyautogui.click(x, y)
        pyautogui.moveTo(x, y-50, 0.1)
        pyautogui.moveTo(x, y, 0.1)
        time.sleep(0.6)
        is_goodshit = getAwakeData(x, y)
        



def buff():
    print('buffing')
    for x in range(2,10):
        print(x)
        time.sleep(0.3)
        keyboard.press('f'+str(x))
        
def press10():
    x, y = pyautogui.position()
    print('pressing 10x')
    pyautogui.click(x, y, clicks=20)

def deleteItem():
    print("deleting item")
    x, y = pyautogui.position()
    print(x," ", y)
    
    #pyautogui.dragTo(x-300, y, 0.1, button='left')
    pyautogui.mouseDown(button="left");
    pyautogui.moveTo(x-300, y, 0.2, pyautogui.easeInQuad)
    pyautogui.mouseUp(button="left");
    pyautogui.click(916, 549)
    pyautogui.moveTo(x+34, y, 0.1)
    
     


keyboard.on_press_key("z", lambda _:awake())
keyboard.add_hotkey("alt+x", lambda: buff())
keyboard.add_hotkey("`", lambda: press10())
keyboard.add_hotkey("alt", lambda: deleteItem())
keyboard.wait('c')
