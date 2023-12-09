import sqlite3


def rowcount():
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bill")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def getcontent(rowid):
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bill WHERE rowid=(?)",rowid)
    a = cursor.fetchone()
    cursor.close()
    conn.close()
    return a[2],a[3],a[4],a[5]

def setcontent(id,d1,d2,d3,d4):
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE bill set CONSIGNEE = ?, DESTINATION = ?, WEIGHT = ?, AMOUNT = ? WHERE SNO = ?",(d1,d2,d3,d4,id))
    conn.commit()
    cursor.close()
    conn.close()

def add_row(sno,date,consignee,destination,weight,amount):
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    t=(sno,date,consignee,destination,weight,amount)
    cursor.execute("INSERT INTO bill VALUES (?,?,?,?,?,?)",t)
    conn.commit()
    conn.close()

   

def allrows():
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bill")
    b= cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return b

def deleterow():
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bill WHERE rowid=(SELECT MAX(rowid) FROM bill);")
    conn.commit()
    cursor.close()
    conn.close()

def totalamount():
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    a=cursor.execute("SELECT SUM(AMOUNT) FROM bill")
    b= a.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return b

def deleteall():
    conn = sqlite3.connect('bills/currentbill.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bill")
    conn.commit()
    cursor.close()
    conn.close()

def getbno():
    conn = sqlite3.connect('bills/billno.db')
    cursor = conn.cursor()
    a = cursor.execute("SELECT bno FROM billno WHERE rowid=1")
    b = a.fetchone()[0]
    cursor.execute("UPDATE billno SET bno=(?) WHERE rowid=1",str(b+1))
    conn.commit()
    cursor.close()
    conn.close()
    return b

def setbno(no):
    conn = sqlite3.connect('bills/billno.db')
    cursor = conn.cursor()
    a = cursor.execute("UPDATE billno SET bno=(?) WHERE rowid=1",str(no))
    conn.commit()
    cursor.close()
    conn.close()

# setbno(1)
def getbnowithoutincrement():
    conn = sqlite3.connect('bills/billno.db')
    cursor = conn.cursor()
    a = cursor.execute("SELECT bno FROM billno WHERE rowid=1")
    b = a.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return b
