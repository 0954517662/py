# -*- coding: utf-8 -*-

from linepy import *
from akad.ttypes import *
from multiprocessing import Pool, Process
from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit

client = LINE("EtHgMthADlOiUjAl4Cc9.21sAkUOl2Bgb1ec67b74Iq.8NBqwIbXWVr17O+ZYANCuMCdDjLUJEjMLtzKNedOlCc=")
client.log("Auth Token : " + str(client.authToken))
client.log("Timeline Token : " + str(client.tl.channelAccessToken))


botStart = time.time()

helpMessage ="""FGM Publik v2.1 Keywords
==========KATEGORI==========
・/alat
・/hiburan
・/kontak
・/grup
・/teks
・/fgmbot
・/ramadhan (Limited!!!)
・/store
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
*Bot ini menggunakan anti-flood
> more info ketik /antiflood"""
#------------------------------
puasaMessage = """=======RAMADHAN==========
Limited Edition sampai tanggal 14/06/2018 [20:00 WIB]
============================
・/iklanpuasa
・Puasa
・Sahur
・Buka puasa
・Ngabuburit
・Takjil
・Bukber
・Energen
・Sprite
・Indomie
・Nastar
・Putri salju
・Marjan
・Kebo
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!"""
fgmguideMessage ="""========FGMBOT GUIDE========
Panduan utk fungsi tiap key
============================
・Fgm bye = mengeluarkan bot
・fgm kontak = kirim kontak bot fgm
・Update = cek fitur baru
・Crtr = cek pembuat bot
・About = liat tentang bot fgm
============================
keywordnya ketik /fgmbot"""
teksguideMessage = """=========TEKS GUIDE=========
Panduan utk fungsi tiap key
============================
・Jumlah teks = cek jumlah huruf pada teks
・Huruf besar = ubah semua teks menjadi kapital semua
・Huruf kecil = ubah semua teks menjadi kecil semua
============================
keywordnya ketik /teks"""
grupguideMessage = """=========GRUP GUIDE=========
Panduan utk fungsi tiap key
============================
・Cek sider = cek nama anggota yang sedang nyimak di grup
・Info grup = cek nama grup, pembuat grup, dll
・Ganti nama grup = ubah nama grup
・Anti spam = anti spam teks diatas 5000 huruf
・Link grup on/off = buka/tutup link grup
・List member = liat daftar nama anggota
・Member teratas/terbawah = Cek member peringkat atas dan bawah
・List pending = cek nama anggota yang masih dalam undangan tertunda
・Tag pending = ngetag anggota yang masih dalam pendingan
・Pembuat grup = ngirim kontak pembuat grup
============================
Keywordnya ketik /grup"""
kntkguideMessage = """=======KONTAK GUIDE========
Panduan utk fungsi tiap key
============================
・Curi dp/home = Mengirim gambar foto profil/foto sampul yang ditag
・Curi kontak = ngirim kontak yang ditag
・Cek kontak = liat info kontak
・My name/status/dp/home = ngirim info anda sendiri dari nama, status, foto profil dan foto sampul
・My kontak = ngirim kontak anda sendiri
・Idl = ngirim kontak lewat id line
・Idl url = ngirim link untuk liat hasil pencarian id line
============================
keywordnya ketik /kontak"""
hibuguideMessage = """=======HIBURAN GUIDE========
Panduan utk fungsi tiap key
============================
・Kerang ajaib = Cek jawaban seperti kerang ajaib di tv
・Penjawab pertanyaan = Menjawab suatu pertanyaan
・Cek profil = cek info orang / sendiri
・Pasangan = cek persen kecocokan kedua orang yang di tag
・Jodoh = Cek jodoh dalam 1 grup
・Nilai gambar/video/stiker = menilai gambar/video/stiker dari 0-100
・Mood = Cek persentase mood melalui tag atau anda sendiri
============================
Note: hanya buat hiburan/candaan aja ya...
keywordnya ketik /hiburan"""
alatguideMessage ="""=========ALAT GUIDE=========
Panduan utk fungsi tiap key
============================
・Translator = menerjemah bahasa
・Kalender = mengirim pesan dalam bentuk kalender 
・Jam wib/wita/wit = melihat tanggal dan jam setiap wilayah indonesia
・Youtube = mencari video youtube dalam bentuk link
・Ig = Cek profile instagram
・Playstore = liat hasil pencarian di playstore lewat link
・Cari web = liat hasil pencarian lewat google
・Link stiker = mengirim link stiker dari stiker yang kamu kirim
・Lokasi = mengirim link lokasi google maps
・Jadwal sholat = cek jadwal sholat disetiap lokasi
・Cuaca = cek suhu di suatu lokasi
============================
keywordnya ketik /alat"""
toolMessage ="""============ALAT============
・/translator
・/kalender
・/jam
・/youtube
・/ig<s><username ig>
・/playstore<s><nama app>
・/cariweb<s><nama search>
・/linkstiker
・/cekpost
・/chatwa
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
Ket: <s> = Spasi
ketik /alathelp utk melihat fungsi fitur"""
#------------------------------
hibuMessage ="""=========HIBURAN============
・/kerangajaib
・/penjwbpertanyaan
・/cekprofil<s><tag orgnya>
・/pasangan<s><tag 2 org>
・/jodoh<s><tag orgnya>
・/jodohku
・/cekprofilku
・/nilaigambar
・/nilaivideo
・/nilaistiker
・/mood<s><tag>
・/moodku
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
Ket: <s> = Spasi
ketik /hiburanhelp utk melihat fungsi fitur"""
#------------------------------
gcMessage ="""============GRUP============
・/ceksider
・/infogrup
・/pembuatgrup
・/gantinamagrup
・/linkgrup on
・/linkgrup off
・/listmember
・/mem teratas
・/mem terbawah
・/listpending
・/pendingtag
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
Ket: <s> = Spasi
ketik /gruphelp utk melihat fungsi fitur"""
#------------------------------
setiMessage ="""==========FGMBOT============
・/fgmbye
・/fgmkontak
・/crtr
・/about
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
ketik /fgmhelp utk melihat fungsi fitur"""
contMessage =  """===========KONTAK===========
・/curidp<s>@tag 
・/curistatus<s>@tag 
・/curinama<s>@tag
・/curihome<s>@tag
・/curikontak<s>@tag
・/cekcontact
・/mycontact
・/myname
・/mystatus
・/mydp
・/myhome
・/idl<s><id line>
・/idlurl<s><id line>
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
Ket: <s> = Spasi
ketik /kontakhelp utk melihat fungsi fitur"""
teksMessage =  """============TEKS============
・/jmlhteks<s><teksnya>
・/hurufbesar<s><teksnya>
・/hurufkecil<s><teksnya>
============================
Note:
*Besar kecilnya huruf tidak berpengaruh!
Ket: <s> = Spasi
ketik /tekshelp utk melihat fungsi fitur"""
aboutMsg="""<<< About FGM Bot Publik >>>
===========================
1) Nama: FGM#2.0#2
2) Versi: 2.1
3) Creator: 🔰Firmansyah🔰
4) Tgl dibuat: 28-11-2017
5. Tipe: Bot Serbaguna
===========================
Terima Kasih Banyak Kepada
===========================
1) Team Line Rangers Indo
>> Moh Erbil, Wendy, Dendri, Rizky Galuh, Anisa Aprilia, Fildzah, Raihan, Dede, Frans, Made, Tio, Okz (Best Friend モの Rangers & ORI)
>> Semua Anggota Clan モの Rangers & ORI

2) Bot Token Generator
>> Tanysyz (by HelloWorld)

3) TEAM NOOB BOT
==========================="""
oepoll = OEPoll(client)
mid = client.getProfile().mid
admin=["u16baba09004cd8424cd2d0a0a47da7c6","u60ba66bd3f555dc5a327c7fb2692e36c"]
beote=["uab9e646523aff014d28162cd65a713ba"]
asdfg=[""]
qwert=[""]
stikr=[""]
athur=["ua6cc52c89aaad7f9bd2d57853ad2ce9c"]
lmlmt=[]
lmlmt1=[]
nilaipic=[]
nilaivid=[]
nilaistk=[]
userlimit=[]
cekpost=[]
iklps=["bCah9UFWW7I","_LRFgEAPovk","e1q54gx4mVA","wyMUG38sbrc","8Uz0vBCg-NY","egDXVZAwe60","7pMdNbCOHc4","8J5UMMJsXUU","9v3ke6eijV4","8DzFC_eyUWg","-05_lLgRQ70","iEAybJM9F7E","WYquS-LjdnU","gmPZ33PvwgI","O-LS8bJMYV4","T82JtdfFxIQ","pEX4S0NQ2Zs","a_5xAC_9oIc","GhLSjFoCQ5E","F-ymZjDyciQ"]
msg_dict = {}
wait = {
    'contact':True,
    'autoJoin':True,
    'autoCancel':{"on":True,"members":1},
    'leaveRoom':True,
    'timeline':True,
    'autoAdd':True,
    'message':"Terima kasih telah menambahkan sebagai teman. silahkan undang bot ini ke grup anda. Bot ini tidak bisa merespon kata kunci dalam personal chat.\n\nJika ada yang ditanyakan bisa menghubungi id line dibawah ini\nhttp://line.me/R/ti/p/~@nya9070u\noa:\nhttp://line.me/R/ti/p/~@wcf4912l",
    "lang":"JP",
    "comment":"Thanks for add me",
    "commentOn":False,
    "commentBlack":{},
    "wblack":False,
    "dblack":False,
    "clock":False,
    "cName":"",
    "lmlmt":{},
    "Dools":{},
    "blacklist":{},
    "wblacklist":False,
    "Fgmchatbot":{},
    "dblacklist":False,
    "protectionOn":False,
    "autosider":{},
    "atjointicket":False,
    "userAgent": [
		"Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
		"Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
		"Mozilla/5.0 (X11; Linux) Gecko Firefox/5.0",
		"Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 FirePHP/0.5",
		"Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Firefox/5.0",
		"Mozilla/5.0 (X11; Linux x86_64) Gecko Firefox/5.0",
		"Mozilla/5.0 (X11; Linux ppc; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (X11; Linux AMD64) Gecko Firefox/5.0",
		"Mozilla/5.0 (X11; FreeBSD amd64; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20110619 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 6.1.1; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 5.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 5.1; U; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 5.0; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
		"Mozilla/5.0 (Windows NT 5.0; rv:5.0) Gecko/20100101 Firefox/5.0"
	],
}

wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
    }

setTime = {}
setTime = wait2['setTime']

def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))

def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                client.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]
            
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def bot(op):
    try:
        if op.type == 0:
            return

        if op.type == 13:
            if mid in op.param3:
                client.acceptGroupInvitation(op.param1)
                ginfo = client.getGroup(op.param1)
                gj = str(len(ginfo.members))
                if int(gj) < 10:
                    client.sendMessage(op.param1, "Mohon maaf anggota grup kurang dari 10. ijin left")
                    client.leaveGroup(op.param1)
                else:
                    client.sendMessage(op.param1, "Terima kasih telah mengundang ke grup. ketik /key untuk bantuan. gak respon? klik link ini\nbit.ly/fgmtutor\n\nKontak admin:\nhttp://line.me/R/ti/p/~@nya9070u\noa:\nhttp://line.me/R/ti/p/~@wcf4912l")
        if op.type == 22:
            if wait["leaveRoom"] == True:
                client.leaveRoom(op.param1)
                
        if op.type == 24:
            if wait["leaveRoom"] == True:
                client.leaveRoom(op.param1)
        if op.type == 26:
            msg = op.message
            if msg.text is None:
                return
            elif "/fgmjoin:" in msg.text:
                    aka = msg.text.replace("/fgmjoin:","")
                    link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = link_re.findall(aka)
                    n_links = []
                    for l in links:
                        if l not in n_links:
                            n_links.append(l)
                    for ticket_id in n_links:
                        group = client.findGroupByTicket(ticket_id)
                        client.acceptGroupInvitationByTicket(group.id,ticket_id)
                        client.sendMessage(group.id, "Terima kasih telah mengundang ke grup. ketik /key untuk bantuan. gak respon? klik link ini\nbit.ly/fgmtutor\n\nKontak admin:\nhttp://line.me/R/ti/p/~@nya9070u\noa:\nhttp://line.me/R/ti/p/~@wcf4912l")
        if op.type == 26:
            msg = op.message
            if msg.contentType == 13:
               if wait["wblack"] == True:
                    if msg.contentMetadata["mid"] in wait["commentBlack"]:
                        client.sendMessage(msg.to,"already")
                        wait["wblack"] = False
                    else:
                        wait["commentBlack"][msg.contentMetadata["mid"]] = True
                        wait["wblack"] = False
                        client.sendMessage(msg.to,"decided not to comment")

            elif msg.contentType == 16:
                if msg._from in cekpost:
                    try:
                        ret_ = "====[ Details Post ]===="
                        if msg.contentMetadata["serviceType"] == "GB":
                            contact = client.getContact(msg._from)
                            auth = "\n> Penulis : {}".format(str(contact.displayName))
                        else:
                            auth = "\n> Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
                        purl = "\n> URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
                        ret_ += auth
                        ret_ += purl
                        if "mediaOid" in msg.contentMetadata:
                            object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
                            if msg.contentMetadata["mediaType"] == "V":
                                if msg.contentMetadata["serviceType"] == "GB":
                                    ourl = "\n> Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                    murl = "\n> Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
                                else:
                                    ourl = "\n> Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                    murl = "\n> Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
                                ret_ += murl
                            else:
                                if msg.contentMetadata["serviceType"] == "GB":
                                    ourl = "\n> Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                else:
                                    ourl = "\n> Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                ret_ += ourl
                        if "stickerId" in msg.contentMetadata:
                            stck = "\n> Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
                            ret_ += stck
                        if "text" in msg.contentMetadata:
                            text = "\n> Tulisan : {}".format(str(msg.contentMetadata["text"]))
                            ret_ += text
                        ret_ += ""
                        client.sendMessage(msg.to, str(ret_))
                        cekpost.remove(msg._from)
                    except:
                        client.sendMessage(msg.to, "Post tidak valid")
                        cekpost.remove(msg._from)
            elif msg.contentType == 7: # <-- elif atau if tergantung posisinya di awal apa ditengah
                if msg._from in stikr:
                    msg.contentType = 0
                    contact = client.getContact(msg._from)
                    targets = []
                    targets.append(contact)
                    for target in targets:
                        try:
                            pkg_id = msg.contentMetadata['STKPKGID']
                            filler = "Ini dia link stikernya...\n==================\nline://shop/detail/%s" % (pkg_id)
                            client.sendMessage(msg.to, filler)
                            stikr.remove(msg._from)
                        except:
                            pass
                if msg._from in nilaistk:
                    contact = client.getContact(msg._from)
                    targets = []
                    targets.append(contact)
                    for target in targets:
                        try:
                            ka = list(range(0,100))
                            aa = random.choice(ka)
                            client.sendMessage(msg.to,"Nilai untuk stiker ini adalah " + str(aa))
                            nilaistk.remove(msg._from)
                        except:
                            pass
            elif msg.contentType == 1:
                if msg._from in nilaipic:
                    ka = list(range(0,100))
                    aa = random.choice(ka)
                    client.sendMessage(msg.to,"Nilai untuk gambar ini adalah " + str(aa))
                    nilaipic.remove(msg._from)
            elif msg.contentType == 2:
                if msg._from in nilaivid:
                    ka = list(range(0,100))
                    aa = random.choice(ka)
                    client.sendMessage(msg.to,"Nilai untuk video ini adalah " + str(aa))
                    nilaivid.remove(msg._from)
            elif msg.text is None:
                return
            elif "/key" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,helpMessage)
                    userlimit.append(msg.to)
            elif "/hiburan" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,hibuMessage)
                    userlimit.append(msg.to)
            elif "/fgmbot" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,setiMessage)
                    userlimit.append(msg.to)
            elif "/grup" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,gcMessage)
                    userlimit.append(msg.to)
            elif "/alat" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,toolMessage)
                    userlimit.append(msg.to)
            elif "/kontak" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,contMessage)
                    userlimit.append(msg.to)
            elif "/teks" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,teksMessage)
                    userlimit.append(msg.to)
            elif "/alathelp" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,alatguideMessage)
                    userlimit.append(msg.to)
            elif "/hiburanhelp" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,hibuguideMessage)
                    userlimit.append(msg.to)
            elif "/gruphelp" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,grupguideMessage)
                    userlimit.append(msg.to)
            elif "/kontakhelp" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,kntkguideMessage)
                    userlimit.append(msg.to)
            elif "/tekshelp" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,teksguideMessage)
                    userlimit.append(msg.to)
            elif "/fgmhelp" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,fgmguideMessage)
                    userlimit.append(msg.to)
            elif "/ramadhan" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,puasaMessage)
                    userlimit.append(msg.to)
