#---IMPORTS---
from pyfiglet import Figlet
from getpass import getpass
import sqlite3
import sys
from time import sleep

#---SETING-----------------------------------------------------------------------------------------------------
sys.setrecursionlimit(997)

#---START------------------------------------------------------------------------------------------------------
def start_mess():
  start = Figlet(font = 'slant')
  print(start.renderText('WALLET'))

def start():
  q = input('[*]Welcome! Reg or log in?\n[!]\n--REG[r]\n--LOG IN[l]\n--ADMIN EDITION[a]\n[!]\n')
  if q == 'r':
    return registr_login()
  elif q == 'l':
    return login()
  elif q == 'a':
    return admin()
  else:
    print('[!]Please, using only r or l')
    return start()

#---DATE BASE--------------------------------------------------------------------------------------------------
def start_db():
  global db, cur
  db = sqlite3.connect('basse.db')
  cur = db.cursor()

  cur.execute("""
    CREATE TABLE IF NOT EXISTS main(
      login TEXT,
      password TEXT,
      all_cashs INT,
      necesary INT,
      moth INT
    )
  """)
  db.commit()

#---REGISTRATION-------------------------------------------------------------------------------------------
def registr_login():
  login = input('[*]Enter login:\n')
  cur.execute(f'SELECT password FROM main WHERE login = "{login}"')
  if cur.fetchone() is None:
    return registr_password(login)
  else:
    print('[!]Account locked')
    return registr_login()

def registr_password(login):
  password = getpass(f'[*]Nice, right now enter password {login}\n')
  password_ag = getpass('[*]Enter password again')
  if password == password_ag:
    print('[!]Succesful')
    try:
      all_cashs = int(input('[*]Enter cash what have:\n'))
      necesary = int(input('[*]Enter necesary costs:\n'))
      moth = int(input('[*]Enter moth costs:\n'))
      cur.execute(f"INSERT INTO main VALUES (?, ?, ?, ?, ?)", (login, password, all_cashs, necesary, moth))
      db.commit()
      print('[!]Succesful')
      return into(login)
    except ValueError as error:
      print(f'[!]Ops.. {error}\n[!]Using intgers\n')
      return registr_password(login)
  else:
    print('[!]Uncorrect, try again')
    return registr_password(login)

#---LOGIN--------------------------------------------------------------------------------------------------
def into(login):
  question = input('[*]Good! What wanna?\n[!]\n--Edit_cash[c]\n--Add_necesary_costs[n]\n--Edit_need_costs[m]\n--Lost_cash[l]\n--List[i]\n--Quit[q]\n[!]\n')
  if question == 'c':
    edit_cash(login)
  elif question == 'n':
    add_necesary_costs(login)
  elif question == 'm':
    edit_need_costs(login)
  elif question == 'l':
    lost_cash(login)
  elif question == 'n':
    lists(login)
  elif question == 'i':
    lists(login)
  elif question == 'q':
    print('[!]Ok, have a good day!')
    quit()
  else:
    print('[!]Please using only commands')
    sleep(2)
    return into(login)

def login():
  login = input('[*]Enter login:\n')
  cur.execute(f'SELECT password FROM main WHERE login = "{login}"')
  if cur.fetchone is None:
    print('[!]Account undefined')
    return login()
  else:
    enter_pas(login)

def enter_pas(login):
  password = getpass(f'[!]Nice, right now enter password {login}\n')
  cur.execute(f'SELECT password FROM main WHERE login = "{login}"')
  if cur.fetchone()[0] != password:
    print('[!]Password uncorrect')
    return enter_pas(login)
  else:
    into(login)

#---ADMIN EDITION----------------------------------------------------------------------------------------------
def admin():
  pass_admin = 'dima1234'
  passwords = getpass('[*]Enter admin password\n')
  if pass_admin == passwords:
    admin_edition()
  else:
    print('[!]Uncorrect, not using this commands[!]\n')
    return start()

def delete_users():
  all_user = cur.execute('SELECT login FROM main')
  for i in all_user:
    print(f'---{i[0]}')
  user = input('[*]Cap, enter who will delete')
  cur.execute(f'DELETE FROM menu WHERE login = "{user}"')
  db.commit()
  sleep(2)
  return admin_edition()

def cheak_list():
  lists = cur.execute('SELECT login, password, all_cashs, necesary, moth FROM main')
  for l, p, a, n, m in lists:
    print(f'---login: {l}||password: {p}||cash: {a}||necesary: {n}||moth: {m}--')
  sleep(2)
  return admin_edition()

