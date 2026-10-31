import json,re,html
T='/workspace/testimonials-v2/'
s=json.load(open(T+'restructure_spec.json'))
wins=json.load(open('/tmp/wins_map.json'))
CAL='https://calendly.com/madeuwatch/strategy-call-clone'
esc=html.escape
NICHE={ # Jake's list (t1034u); lines marked (inferred) come from the screenshot bio, placeholders are 'Creator'
 'masonjinfu':'Health coach','alexuscazares':'PhD student coach','blueandkim':'Personal branding coach','rhian_marie':'Personal branding coach',
 'owenditzel':'Athlete','maisiesmunch':'Artist','soyjoseperezz':'Lifestyle creator','joshevans_training':'Fitness coach','rileylistonn':'Athlete',
 'kaitdevir':'Lifestyle creator / videographer','brodyriseborough':'Gym owner','masongothard':'Health coach','iamkenyamarie_':'Mindset coach',
 'elijahvane_':'Makeup artist','haleighhock':'Lifestyle creator','alexjbarbas':'Fitness coach','jake.racc':'Lifestyle creator',
 'the.limitlesscoach':'Entrepreneur / health coach','charliebj':'Lifestyle creator','ioihei_':'Olympic athlete','crowncapital._':'Betting company',
 'fitwithmiarae':'Fitness coach','shaun_alisa':'Online coach','surfwithruben_':'Surf coach','koberugless':'Rugby player & coach',
 # earlier verified descriptors (Client Wins Master Doc)
 'itsmarcofontana':'Fitness coaching','claybarrett.official':'Fitness coaching','colby_offutt':'Fascia-release & bodywork education',
 'leanwithduncan':'Fat-loss coaching','jaredto100':'Hybrid-training coaching','surfing_with_grant':'Surf coaching','caelahstanley':'Tech-sales coaching',
 'itsbradyhughes':'Agency','james.dylan.russell':'UGC creator','iam_jamesrussell':'UGC creator','benxmills':'Lifestyle creator','studywithjack_':'Study creator',
 'antoinemarneffe':'Online transformation coach','eabhaom':'Coaching','tearaibryers':'Fitness coaching',
 # placeholders - waiting on Jake
 'stenmeulink':'Creator','aidan.melograna':'Student coach','socraticalexa':'Creator','axel.bustad':'Creator','danielsmyth_':'Creator','claraalessandra_':'Creator','777lachy':'High-ticket sales'}
# Follower profiles: (name, handle, followers shown in the screenshot). Coach accounts are NOT in this list.
FOLL=[
 ('Ben Mills','benxmills',245000),('Colby Offutt','colby_offutt',158000),('Clara Alessandra','claraalessandra_',91600),('Antoine Marneffe','antoinemarneffe',92613),
 ('Clay Barrett','claybarrett.official',66000),('Mason Jinfu','masonjinfu',57077),('Alexus Cazares','alexuscazares',53651),('Sten Meulink','stenmeulink',52900),
 ('Grant Williams','surfing_with_grant',45400),('Blue & Kim','blueandkim',41200),('Kobe Rugless','koberugless',41600),('Ruben Galjaard','surfwithruben_',40900),
 ('Caelah Stanley','caelahstanley',39018),('Marco Fontana','itsmarcofontana',38763),('Shaun Alisa','shaun_alisa',35200),('Owen Ditzel','owenditzel',33600),
 ('Rhian (Rhi Marie)','rhian_marie',29999),('Jose Perez','soyjoseperezz',28404),('Josh Evans','joshevans_training',26737),('Maisie Price','maisiesmunch',24600),
 ('Kait Devir','kaitdevir',23800),('Aidan Melograna','aidan.melograna',23800),('Riley Liston','rileylistonn',23100),('Brody Riseborough','brodyriseborough',22501),
 ('Kenya Werenett','iamkenyamarie_',20988),('James Russell','iam_jamesrussell',19600),('Elijah Avalos','elijahvane_',17199),('Alexandrina','socraticalexa',17000),
 ('Mason Gothard','masongothard',15800),('Jack Rigg','studywithjack_',15939),('Haleigh Hockenberry','haleighhock',14463),('Alex Barbas','alexjbarbas',14418),
 ('Jake Racciatti','jake.racc',13928),('Axel Bustad','axel.bustad',11700),('Mia Stewart','fitwithmiarae',11000),('Oli Andrijasevich','the.limitlesscoach',10863),
 ('Charlie Johnson','charliebj',10853),('Hilary Iong','ioihei_',10233),('Jamar Scarvelis','crowncapital._',10101),('Jared Justian','jaredto100',10000),
 ('Daniel Smyth','danielsmyth_',9150),('Lachie Campbell','777lachy',4999)]
