import requests
import pandas as pd
import sqlite3 as sq
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/", status_code=200)
def joker():

    jokeList = []
    tableName = "test"
    print("Fetching jokes.....")
    for i in range(0,100):
        r = requests.get('https://v2.jokeapi.dev/joke/Any')
        resp = r.json()
        # print(resp)

        category = resp["category"]
        type = resp["type"]

        if 'joke' not in resp:
            joke = "$" 
        else:
            joke = resp["joke"] 

        if 'setup' not in resp:
            setup = "$"
            delivery = "$"
        else:
            setup = resp["setup"]
            delivery = resp["delivery"]

        flags_nsfw = resp["flags"]["nsfw"]
        flags_political = resp["flags"]["political"]
        flags_sexist = resp["flags"]["sexist"]
        safe = resp["safe"]
        lang = resp["lang"]

        temp = [category ,type ,joke ,setup ,delivery ,flags_nsfw ,flags_political ,flags_sexist ,safe ,lang]
        # print(temp)
        jokeList.append(temp)

    print(jokeList)

    df = pd.DataFrame(jokeList, columns = ["category","type","joke","setup","delivery","flags_nsfw","flags_political","flags_sexist","safe","lang"])

    # print(df.head())
    print("Adding jokes to DB")
    conn = sq.connect('{}.sqlite'.format(tableName))
    df.to_sql(tableName, conn, if_exists='replace', index=False)
    conn.close()

    return {"message":"success. 100 jokes added to DB"}


if __name__ == "__main__":
   uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)



# import sqlite3 as sq
# tableName = "test"
# conn = sq.connect('{}.sqlite'.format(tableName))
# res = conn.execute("SELECT count(*) FROM test")
# print(res.fetchall())