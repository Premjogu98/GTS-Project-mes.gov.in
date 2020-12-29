from selenium import webdriver
import time
from datetime import datetime
import Global_var
import sys , os
import ctypes
import wx
import string
import re
import html
from insert_on_database import insert_in_Local
app = wx.App()
    
browser = webdriver.Chrome(executable_path=str(f"C:\\Translation EXE\\chromedriver.exe"))
browser.maximize_window()
browser.get('https://mes.gov.in/')
time.sleep(2)

for Search_tender in browser.find_elements_by_xpath('//*[@id="edit-submit-test"]'):
    browser.execute_script("arguments[0].scrollIntoView();", Search_tender)
    Search_tender.click()
    time.sleep(5)
    break
def Scrap_details():
    a = 0
    while a == 0:
        try:
            tr_count = 1
            for table_tr in browser.find_elements_by_xpath('//*[@id="block-system-main"]/div/div/div[2]/div/table/tbody/tr'):
                SegFeild = []
                for data in range(46):
                    SegFeild.append('')
                Start_Date = ''
                for Start_Date in browser.find_elements_by_xpath(f'//*[@id="block-system-main"]/div/div/div[2]/div/table/tbody/tr[{str(tr_count)}]/td[3]'):
                    Start_Date = Start_Date.get_attribute('innerText').strip()
                    # print(Start_Date)
                    SegFeild[44] = Start_Date
                    break
                
                for Title in browser.find_elements_by_xpath(f'//*[@id="block-system-main"]/div/div/div[2]/div/table/tbody/tr[{str(tr_count)}]/td[2]'):
                    Title = Title.get_attribute('innerText').strip()
                    SegFeild[19] = string.capwords(Title).strip()
                    # print(Title)
                    break

                for End_Date in browser.find_elements_by_xpath(f'//*[@id="block-system-main"]/div/div/div[2]/div/table/tbody/tr[{str(tr_count)}]/td[4]'):
                    End_Date = End_Date.get_attribute('innerText').strip()
                    SegFeild[41] = End_Date
                    datetime_object = datetime.strptime(End_Date.strip() , '%d/%m/%Y')
                    SegFeild[24] = datetime_object.strftime("%Y-%m-%d")
                    break

                for Document in browser.find_elements_by_xpath(f'//*[@id="block-system-main"]/div/div/div[2]/div/table/tbody/tr[{str(tr_count)}]/td[5]/a'):
                    Document = Document.get_attribute('href').strip()
                    SegFeild[45] = Document.strip()
                    break
                SegFeild[18] = f'{str(SegFeild[19])}<br>\nStart Date: {str(SegFeild[44])}<br>\nEnd Date: {str(SegFeild[41])}'
                SegFeild[28] = 'https://mes.gov.in/'

                SegFeild[12] = "MILITARY ENGINEER SERVICES"

                # Tender Source
                SegFeild[31] = "mes.gov.in"
                SegFeild[22] = ""  # doc_cost
                SegFeild[26] = ""  # earnest_money
                SegFeild[27] = "0"  # Financiers
                SegFeild[42] = SegFeild[7]
                SegFeild[43] = ""
                SegFeild[14] = "2"  # notice_type
                SegFeild[7] = "IN"
                SegFeild[3] = 'NA~NA~NA~NA~NA'
                SegFeild[8] = 'www.mes.gov.in'
                for SegIndex in range(len(SegFeild)):
                    print(SegIndex, end=' ')
                    SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                    SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''").replace('#39;', '\'')
                    print(SegFeild[SegIndex])
                Check_date(SegFeild)
                Global_var.Total += 1
                print(" Total: " + str(Global_var.Total) + " Duplicate: " + str(Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(Global_var.inserted) + " Skipped: " + str(Global_var.skipped) + " Deadline Not given: " + str(Global_var.deadline_Not_given) + " QC Tenders: "+ str(Global_var.QC_tender),"\n")
                tr_count +=1
                    
            next_apge_url = ''
            for next_page in browser.find_elements_by_xpath('//*[@id="block-system-main"]/div/div/div[3]/ul/li/a'):
                next_page_text = next_page.get_attribute('innerText').strip()
                next_page_href = next_page.get_attribute('href').strip()
                if 'next ›' in next_page_text:
                    next_apge_url = next_page_href

            if next_apge_url == '':
                ctypes.windll.user32.MessageBoxW(0 , "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(Global_var.inserted) + "\n""Skipped: " + str(Global_var.skipped) + "\n""Deadline Not given: " + str(Global_var.deadline_Not_given) + "\n""QC Tenders: "+ str(Global_var.QC_tender) + "" , "mes.gov.in" , 1)
                browser.close()
                sys.exit()
            else:
                browser.get(next_apge_url)
                time.sleep(2)
                
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
            a = 0

def Check_date(SegFeild):
    a = 0
    while a == 0:
        tender_date = str(SegFeild[24])
        nowdate = datetime.now()
        date2 = nowdate.strftime("%Y-%m-%d")
        try:
            if tender_date != '':
                deadline = time.strptime(tender_date , "%Y-%m-%d")
                currentdate = time.strptime(date2 , "%Y-%m-%d")
                if deadline > currentdate:
                    insert_in_Local(SegFeild)
                    a = 1
                else:
                    print("Expired")
                    Global_var.expired += 1
                    a = 1
            else:
                print("Deadline was not given")
                Global_var.deadline_Not_given += 1
                a = 1
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)
            a = 0
Scrap_details()