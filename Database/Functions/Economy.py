from ..Database import conn, cursor

def createUserAccount(id: int, money: int):
    result = cursor.execute("SELECT * FROM economy WHERE id = ?", [id]).fetchone()
    if result is None:
        cursor.execute("INSERT INTO economy(id, wallet) VALUES(?, ?)", (id, money))
        conn.commit()
        return True
    else:
        print("test")
        return False
    
def addMoneyToWallet(id: int, money):
    cursor.execute("UPDATE economy SET wallet = wallet + ? WHERE id = ?", (money, id))
    conn.commit()

def addMoneyToBank(id: int, money):
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
    print(money)
    cursor.execute("UPDATE economy SET wallet = wallet - ? WHERE id = ?", (money, id))
    conn.commit()