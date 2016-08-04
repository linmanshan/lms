from flask import Flask, request, url_for
import json
from watson_developer_cloud import LanguageTranslationV2 as LanguageTranslation, ToneAnalyzerV3
import urllib, urllib2
from cassandra.cluster import Cluster

'''class TransPassword(urllib2.HTTPPasswordMgr):
    def find_user_password(self, realm, authurl):
        return ('be0889e0-2694-40d2-978a-144accb08dc3', '1LXnqxetPsfY')
'''

app = Flask(__name__)

@app.route("/")
def login():
    tone_analyzer = ToneAnalyzerV3(
        username='6e4c0424-2ac3-4dee-a231-ebff63fab4dc',
        password='NMjsEehEZSe0',
        version='2016-05-19 ')
    text=json.dumps(request.get_json()["text"])
    id=int(json.dumps(request.get_json()["id"]))
    res=tone_analyzer.tone(text)

    a= (json.dumps(tone_analyzer.tone(text), indent=2))

    language_translation = LanguageTranslation(
        username='58bcd279-bb41-4e51-adeb-78e60435aad5',
        password='SFOzV3qZaDoM')
    tone=[]
    score=[]
    for i in range(3):
        tone.append(language_translation.translate(
            text=res["document_tone"]["tone_categories"][0]["tones"][i]["tone_name"],
            source='en',
            target='fr'))
        score.append(res["document_tone"]["tone_categories"][0]["tones"][i]["score"])
    #b=b.encode("utf-8")
    #c=c.encode("utf-8")

    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    session.execute("""create keyspace demo3 with replication={'class':'SimpleStrategy','replication_factor':'1'};""")
    session.execute("""use demo3""")
    session.execute("create table users(tone_name text ,score float,tone_id int, primary key(tone_id))")
    prepared_stmt = session.prepare ( "INSERT INTO users (tone_name,score,tone_id) VALUES (?, ?, ?)")
    for i in range(3):
        bound_stmt = prepared_stmt.bind([tone[i], score[i],(id*10+i+1)])
        stmt = session.execute(bound_stmt)
    #session.execute("""insert into demo2.users(id,input)values(request.args.get("id"),request.args.get("text"));""")
    ##session.execute("create table demo.users(tone_name text primary key,score float,tone_id text)")
    #session.execute("""insert into demo.users(tone_name,score,tone_id)values('Anger',a["document_tone"]["tone_categories"]["tones"]["score"],'anger');""")
    #session.execute("""insert into demo.users(tone_name,score,tone_id)values('Disgust',a["document_tone"]["tone_categories"]["tones"]["score"],'disgust');""")
    #session.execute("""insert into demo.users(tone_name,score,tone_id)values('Happy',0.2082342,'happy');""")
    #session.execute("""select * from users;""")
    translation = "id\ttone\tscore\t\n"+str(id*10+1)+"\t"+tone[0]+"\t"+str(score[0])+"\n"+str(id*10+2)+"\t"+tone[1]+"\t"+str(score[1])+"\n"+str(id*10+3)+"\t"+tone[2]+"\t"+str(score[2])
    return translation
    #return json.dumps(translation,indent=2,ensure_ascii=True)

@app.route("/trans")
def login1():
    tone_analyzer = ToneAnalyzerV3(
        username='6e4c0424-2ac3-4dee-a231-ebff63fab4dc',
        password='NMjsEehEZSe0',
        version='2016-05-19 ')
    text=json.dumps(request.get_json()["text"])
    id=int(json.dumps(request.get_json()["id"]))
    res=tone_analyzer.tone(text)

    a= (json.dumps(tone_analyzer.tone(text), indent=2))

    language_translation = LanguageTranslation(
        username='58bcd279-bb41-4e51-adeb-78e60435aad5',
        password='SFOzV3qZaDoM')
    tone=[]
    score=[]
    for i in range(3):
        tone.append(language_translation.translate(
            text=res["document_tone"]["tone_categories"][0]["tones"][i]["tone_name"],
            source='en',
            target='fr'))
        score.append(res["document_tone"]["tone_categories"][0]["tones"][i]["score"])
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect("demo3")
    session.execute("use demo3")
    #session.execute("""create keyspace demo with replication={'class':'SimpleStrategy','replication_factor':'1'};""")
    #session.execute("create table demo.users(id int primary key,input text)")
    #session.execute("""insert into demo1.users(id,input)values(b,request.args.get("text"));""")
    for i in range(3):
        prepared_stmt = session.prepare ( "INSERT INTO users (tone_name,score,tone_id) VALUES (?, ?, ?)")
        bound_stmt = prepared_stmt.bind([tone[i], score[i],(id*10+i+1)])
        stmt = session.execute(bound_stmt)
    ##session.execute("create table demo.users(tone_name text primary key,score float,tone_id text)")
    #session.execute("""insert into demo.users(tone_name,score,tone_id)values('Anger',a["document_tone"]["tone_categories"]["tones"]["score"],'anger');""")
    #session.execute("""insert into demo.users(tone_name,score,tone_id)values('Disgust',a["document_tone"]["tone_categories"]["tones"]["score"],'disgust');""")
    #session.execute("""insert into demo.users(tone_name,score,tone_id)values('Happy',0.2082342,'happy');""")
    #session.execute("""select * from users;""")
    translation = "id\ttone\tscore\t\n"+str(id*10+1)+"\t"+tone[0]+"\t"+str(score[0])+"\n"+str(id*10+2)+"\t"+tone[1]+"\t"+str(score[1])+"\n"+str(id*10+3)+"\t"+tone[2]+"\t"+str(score[2])
    return translation
    #return json.dumps(e,indent=2,ensure_ascii=False)
    #return json.dumps(translation,indent=2,ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0")