NEWHDR={'kaitdevir','jaredto100','colby_offutt','blueandkim','surfing_with_grant','benxmills','surfwithruben_','claybarrett.official','claraalessandra_','777lachy','koberugless','iam_jamesrussell','maisiesmunch','rileylistonn','masongothard','owenditzel','stenmeulink','aidan.melograna','socraticalexa','axel.bustad','danielsmyth_','fitwithmiarae','shaun_alisa'}
TOTAL_FOLLOWERS=sum(f for _,_,f in FOLL)
def short(n): return f'{n/1e6:.1f}M' if n>=1e6 else f'{round(n/1000)}K'
def clean(n): return re.sub(r'\s*\(.*$','',n).strip()
FC={h:f for _,h,f in FOLL}
FC.update({'eabhaom':110000,'tearaibryers':49200,'iamjakepeterz':68800,'reidseddon':100000,'tessachen.29':62200})
def fmtf(n):
    if n<10000: return f'{n:,}'
    return f'{n/1000:.1f}'.rstrip('0').rstrip('.')+'K'
MISSING=[]
def title(name,handle,niche,where=''):
    t=f'<h3>{esc(name)}'
    if handle:
        f=FC.get(handle)
        if f is None: MISSING.append((where,name,handle))
        t+=f' <span class="h">@{esc(handle)}'+(f' · {fmtf(f)} followers' if f else '')+'</span>'
    else: MISSING.append((where,name,'(no handle)'))
    t+='</h3>'
    if niche: t+=f'<p class="niche">{esc(niche)}</p>'
    return t
# wins
AMT={'Blue & Kim':'$38K in 3 months','Caelah Stanley':'$42K cash collected in a month · $0 → $150K in 2 months','Lachie Campbell':'$100K month in personal profit · $87.4K cash / $128.4K revenue in 30 days',
 'Shaun Alisa':'$27.5K from coaching in 6 weeks · ~$60K cash in 60 days · $10K AUD closed in 7 days · $16K revenue in a day (~$8K cash)','Éabha O\'Mahony':'$22K total revenue','Kobe Rugless':'$4,500 in 8 days',
 'Brady Hughes':'$10.5K MRR · new $3K AUD/mo retainer · $3K AUD day','James Russell':'“$2k away from a $50k month” (his words, 21 Oct 2026) · $5k cash collected PIF by 9am on a Wednesday · 23 hot leads · $14k+ revenue in Aug · 16K followers · 5 brand collabs · $14K in 4 months full-time on content','Julian Zand':'$7.5K in PIFs',
 'Jylise':'$1,200 first sale','Kenya Werenett':'$2,700 first client','Mason':'2 × $3K PIFs','Owen Ditzel':'$3K PIF','Pavle':'3 PIFs in one day (setter)',
 'Rhian':'$4K+ high-ticket client','Riley Liston':'$1,500 first client'}
PRE={'James Russell':['james-russell-50k.jpg','james-russell-aug.jpg'],'Lachie Campbell':['lachie-campbell-100k.jpg'],'Caelah Stanley':['caelah-stanley-150k.jpg'],'Shaun Alisa':['shaun-alisa-27k.jpg','shaun-alisa-10kaud.jpg','shaun-alisa-7.jpg'],'Brady Hughes':['brady-hughes-2.jpg','brady-hughes-3.jpg'],'Julian Zand':['julian-zand-3.jpg']}
BAN={'Duncan Coombs'}
POST={'James Russell':['james-russell-2.jpg']}
cards=[]
for c in s['fin']:
    name=clean(c['name']); h=c['handle']
    if name in BAN: continue
    if name.startswith('Mason'): name='Mason'
    if name.startswith('Pavle'): name='Pavle'
    imgs=PRE.get(name,[])+wins[c['name']]+POST.get(name,[])
    niche=NICHE.get(h) if h else None
    if name=='Blue & Kim': h='blueandkim'; niche=NICHE['blueandkim']
    cards.append((name,h,niche,AMT.get(name,''),imgs))
