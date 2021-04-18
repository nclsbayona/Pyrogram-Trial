from typing import Tuple
from pyrogram.handlers.handler import Handler
from pyrogram import Client
from os import name, system
from pyrogram.handlers import *
from pyrogram.filters import *
import json
from random import choice as random_choice
from pyrogram.types.object import Object


def main(file_name, handlers: List[Tuple[Handler]]):
    """
    .format for archive :
    ID: [ID]
    HASH: [HASH]
        ***OPTIONALLY**
    NAME: [NAME] (DEFAULT WOULD BE "Account API")
    PHONE: [PHONE_NUMBER] (YOUR PHONE NUMBER (PREFIX INCLUDED) TO AVOID ENTERING IT MANUALLY)
    It can contain any other order, but be sure to follow that .format
    """

    id_hash = open(file_name, "r")
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

    else:
        global __app
        if (phone_number != ""):
            __app = Client(session_name=session_name, api_id=id,
                           api_hash=hash, phone_number=phone_number)
        else:
            __app = Client(session_name=session_name,
                           api_id=id, api_hash=hash)

    for handler, group in (handlers):
        add_handler(handler, group)

    with __app as __app:
        user = __app.get_me()
        p_name = ""
        p_name += ("verified " if user.is_verified else "un-verified ")
        p_name += ("bot " if user.is_bot else "user ")
        opt = "Y"
        while(opt.lower() == "y"):
            try:
                clear()

                print("Welcome {name}! @{user.username}".format(name=p_name +
                                                                user.first_name+' '+user.last_name, **locals()))
                print("0 Send message")
                print("1 Send sticker")
                print("2 Join Chat")
                print("3 Print iter dialiogs")
                choice = input("Choice? ")

                if (choice == "0"):
                    """Send message"""
                    message = input("Enter message: ")
                    try:
                        chat_id = input(
                            "Chat id (Unique_identifier/username/phone number): ")
                        chat_id = int(chat_id)
                    except:
                        pass
                    if(send_message(chat_id=chat_id, message=message)):
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
                    if(send_sticker(chat_id=chat_id, sticker=sticker)):
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
                            linked_chat = __app.get_chat(
                                chat_id).linked_chat_id
                    except:
                        pass
                    if (join_chat(chat_id=chat_id)):
                        print("Successfully joined chat '{}'".format(chat_id))
                    else:
                        raise TypeError

                elif (choice == "3"):
                    try:
                        print_iter_dialogs()
                    except:
                        raise TypeError

            except:
                print("-___(^*^)___-")

            opt = input("Again? (Y/N)")


def print_members(chat_id):
    print("Members")

    for member in (__app.iter_chat_members(chat_id)):
        print("\t"+type(member))

    print()


def print_iter_dialogs():

    def print_dialog(dialog: Object):

        chat_type=str(dialog.chat.type)
        print("This is {chat.type} ID: {chat.id}".format(
            **dialog.__dict__), end=' ')
        if(chat_type.__contains__("grupo") or chat_type.__contains__("group")):
            # Grupo

            print("title: {chat.title}, unread_messages {unread_messages_count}".format(
                **dialog.__dict__))

            print_members(int(dialog.chat.id))

        else:
            print("username: {chat.username}, Name {chat.first_name} {chat.last_name}".format(
                **dialog.__dict__))

    for dialog in __app.iter_dialogs():
        print_dialog(dialog)


def addHandler(handler: Handler, group=None):
    if (group is not None):
        __app.add_handler(handler, group)
    else:
        __app.add_handler(handler)
    try:
        __app.restart()
    except:
        pass


def send_sticker(chat_id, sticker):
    try:
        __app.send_sticker(chat_id=chat_id, sticker=sticker)
        return True
    except:
        return False


def send_message(chat_id, message):
    try:
        __app.send_message(chat_id=chat_id, text=message)
        return True
    except:
        return False


def join_chat(chat_id):
    try:
        __app.join_chat(chat_id=chat_id)
        return True
    except:
        return False


def add_handler(function: Handler, group):
    try:
        if (group is not None):
            __app.add_handler(function, group)
        else:
            __app.add_handler(function)
        return True
    except:
        return False


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")