#--------===---====--------------
            elif msg.text in ["..."]: #Melihat List Group + ID Groupnya (Gunanya Untuk Perintah InviteMeTo:)
              if msg._from in admin:
                akl = client.getGroupIdsInvited()
                gid = client.getGroupIdsJoined()
                rdr = client.getAllContactIds()
                ffd = str(len(rdr))
                ghf = str(len(gid))
                lol = str(len(akl))
                client.sendMessage(msg.to,"Total grup: " + ghf + "\nTotal friends: " + ffd + "/5000" + "Ketunda: " + lol)
            elif "/store" == msg.text.lower():
                client.sendMessage(msg.to,"1. Jasa selfbot\nbit.ly/selfbotfgm\n\n2. Pembuatan nick line emoji\nbit.ly/emojifgm")
#---------------------------------
            elif "/reset" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to, "daftar sider telah direset\nCheckpoint telah di set")
                    try:
                      del wait2['readPoint'][msg.to]
                      del wait2['readMember'][msg.to]
                    except:
                      pass
                    now2 = datetime.now()
                    os.environ['TZ'] = 'BST-7'
                    time.tzset()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = time.strftime("%H:%M:%S")
                    wait2['ROM'][msg.to] = {}
                    userlimit.append(msg.to)

            elif "/sider" == msg.text.lower():
                if msg.to not in userlimit:
                        now2 = datetime.now()
                        nowt = datetime.strftime(now2,"%H:%M:%S")
                        if msg.to in wait2['readPoint']:
                            if wait2["ROM"][msg.to].items() == []:
                                chiya = ""
                            else:
                                chiya = ""
                                for rom in wait2["ROM"][msg.to].items():
                                    #print rom
                                    chiya += rom[1] + "\n"
                                    
                            client.sendMessage(msg.to, "========#SIDERS LIST#========%s\n%s============================\nWaktu Checkpoint: %s WIB\nWaktu sekarang: %s WIB" % (wait2['readMember'][msg.to],chiya,setTime[msg.to],nowt))
                            userlimit.append(msg.to)
                        else:
                            client.sendMessage(msg.to, "Auto setpoin sider\nSilahkan ketik /sider")
                            try:
                              del wait2['readPoint'][msg.to]
                              del wait2['readMember'][msg.to]
                            except:
                              pass
                            now2 = datetime.now()
                            os.environ['TZ'] = 'BST-7'
                            time.tzset()
                            wait2['readPoint'][msg.to] = msg.id
                            wait2['readMember'][msg.to] = ""
                            wait2['setTime'][msg.to] = time.strftime("%H:%M:%S")
                            wait2['ROM'][msg.to] = {}
                            userlimit.append(msg.to)
