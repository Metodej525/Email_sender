from tkinter import *
from tkinter import ttk

from gui.email_preview_window import EmailPreviewTab
from gui.email_window import EmailTab
from gui.excel_window import ExcelTab
from gui.signature_window import SignatureTab

from Service.email_preview_service import load_email_details, html_converter
from Service.email_service import selected_value_manager, EmailSendManager
from Service.excel_service import excel_path_load, excel_search, excel_load
from Service.signature_service import save_signature, load_signature_data

from infra.email_details import email_details

from core.utilities import safe_write_config
import constants as c

import logging

logger = logging.getLogger(__name__)

def setup_gui(config):
    root = Tk()
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    root.title(c.ROOT_TITLE)
    root.option_add("*Font", ("Arial", 12))

    # signature_tab = SignatureTab(notebook,config,save_signature,safe_write_config,load_signature_data)
    email_preview_tab = EmailPreviewTab(notebook, load_email_details, html_converter, config)
    excel_tab = ExcelTab(notebook, excel_path_load, safe_write_config, config, excel_load)
    email_tab = EmailTab(notebook, root, excel_search, config, excel_tab.df, selected_value_manager, html_converter,
                         EmailSendManager,email_details)

    notebook.add(email_tab, text="Email")
    notebook.add(email_preview_tab, text='Náhled emialu')
    # notebook.add(signature_tab, text="Signature")
    notebook.add(excel_tab, text="Excel")

    TAB_FIELDS = {
        email_tab: '700x350',
        email_preview_tab: '1200x600',
        # signature_tab: '300x200',
        excel_tab: '600x300'
    }

    def resize_tab(event):
        tab_id = event.widget.select()
        tab = event.widget.nametowidget(tab_id)

        if tab in TAB_FIELDS:
            root.geometry(TAB_FIELDS[tab])

    notebook.bind("<<NotebookTabChanged>>", resize_tab)
    root.geometry("500x150")
    logger.info("app started")
    root.mainloop()

