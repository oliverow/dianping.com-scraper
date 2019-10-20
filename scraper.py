from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
import time
import pytesseract


def parseSummary(s):
    result = {}
    prev = ''
    key = ''  # '总评论数'
    num = 0
    readNum = False  # True
    for c in s:
        if readNum:
            if c.isnumeric() or c == '.':
                prev += c
            else:
                result[key] = float(prev)
                prev = c
                readNum = False
            continue
        if len(prev) < 3:
            prev += c
        else:
            prev = prev[1:] + c
        if prev == '人均:' or prev == '口味:' or prev == '环境:' or prev == '服务:':
            key = prev[:-1]
            prev = ''
            readNum = True
    if readNum:
        result[key] = float(prev)

    return result


def parseRatings(s):
    reviews = {}
    comments = {}
    prev = ''
    key = ''
    readNum = False
    for c in s:
        if c == '\n':
            prev = ''
            key = ''
            readNum = False
            continue
        if readNum:
            if c.isnumeric():
                prev += c
            else:
                val = prev
                if '评' in key:
                    reviews[key] = val
                elif '图片' in key:
                    reviews['图片点评'] = val
                else:
                    comments[key] = val
                prev = ''
                readNum = False
            continue
        if c == '(':
            key = prev
            prev = ''
            readNum = True
            continue
        prev += c

    return reviews, comments


def decodePage(driver, writer, shopID, link):
    print(shopID)

    driver.get(link)
    attempt = 3
    while (attempt > 0):
        try:
            popUpClose = driver.find_element_by_class_name('J-bonus-close')
            popUpClose.click()
            attempt = 0
        except:
            print('fail to click, remaining attempts: {}'.format(attempt))
            attempt -= 1
    WebDriverWait(driver, 100)
    driver.save_screenshot("ScreenShot1{}.png".format(shopID))
    driver.execute_script('document.getElementById("comment").scrollIntoView()')
    driver.save_screenshot("ScreenShot2{}.png".format(shopID))

    im = Image.open('ScreenShot1{}.png'.format(shopID))
    x, y = (250, 500)
    cropped_img = im.crop((x, y, x + 850, y + 63))
    cropped_img.save('summary{}.png'.format(shopID))

    im = Image.open('ScreenShot2{}.png'.format(shopID))
    x, y = (0, 0)
    cropped_img = im.crop((x, y, x + 1750, y + 450))
    cropped_img.save('review{}.png'.format(shopID))

    s = pytesseract.image_to_string('summary{}.png'.format(shopID), lang = 'chi_sim')
    s = s.replace(' ', '')
    summary = parseSummary(s)
    summary['店名'] = shopID

    s = pytesseract.image_to_string('review{}.png'.format(shopID), lang = 'chi_sim')
    s = s.replace(' ', '')
    reviews, comments = parseRatings(s)

    result = {**summary, **reviews, '标签': str(comments)}
    writer.writerow(result)