#------------------RAMADHAN EDITION------------
            elif "/iklanpuasa" in msg.text.lower():
                if msg.to not in userlimit:
                 client.sendMessage(msg.to,"=========LIST IKLAN=========\n1. Sprite\n2. Axis\n3. Frisan Flag\n4. Sirup ABC\n5. Pocari Sweat\n6. Mie Sedap\n7. Dettol\n8. Kecap Sedap\n9. Energen\n10. Nissin Wafer\n11. Promag\n12. Sunlight\n13. Kraft\n14. Coca cola\n15. Indomie\n16. Bimoli\n17. Wadimor\n18. Djarum\n19. Bukalapak\n20. App yg lg dipake skrg :v\n============================\nPilih nomernya\nContoh: /iklan2")
            elif "/iklan" in msg.text.lower():
                if msg.to not in userlimit:
                    see = msg.text.lower().replace("/iklan","")
                    hsh = int(see)
                    aak = iklps[hsh-1]
                    client.sendMessage(msg.to,"https://www.youtube.com/watch?v=" + aak)
            elif "bukber" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Kuy lah di rumah siapa gitu...")
            elif "takjil" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Borong semuanya...")
            elif "ngabuburit" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Ayoklah jangan wacana doang :v")
            elif "buka puasa" == msg.text.lower():
                    kkl = ["Berbukalah dengan yang halal karena yang manis belum tentu halal","Berbukalah dengan yang manis-manis. Asal jangan janji-janji manis mantan ngaco","Berbukalah dengan yang manis-manis. Mantan di siram sirup misalnya *krik*","Berbukalah dengan yang manis-manis. Janji manis mantan misalnya","Berbukalah dengan yang manis-manis. Asal jangan kenangan manis ya. Nanti gak bikin kenyang malah bikin nangis","Selamat berbuka puasa bagi jomblo yang gak ada ngucapin selamat berbuka","Selamat berbuka puasa. Apapun makanan nya, yang penting jangan makan ati. Nyesek iya","Cie yang cuma dapet ucapan selamat berbuka puasa dari brotkes :|","Cie yang nulis status buka puasa biar ada yang ngucapin selamat berbuka ya? pfft ","Selamat berbuka puasa. Jangan langsung makan makanan yang berat-berat dulu ya, seperti batu, besi, dll","Pas puasa pengen makan ini itu, pas buka cukup makan dikit aja uda kenyang. Perut emang susah di tebak :|"]
                    cak = random.choice(kkl)
                    client.sendMessage(msg.to,cak)
            elif "sahur" == msg.text.lower():
                    aha = ["Cie yang tahun lalu sahurnya bareng sama pacar, sekarang sahurnya sendirian. HAHA","Menunggu sahur bagi jomblo itu sudah hal biasa. Karena dia selalu begadang","Jam-jam dimana jomblo alasan nunggu sahur ketika gak bisa tidur :|","Yang pacaran kalo sahur nanti di bangunin pacar. Yang jomblo di bangunin petasan pfft","Sahur dulu gih, abis itu jomblo nya di lanjut lagi","Selain di bangunin petasan, jomblo juga di bangunin broadcast saat sahur :|","Makan sahurnya sih udah, jadian nya yang belom :|","Abis sahur itu enaknya tidur. Asal jangan meniduri ya","Ketika binggung mau bangunin sahur ke siapa. Jomblo biasanya ngetwit 'Sahur sahur'","Sahur itu sarapan yang kepagian, sedangkan buka itu makan malam yang kecepetan :|","Makan sahur itu secukupnya. Cukup nasi aja misalnya :|","Jomblo gak tidur saat nungguin sahur itu karena dia takut ketiduran gak ada yg bangunin.","Kasian ya LDR, mau bawain makanan sahur buat pacar aja harus beli tiket dulu pfft"]
                    gg = random.choice(aha)
                    client.sendMessage(msg.to,gg)
            elif "puasa" == msg.text.lower():
                    ka = ["Godaan teberat di bulan puasa itu bukan ketika temen ngajak makan, tapi ketika mantan ngajak balikan","Sesungguhnya mantan ngajakin balikan mulu itu adalah godaan di bulan puasa","Baca aturan puasa, jika lapar berlanjut, hubungi penjual soto :v","Puasa sebulan aja gak kuat, jomblo bertahun-tahun kuat #persoalan ┒(ˇ_ˇ)┎","Puasa itu jangan malas2an. Lebih baik tidur lagi. Puasa itu jangan banyak mengeluh. Karena puasa itu bukan kotak saran","Puasa tinggal beberapa hari lagi, tapi jomblo nya yg masih lama :|"]
                    gg = random.choice(ka)
                    client.sendMessage(msg.to,gg)
            elif "energen" == msg.text.lower():
                    client.sendMessage(msg.to,"Minumlah energen 1 liter tiap sahur dan berbuka puasa biar kuat puasa seharian")
            elif "sprite" == msg.text.lower():
                    client.sendMessage(msg.to,"Minumlah sprite 6 kaleng tiap sahur dan berbuka puasa biar badan terasa seger seharian puasa")
            elif "indomie" == msg.text.lower():
                    client.sendMessage(msg.to,"Makanlah indomie 5 bungkus tiap sahur dan berbuka puasa biar kenyang tahan lama seharian puasa")
            elif "nastar" == msg.text.lower():
                    client.sendMessage(msg.to,"Keliatan enak tapi kadang2 isinya dikit :v")
            elif "putri salju" == msg.text.lower():
                    client.sendMessage(msg.to,"kue yang terasa adem dimulut...")
            elif "marjan" == msg.text.lower():
                    client.sendMessage(msg.to,"Iklan sirup paling ngeselin tiap puasa dari iklan sirup lainnya :v")
            elif "kebo" == msg.text.lower():
                    client.sendMessage(msg.to,"Paling banyak tiap bulan puasa :v\nBiarin daripada gabut")
#----------------2.1---------------------------
            elif "/cekpost" == msg.text.lower():
                if msg.to not in userlimit:
                    sl = client.getContact(msg._from).displayName
                    client.sendMessage(msg.to,"Silahkan dikirim postnya kak " + sl)
                    cekpost.append(msg._from)
                    userlimit.append(msg.to)
            elif "/chatwa" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"[Cara menggunakan]\n\nKetik /linkwa<spasi><no.telp tujuan>\nContoh: /linkwa 081212345670")
                    userlimit.append(msg.to)
            elif "/linkwa " in msg.text.lower():
                if msg.to not in userlimit:
                    ala = msg.text.lower().replace("/linkwa ","")
                    aaj = ala.replace("0","62",1)
                    client.sendMessage(msg.to,"https://api.whatsapp.com/send?phone=" + aaj)
                    userlimit.append(msg.to)
            elif "/antiflood" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"[Anti Flood System]\nApa itu Anti Flood?\n\nAnti Flood adalah suatu sistem yang berfungsi untuk mengurangi respon bot yang terlalu berlebihan. Biasanya orang yang tidak bijak yang membuat bot respon terlalu berlebihan sehingga bot suka lemot.\n\nBot ini akan silent beberapa detik jika ada satu anggota yang mengirim keyword bot. Waktu silent tidak sampai 10 detik.")
                    userlimit.append(msg.to)
#----------------2.0---------------------------
            elif "/nilaigambar" == msg.text.lower():
                if msg.to not in userlimit:
                    sl = client.getContact(msg._from).displayName
                    client.sendMessage(msg.to,"Silahkan dikirim gambarnya kak " + sl)
                    nilaipic.append(msg._from)
                    userlimit.append(msg.to)
            elif "/nilaivideo" == msg.text.lower():
                if msg.to not in userlimit:
                    sl = client.getContact(msg._from).displayName
                    client.sendMessage(msg.to,"Silahkan dikirim videonya kak " + sl)
                    nilaivid.append(msg._from)
                    userlimit.append(msg.to)
            elif "/nilaistiker" == msg.text.lower():
                if msg.to not in userlimit:
                    sl = client.getContact(msg._from).displayName
                    client.sendMessage(msg.to,"Silahkan dikirim stikernya kak " + sl)
                    nilaistk.append(msg._from)
                    userlimit.append(msg.to)
            elif "/mood @" in msg.text.lower():
                if msg.to not in userlimit:
                    ks = msg.text.lower().replace("/mood @","")
                    ak = list(range(0,100))
                    aa = random.choice(ak)
                    client.sendMessage(msg.to,"Persentase mood " + ks + " adalah " + str(aa) + "%")
                    userlimit.append(msg.to)
            elif "/moodku" in msg.text.lower():
                if msg.to not in userlimit:
                    la = client.getContact(msg._from).displayName
                    ak = list(range(0,100))
                    aa = random.choice(ak)
                    client.sendMessage(msg.to,"Persentase mood " + la + " adalah " + str(aa) + "%")
                    userlimit.append(msg.to)
