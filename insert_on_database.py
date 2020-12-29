from datetime import datetime
import Global_var
import time
import mysql.connector
import sys, os


def DB_connection():
    a = 0
    while a == 0:
        try:
            mydb_Local = mysql.connector.connect(host='185.142.34.92' ,user='ams' ,passwd='TgdRKAGedt%h' ,database='tenders_db' ,charset='utf8')
            a = 1
            return mydb_Local
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


# def L2L_connection():
#     a3 = 0
#     while a3 == 0:
#         try:
#             mydb_L2L = mysql.connector.connect(
#                 host='192.168.0.202' ,
#                 user='ams' ,
#                 passwd='amsbind' ,
#                 database='AMS_Master_FinalDB' ,
#                 charset='utf8')
#             print('SQL Connected L2L_connection')
#             print("Live Tender")
#             a3 = 1
#             return mydb_L2L
#         except mysql.connector.ProgrammingError as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
#                   "\n", exc_tb.tb_lineno)
#             a3 = 0
#             time.sleep(10)
            
def Error_fun(Error,Function_name,SegFeild):
    mydb = DB_connection()
    mycursor = mydb.cursor()
    sql1 = "INSERT INTO errorlog_tbl(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error).replace("'","''") + "','" + str(Function_name).replace("'","''")+ "','"+str(SegFeild[31])+"')"
    mycursor.execute(sql1)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return sql1

def check_Duplication(SegFeild):
    mydb_Local = DB_connection()
    mycursorLocal = mydb_Local.cursor()
    a1 = 0
    while a1 == 0:
        try:
            if SegFeild[13] != '' and SegFeild[24] != '' and SegFeild[7] != '':
                commandText = "SELECT Posting_Id from india_tenders_tbl where tender_notice_no = '" + str(SegFeild[13]) + "' and Country = '" + str(SegFeild[7]) + "' and doc_last= '" + str(SegFeild[24]) + "'"
            elif SegFeild[13] != "" and SegFeild[7] != "":
                commandText = "SELECT Posting_Id from india_tenders_tbl where tender_notice_no = '" + str(SegFeild[13]) + "' and Country = '" + str(SegFeild[7]) + "'"
            elif SegFeild[19] != "" and SegFeild[24] != "" and SegFeild[7] != "":
                commandText = "SELECT Posting_Id from india_tenders_tbl where short_desc = '" + str(SegFeild[19]) + "' and doc_last = '" + SegFeild[24] + "' and Country = '" + SegFeild[7] + "'"
            else:
                commandText = "SELECT Posting_Id from india_tenders_tbl where short_desc = '" + str(SegFeild[19]) + "' and Country = '" + str(SegFeild[7]) + "'"
            mycursorLocal.execute(commandText)
            results = mycursorLocal.fetchall()
            a1 = 1
            print("Code Reached On check_Duplication")
            return results
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Error_fun(Error,Function_name,SegFeild)
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
            a1 = 0
            time.sleep(10)