cards+=[
 ('Ruben Galjaard','surfwithruben_','Surf coach','€15.2K gross volume in a month (+26%)',['ruben-galjaard-1.jpg','ruben-galjaard-2.jpg']),
 ('Grant Williams','surfing_with_grant','Surf coach','$21.5K in sales',['grant-williams-1.jpg']),
 ('Joe Price','joe._.price','Online course','$18,755 course launch',['joe-price-1.jpg']),
 ('Oliver Andrijasevich','the.limitlesscoach','Entrepreneur / health coach','$5K close',['oliver-andrijasevich-1.jpg']),
 ('Leon Frangenberg','','Fitness coach','$5K cash collected',['leon-frangenberg-1.jpg']),
 ('Jared','jaredto100','Hybrid-training coach','$1.5K PIF · first high-ticket client',['jared-1.jpg']),
 ('Aidan Melograna','aidan.melograna','Student coach','$1K close',['aidan-melograna-1.jpg']),
 ('Sander','','Done4U 1-1 client','$1.8K PIF',['sander-1.jpg']),
 ('Marco Fontana','itsmarcofontana','Fitness coach','€3,250 cash collected in a month',['marco-fontana-1.jpg']),
 ('Gabe Marzano','','Done4U client','$100K month in his 3rd month · $0 → $200K in the first quarter',['gabe-marzano-1.jpg','gabe-marzano-2.jpg']),
 ('Te Arai Bryers','tearaibryers','UGC creator & Head of UGC','$40K+ USD cash collected in his first 4 months',['te-arai-1.jpg']),
 ('Jamar Scarvelis','crowncapital._','Betting company','$0 → $400K AUD a month (self-reported)',['jamar-scarvelis-1.jpg']),
]
SORTV={'Jamar Scarvelis':400000,'Gabe Marzano':200000,'Caelah Stanley':150000,'Lachie Campbell':128400,'Shaun Alisa':60000,'Te Arai Bryers':40000,'Blue & Kim':38000,'Éabha O\'Mahony':22000,'Grant Williams':21500,'Joe Price':18755,'Ruben Galjaard':15200,'James Russell':14000,'Brady Hughes':10500,'Julian Zand':7500,'Mason':6000,'Oliver Andrijasevich':5000,'Leon Frangenberg':5000,'Kobe Rugless':4500,'Rhian':4000,'Marco Fontana':3300,'Owen Ditzel':3000,'Pavle':3000,'Kenya Werenett':2700,'Sander':1800,'Riley Liston':1500,'Jared':1500,'Jylise':1200,'Aidan Melograna':1000}
cards.sort(key=lambda c:-SORTV.get(c[0],0))
fin=''
for name,h,niche,amt,imgs in cards:
    sl=''.join(f'<figure class="slide"><img loading="lazy" src="img/wins/{i}" alt="{esc(name)} result screenshot {k+1}" data-full="img/wins/{i}"></figure>' for k,i in enumerate(imgs))
    nav=f'<div class="nav"><button class="prev" aria-label="Previous">‹</button><span class="count">1 / {len(imgs)}</span><button class="next" aria-label="Next">›</button></div>' if len(imgs)>1 else ''
    am=f'<p class="amt">{esc(amt)}</p>' if amt else ''
    fin+=f'<article class="card win" data-n="{len(imgs)}">{title(name,h,niche,'wins')}{am}<div class="frame"><div class="slides">{sl}</div></div>{nav}</article>\n'
NFIN=len(cards)
# follower growth
import os
fol='';split=False
order=sorted(FOLL,key=lambda r:(r[1] not in NEWHDR,-r[2]))
for name,h,f in order:
    cls='hdr' if h in NEWHDR else 'ig'
    assert os.path.exists(f'img/ig/{h}.jpg'),h
    body=f'<div class="frame {cls}"><img loading="lazy" src="img/ig/{h}.jpg" alt="{esc(name)} Instagram profile" data-full="img/ig/{h}.jpg"></div>'
    if cls=='ig' and '</div><div' not in fol[-300:] and not split: fol+='</div><div class="grid flexc" style="margin-top:var(--gap)">'; split=True
    fol+=f'<article class="card fol">{title(name,h,NICHE.get(h),'fol')}{body}</article>\n'
