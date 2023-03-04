import sqlite3

conn = sqlite3.connect("economy.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS economy(
    id INTEGER PRIMARY KEY,
    name TEXT,
    wallet INTEGER DEFAULT 0,
    bank INTEGER DEFAULT 0
)""")

def createUserAccount(id: int, money: int):
    result = cursor.execute("SELECT * FROM economy WHERE id = ?", [id]).fetchone()
    if result is None:
        cursor.execute("INSERT INTO economy(id, wallet) VALUES(?, ?)", (id, money))
        conn.commit()
        return True
    else:
        print("test")
        return False
    
def addMoneyWallet(id: int, money):
    cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE id = ?", (money, id))
    conn.commit()

def addMoneyBank(id: int, money):
    cursor.execute("UPDATE economy SET bank = bank + ? WHERE id = ?", (money, id))
    conn.commit()
    
def checkIfUserExists(id: int):
    result = cursor.execute("SELECT * FROM economy WHERE id = ?", [id]).fetchone()
    if result is None:
        return False
    elif result is not None:
        return True
  
def getUserMoney(id: int):
    result = cursor.execute("SELECT wallet, bank FROM economy WHERE id = ?", [id])
    return result.fetchone()
  
def removeMoney(id: int, money):
    cursor.execute("UPDATE economy SET wallet = wallet - ? WHERE id = ?", (money, id))
    conn.commit()