#------------------1.8-------1.9---------------
            elif "/pendingtag" == msg.text.lower():
                 if msg.to not in userlimit:
                    group = client.getGroup(msg.to)
                    nama = [contact.mid for contact in group.invitee]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Zero \n'
                        client.sendMessage(msg.to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        client.sendMessage(msg.to, "Total {} Mention".format(str(len(nama))))
                        userlimit.append(msg.to)
            elif "/ceksider" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Cek sider (silent reader)\n\nketik:\n* /reset > /sider")
                    userlimit.append(msg.to)
            elif "/listmember" == msg.text.lower():
                if msg.to in lmlmt:
                    client.sendMessage(msg.to, "Fitur ini dibatasi. Tunggu beberapa saat")
                else:
                    kontak = client.getGroup(msg.to)
                    group = kontak.members
                    num=1
                    msgs="========LIST MEMBER========\n"
                    for ids in group:
                        msgs+="\n[%i] %s" % (num, ids.displayName)
                        num=(num+1)
                    msgs+="\n============================\nTotal : %i orang" % len(group)
                    client.sendMessage(msg.to, msgs)
                    lmlmt.append(msg.to)
            elif "/listpending" == msg.text.lower():
                if msg.to in lmlmt1:
                    client.sendMessage(msg.to, "Fitur ini dibatasi. Tunggu beberapa saat")
                else:
                    try:
                        kontak = client.getGroup(msg.to)
                        group = kontak.invitee
                        num=1
                        msgs="========ListPending========\n"
                        for ids in group:
                            msgs+="\n[%i] %s" % (num, ids.displayName)
                            num=(num+1)
                        msgs+="\n============================\nTotal : %i orang\nliat profi member ketik /pendingmem#<no.member>\nContoh: /pendingmem#1" % len(group)
                        client.sendMessage(msg.to, msgs)
                        lmlmt1.append(msg.to)
                    except:
                        client.sendMessage(msg.to,"Tidak ada undangan tertunda")
#-----------------------2.0-----------------------
            elif "/pembuatgrup" == msg.text.lower():
                if msg.to not in userlimit:
                    try:
                        ginfo = client.getGroup(msg.to)
                        la = ginfo.creator.mid
                        client.sendContact(msg.to,la)
                        userlimit.append(msg.to)
                    except:
                        client.sendMessage(msg.to,"Pembuat grup telah hapus akun/reset akun")
                        userlimit.append(msg.to)
#------------------------------------------------
            elif "/mycontact" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendContact(msg.to,msg._from)
                    userlimit.append(msg.to)
            elif "/crtr" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to, "Ini creatornya....")
                    client.sendContact(msg.to,"u16baba09004cd8424cd2d0a0a47da7c6")
                    client.sendMessage(msg.to,"u44b3d1340a7765727507d2aa3cd22b5a")
                    userlimit.append(msg.to)
              
            elif "/fgmkontak" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to, "Ini Botnya...\n1 grup hanya bisa 1 bot ya...")
                    client.sendContact(msg.to,"udb549a2aea0bd9b181d440baec1ef889")
                    client.sendContact(msg.to,"uab9e646523aff014d28162cd65a713ba")
                    userlimit.append(msg.to)

            elif msg.text in ["Leader ori"]:
              client.sendContact(msg.to,"uab8464cbc9dcea652e03784746542538")
            
            elif msg.text in ["Colead ori"]:
              client.sendContact(msg.to,'u66e5cd3afa43ff0e7053395b47192b0f')
            
            elif msg.text in ["Admin ori"]:
              client.sendContact(msg.to,'u700e599409b4f9b008f93e06687d5767')
              
            elif msg.text in ["Penasehat ori"]:
              client.sendContact(msg.to,'u584253cbe46eced0a97a44758a939050')
              
            elif msg.text in ["Emak ori"]:
              client.sendContact(msg.to,'u54fb532a8af80137a87613be7639506c')
            
            elif "/staff " in msg.text:
                dd = msg.text.replace("/staff ","")
                kl = int(dd)
                cc = stafori[kl-1]
                client.sendContact(msg.to,cc)
#-----------------------------------------------
            elif "/pasangan" in msg.text:
                if msg.to not in userlimit:
                    df = msg.text.split("@")
                    sd = df[1]
                    dg = df[2]
                    uy = [" 10% cocok. gaskeun bosque"," 20% cocok. teruskan..."," 30% cocok. kyknya gk cocok deh"," 40% cocok. jangan males atuh. tingkatin lagi"," 50% cocok. kurang setengah nih..."," 60% cocok. lanjutkan"," 70% cocok. never give up"," 80% cocok. ayo bosque"," 90% cocok. sikattttt"," 100% cocok. selamat ya..."," gak cocok. sabar ya wkwkwk"]
                    qw = random.choice(uy)
                    client.sendMessage(msg.to,sd + "dan " + dg + qw)
                    userlimit.append(msg.to)
            elif "/kalender#" in msg.text:
                if msg.to not in userlimit:
                    txt = msg.text.split("#")
                    tgl = int(txt[2])
                    jmlh = int(txt[1])
                    cal = calendar.month(tgl, jmlh)
                    gj = cal.replace(" ","-",7)
                    jk = gj.replace(" ","   ")
                    a = jk.replace("     1","01",1)
                    b = a.replace("   2","02",1)
                    c = b.replace("   3","03",1)
                    d = c.replace("   4","04",1)
                    e = d.replace("   5","05",1)
                    f = e.replace("   6","06",1)
                    g = f.replace("   7","07",1)
                    h = g.replace("   8","08",1)
                    i = h.replace("   9","09",1)
                    j = i.replace(" Tu","Tu",1)
                    k = j.replace(" We"," We",1)
                    l = k.replace(" Th","Th",1)
                    m = l.replace(" Fr"," Fr",1)
                    n = m.replace(" Sa"," Sa",1)
                    o = n.replace(" Su"," Su",1)
                    client.sendMessage(msg.to,"Nih kalendernya. sori sedikit berantakan dari sananya emang kyk gitu wkwkwk\n===========================\n" + o + "===========================")
                    userlimit.append(msg.to)
            elif "/kalender" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Fitur baru...\nCara menggunakan\nKetik /kalender#(bulan)#(tahun)\nContoh: /kalender#1#2018")
                    userlimit.append(msg.to)
#-----------------------------------------------
            elif msg.text in ["aa"]: #Melihat List Group
              if msg._from in admin:
                gids = client.getGroupIdsJoined()
                num = 1
                h = ""
                for i in gids:
                  #####gn = client.getGroup(i).name
                  c = client.getGroup(i)
                  h += "\n " + str(num) + ". " + c.name +"👉" + str(len(c.members)) + "   Mid: " + i
                  num = (num+1)
                h += ""
            elif "/h " in msg.text:
                acc = msg.text.replace("/h ","")
                kontak = client.getGroupIdsJoined()
                ab = int(acc)
                lj = kontak[ab]
                ui = client.getGroup(lj)
                kk = ui.name
                client.sendMessage(msg.to,kk)
            elif "/o " in msg.text:
                acc = msg.text.replace("/o ","")
                kontak = client.getGroupIdsJoined()
                ab = int(acc)
                lj = kontak[ab]
                client.sendMessage(lj,"Maaf disuruh left sama creator")
                client.leaveGroup(lj)
#-----------------------------------------------
            elif msg.text.lower() == '.reboot':
                if msg._from in admin:
                    try:
                        client.sendMessage(msg.to,"Restarting...")
                        restart_program()
                    except:
                        client.sendMessage(msg.to,"Please wait")
                        restart_program()
                        pass
#--------------------------------------------------------            
            elif msg.text in ["runtime"]:
                eltime = time.time() - mulai
                van = "Bot sudah berjalan selama "+waktu(eltime)
                client.sendMessage(msg.to,van)
#------------------------------------------------
            elif "/linkgrup off" == msg.text.lower():
                if msg.toType == 2:
                  if msg.to not in userlimit:
                    group = client.getGroup(msg.to)
                    group.preventJoinByTicket = True
                    client.updateGroup(group)
                    if wait["lang"] == "JP":
                        client.sendMessage(msg.to,"Link/qr grup telah ditutup")
                        userlimit.append(msg.to)
                    else:
                        client.sendMessage(msg.to,"Sukses Menutup QR")
                        userlimit.append(msg.to)
                else:
                    if wait["lang"] == "JP":
                        client.sendMessage(msg.to,"It can not be used outside the group  👈")
                    else:
                        client.sendMessage(msg.to,"Can not be used for groups other than ô€œ")
            elif "/linkgrup on" == msg.text.lower():
                if msg.toType == 2:
                  if msg.to not in userlimit:
                    x = client.getGroup(msg.to)
                    if x.preventJoinByTicket == True:
                        x.preventJoinByTicket = False
                        client.updateGroup(x)
                    gurl = client.reissueGroupTicket(msg.to)
                    client.sendMessage(msg.to,"Link/qr Grup telah dibuka. ini linknya\n===========================\nline://ti/g/" + gurl)
                    userlimit.append(msg.to)
                else:
                    if wait["lang"] == "JP":
                        client.sendMessage(msg.to,"Can't be used outside the group")
                    else:
                        client.sendMessage(msg.to,"Not for use less than group")
