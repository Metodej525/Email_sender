def send_email(date_list,email_list,delete_email_buttons,email_preview_buttons):
    #vytvori potvrzovaci label
    # temp_label = Label(email_tab, text='mail odeslán')
    # temp_label.grid(column=1,row=3, columnspan=2)
    #po 2 sekundách label skryje, pro kazdy label bezi samostatny timeout jestli nekdo bude klikat jak jeblej tak se to rozbije
    # root.after(2000, temp_label.destroy)
    # date_list.pop(0)
    # email_list.pop(0)

    for button in delete_email_buttons[:]:
        delete_email_buttons.remove(button)
        button.destroy()

    for button in email_preview_buttons[:]:
        email_preview_buttons.remove(button)
        button.destroy()

    for entry in date_list[1:]:
        date_list.remove(entry)
        entry.destroy()

    for entry in email_list[1:]:
        email_list.remove(entry)
        entry.destroy()
def load_email_details(config):
    smtp_server = config.get('EMAIL', 'smtp_server', fallback='')
    smtp_port = config.get('EMAIL', 'smtp_port', fallback='')
    username = config.get('EMAIL', 'username', fallback='')
    sender_email = config.get('EMAIL', 'sender_email', fallback='')
    subject = config.get('EMAIL', 'subject', fallback='')
    body = config.get('EMAIL', 'body', fallback='')
    return {'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'sender_email': sender_email,
            'subject': subject,
            'body':body
            }

