import psycopg2
import bot
import time

def check():
    conn = psycopg2.connect(host='localhost', dbname="newton",user="newton",password="1234",port=5432)
    cur=conn.cursor()
    cur.execute("SELECT * FROM queue")
    db = cur.fetchall()
    current=time.time()
    k=0
    for i in range(len(db)-1,-1,-1):
        if current-db[i][6]>=24*60*60 and db[i][7]!=0:
            cur.execute("UPDATE queue SET min_score=%s WHERE id = %s;"%(0,db[i][0]));
            k=i
            break
        if current-db[i][6]>=5*60 and db[i][7]!=50:
            cur.execute("UPDATE queue SET min_score=%s WHERE id = %s;"%(50,db[i][0]));
            
            for j in range(0,i):
                if (db[i][3] == db[j][5] and db[i][4] >= db[j][6]) or (db[i][5] == db[j][3] and db[i][6] <= db[j][4]):
                    print('50')
                    bot.create_private_channel_and_invite_users(db[i][1], db[j][1])
                    cur.execute("DELETE FROM queue WHERE id = %s" % db[i][0])
                    cur.execute("DELETE FROM queue WHERE id = %s" % db[j][0])
                    break


    for i in range(0,(k//2)):
        print('0')
        bot.create_private_channel_and_invite_users(db[i*2][1], db[i*2+1][1])
        cur.execute("DELETE FROM queue WHERE id = %s" % db[i*2][0])
        cur.execute("DELETE FROM queue WHERE id = %s" % db[i*2+1][0])

def apply(me):
    conn = psycopg2.connect(host='localhost', dbname='newton',user='newton',password='1234',port=5432)

    cur=conn.cursor()

    cur.execute("SELECT * FROM queue")
    db = cur.fetchall()
    score = 0
    pair_el = []
    for element in db:
        score = 0
        if str(me[2]) == element[5] and me[3] >= element[6] : # me give , element take
            score += 50
        if str(me[4]) == element[3] and me[5] <= element[4] : # me take , element give
            score += 50
        if score == 100:
            print('100')
            pair_el = element
            cur.execute("DELETE FROM queue WHERE id = %s" % element[0])
            bot.create_private_channel_and_invite_users(me[0],pair_el[1])
            break
                if pair_el != []:
        pass
    else:
        cur.execute("INSERT INTO queue (pid, name, give, givenum, take, takenum, time, min_score) VALUES (%s, %s, %s,%s, %s, %s,%s,%s);",
            me
            )

    conn.commit()
    cur.close()
    conn.close()
    check()
    return pair_el