def admin_edition():
  q = input('[*]What u wanna cap?\n--Delete user[d]\n--Cheak all users[u]\n--Go to log in[g]\n--Go to registration[r]\n--Exit[e]\n')
  if q == 'd':
    return delete_users()
  elif q == 'u':
    return cheak_list()
  elif q == 'g':
    return login()
  elif q == 'r':
    return registr_login()
  elif q == 'e':
    print('[!]Ok cap, bye')
    exit()

#---QUESTIONS----------------------------------------------------------------------------------------------
def edit_cash(login):
  try:
    edit_c = int(input('[*]Enter new cash:\n'))
    cur.execute(f'UPDATE main SET all_cashs = "{edit_c}" WHERE login = "{login}"')
    db.commit()
    cur.execute(f'SELECT all_cashs FROM main WHERE login = "{login}"')
    print(f'[!]Succesful!\n[!]Lost: {cur.fetchone()[0]}\n')
    sleep(3)
    return into(login)
  except ValueError as error:
    print(f'[!]Ops.. {error}\n[!]Using intgers\n')
    return edit_cash(login)

def lists(login):
  try:
    cur.execute(f'SELECT all_cashs, moth, necesary FROM main WHERE login = "{login}"')
    data = cur.fetchone()
    all_cashs = data[0]
    moth = data[1]
    necesary = data[2]
    print(f'[!]\n--Cash: {all_cashs}\n--Need costs: {moth}\n--Necesary: {necesary}\n[!]\n')
    sleep(3)
    into(login)
  except ValueError as error:
    print(f'[!]Ops.. {error}\n[!]Using intgers\n')
    return lists(login)

def add_necesary_costs(login):
  try:
    cur.execute(f'SELECT necesary FROM main WHERE login = "{login}"')
    old_necesary = cur.fetchone()[0]
    edit_n = int(input('[*]Enter costs:\n'))
    cur.execute(f'UPDATE main SET necesary = "{old_necesary}" - "{edit_n}" WHERE login = "{login}"')
    db.commit()
    cur.execute(f'SELECT necesary FROM main WHERE login = "{login}"')
    print(f'[!]Succesful!\n[!]Lost: {cur.fetchone()[0]}\n')
    sleep(3)
    return into(login)
  except ValueError as error:
    print(f'[!]Ops.. {error}\n[!]Using intgers\n')
    return add_necesary_costs(login)

def edit_need_costs(login):
  try:
    cur.execute(f'SELECT moth FROM main WHERE login = "{login}"')
    old_moth = cur.fetchone()[0]
    edit_m = int(input('[*]Enter costs:\n'))
    cur.execute(f'UPDATE main SET moth = "{old_moth}" - "{edit_m}" WHERE login = "{login}"')
    db.commit()
    cur.execute(f'SELECT moth FROM main WHERE login = "{login}"')
    print(f'[!]Succesful!\n[!]Lost: {cur.fetchone()[0]}\n')
    sleep(3)
    return into(login)
  except ValueError as error:
    print(f'[!]Ops.. {error}\n[!]Using intgers\n')
    return edit_need_costs(login)

def lost_cash(login):
  try:
    cur.execute(f'SELECT moth FROM main WHERE login = "{login}"')
    edit_m = cur.fetchone()[0]
    cur.execute(f'SELECT necesary FROM main WHERE login = "{login}"')
    edit_n = cur.fetchone()[0]
    res = edit_m + edit_n
    cur.execute(f'SELECT all_cashs FROM main WHERE login = "{login}"')
    old_all_cashs = cur.fetchone()[0]
    cur.execute(f'UPDATE main SET all_cashs = "{old_all_cashs}" - "{res}" WHERE login = "{login}"')
    db.commit()
    cur.execute(f'SELECT all_cashs FROM main WHERE login = "{login}"')
    print(f'[!]Nice!\n[!]All lost: {cur.fetchone()[0]}\n')
    sleep(3)
    return into(login)
  except ValueError as error:
    print(f'[!]Ops.. {error}\n[!]Using intgers\n')
    return lost_cash(login)

#---INIT---------------------------------------------------------------------------------------------------
def main():
  try:
    start_db()
    start_mess()
    start()
  except KeyboardInterrupt:
    print('\n[!][!][!]BEEN ERROR[!][!][!]')
    return main()

if __name__ == '__main__':
  main()