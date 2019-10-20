from selenium import webdriver
import csv
from scraper import decodePage


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--headless")
    options.binary_location = "/usr/local/bin/chromedriver"
    
    driver = webdriver.Chrome()
    
    outFile = open('data.csv', 'w+')
    header = ['店名', '人均', '口味', '环境', '服务', '网友点评', '图片点评', '好评', '中评', '差评', '标签']
    writer = csv.DictWriter(outFile, delimiter = ',', fieldnames = header)
    writer.writeheader()

    inFile = open('list.txt', 'r')
    for line in inFile:
        name, link = line.replace('\n', '').split(' ')
        decodePage(driver, writer, name, link)

    inFile.close()
    outFile.close()


if __name__ == '__main__':
    main()
