import pyautogui

pyautogui.click()
for year in range(2000, 2018):
    for type in ["H", "S"]:
        pyautogui.typewrite(type+str(year), interval=0.05)
        pyautogui.press('enter')
