from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import datetime
import database


date=datetime.date.today().strftime("%d/%m/%Y")
month=datetime.date.today().strftime("%B")

def generatepdf(billno):

    data = getdata(billno)

    # Define the styles for the table
    style = TableStyle([('SPAN', (0, 1), (1, 1)),
                        ('OUTLINE', (0, 0), (-1, -1), 1, colors.black),
                        ('ALIGN', (0, 4), (-1, -1), 'CENTER'),                   
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                        ('GRID', (0, 4), (-1, -4), 1, colors.black),
                        ('GRID', (-1, -3), (-1, -3), 1, colors.black)])

    # Create the table and add the data and styles
    table = Table(data,colWidths=[50,70,220,70])
    table.setStyle(style)

    # Create the PDF document and add the table
    doc = SimpleDocTemplate("bills/Bill_No_"+billno+".pdf", pagesize=letter, leftMargin=100, rightMargin=100, topMargin=10, bottomMargin=20)

    doc.build([table])


def getdata(billno): 
    res=list()
    res.append([None]*6)
    res.append([Paragraph(f"Bill No. : <font color='red'>{billno.zfill(3)}</font>",ParagraphStyle(
    name='HelveticaBold12',
    fontName='Helvetica',
    fontSize=12,
    wordWrap=False,
    width=200
)),None,None,None,"Date : "+date])
    res.append([None,None,None,None,"Billing Month : "+month])
    res.append(["To, _____________________________________________________________________________",None,None,None,None,None])
    res.append(["S.No.","Date","Consignee","Dest.","Weight","Amount"])
    li=list()
    total=0


    for entry in database.allrows():
        li=list()
        li.append(entry[0])
        li.append(entry[1])
        li.append(entry[2])
        li.append(entry[3])
        li.append(entry[4])
        if entry[5]=="":
            li.append(0)
        else:
            li.append(entry[5])
        
        res.append(li)
        total+=li[-1]

    if len(res)<=30:
        res.extend([[None]*6]*(33-len(res)))
    else:
        res.extend([[None]*6]*3)
    res[-3]=[None,None,None,None,"TOTAL",total]
    res[-1]=[None,"Seal & Signature",None,None,None,None]
    return res
















