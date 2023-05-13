import psycopg2


def apply(me):
    conn = psycopg2.connect(host='localhost', dbname='minjoon',user='minjoon',password='79427749',port=5432)

    cur=conn.cursor()

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
            

    if pair_el != []:
        pair_el = -1
    else:
        cur.execute("INSERT INTO queue (pid, name, give, givenum, take, takenum, time, min_score) VALUES (%s, %s, %s,%s, %s, %s,%s,%s);",
            me
            )
    
    conn.commit()
    cur.close()
    conn.close()

    return pair_el


print(apply((120, 'n1','국',5, '수', 1, 1534, 100)))
# import schedule
# import time

# def match():


# schedule.every(5).minutes.do(match)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
# ---------------------------------

# cur.execute("CREATE TABLE queue (id serial PRIMARY KEY,pid integer, name varchar(50),give varchar(50),givenum integer, take varchar(50), takenum integer, time integer, min_score integer);")

# db.commit()

# (id, num, data) = cur.fetchone()
# print(f"{id}, {num}, {data}")




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


#             time=me[6]-db[i][6]
