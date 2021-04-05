from pyrogram import Client
from os import name, system
from pyrogram.types.messages_and_media import message
from pyrogram.handlers import *
from random import choice as random_choice


class MyClient:
    __slots__ = ["app", "file_name"]

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        """
        Format for archive :
        ID: [ID]
        HASH: [HASH]
            ***OPTIONALLY**
        NAME: [NAME] (DEFAULT WOULD BE "Account API")
        PHONE: [PHONE_NUMBER] (YOUR PHONE NUMBER (PREFIX INCLUDED) TO AVOID ENTERING IT MANUALLY)
        It can contain any other order, but be sure to follow that format
        """

        id_hash = open(self.file_name, "r")
        id, hash, phone_number, session_name = -1, "", "", "Account API"

        for line in (id_hash):
            if (line.count("ID: ") == 1):
                line = line.split('ID: ')[-1].replace('\n', '')
                try:
                    id = int(line)
                except:
                    pass

            elif (line.count("HASH: ") == 1):
                line = line.split('HASH: ')[-1].replace('\n', '')
                try:
                    hash = str(line)
                except:
                    pass

            elif (line.count("NAME: ") == 1):
                line = line.split('NAME: ')[-1].replace('\n', '')
                try:
                    session_name = str(line)
                except:
                    pass

            elif (line.count("PHONE: ") == 1):
                line = line.split('PHONE: ')[-1].replace('\n', '')
                try:
                    phone_number = str(line)
                except:
                    pass

            else:
                continue

        if (id == -1 or hash == ""):
            print("Missing credentials")

        if (phone_number != ""):
            self.app = Client(session_name=session_name, api_id=id,
                              api_hash=hash, phone_number=phone_number)
        else:
            self.app = Client(session_name=session_name,
                              api_id=id, api_hash=hash)

    def main(self):
            #self.app.run()
        with self.app:
            user = self.app.get_me()
            p_name = ""
            p_name += ("verified " if user.is_verified else "un-verified ")
            p_name += ("bot " if user.is_bot else "user ")
            print("Welcome {name}! @{user.username}".format(name=p_name +
                  user.first_name+' '+user.last_name, **locals()))
            opt = "Y"
            while(opt.lower() == "y"):
                self.clear()
                print("0. Send message")
                print("1. Send sticker")
                print("2. Join Chat")
                print("3. Add Message Handler")
                choice = input("Choice? ")

                try:
                    if (choice == "0"):
                            """Send message"""
                            message = input("Enter message: ")
                            try:
                                chat_id = input(
                                    "Chat id (Unique_identifier/username/phone number): ")
                                chat_id = int(chat_id)
                            except:
                                pass
                            if(self.send_message(chat_id=chat_id, message=message)):
                                print("Successfully sent message '{}'".format(message))
                            else:
                                raise TypeError

                    elif (choice == "1"):
                            """Send sticker"""
                            try:
                                chat_id = input(
                                    "Chat id (Unique_identifier/username/phone number): ")
                                chat_id = int(chat_id)
                            except:
                                pass
                            # I'll figure a way for BinaryIO, might be casting
                            stickers = ["CAACAgEAAxkBAAECJONgafOJ_Thz6r8CHd51MwtFwuDnZgACPQoAAr-MkATw-kKsJZetrh4E", "CAACAgEAAxkBAAECJONgafOJ_Thz6r8CHd51MwtFwuDnZgACPQoAAr-MkATw-kKsJZetrh4E",
                                        "CAACAgIAAxkBAAECJOdgaf0vuvbOr13UmDY6l9JriQwF5gACDwEAAiteUwtmHUnnGkg7RB4E", "CAACAgIAAxkBAAECJOVgaf0c5eaesQKUwU5B1FT0Vm5hVwACEwEAAiteUwuoZCFUWCiWHh4E", "CAACAgIAAxkBAAECJO1gaf2d1gG1eNpH8MVychBhQV6OdgACewADwZxgDNsaH7YdVDaIHgQ"]
                            sticker = random_choice(stickers)
                            if(self.send_sticker(chat_id=chat_id, sticker=sticker)):
                                print("Successfully sent sticker '{}'".format(sticker))
                            else:
                                raise TypeError

                    elif (choice == "2"):
                            """Join chat"""
                            try:
                                chat_id = input(
                                    "Chat id (Unique_identifier/username/link/): ")
                                linked_chat = bool(input("Linked chat? (1/0) "))
                                if (linked_chat):
                                    linked_chat = self.app.get_chat(
                                        chat_id).linked_chat_id
                            except:
                                pass
                            if (self.join_chat(chat_id=chat_id)):
                                print("Successfully joined chat '{}'".format(chat_id))
                            else:
                                raise TypeError

                    elif (choice == "3"):
                            """Add Message Handler"""
                            try:
                                function=input("Function? ")
                                function=exec(function)
                            except:
                                pass
                            if (self.add_message_handler(function=function)):
                                print("Successfully added function '{}'".format(function))
                            else:
                                raise TypeError

                except:
                    print ("Try again")

                opt = input("Again? (Y/N)")

    def send_sticker(self, chat_id, sticker):
        try:
            self.app.send_sticker(chat_id=chat_id, sticker=sticker)
            return True
        except:
            return False

    def send_message(self, chat_id, message):
        try:
            self.app.send_message(chat_id=chat_id, text=message)
            return True
        except:
            return False

    def join_chat(self, chat_id):
        try:
            self.app.join_chat(chat_id=chat_id)
            return True
        except:
            return False
        
    def add_message_handler(self, function):
        try:
            self.app.add_handler(MessageHandler(function))
            return True
        except:
            return False

    def clear(self):
        if name == "nt":
            system("cls")
        else:
            system("clear")