#------------------------------------------
            elif "/jumlahteks " in msg.text.lower():
                if msg.to not in userlimit:
                    jarak = msg.text.lower().replace("/jumlahteks ","")
                    fh = str(len(jarak))
                    client.sendMessage(msg.to,"Jumlah teks tersebut adalah " + fh)
                    userlimit.append(msg.to)
            elif "/hurufkecil " in msg.text.lower():
                if msg.to not in userlimit:
                    jarak = msg.text.lower().replace("/hurufkecil ","")
                    if len(jarak) <= 200:
                        fh = jarak.lower()
                        client.sendMessage(msg.to,"ini hasilnya jika hurufnya dikecilin semua\n===========================\n" + fh)
                        userlimit.append(msg.to)
                    else:
                        client.sendMessage(msg.to,"Fitur ini hanya bisa menampung huruf sebesar 200 huruf")
                        userlimit.append(msg.to)
            elif "/hurufbesar " in msg.text.lower():
                if msg.to not in userlimit:
                    jarak = msg.text.lower().replace("/hurufbesar ","")
                    if len(jarak) <= 200:
                        fh = jarak.upper()
                        client.sendMessage(msg.to,"ini hasilnya jika hurufnya dikapital semua\n===========================\n" + fh)
                        userlimit.append(msg.to)
                    else:
                        client.sendMessage(msg.to,"Fitur ini hanya bisa menampung huruf sebesar 200 huruf")
                        userlimit.append(msg.to)
#---------------------------------------------1.7
#--------------------------------- TRANSLATE ------------
            elif "/tr-" in msg.text.lower():
                if msg.to not in userlimit:
                    dt = msg.text.lower().replace("/tr-","")
                    df = dt.split("@")
                    gf = df[1].split(" ", 1 )
                    awal = df[0]
                    akhir = gf[0]
                    kata = gf[1]
                    url = 'https://translate.google.com/m?sl=%s&tl=%s&ie=UTF-8&prev=_m&q=%s' % (awal, akhir, kata.replace(" ", "+"))
                    agent = {'User-Agent':'Mozilla/5.0'}
                    cari_hasil = 'class="t0">'
                    request = urllib2.Request(url, headers=agent)
                    page = urllib2.urlopen(request).read()
                    result = page[page.find(cari_hasil)+len(cari_hasil):]
                    result = result.split("<")[0]
                    client.sendMessage(msg.to,result)
                    userlimit.append(msg.to)
#-----------------------------------------------
#-----------------------------------------------
#--------------------------------------------------------
#-----------------------------------------------
            elif "/idl " in msg.text:
                if msg.to not in userlimit:
                    try:
                        msgg = msg.text.replace('/idl ','')
                        conn = client.findContactsByUserid(msgg)
                        msg.contentType = 13
                        msg.contentMetadata = {'mid': conn.mid}
                        client.sendMessage(msg)
                        userlimit.append(msg.to)
                    except:
                        client.sendMessage(msg.to,"Id tidak ditemukan atau mungkin pencarian id tersebut diblokir oleh pemilik id")
                        userlimit.append(msg.to)
            elif "/idlurl " in msg.text:
                if msg.to not in userlimit:
                    try:
                        msgg = msg.text.replace('/idlurl ','')
                        conn = client.findContactsByUserid(msgg)
                        client.sendMessage(msg.to,"http://line.me/R/ti/p/~" + msgg)
                        userlimit.append(msg.to)
                    except:
                        client.sendMessage(msg.to,"Link tdk dapat ditampilkan karena id tidak ditemukan")
                        userlimit.append(msg.to)
#-----------------------------------------------
            elif "infofood " in msg.text:
                sep = msg.text.split(" ")
                query = text.replace(sep[0] + " ","")
                r = requests.get("https://sites.google.com/macros/exec?service=AKfycbx_-gZbLP7Z2gGxehXhWMWDAAQsTp3e3bmpTBiaLuzSDQSbIFWD&menu=nama_produk&query=" + query)
                data=r.text
                data=json.loads(data)                                
                if data["data"] != []:                                     
                     hasil = "Produk makanan\n"
                     for news in data["data"]:                                          
                         hasil += "\n" + ". Title: " + str(news["title"]) + "\nNomor Sertifikat: " + str(news["nomor_sertifikat"]) + "\nProdusen: " + str(news["produsen"]) + "\nExpired: " + str(news["berlaku_hingga"])
                         hasil += "\n"
                         client.sendMessage(msg.to, str(hasil))
#-----------------------------------------------
#-----------------------------------------------
            elif "/ytsrch " in msg.text.lower():
                if msg.to not in userlimit:
                  ddtxt = msg.text.lower().replace("/ytsrch","")
                  yeye = ddtxt.replace(" ", "+")
                  client.sendMessage(msg.to,"Hasil pencarian:\nKlik link dibawah ini\n================\nhttps://www.youtube.com/results?search_query=" + (yeye))
                  userlimit.append(msg.to)
#-----------------------------------------------
            elif "/playstore " in msg.text.lower():
                if msg.to not in userlimit:
                    ddtxt = msg.text.lower().replace("/playstore ","")
                    yeye = ddtxt.replace(" ", "%20")
                    client.sendMessage(msg.to,"Hasil pencarian:\nKlik link dibawah ini\n================\nhttps://play.google.com/store/search?q=" + (yeye))
                    userlimit.append(msg.to)
#-----------------------------------------------
            elif "/cariweb " in msg.text.lower():
                if msg.to not in userlimit:
                    ddtxt = msg.text.lower().replace("/cariweb ","")
                    yeye = ddtxt.replace(" ", "+")
                    client.sendMessage(msg.to,"Hasil pencarian:\nKlik link dibawah ini\n================\nhttps://www.google.co.id/search?q=" + (yeye))
                    userlimit.append(msg.to)
#-----------------------------------------------
            elif msg.text in ["Remove all chat"]:
                client.removeAllMessages(op.param2)
                client.sendMessage(msg.to,"Removed all chat")
#-----------------------------------------------
            elif "/youtube" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Fitur mencari link video/channel/hasil pencarian youtube\nCara menggunakan\n* Ketik /vidyt <Nama pencarian>\n  Contoh: /vidyt Sepak Bola\n* /ytsrch <Nama pencarian>\n  Contoh: /ytsrch Sepak Bola")
                    userlimit.append(msg.to)
            elif "/translator" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"ketik /tr-<bahasa awal>@<bahasa tujuan>spasi<kata yg ingin ditranslate>\nContoh /tr-id@ja Terima kasih\n\nKode bahasa untuk translate silahkan klik link dibawah ini\nhttp://line.me/R/home/public/post?id=wcf4912l&postId=1151873880203052035")
                    userlimit.append(msg.to)
#-----------------------------------------------
            elif "/clearlimit" == msg.text.lower():
                del lmlmt[:]
                del lmlmt1[:]
