from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).parent
FONT_PATH = ROOT / ".fonts" / "NotoSansThai-Regular.ttf"
OUTPUT_PATH = ROOT / "main_summary_th.pdf"


def build_pdf():
    pdfmetrics.registerFont(TTFont("NotoThai", str(FONT_PATH)))
    document = SimpleDocTemplate(
        str(OUTPUT_PATH), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="สรุปการทำงานของ main.py", author="To-Do List Project",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ThaiTitle", parent=styles["Title"], fontName="NotoThai", fontSize=22, leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#17324D"), spaceAfter=8 * mm))
    styles.add(ParagraphStyle(name="ThaiHeading", parent=styles["Heading2"], fontName="NotoThai", fontSize=15, leading=21, textColor=colors.HexColor("#176B87"), spaceBefore=5 * mm, spaceAfter=2 * mm))
    styles.add(ParagraphStyle(name="ThaiBody", parent=styles["BodyText"], fontName="NotoThai", fontSize=10.5, leading=17, alignment=TA_LEFT, spaceAfter=2.5 * mm))
    styles.add(ParagraphStyle(name="ThaiSmall", parent=styles["BodyText"], fontName="NotoThai", fontSize=9, leading=14, textColor=colors.HexColor("#4A5568")))
    styles.add(ParagraphStyle(name="ThaiCode", parent=styles["Code"], fontName="NotoThai", fontSize=8.2, leading=11, leftIndent=4 * mm, rightIndent=4 * mm, textColor=colors.HexColor("#203040"), backColor=colors.HexColor("#F1F5F7"), borderPadding=3 * mm))
    styles.add(ParagraphStyle(name="ThaiTable", parent=styles["BodyText"], fontName="NotoThai", fontSize=9, leading=13))

    story = []
    story.append(Paragraph("สรุปการทำงานของคำสั่งใน main.py", styles["ThaiTitle"]))
    story.append(Paragraph("เอกสารนี้อธิบายโปรแกรม To-Do List ที่ทำงานผ่านเมนูในเทอร์มินัล เขียนด้วยภาษา Python และบันทึกรายการงานไว้ในไฟล์ tasks.json", styles["ThaiBody"]))
    story.append(Paragraph("1. ภาพรวมการทำงาน", styles["ThaiHeading"]))
    story.append(Paragraph("เมื่อเริ่มโปรแกรม ฟังก์ชัน main() จะอ่านรายการงานจาก tasks.json เริ่มเธรดตรวจสอบการแจ้งเตือน และแสดงเมนูวนซ้ำจนกว่าผู้ใช้จะเลือก Exit ผู้ใช้สามารถเพิ่ม แสดง ทำเสร็จ หรือลบงานได้ โดยการเปลี่ยนแปลงจะถูกบันทึกกลับลงไฟล์", styles["ThaiBody"]))
    story.append(Paragraph("ลำดับการทำงานหลัก", styles["ThaiHeading"]))
    story.append(Preformatted("เริ่มโปรแกรม\n  -> load_task() อ่าน tasks.json\n  -> เริ่ม reminder_loop() ในเธรดเบื้องหลัง\n  -> แสดงเมนูและรับ choice\n  -> ทำงานตามตัวเลือก 1-5\n  -> วนกลับไปแสดงเมนู หรือจบเมื่อเลือก 5", styles["ThaiCode"]))

    story.append(Paragraph("2. ไลบรารีและตัวแปรสำคัญ", styles["ThaiHeading"]))
    rows = [[Paragraph("ส่วนประกอบ", styles["ThaiTable"]), Paragraph("หน้าที่", styles["ThaiTable"])],
            [Paragraph("json", styles["ThaiTable"]), Paragraph("อ่านและเขียนข้อมูลรายการงานในรูปแบบ JSON", styles["ThaiTable"])],
            [Paragraph("time", styles["ThaiTable"]), Paragraph("หยุดการทำงานของเธรด 1 วินาทีระหว่างตรวจเตือน", styles["ThaiTable"])],
            [Paragraph("datetime", styles["ThaiTable"]), Paragraph("ตรวจสอบรูปแบบวันเวลาและเปรียบเทียบเวลาปัจจุบัน", styles["ThaiTable"])],
            [Paragraph("threading", styles["ThaiTable"]), Paragraph("สร้างเธรดตรวจแจ้งเตือนแยกจากเมนูหลัก", styles["ThaiTable"])],
            [Paragraph("ZoneInfo", styles["ThaiTable"]), Paragraph("กำหนดเขตเวลา Asia/Bangkok", styles["ThaiTable"])],
            [Paragraph("TASK_FILE", styles["ThaiTable"]), Paragraph("เก็บชื่อไฟล์ข้อมูล คือ tasks.json", styles["ThaiTable"])],
            [Paragraph("tasks", styles["ThaiTable"]), Paragraph("ลิสต์ที่เก็บรายการงานทั้งหมดในหน่วยความจำ", styles["ThaiTable"])],
            [Paragraph("tasks_lock", styles["ThaiTable"]), Paragraph("ล็อกเพื่อป้องกันการอ่านหรือเขียน tasks พร้อมกันจากหลายเธรด", styles["ThaiTable"])]]
    table = Table(rows, colWidths=[47 * mm, 117 * mm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#176B87")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C7D1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F7F8")]), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(table)

    story.append(Paragraph("3. อธิบายฟังก์ชัน", styles["ThaiHeading"]))
    functions = [("reminder_loop()", "วนทำงานตลอดเวลา เรียก check_reminders() แล้วหยุด 1 วินาทีด้วย time.sleep(1) ฟังก์ชันนี้ทำงานในเธรด daemon จึงไม่ขวางการปิดโปรแกรมเมื่อ main thread จบ"), ("check_reminders()", "อ่านเวลาปัจจุบันตามเขตเวลา Bangkok แล้วตรวจงานทีละรายการ โดยข้ามงานที่ reminded หรือ complete เป็น True จากนั้นแปลง date และ time เป็น datetime หากถึงกำหนดจะแสดงข้อความเตือน ตั้ง reminded เป็น True และบันทึกข้อมูล"), ("load_task()", "เปิด tasks.json แล้วใช้ json.load() แปลงข้อมูล JSON เป็นลิสต์ Python จากนั้นส่งค่ากลับให้ main()"), ("save_task()", "ล็อก tasks_lock เปิด tasks.json ในโหมดเขียน และใช้ json.dump() บันทึกลิสต์ tasks ด้วย indent=4 ให้อ่านง่าย"), ("get_task_number(prompt)", "รับหมายเลขงานจากผู้ใช้ แปลงเป็นจำนวนเต็ม ตรวจว่าหมายเลขอยู่ในช่วง 1 ถึงจำนวนงาน แล้วคืนค่าเป็นดัชนีแบบเริ่มที่ 0 หากข้อมูลไม่ถูกต้องจะพิมพ์ข้อความแจ้งและคืน None"), ("main()", "เป็นศูนย์กลางของโปรแกรม โหลดข้อมูล เริ่มเธรดแจ้งเตือน แสดงเมนู และจัดการคำสั่งของผู้ใช้จนกว่าจะเลือก 5")]
    for name, description in functions:
        story.append(Paragraph(f"<b>{escape(name)}</b> — {escape(description)}", styles["ThaiBody"]))

    story.append(PageBreak())
    story.append(Paragraph("4. รายละเอียดเมนูใน main()", styles["ThaiHeading"]))
    menu_rows = [[Paragraph("ตัวเลือก", styles["ThaiTable"]), Paragraph("การทำงาน", styles["ThaiTable"])],
                 [Paragraph("1. Add Tasks", styles["ThaiTable"]), Paragraph("รับชื่อ รายละเอียด วันที่ และเวลา ตรวจรูปแบบด้วย %Y-%m-%d %H:%M แล้วเพิ่มดิกชันนารีงานใหม่ลงใน tasks โดยเริ่ม complete และ reminded เป็น False", styles["ThaiTable"])],
                 [Paragraph("2. Show Tasks", styles["ThaiTable"]), Paragraph("วนแสดงทุกงานพร้อมหมายเลข สถานะ เครื่องหมาย ✓ เมื่อทำเสร็จ ชื่องาน วันที่ และเวลา", styles["ThaiTable"])],
                 [Paragraph("3. Complete Tasks", styles["ThaiTable"]), Paragraph("เรียก get_task_number() รับหมายเลขงาน ตั้งค่า complete เป็น True แล้วบันทึกไฟล์", styles["ThaiTable"])],
                 [Paragraph("4. Delete Tasks", styles["ThaiTable"]), Paragraph("เรียก get_task_number() รับหมายเลขงาน ลบด้วย tasks.pop(index) แล้วบันทึกไฟล์", styles["ThaiTable"])],
                 [Paragraph("5. Exit", styles["ThaiTable"]), Paragraph("ออกจาก while loop ทำให้ main() จบการทำงาน ส่วน reminder thread เป็น daemon จึงหยุดตามโปรแกรม", styles["ThaiTable"])]]
    menu_table = Table(menu_rows, colWidths=[43 * mm, 121 * mm], repeatRows=1)
    menu_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#176B87")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C7D1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F7F8")]), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(menu_table)

    story.append(Paragraph("5. โครงสร้างข้อมูลใน tasks.json", styles["ThaiHeading"]))
    story.append(Paragraph("แต่ละงานเป็นออบเจ็กต์ที่มีคีย์ title, des, date, time, complete และ reminded ตัวอย่างโครงสร้างที่โปรแกรมสร้างเมื่อเพิ่มงานคือ:", styles["ThaiBody"]))
    story.append(Preformatted('{\n    "title": "อ่านหนังสือ",\n    "des": "บทที่ 1",\n    "date": "2026-09-23",\n    "time": "18:30",\n    "complete": false,\n    "reminded": false\n}', styles["ThaiCode"]))

    story.append(Paragraph("6. ระบบแจ้งเตือนและการทำงานหลายเธรด", styles["ThaiHeading"]))
    story.append(Paragraph("main() สร้างเธรดด้วย threading.Thread(target=reminder_loop, daemon=True) แล้วเริ่มด้วย start() ทำให้ระบบแจ้งเตือนตรวจงานได้ทุก 1 วินาทีขณะที่ผู้ใช้ยังเลือกเมนูได้ตามปกติ ก่อนเข้าถึง tasks ใน check_reminders() และ save_task() โปรแกรมใช้ with tasks_lock เพื่อป้องกันข้อมูลชนกันระหว่างเธรด", styles["ThaiBody"]))
    story.append(Paragraph("7. การตรวจสอบข้อผิดพลาด", styles["ThaiHeading"]))
    story.append(Paragraph("การเพิ่มงานตรวจวันเวลาและปฏิเสธค่าที่ไม่ตรงรูปแบบ หากกรอกหมายเลขงานไม่ใช่ตัวเลขหรืออยู่นอกช่วงจะไม่แก้ไขข้อมูล ส่วน check_reminders() จัดการ KeyError, TypeError และ ValueError โดยพิมพ์ข้อความ Invalid date/time แล้วข้ามงานนั้น", styles["ThaiBody"]))
    story.append(Paragraph("8. ข้อสังเกตจากโค้ดปัจจุบัน", styles["ThaiHeading"]))
    story.append(Paragraph("• ฟังก์ชัน save_task() ใช้ไฟล์ชื่อ tasks.json แบบ relative path ดังนั้นควรรันโปรแกรมจากโฟลเดอร์โปรเจกต์<br/>• โปรแกรมไม่ได้ตรวจโครงสร้าง JSON ตอน load_task() หากไฟล์เสียหายอาจเกิดข้อผิดพลาดก่อนแสดงเมนู<br/>• ช่อง des ถูกบันทึกและรับค่า แต่เมนู Show Tasks ยังไม่ได้แสดงรายละเอียดนี้<br/>• เมื่อแจ้งเตือนแล้วจะตั้ง reminded เป็น True เพื่อไม่ให้เตือนซ้ำ แม้ผู้ใช้ยังไม่ได้ทำงานเสร็จ", styles["ThaiBody"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("สรุป: main.py เป็นโปรแกรมจัดการงานแบบโต้ตอบที่ใช้ JSON เป็นที่เก็บข้อมูล และใช้เธรดเบื้องหลังสำหรับแจ้งเตือนตามกำหนดเวลา", styles["ThaiSmall"]))
    document.build(story)
    print(f"Created {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()