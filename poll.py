import time
from send_email import *
from read_email import *
import os.path
from db import create_db
import sqlite3
from datetime import date

if not os.path.isfile('swimmers.db'):
    create_db()

conn = sqlite3.connect('swimmers.db')
c = conn.cursor()

def messaged_back(idn):
    c.execute("SELECT email_id FROM messages where email_id=?", [idn])
    msg_id = c.fetchall()
    if len(msg_id) == 0:
        return False
    else:
        return True

def insert_message(email_id, sender, receiver, message):
    today = date.today()
    date_str = str(today.month) + "-" + str(today.day) + "-" + str(today.year)
    c.execute("INSERT INTO messages (email_id, sender, receiver, message, date_added) VALUES (?, ?, ?, ?, ?)", (email_id, sender, receiver, message, date_str))
    conn.commit()


def tasks(person):
    '''
    gets data from db based on who is wanted and return string
    m - myroslav
    d - danylo
    all - both
    '''
    s = []
    output = ""
    if person == "m":
        c.execute("SELECT * FROM myroslav")
        s = c.fetchall()
        output += "\nMyroslav: " + "\n"
    elif person == "d":
        c.execute("SELECT * FROM danylo")
        s = c.fetchall()
        output += "\nDanylo: " + "\n"
    elif person == "all":
        return tasks("m") + "\n\n\n" + tasks("d")
    else:
        return "\nincorrect person specified \nshould only be `m`, `d`, or `all`"

    for i in s:
        output += "-"
        for j in i:
            output += str(j) + "   "
        output += "\n"
    return output


def add_task(person, data, imp):
    today = date.today()
    print("type " + str(type(data)))
    date_str = str(today.month) + "-" + str(today.day) + "-" + str(today.year)
    if person == "m":
        c.execute("INSERT INTO myroslav (task, date_added, importance) VALUES (?, ?, ?)", (data, date_str, imp))
        conn.commit()
        return "\nInserted {0} into {1} with {2} importance".format(data, person, imp)
    elif person == "d":
        c.execute("INSERT INTO danylo (task, date_added, importance) VALUES (?, ?, ?)", (data, date_str, imp))
        conn.commit()
        return "\nInserted {0} into {1} with {2} importance".format(data, person, imp)
    else:
        return "Could not add task"


def remove_task(person, idnum):
    '''
    remove task from either myroslav table or danylo table
    '''
    if person == "m":
        c.execute("DELETE FROM myroslav WHERE id=?", [idnum])
        conn.commit()
        return "\nDeleted task #{0} for {1}".format(idnum, person)
    elif person == "d":
        c.execute("DELETE FROM danylo WHERE id=?", [idnum])
        conn.commit()
        return "\nDeleted task #{0} for {1}".format(idnum, person)

def tips():
    return " \n \
            Freetyle pull technique video: https://www.youtube.com/watch?v=SONx52cyltI \n \
            Freestyle flip turn technique: https://www.youtube.com/watch?v=EJ2HhVID8_w \n \
            Caleb Dressel underwater view: https://www.youtube.com/watch?v=vE-4whlB1IY \n \
            Michael Phelps underwater kick: https://youtu.be/hvbGrfpCsjo?t=1m11s \
    "


def commands():
    return " \n \
        Keywords \n \
        `m` stands for Myroslav \n \
        `d` stands for Danylo \n \
        `all` stands for both \n \
        \n \
        View Tasks \n \
        `$tasks` - views the task list of the certain swimmer(s) \n \
        `$tasks:*NAME HERE*` \n \
        \n \
        View Tips Section \n \
        `$tips` - views the tips and links section \
    "


def reply(command, person):
    split_command = command.split(":")
    if person == config.ADMIN:
        if split_command[0] == "$tasks":
            return tasks(split_command[1])
        elif split_command[0] == "$add":
            return add_task(split_command[1], split_command[2], split_command[3])
        elif split_command[0] == "$tips":
            return tips()
        elif split_command[0] == "$remove":
            return remove_task(split_command[1], split_command[2])
        elif split_command[0] == "$commands":
            return commands()
        else:
            return "\nincorrect command, type $commands to view all commands"
    else:
        if split_command[0] == "$tasks":
            return tasks(split_command[1])
        elif split_command[0] == "$tips":
            return tips()
        elif split_command[0] == "$commands":
            return commands()
        else:
            return "\nincorrect command, type $commands to view all commands"


email_account = Account(config.EMAIL, config.PASSWORD)
email_sender = SendEmail()

while True:
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    if hour == 18 and minute == 0:
        for person in config.ALLOWED_CONTACTS:
            email_sender.send_msg(person, tasks("all") + "  ", "daily task reminder")
        time.sleep(60)
    email = email_account.get_email()
    if email[0] in config.ALLOWED_CONTACTS or email[0] == config.ADMIN and not messaged_back(email[2]):
        # need to add two spaces to the end of the send email data param
        reply_msg = reply(email[1], email[0])
        email_sender.send_msg(email[0], reply_msg + "  ", email[1])
        insert_message(email[2], config.EMAIL, email[0], reply_msg)

    time.sleep(0.25)
