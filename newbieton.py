import psycopg2
​import schedule
import time
import bot

​dbname=""
user=""
password=""
def apply(me):
    conn = psycopg2.connect(host='localhost', dbname=dbname,user=user,password=password,port=5432)
​
    cur=conn.cursor()
​
    cur.execute("SELECT * FROM queue")
    db = cur.fetchall()
    score = 0
    pair_el = []
    for element in db:
        score = 0
        if me[2] == element[5] and me[3] >= element[6] : # me give , element take
            score += 50
        if me[4] == element[3] and me[5] <= element[4] : # me take , element give
            score += 50
        if score == 100:
            pair_el = element
            cur.execute("DELETE FROM queue WHERE id = %s" % element[0])
            break
            
​
    if pair_el != []:
        pair_el = -1
    else:
        cur.execute("INSERT INTO queue (pid, name, give, givenum, take, takenum, time, min_score) VALUES (%s, %s, %s,%s, %s, %s,%s,%s);",me)
    
    conn.commit()
    cur.close()
    conn.close()
​
    return pair_el
​
def check():
    conn = psycopg2.connect(host='localhost', dbname=dbname,user=user,password=password,port=5432)
    cur=conn.cursor()
    cur.execute("SELECT * FROM queue")
    db = cur.fetchall()
    current=time.time()
    k=0
    for i in range(len(db)-1,-1,-1):
        if current-db[i][6]>=24*60*60 and db[i][7]!=0:
            db[i][7]=0
            cur.execute("UPDATE queue SET min_score=%s WHERE id = %s;"%(0,db[i][0]));
            k=i
            break
        if current-db[i][6]>=5*60 and db[i][7]!=50:
            db[i][7]=50
            cur.execute("UPDATE queue SET min_score=%s WHERE id = %s;"%(50,db[i][0]));
            
            for j in range(0,i):
                if (db[i][3] == db[j][5] and db[i][4] >= db[j][6]) or (db[i][5] == db[j][3] and db[i][6] <= db[j][4]):
                    bot.create_private_channel_and_invite_users(db[i][1], db[j][1])
                    cur.execute("DELETE FROM queue WHERE id = %s" % db[i][0])
                    cur.execute("DELETE FROM queue WHERE id = %s" % db[j][0])
                    break


    for i in range(0,(k//2)):
        bot.create_private_channel_and_invite_users(db[i*2][1], db[i*2+1][1])
        cur.execute("DELETE FROM queue WHERE id = %s" % db[i*2][0])
        cur.execute("DELETE FROM queue WHERE id = %s" % db[i*2+1][0])





​schedule.every(10).minutes.do(check)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)


print(apply((120, 'n1','국',5, '수', 1, 1534, 100)))
# import schedule
# import time
​
# def match():
​
​
# schedule.every(5).minutes.do(match)
​
# while True:
#     schedule.run_pending()
#     time.sleep(1)
# ---------------------------------
​
# cur.execute("CREATE TABLE queue (id serial PRIMARY KEY,pid varchar(50), name varchar(50),give varchar(50),givenum integer, take varchar(50), takenum integer, time integer, min_score integer);")
​
# db.commit()
​
# (id, num, data) = cur.fetchone()
# print(f"{id}, {num}, {data}")
​
​
​
​
# def apply(me, mx):
#     global db
#     l=len(db)
#     idx=-1
#     time=-1
#     for i in range(l):
#         score=0
#         if me['take']==db[i]['give'] and me['takenum']<=db[i]['givenum']:score+=50
#         if me['give']==db[i]['take'] and me['givenum']>=db[i]['takenum']:score+=50
#         if mx<score:
#             mx=score
#             idx=i
#     if mx==100:
#     db[i]['maxscore']=mx
#     db[i]['maxindex']=l
​
​
#             time=me[6]-db[i][6]