def insert_in_Local(SegFeild):
    results = check_Duplication(SegFeild)
    if len(results) > 0:
        print('Duplicate Tender')
        Global_var.duplicate += 1
        return 1
    else:
        Fileid = create_filename(SegFeild)
        HtmlDaoc_fileid = Fileid
        Current_dateTime = datetime.now().strftime("%Y-%m-%d")
        mydb_Local = DB_connection()
        mycursorLocal = mydb_Local.cursor()
        MyLoop = 0
        while MyLoop == 0:
            sql = "INSERT INTO india_tenders_tbl(Tender_ID,EMail,add1,add2,City,State,PinCode,Country,URL,Tel,Fax,Contact_Person,Maj_Org,tender_notice_no,notice_type,ind_classification,global,MFA,tenders_details,short_desc,est_cost,currency,doc_cost,doc_start,doc_last,open_date,earnest_money,Financier,tender_doc_file,Sector,corregendum,source,entry_date,cpv)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (str(HtmlDaoc_fileid),SegFeild[1],SegFeild[2],SegFeild[3],SegFeild[4],SegFeild[5],SegFeild[6],SegFeild[7],SegFeild[8],SegFeild[9],SegFeild[10],SegFeild[11],SegFeild[12],SegFeild[13],SegFeild[14],SegFeild[15],SegFeild[16],SegFeild[17],SegFeild[18],SegFeild[19],SegFeild[20],SegFeild[21],SegFeild[22],SegFeild[23],SegFeild[24],SegFeild[25],SegFeild[26],SegFeild[27],SegFeild[28],SegFeild[29],SegFeild[30],SegFeild[31],str(Current_dateTime),SegFeild[36])
            try:
                mycursorLocal.execute(sql, val)
                mydb_Local.commit()
                Global_var.inserted += 1
                print("Code Reached On insert_in_Local")
                MyLoop = 1
            except Exception as e:
                Function_name: str = sys._getframe().f_code.co_name
                Error: str = str(e)
                Error_fun(Error,Function_name,SegFeild)
                exc_type , exc_obj , exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
                MyLoop = 0
                time.sleep(10)
    insert_L2L(SegFeild, Fileid)