#-----------------------------------------------
            elif "/kerangajaib" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Cara menggunakan\n* Ketik '/apakah setelah kata tersebut bebas. Contoh\n\n/apakah saya Ganteng?")
                    userlimit.append(msg.to)

            elif "notice" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"supaya anda mendapat informasi terbaru seputar bot ini ilahkan add oa ini\n\nhttp://line.me/R/ti/p/~@wcf4912l")
                    userlimit.append(msg.to)

            elif "/about" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,aboutMsg)
                    userlimit.append(msg.to)

            elif "/penjwbpertanyaan" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"Bot ini bisa menjawab pertanyaan secara acak. Kata tanya yang bisa kamu tanya adalah sebagai berikut.\n\n* /kapan\n* /dimana\n* /ada apa dengan\n* /kenapa\n* /mengapa\n\nNB: Buat pertanyaannya yang bener biar nyambung jawabannya :D")
                    userlimit.append(msg.to)
#-----------------------------------------------
            elif "/myname" == msg.text.lower():
                if msg.to not in userlimit:
                    contact = client.getContact(msg._from)
                    nama = contact.displayName
                    client.sendMessage(msg.to,nama)
                    userlimit.append(msg.to)
            elif "/mystatus" == msg.text.lower():
                if msg.to not in userlimit:
                    kf = client.getContact(msg._from)
                    path = kf.statusMessage
                    client.sendMessage(msg.to,path)
                    userlimit.append(msg.to)
#----------------------------------------------
            elif "/cekprofilku" in msg.text: 
                if msg.to not in userlimit:
                  n = client.getContact(msg._from)
                  nama = n.displayName
                  stts = ('Hidup','Nikah','Single','Jones','Hode','Nganggur',"Stress","Sultan","Miskin","Badmood")
                  lokas = ('Di bumi','Di darat','Di pantai','Di Goa','Di Laut','Di pulau terpencil',"Di warnet","Ditempat dugem")
                  ctct = ('Tukang kredit','Gamer noob','Nikah seumur hidup','Dokter cinta','Tukang gabut','Tukang Gosip')
                  aktv = ('Liat postingan org','Gabut','Nyider','Like postingan org','Nongkrong','Ngegame',"Dugem","Nge DJ")
                  ting = ('lebih dari 1 mm','50 cm','2 m','1,5 m','4 m','Tak terhingga')
                  bert = ('Sekilo','Seberat pensil','Se ton','50 kg','Seberat sumo','Tak terhingga')
                  btkb = ('Sixpack','segitiga','seperti lidi','Gendut','Ramping','Kotak')
                  hobi = ('Godain mantan','Ngesot dijalan raya','Godain mantan orang','Stalking','Ngelap batu akik','Makan kuaci')
                  pesa = ('Di pertahankan ya..','Se abad yang akan datang harus lebih baik lagi','Terima apa adanya ya....','Yang semangat ya...')
                  a = random.choice(stts)
                  b = random.choice(lokas)
                  c = random.choice(ctct)
                  d = random.choice(aktv)
                  e = random.choice(ting)
                  f = random.choice(bert)
                  g = random.choice(btkb)
                  h = random.choice(pesa)
                  i = random.choice(hobi)
                  client.sendMessage(msg.to,"Profil Seseorang\n\n* Nama: " + nama + "\n* Status: " + a + "\n* Lokasi saat ini: " + b + "\n* Cita-cita: " + c + "\n* Lagi ngapain: " + d + "\n* Tinggi: " + e + "\n* Berat: " + f + "\n* Bentuk tubuh: " + g + "\n* Hobi: " + i + "\n\nPesan: " + h)
                  userlimit.append(msg.to)

            elif "/cekprofil @" in msg.text: 
                if msg.to not in userlimit:
                  nama = msg.text.replace("/cekprofil @", "")
                  stts = ('Hidup','Nikah','Single','Jones','Hode','Nganggur',"Stress","Sultan","Miskin","Badmood")
                  lokas = ('Di bumi','Di darat','Di pantai','Di Goa','Di Laut','Di pulau terpencil',"Di warnet","Ditempat dugem")
                  ctct = ('Tukang kredit','Gamer noob','Nikah seumur hidup','Dokter cinta','Tukang gabut','Tukang Gosip')
                  aktv = ('Liat postingan org','Gabut','Nyider','Like postingan org','Nongkrong','Ngegame',"Dugem","Nge DJ")
                  ting = ('lebih dari 1 mm','50 cm','2 m','1,5 m','4 m','Tak terhingga')
                  bert = ('Sekilo','Seberat pensil','Se ton','50 kg','Seberat sumo','Tak terhingga')
                  btkb = ('Sixpack','segitiga','seperti lidi','Gendut','Ramping','Kotak')
                  hobi = ('Godain mantan','Ngesot dijalan raya','Godain mantan orang','Stalking','Ngelap batu akik','Makan kuaci')
                  pesa = ('Di pertahankan ya..','Se abad yang akan datang harus lebih baik lagi','Terima apa adanya ya....','Yang semangat ya...')
                  a = random.choice(stts)
                  b = random.choice(lokas)
                  c = random.choice(ctct)
                  d = random.choice(aktv)
                  e = random.choice(ting)
                  f = random.choice(bert)
                  g = random.choice(btkb)
                  h = random.choice(pesa)
                  i = random.choice(hobi)
                  client.sendMessage(msg.to,"Profil Seseorang\n\n* Nama: " + nama + "\n* Status: " + a + "\n* Lokasi saat ini: " + b + "\n* Cita-cita: " + c + "\n* Lagi ngapain: " + d + "\n* Tinggi: " + e + "\n* Berat: " + f + "\n* Bentuk tubuh: " + g + "\n* Hobi: " + i + "\n\nPesan: " + h)
                  userlimit.append(msg.to)
#----------------------------------------------
#----------------------------------------------
            elif "/apakah " in msg.text.lower(): 
                if msg.to not in userlimit:
                    quote = ('Ya','Tidak','Gak tau','Bisa jadi')
                    psn = random.choice(quote)
                    client.sendMessage(msg.to,psn)
                    userlimit.append(msg.to)
            elif "/kenapa " in msg.text.lower(): 
                if msg.to not in userlimit:
                    quote = ('dia sedang mempunyai masalah pribadi','dia lagi gabut','memang begitu dari sananya :v','sudah kebiasaan jadi susah ngilanginnya :v','dia sedang bahagia')
                    psn = random.choice(quote)
                    client.sendMessage(msg.to,"Karena " + psn)
                    userlimit.append(msg.to)
            elif "/mengapa " in msg.text.lower(): 
                if msg.to not in userlimit:
                    quote = ('dia sedang mempunyai masalah pribadi','dia lagi gabut','memang begitu dari sananya :v','sudah kebiasaan jadi susah ngilanginnya :v','dia sedang bahagia')
                    psn = random.choice(quote)
                    client.sendMessage(msg.to,"Karena " + psn)
                    userlimit.append(msg.to)
            elif "/kapan " in msg.text.lower(): 
                if msg.to not in userlimit:
                  jawab = ('Hari ini','Besok','lusa','Setelah laut mengering','Sebulan lagi','Setahun lagi')
                  dll = random.choice(jawab)
                  client.sendMessage(msg.to,dll)
                  userlimit.append(msg.to)

            elif "/dimana " in msg.text.lower(): 
                if msg.to not in userlimit:
                  jawao = ('di comberan','di rumah','di luar angkasa','di tempat dugem','dirumah','di tempat nongkrong','di warnet','di arab','di jalan raya')
                  dsb = random.choice(jawao)
                  client.sendMessage(msg.to,dsb)
                  userlimit.append(msg.to)
            
            elif "/ada apa dengan " in msg.text.lower(): 
                if msg.to not in userlimit:
                  jawas = ('lagi badmood kali...','diputusin pacar kali...','gabut kali...','kesel kali')
                  dss = random.choice(jawas)
                  client.sendMessage(msg.to,dss)
                  userlimit.append(msg.to)