# youtube
YT=[
 ('q_vES40q-lA','20-year-old fitness coach',None,'Fitness coaching','Jake Peters'),
 ('n93ljutcW64','Lachie Campbell','777lachy',None,'Jake Peters'),
 ('7XxBWjo4k9U','Mason',None,None,'Reid Seddon'),
 ('pV8U6-pmeYo','Blue & Kim','blueandkim',None,'Jake Peters'),
 ('RnqlQkUFJKE','Kobe Rugless','koberugless','Athlete coaching','Jake Peters'),
 ('weeMgs0PQfI','Caelah Stanley','caelahstanley','Tech-sales coaching','Jake Peters'),
 ('ZO0ByjkPqZ4',"Éabha O'Mahony",'eabhaom','Coaching','Jake Peters'),
 ('BkZO60E9PeA','TeAri Bryers','tearaibryers','Fitness coaching','Jake Peters'),
]
vt={y['id']:y['title'] for y in s['youtube']}
yt=''
for vid,name,h,niche,by in YT:
    by=next(y['channel'] for y in s['youtube'] if y['id']==vid)
    yt+=f'''<article class="card vid">{title(name,h,niche,'video')}
<button class="vframe" data-yt="{vid}" aria-label="Play: {esc(vt[vid])}"><img loading="lazy" src="img/yt/{vid}.jpg" alt="{esc(vt[vid])}"><span class="play"></span></button>
<p class="vt">{esc(vt[vid])}</p><p class="by">Channel: {esc(by)} · <a href="https://youtu.be/{vid}" target="_blank" rel="noopener">Watch on YouTube ↗</a></p></article>\n'''
CV=[('Lachie Campbell','777lachy','High-ticket sales','lachie-testimonial'),('Colby Offutt','colby_offutt',NICHE['colby_offutt'],'colby-testimonial')]
cvid=''.join(f'<article class="card cvid">{title(n,h,ni,"clientvideo")}<video controls preload="none" playsinline poster="img/vid/{f}.jpg"><source src="img/vid/{f}.mp4" type="video/mp4"></video></article>\n' for n,h,ni,f in CV)
# coaches: (name, role, photo, [(handle, followers label, screenshot)] )
CO=[('Jake Peters','Co-founder · Sales &amp; Strategy','img/coaches/jake.jpg',[('iamjakepeterz','68.8K')]),
    ('ReidBranded','Co-founder · Content Coach','img/coaches/reid.jpg',[('reidseddon','100K'),('reidbranded','5,436')]),
    ('TeAri Bryers','Content Coach · Client Success','img/coaches/teari.jpg',[('tearaibryers','49.2K')]),
    ("Éabha O'Mahony",'Content Coach','img/coaches/eabha.jpg',[('eabhaom','110K'),('eabhabranded','13.4K')]),
    ('Tessa Chen','Client Success Manager (CSM)','img/coaches/tessa.jpg',[('tessachen.29','62.2K')])]
co=''
for n,r,ph,accs in CO:
    av=f'<img src="{ph}" alt="{esc(n)}">'
    fcs=''.join(f'<div class="fc"><b>{c}</b><span><a href="https://www.instagram.com/{h}/" target="_blank" rel="noopener">@{h}</a> followers</span></div>' for h,c,_ in [(h,c,0) for h,c in accs])
    fcs=f'<div class="fcs">{fcs}</div>' if accs else ''
    shots=''.join(f'<img loading="lazy" src="img/coaches/ig-{h}.jpg" alt="@{h} Instagram profile, {c} followers" data-full="img/coaches/ig-{h}.jpg">' for h,c in accs)
    shots=f'<div class="cshots">{shots}</div>' if accs else ''
    ch=(f' <span class="h">@{accs[0][0]} · {accs[0][1]} followers</span>' if accs else '')
    co+=f'<div class="coach"><div class="av">{av}</div><h3>{esc(n)}{ch}</h3><p class="role">{r}</p>{fcs}{shots}</div>\n'
QAV=[('“I’m not an expert yet”', 'You don’t need authority — you need relatability. This explains why documenting beats teaching.', '1zPUU--7N8g'), ('“I’m worried what people will think”', 'Everyone goes through this stage. This breaks down why it doesn’t matter as much as you think.', '0u7XB9SDvg0'), ('“I don’t have time”', 'Content doesn’t need to take over your life. We build systems that take under 30 minutes a day.', '5IsW5jRT3rE'), ('“Why does a personal brand even matter?”', 'Attention is leverage. This shows how personal brands turn into real opportunities and income.', 'MVAVrWVgeUQ'), ('“What’s the cost to get started?”', 'A straight answer on the investment and what it gets you.', 't6_aX5NNYws')]
qa=''.join(f'<article class="card qitem"><h3>{esc(q)}</h3><p>{esc(d)}</p><div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/{v}?rel=0" title="{esc(q)}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></article>\n' for q,d,v in QAV)
page=open('template.html').read()
for k,v in dict(CVID=cvid,COACHES=co,FIN=fin,FOL=fol,YT=yt,CAL=CAL,QA=qa,NFIN=str(NFIN),NFOL=str(len(FOLL)),NYT=str(len(YT))).items():
    page=page.replace('{{'+k+'}}',v)
open('index.html','w').write(page)
print(len(fin),len(FOLL),len(yt),TOTAL_FOLLOWERS);print('MISSING',MISSING)