def create_filename(SegFeild):
    basename = "PY219"
    Current_dateTime = datetime.now().strftime("%Y%m%d%H%M%S%f")
    Fileid = "".join([basename, Current_dateTime])
    a = 0
    while a == 0:
        try:
            tag = ''
            if str(SegFeild[45]) == '':
                tag = "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Document </td><td style=\"padding:7px;\"></td></tr>"
            else:
                tag = "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Document </td><td style=\"padding:7px;\"><a href="+str(str(SegFeild[45]))+" target=\"_blank\">View</a></td></tr>"
               
            Html_wala_Tag = "<table align=\"center\" border=\"1\" style=\"width:98%;border-spacing:0;border-collapse: collapse;border:1px solid #666666; margin-top:5px; margin-bottom:5px;\">" + \
                            "<tr><td colspan=\"2\"; style=\"background-color:#146faf; font-weight: bold; padding:7px;border-bottom:1px solid #666666; color:white;\">Tender Details</td></tr>" + \
                            "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Title Number</td><td style=\"padding:7px;\">" + str(SegFeild[19]) + "</td></tr>" + \
                            "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Start Date</td><td style=\"padding:7px;\">" + str(SegFeild[44]) + "</td></tr>" + \
                            "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">End Date</td><td style=\"padding:7px;\">" + str(SegFeild[41]) + "</td></tr>" + \
                            ""+str(tag)+"" + "</tr></table>"
            HTML_File_String = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\">" + \
                               "<head><meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\" /><title>Tender Document</title></head>" + \
                               "<body>" + Html_wala_Tag + "</body></html>"
            File_path = 'Z:\\' + Fileid + '.html'
            file1 = open(File_path, "w", encoding='utf-8')
            file1.write(str(HTML_File_String))
            file1.close()
            time.sleep(2)
            SegFeild[44] = ''
            SegFeild[41] = ''
            SegFeild[45] = ''
            a = 1
            return Fileid
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Error_fun(Error,Function_name,SegFeild)
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def insert_L2L(SegFeild, Fileid):
    ncb_icb = "ncb"
    added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_id = "1"
    cpv_userid = ""
    dms_entrynotice_tblquality_status = '1'
    quality_id = '1'
    quality_addeddate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Col1 = 'https://mes.gov.in/'
    Col2 = '' 
    Col3 = ''
    Col4 = ''
    Col5 = SegFeild[3]
    file_name = "D:\\Tide\\DocData\\" + Fileid + ".html"
    dms_downloadfiles_tbluser_id = 'DWN00541021'
    # Europe-DWN2554488,India-DWN00541021,Asia-DWN5046627,Africa-DWN302520,North America-DWN1011566,
    # South America-DWN1456891,Semi-Auto-DWN30531073,MFA-DWN0654200
    selector_id = ''
    is_english = '0'
    select_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if SegFeild[36] == "":
        dms_entrynotice_tblstatus = "1"
        dms_downloadfiles_tblsave_status = '1'
        dms_downloadfiles_tblstatus = '1'
        dms_entrynotice_tbl_cqc_status = '1'
    else:
        dms_entrynotice_tblstatus = "2"
        dms_downloadfiles_tblsave_status = '2'
        dms_downloadfiles_tblstatus = '1'
        dms_entrynotice_tbl_cqc_status = '2'
    dms_downloadfiles_tbldatatype = "A"
    dms_entrynotice_tblnotice_type = '2'
    file_id = Fileid
    mydb_L2L = DB_connection()
    mycursorL2L = mydb_L2L.cursor()
    if SegFeild[12] != "" and SegFeild[19] != "" and SegFeild[24] != "" and SegFeild[7] != "" and SegFeild[2] != "":
        dms_entrynotice_tblcompulsary_qc = "2"
    else:
        dms_entrynotice_tblcompulsary_qc = "1"
        Global_var.QC_tender += 1
        sql = "INSERT INTO qctenders_tbl (Source,tender_notice_no,short_desc,doc_last,Maj_Org,Address,doc_path,Country)VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
        val = (str(SegFeild[31]), str(SegFeild[13]), str(SegFeild[19]), str(SegFeild[24]), str(SegFeild[12]), str(SegFeild[2]),"http://tottestupload3.s3.amazonaws.com/" + file_id + ".html", str(SegFeild[7]))
        a4 = 0
        while a4 == 0:
            try:
                mycursorL2L.execute(sql, val)
                mydb_L2L.commit()
                a4 = 1
                print("Code Reached On QCTenders")
            except Exception as e:
                Function_name: str = sys._getframe().f_code.co_name
                Error: str = str(e)
                Error_fun(Error,Function_name,SegFeild)
                exc_type , exc_obj , exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
                a4 = 0
                time.sleep(10)
    sql = "INSERT INTO l2l_tenders_tbl(notice_no,file_id,purchaser_name,deadline,country,description,purchaser_address,purchaser_email,purchaser_url,purchaser_emd,purchaser_value,financier,deadline_two,tender_details,ncbicb,status,added_on,search_id,cpv_value,cpv_userid,quality_status,quality_id,quality_addeddate,source,tender_doc_file,Col1,Col2,Col3,Col4,Col5,file_name,user_id,status_download_id,save_status,selector_id,select_date,datatype,compulsary_qc,notice_type,cqc_status,DocCost,DocLastDate,is_english,currency,sector,project_location,set_aside)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(SegFeild[13]) , file_id , str(SegFeild[12]) , str(SegFeild[24]) , str(SegFeild[7]) , str(SegFeild[19]) ,str(SegFeild[2]) ,str(SegFeild[1]) , str(SegFeild[8]) , str(SegFeild[26]) , str(SegFeild[20]) , str(SegFeild[27]) ,str(SegFeild[24]) , str(SegFeild[18]) , ncb_icb , dms_entrynotice_tblstatus , str(added_on) , search_id ,str(SegFeild[36]) ,cpv_userid , dms_entrynotice_tblquality_status , quality_id , str(quality_addeddate) , str(SegFeild[31]) ,str(SegFeild[28]) ,Col1 , Col2 , Col3 , Col4 , Col5 ,file_name , dms_downloadfiles_tbluser_id , dms_downloadfiles_tblstatus , dms_downloadfiles_tblsave_status ,selector_id , str(select_date) , dms_downloadfiles_tbldatatype ,dms_entrynotice_tblcompulsary_qc , dms_entrynotice_tblnotice_type , dms_entrynotice_tbl_cqc_status ,str(SegFeild[22]) , str(SegFeild[41]),is_english, str(SegFeild[21]),SegFeild[29],SegFeild[42],SegFeild[43])
    a5 = 0
    while a5 == 0:
        try:
            mycursorL2L.execute(sql, val)
            mydb_L2L.commit()
            print("Code Reached On insert_L2L")
            a5 = 1
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Error_fun(Error,Function_name,SegFeild)
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)
            a5 = 0
            time.sleep(10)