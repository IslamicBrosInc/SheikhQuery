from getenglish import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import *
from flask.json import jsonify
import simplejson as json 




app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cardbase"
mongo = PyMongo(app)
client = MongoClient('localhost', 27017)
db = client['cardbase'] 
# videodb = client['videos']
# urldbb = client['urls']
# urlcollection = urldbb['url']
# laymanurl = urldbb['laymanurl']
# videocollection = db['videos']
cardcollection = db['cards']
englishcollection = db['englishcards']
laymaneng = db['laymanenglish']

def setup(FatwaCard):
    FatwaCard.set_title_and_filename()
    FatwaCard.set_transcript()
    # FatwaCard.set_summary()
    # FatwaCard.remove_video_from_server()



bad_words = ("Sheikh Assim Al Hakeem","assim alhakeem","assim al hakeem", "- assim al hakeem","-assim al hakeem","Assim al hakeem","- Assim al hakeem", "assim", "- assim","-assim", "Assim","JAL")
bad_chars = ("\ ","/",":","*","?","<", ">" ,"|","-")


def cleanup_transcript(title): 
    # for charbad in bad_chars:
    #     for chartest in title:
    #         title = title.replace(charbad,"")

    # for bad_word in bad_words:
    #     if bad_word in title:
    #             title = title.replace(bad_word, "")
    #             break;
    if "JAL" in title:
        title = title.replace("JAL","")
    if "foreign" in title:
        title = title.replace("foreign","")
    if "Consider Subscribing 😄" in title:
        title = title.replace("Consider Subscribing 😄","")
        print(title)
    if "Consider subscribing." in title:
        title = title.replace("Consider Subscribing!!! 😄","")
    if "consider subscribing" in title:
        title = title.replace("Consider Subscribing","")
        


    title = title.rstrip()
    return title

#access video collection
# videos = laymanurl.find()


def set_transcript(code):
    srt = YouTubeTranscriptApi.list_transcripts(code)

    for script in srt:
        if(script.is_generated==False):
            srt = script.translate('en').fetch()
    transcript_text = ""
    for line in srt:
            transcript_text+=line['text']
    transcript_text = transcript_text
    transcript_text = cleanup_transcript(transcript_text)
    return transcript_text



cards = laymaneng.find()

for card in cards:
    url = card.get('video_url')
    code = url[32:len(url)]
    id = card.get('cardID')
    status = card.get('beta_status')
    old = card.get('transcript')
    if old == "":
        try:
            transcript_text = set_transcript(code)
            print(transcript_text)
            print(id)
            filter = { 'cardID' : id }
            setts = { "$set" : { 'transcript': transcript_text } }
            laymaneng.update_one(filter,setts)
        except:
            continue
    else:
        continue

    # if "counsel" and "[Music]" in transcript_text:
    #     index_of_music = transcript_text.find("[Music]")
    #     transcript_text = transcript_text[:index_of_music]
    #     filter = { 'cardID' : id }
    #     setts = { "$set" : { 'transcript': transcript_text } }
    #     laymaneng.update_one(filter,setts)
    
    # if "and have you ever taken a counseling session" in transcript_text:
    #     index = transcript_text.find("and have you ever taken a counseling session")
    #     transcript_text = transcript_text[:index]
    #     filter = { 'cardID' : id }
    #     setts = { "$set" : { 'transcript': transcript_text } }
    #     laymaneng.update_one(filter,setts)

    # if "And have you ever taken a" in transcript_text:
    #     index = transcript_text.find("And have you ever taken a")
    #     transcript_text = transcript_text[:index]
    #     filter = { 'cardID' : id }
    #     setts = { "$set" : { 'transcript': transcript_text } }
    #     laymaneng.update_one(filter,setts)

    # if "If you have any questions, please contact me at" in transcript_text:
    #     index = transcript_text.find("If you have any questions, please contact me at")
    #     transcript_text = transcript_text[:index]
    #     filter = { 'cardID' : id }
    #     setts = { "$set" : { 'transcript': transcript_text } }
    #     laymaneng.update_one(filter,setts)

   




# cards = laymaneng.find()
# for card in cards:
#     currurl = card.get('video_url')
#     vidID = currurl[32:len(currurl)]
#     embed = "https://www.youtube.com/embed/" + vidID
#     filter = { 'video_url' : currurl }
#     urlembed = { "$set" : { 'vidembed': embed } }
#     englishcollection.update_one(filter,urlembed)
    


# ctr=0
# for video in videos:
#     ctr+=1
#     urlID = video.get('cardID')
#     url = video.get('url')
#     embed = video.get('embed')
#     title = video.get('title')
#     card = FatwaCard(url,title)
#     setup(card)
#     title = card.get_title_and_filename()[0]
#     # summary = card.get_summary()
#     transcript_text = card.get_transcript()
#     transcript_text = set_transcript
#     url = card.url
#     betastatus = card.get_betastatus()
#     card.set_cardID(ctr)
#     author = card.author
#     video_data = {
#         'title': title,
#         # 'summary': summary,
#         'transcript': transcript_text,
#         'video_url': url,
#         'embed':embed,
#         'author':author,
#         'cardID':ctr,
#         'beta_status':betastatus,
#         'question_status':card.isQuestion
#     }
#     laymaneng.insert_one(video_data)
#     print(card.get_cardID())





# cards = laymaneng.find()
# for card in cards:
#     currurl = card.get('video_url')
#     vidID = currurl[32:len(currurl)]
#     embed = "https://www.youtube.com/embed/" + vidID
#     filter = { 'video_url' : currurl }
#     urlembed = { "$set" : { 'vidembed': embed } }
#     englishcollection.update_one(filter,urlembed)
    