#-----------------------------------------------
            elif msg.text in ["Py"]:
                start = time.time()
                elapsed_time = time.time() - start
                client.sendMessage(msg.to, "%sseconds" % (elapsed_time))
#------------------------------------------------------------------
            elif "/jam" == msg.text.lower():
                if msg.to not in userlimit:
                    client.sendMessage(msg.to,"[Cara menggunakan]\n\nKetik /time<spasi><+/-><1-12>\nContoh: /time -4")
                    userlimit.append(msg.to)
            elif "/time " in msg.text.lower():
                if msg.to not in userlimit:
                  ala = msg.text.lower().replace("/time ","")
                  if "-" in ala:
                    al = ala.replace("-","+")
                    os.environ['TZ'] = 'BST' + al
                    time.tzset()
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    month =["January","February","March","April","May","June","July","August","September","October","November","December"]
                    hr = time.strftime('%A')
                    bln = time.strftime('%B')
                    jm = time.strftime('\nJam %T')
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for o in range(len(month)):
                        if bln == month[o]: res = bulan[o]
                    rst = "Hari " + hasil + ", " + time.strftime('%e') + " " + res + " " + time.strftime('%Y') + jm
                    client.sendMessage(msg.to, rst)
                    userlimit.append(msg.to)
                  if "+" in ala:
                    al = ala.replace("+","-")
                    os.environ['TZ'] = 'BST' + al
                    time.tzset()
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    month =["January","February","March","April","May","June","July","August","September","October","November","December"]
                    hr = time.strftime('%A')
                    bln = time.strftime('%B')
                    jm = time.strftime('\nJam %T')
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for o in range(len(month)):
                        if bln == month[o]: res = bulan[o]
                    rst = "Hari " + hasil + ", " + time.strftime('%e') + " " + res + " " + time.strftime('%Y') + jm
                    client.sendMessage(msg.to, rst)
                    userlimit.append(msg.to)
                  else:
                    pass
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
            elif "/linkstiker" == msg.text:
                if msg.to not in userlimit:
                    contact = client.getContact(msg._from)
                    _nametarget = contact.displayName
                    stikr.append(msg._from)
                    client.sendMessage(msg.to,"Silahkan kirim stikernya kak " + _nametarget)
                    userlimit.append(msg.to)
#------------------------------------------------------------------
            elif "/batal" == msg.text:
                if msg.to in qwert:
                    contact = client.getContact(msg._from)
                    _nametarget = contact.displayName
                    client.sendMessage(msg.to,"Perintah dibatalkan")
                    qwert.remove(msg._from)
#--------------------------------------------------
#------------------------------------------------------------------	
#------------------------------------
#--------------------------------------------------------------
            elif "/curinama @" in msg.text:
                if msg.to not in userlimit:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]                
                    mmid = client.getContact(key1)
                    client.sendMessage(msg.to,mmid.displayName)
                    userlimit.append(msg.to)
    #-------------Fungsi Tag All Start---------------#
#------------------------------------------------------------------
            elif "Gt: " in msg.text:
                bc = msg.text.replace("Gbroadcast: ","")
                gid = client.getGroupIdsJoined()
                for i in gid:
                    client.sendMessage(i,"======[BROADCAST]======\n\n"+bc+"\n\n#BROADCAST!!")
#------------------------------------------------------------------
            elif "terima kasih telah mengundang ke grup" in msg.text.lower(): #Bot Ninggalin Group termasuk Bot Induk
                if msg.to in beote:
                    if msg.toType == 2:
                        ginfo = client.getGroup(msg.to)
                        try:
                            client.sendMessage(msg.to,"Ada kembaran aku nih... Kaboor...")
                            client.leaveGroup(msg.to)
                        except:
                            pass
#------------------------------------------------------------------
            elif "/fgmbye" == msg.text.lower(): #Bot Ninggalin Group termasuk Bot Induk
                if msg.toType == 2:
                    ginfo = client.getGroup(msg.to)
                    try:
                        client.sendMessage(msg.to,"Terima kasih telah menggunakan bot ini.\nBye all...")
                        client.leaveGroup(msg.to)
                    except:
                        pass
#------------------------------------------------------------------
#------------------------------------------------------------------
            elif "/curistatus @" in msg.text:            
                if msg.to not in userlimit:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]                
                    contact = client.getContact(key1)
                    path = contact.statusMessage
                    client.sendMessage(msg.to, path)
                    userlimit.append(msg.to)

            elif "/curikontak @" in msg.text:            
                if msg.to not in userlimit:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]                
                    mmid = client.getContact(key1)
                    msg.contentType = 13
                    msg.contentMetadata = {"mid": key1}
                    client.sendMessage(msg)
                    userlimit.append(msg.to)
#------------------------------------------------------------------
#------------------------------------------------------------------
            elif "/gantinamagrup" == msg.text:
                if msg.to not in userlimit:
                    contact = client.getContact(msg._from)
                    _nametarget = contact.displayName
                    qwert.append(msg._from)
                    client.sendMessage(msg.to,"========KONFIRMASI========\nUntuk: " + _nametarget + "\nApakah anda Ingin mengganti nama grup?\n\npilihan:\n* /y <nama grup yg ingin diganti>\n* /batal")
                    userlimit.append(msg.to)

            elif "/y" in msg.text:
                if msg._from in qwert:
                  if msg.toType == 2:
                    try:
                        gs = client.getGroup(msg.to)
                        contact = client.getContact(msg._from)
                        _nametarget = contact.displayName
                        gs.name = msg.text.replace("/y ","")
                        client.updateGroup(gs)
                        client.sendMessage(msg.to,"Nama grup telah diubah")
                        qwert.remove(msg._from)
                    except:
                        client.sendMessage(msg.to,"Namanya diatas 20 huruf kak")
#----------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
        if op.type == 59:
            pass
            
        if op.type == 55:
          try:
            if op.param1 in wait2['readPoint']:
                    os.environ['TZ'] = 'BST-7'
                    time.tzset()
                    jm = time.strftime('%X')
                    Name = client.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n> " + jm + " " + Name
                        if wait['autosider'][op.param1] == True:
                            dr = ["0","1","2","3","4","5","6","7","8","9","10","11","12","e","f","r","h","u","k","l"]
                            gk = random.choice(dr)
                            if "0" in gk:
                                client.sendMessage(op.param1,"Auto check sider")
                            else:
                                pass
                        else:
                            pass
            else:
                client.sendMessage
          except:
             pass
         
        #if op.type == 17:
          #if op.param2 in beote:
            #return
          #ginfo = client.getGroup(op.param1)
          #client.sendMessage(op.param1, "Fitur sambutan disable")
          #print "MEMBER HAS JOIN THE GROUP"


    except Exception as error:
        print (error)


def a2():
    now2 = datetime.now()
    nowT = datetime.strftime(now2,"%M")
    if nowT[14:] in ["10","20","30","40","50","00"]:
        return False
    else:
        return True

def nameUpdate():
    while True:
        try:
        #while a2():
            #pass
            del userlimit[:]
            time.sleep(12)
        except:
            pass
thread2 = threading.Thread(target=nameUpdate)
thread2.daemon = True
thread2.start()

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                oepoll.setRevision(op.revision)
                thread = threading.Thread(target=bot, args=(op,))
                thread.start()
    except Exception as e:
        print(e)
