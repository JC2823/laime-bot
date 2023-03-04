import sqlite3
from io import BytesIO

conn = sqlite3.connect("poll.db")
sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS poll(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    guild TEXT,
    channel TEXT,
    message TEXT,
    ended BOOLEAN DEFAULT FALSE,
    options TEXT,
    results BLOB
)""")

def getPollByMessageId(guild, message):
    result = cursor.execute("SELECT * FROM poll WHERE guild = ? AND message = ?", (guild, message)).fetchone()
    if result is None:
        return False
    else:
        return result

def getPollById(guild, id):
    result = cursor.execute("SELECT * FROM poll WHERE guild = ? AND id = ?", (guild, id)).fetchone()
    return result

def createPoll(title, guild, channel, message, options):
    cursor.execute("INSERT INTO poll(title, guild, channel, message, options) VALUES(?, ?, ?, ?, ?)", (title, guild, channel, message, options))
    conn.commit()
    
def deletePoll(id):
    cursor.execute("UPDATE poll SET ended = True WHERE id = ?", [id])
    conn.commit()
    
def getPollList(guild):
    result = cursor.execute("SELECT id, title FROM poll WHERE guild = ? AND ended = False", [guild])
    data = []
    
    for i in result.fetchall():
        data.append([i[0], i[1] if len(i[1]) < 24 else f"{i[1][:24]}..."])
        
    return data

def getPollHistory(guild):
    result = cursor.execute("SELECT id, title, ended FROM poll WHERE guild = ?", [guild])
    data = []
    
    for i in result.fetchall():
        data.append([i["id"], i["title"] if len(i["title"]) < 24 else f"{i['title'][:24]}...", bool(i["ended"])])
        
    return data

def setPollResults(guild, id, results):
    cursor.execute("UPDATE poll SET results = ? WHERE guild = ? AND id = ?", (results.getvalue(), guild, id))
    conn.commit()
    
def getPollResults(guild, id):
    return cursor.execute("SELECT results FROM poll WHERE guild = ? AND id = ?", (guild, id)).fetchone()
