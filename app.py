from tkinter import Tk, messagebox, ttk, IntVar, scrolledtext
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText


def send_mail(mydict: dict):
    """sends mail with info from dict data"""
    if mydict['ssl']:
        print('ssl on')
        server = SMTP_SSL(mydict['host'], mydict['port'])  # Port -> int
    else:
        print('ssl off')
        server = SMTP(mydict['host'], mydict['port'])
    
    server.login(mydict['id'], mydict['pw'])  # Strings

    msg = MIMEText(mydict['content'], _charset='euc-kr')
    msg['Subject'] = mydict['subject']
    msg['From'] = mydict['from']
    msg['To'] = mydict['to']

    server.sendmail(mydict['from'], mydict['to'], msg.as_string())
    server.quit()
    
    return

def send_button(host, port, ssl, id_, pw, from_, to, subject, content):
    """packs data from entry, multi-Recipients not supported yet"""
    mydict = {
        'host': host,
        'port': int(port),
        'ssl': ssl,
        'id': id_,
        'pw': pw,
        'from': from_,
        'to': to,
        'subject': subject,
        'content': content
    }
    try:
        send_mail(mydict)
    except Exception as e:
        print(e)
        messagebox.showerror('Return Msg', e)
        return
    
    messagebox.showinfo('메일 전송완료', f'다음 수신자에게 메일이 발송되었습니다:\n{mydict["to"]}')

    return

if __name__=='__main__':
    root = Tk()
    root.title('메일 발송')

    # SMTP 설정 프레임
    frame_server = ttk.LabelFrame(root, text='SMTP 설정')
    frame_server.pack(fill='x', padx=10, pady=5, ipadx=2, ipady=2)
    
    label_host = ttk.Label(frame_server, text='보내는 서버:')
    label_host.grid(column=0, row=0, padx=5, pady=5, rowspan=2)
    entry_host = ttk.Entry(frame_server, width=20)
    entry_host.grid(column=1, row=0, rowspan=2)

    label_port = ttk.Label(frame_server, text='포트:')
    label_port.grid(column=2, row=0, padx=5, rowspan=2)
    entry_port = ttk.Entry(frame_server, width=6)
    entry_port.grid(column=3, row=0, rowspan=2)
    entry_port.insert('end', '465')

    var_ssl = IntVar()
    var_ssl.set(1)
    checkbox_ssl = ttk.Checkbutton(frame_server, text='SSL', variable=var_ssl)
    checkbox_ssl.grid(column=4, row=0, padx=5, rowspan=2)

    label_id = ttk.Label(frame_server, text='ID:')
    label_id.grid(column=5, row=0, pady=2)
    entry_id = ttk.Entry(frame_server, width=25)
    entry_id.grid(column=6, row=0, pady=2)
    label_pw = ttk.Label(frame_server, text='PW:')
    label_pw.grid(column=5, row=1, pady=2)
    entry_pw = ttk.Entry(frame_server, width=25)
    entry_pw.grid(column=6, row=1, pady=2)

    # 헤더 프레임
    frame_header = ttk.LabelFrame(root, text='헤더')
    frame_header.pack(fill='x', padx=10, pady=5, ipadx=2, ipady=2)

    label_sender = ttk.Label(frame_header, text='발신자:')
    label_sender.grid(column=0, row=0, padx=5, pady=3)
    entry_sender = ttk.Entry(frame_header, width=70)
    entry_sender.grid(column=1, row=0, padx=5, pady=3)

    label_receiver = ttk.Label(frame_header, text='수신자:')
    label_receiver.grid(column=0, row=1, padx=5, pady=3)
    entry_receiver = ttk.Entry(frame_header, width=70)
    entry_receiver.grid(column=1, row=1, padx=5, pady=3)

    label_subject = ttk.Label(frame_header, text='제목:')
    label_subject.grid(column=0, row=2, padx=5, pady=3)
    entry_subject = ttk.Entry(frame_header, width=70)
    entry_subject.grid(column=1, row=2, padx=5, pady=3)

    # 바디 프레임
    frame_body = ttk.LabelFrame(root, text='본문')
    frame_body.pack(fill='x', padx=10, pady=5, ipadx=2, ipady=2)
    
    textbox_body = scrolledtext.ScrolledText(frame_body)
    textbox_body.pack(fill='x', padx=10, pady=5)

    # sumbit button
    button_submit = ttk.Button(root, text='보내기',
    command=lambda: send_button(entry_host.get(), entry_port.get(), var_ssl.get(), entry_id.get(), entry_pw.get(),
    entry_sender.get(), entry_receiver.get(), entry_subject.get(), textbox_body.get(1.0, 'end')))
    button_submit.pack(padx=10, pady=10, anchor='e')

    root.mainloop()