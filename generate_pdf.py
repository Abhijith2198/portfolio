"""Create the 20-page, 16:9 portfolio from content/portfolio.json.
Requires reportlab and Pillow. Uses the bundled static font files.
"""
from pathlib import Path
import json, html, shutil, math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from PIL import Image
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'content/portfolio.json').read_text(encoding='utf-8'))
P=D['projects']; W,H=960,540
OUT=ROOT.parent/'Abhijith-U-Portfolio.pdf'
INK='#252525'; PAPER='#FFFFFF'; MUTED='#696969'; LINE='#E1E1E1'; ACID='#E8EFFF'; BLUE='#376ADA'
for name,file in [('Sans','Archivo-Regular.ttf'),('Medium','Archivo-Semibold.ttf'),('Serif','InstrumentSerif-Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,str(ROOT/'assets/fonts'/file)))
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('Abhijith U — Selected design work, 2026');c.setAuthor('Abhijith U');c.setSubject('UI/UX portfolio: RepUp, Meridian, Zomato IA redesign and Verge')
num=0; checks=[]
def rect(x,y,w,h,color,r=0,stroke=None):
    c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke or color))
    if r:c.roundRect(x,H-y-h,w,h,r,stroke=bool(stroke),fill=1)
    else:c.rect(x,H-y-h,w,h,stroke=bool(stroke),fill=1)
def line(x,y,x2,y2,color=LINE):c.setStrokeColor(HexColor(color));c.setLineWidth(.7);c.line(x,H-y,x2,H-y2)
def text(s,x,y,size=16,font='Sans',color=INK):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size*.82,str(s))

def identity_badge(cx,top,diameter=70.34):
    c.saveState();c.translate(cx,H-top);c.scale(diameter/120,diameter/120)
    c.setStrokeColor(HexColor('#253129'));c.setLineWidth(.8);c.circle(0,0,58,stroke=1,fill=0)
    c.setFillColor(HexColor('#253129'));c.setFont('Medium',38);c.drawCentredString(0,-12,'au.')
    for label,is_top in [('UI / UX DESIGN',True),('THINK / MAKE / BUILD',False)]:
        size=10.5;tracking=.15;radius=44
        widths=[pdfmetrics.stringWidth(char,'Medium',size) for char in label]
        total=sum(widths)+tracking*(len(label)-1);position=0
        for char,width in zip(label,widths):
            midpoint=position+width/2
            angle=math.pi/2+(total/2-midpoint)/radius if is_top else 3*math.pi/2+(midpoint-total/2)/radius
            rotation=math.degrees(angle)+(-90 if is_top else 90)
            c.saveState();c.translate(radius*math.cos(angle),radius*math.sin(angle));c.rotate(rotation)
            c.setFont('Medium',size);c.drawString(-width/2,0,char);c.restoreState()
            position+=width+tracking
    c.restoreState()
def para(s,x,y,w,size=15,color=MUTED,font='Sans',leading=None,maxh=None):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.45,textColor=HexColor(color))
    obj=Paragraph(html.escape(s).replace('\n','<br/>'),style);ww,hh=obj.wrap(w,1000)
    if maxh and hh>maxh:raise ValueError(f'Page {num}: text too tall {hh}>{maxh}: {s[:60]}')
    checks.append({'page':num,'y':y,'bottom':y+hh,'text':s[:70]})
    obj.drawOn(c,x,H-y-hh);return hh
def label(s,x=48,y=32,color=MUTED):text(s.upper(),x,y,9.5,'Medium',color)
def heading(s,x=48,y=78,size=42,w=850,color=INK):return para(s,x,y,w,size,color,'Medium',size*1.02)
def photo(file,x,y,w,h,rounding=0):
    path=ROOT/'assets/img'/file
    im=Image.open(path);iw,ih=im.size;scale=min(w/iw,h/ih);ww,hh=iw*scale,ih*scale
    xx=x+(w-ww)/2;yy=y+(h-hh)/2
    if rounding:
        c.saveState();p=c.beginPath();p.roundRect(xx,H-yy-hh,ww,hh,rounding);c.clipPath(p,stroke=0)
    c.drawImage(ImageReader(im),xx,H-yy-hh,ww,hh,mask='auto')
    if rounding:c.restoreState()
    return (xx,yy,ww,hh)
def phone(file,x,y,h=330):
    im=Image.open(ROOT/'assets/img'/file);w=h*im.width/im.height
    rect(x-3,y-3,w+6,h+6,'#253125',12);photo(file,x,y,w,h,9);return w
def start(section,bg=PAPER,dark=False,background_image=None):
    global num
    num+=1;rect(0,0,W,H,bg)
    if background_image:
        c.drawImage(ImageReader(str(ROOT/'assets/img'/background_image)),0,0,W,H,mask='auto')
        c.saveState();c.setFillColor(HexColor('#0C2444'));c.setFillAlpha(.68);c.rect(0,0,W,H,stroke=0,fill=1);c.restoreState()
    label('ABHIJITH U / SELECTED WORK',color='#E6EDFF' if dark else MUTED);label(section,610,32,'#E6EDFF' if dark else MUTED)
    foot='#E6EDFF' if dark else MUTED;line(48,505,912,505,'#B5C9F4' if dark else LINE);text('UI/UX DESIGNER · 2026',48,516,8.5,'Sans',foot);text(f'{num:02d} / 20',865,516,9,'Sans',foot)
def end():c.showPage()
def link(s,url,x,y,w=300,color=INK):
    text(s,x,y,12,'Medium',color);c.linkURL(url,(x,H-y-18,x+w,H-y+2),relative=0,thickness=0)
def facts(p,x=48,y=338,w=350):
    for i,(name,key) in enumerate([('ROLE','role'),('TIMEFRAME','timeline'),('PLATFORM / SCOPE','platform')]):
        yy=y+i*45;label(name,x,yy);para(p[key],x+113,yy-2,w-113,12,INK,maxh=36)
def rotated_photo(file,x,y,w,h,angle=0):
    im=Image.open(ROOT/'assets/img'/file);scale=min(w/im.width,h/im.height);ww,hh=im.width*scale,im.height*scale
    c.saveState();c.translate(x+w/2,H-y-h/2);c.rotate(angle);c.drawImage(ImageReader(im),-ww/2,-hh/2,ww,hh,mask='auto');c.restoreState()

def cover(p,color,kind):
    start(p['number']+' / '+p['name']);c.bookmarkPage(p['slug']);c.addOutlineEntry(p['name'],p['slug'])
    bg={'repup':'#1A2220','meridian':'#D9DFD4','zomato':'#F0F0F0','verge':'#E6E6EF'}[kind]
    fg='#E1F4C6' if kind=='repup' else INK
    rect(28,77,904,374,bg,17)
    label(p['category'],52,97,'#B9C9B1' if kind=='repup' else MUTED)
    if kind=='zomato':
        text('Zomato',52,141,65,'Medium','#AE2B3A');text('IA redesign',54,213,25,'Sans',INK)
        text('Intent.',503,140,53,'Medium');text('Then action.',503,197,53,'Medium','#AE2B3A')
        rect(503,283,119,32,'#AE2B3A',16);text('Order in',535,294,11,'Medium','#FFFFFF')
        rect(635,283,119,32,'#FFFFFF',16);text('Dine out',665,294,11,'Medium',MUTED)
        for i,t in enumerate(p['tabs']):rect(503+i*98,342,89,46,'#FFFFFF',7);text(t['title'],515+i*98,359,11,'Medium')
        para(p['tagline'],54,277,295,22,INK,leading=27,maxh=81)
    else:
        text(p['name'],52,144,66 if kind=='meridian' else 76,'Medium',fg)
        para(p['tagline'],56,241,268,24,fg,'Sans',29,maxh=110)
        if kind=='repup':
            rotated_photo('mockups/repup-insights.png',368,151,173,280,9)
            rotated_photo('mockups/repup-workout.png',727,153,172,280,-9)
            rotated_photo('mockups/repup-home.png',529,105,206,332)
        elif kind=='meridian':
            rotated_photo('mockups/meridian-home.png',411,117,490,296,5)
        else:
            rotated_photo('mockups/verge-start.png',449,121,150,309,8)
            rotated_photo('mockups/verge-review.png',687,126,153,315,-8)
    label(p['status'],56,424,'#B9C9B1' if kind=='repup' else MUTED)
    for i,(lab,key) in enumerate([('ROLE','role'),('TIMEFRAME','timeline'),('PLATFORM','platform')]):
        x=48+i*292;label(lab,x,464);para(p[key],x,480,276,11,INK,leading=14,maxh=21)
    end()
# 01 — A studio stage for the original project mockups
start('PORTFOLIO / 2026','#EEF1EB');c.bookmarkPage('intro')
c.drawImage(ImageReader(str(ROOT/'assets/img'/D['coverBackground'])),0,0,W,H,mask='auto')
text('Selected design work',48,39,16,'Sans',INK);text('Abhijith U',48,62,17,'Medium',INK)
text('Product design / Web design',48,101,10.5,'Sans',INK)
identity_badge(867,67)
c.saveState();c.setFillColor(HexColor('#61745B'));c.setFillAlpha(.09);c.ellipse(103,H-403,861,H-373,stroke=0,fill=1);c.restoreState()
platform=c.beginPath();platform.moveTo(138,H-347);platform.lineTo(822,H-347);platform.lineTo(856,H-375);platform.lineTo(104,H-375);platform.close()
c.setFillColor(HexColor('#F6F5EF'));c.drawPath(platform,stroke=0,fill=1)
rect(104,375,752,15,'#D1D0C7');line(104,375,856,375,'#FFFFFF')
photo('mockups/meridian-home.png',176,116,403,243)
photo('mockups/verge-review.png',690,193,81,166)
text('Portfolio',44,400,100,'Medium',INK)
for i,proj in enumerate(P):
    x=48+i*221;text(proj['number']+' / '+proj['name'],x,512,10,'Sans',INK);c.linkRect('',proj['slug'],(x,12,x+202,34),relative=0,thickness=0)
end()
# 02 — About
start('ABOUT / FROM SYSTEMS TO PEOPLE');text('Hello!',48,79,68,'Medium');text('I’m Abhijith.',48,151,37,'Medium')
para(D['about'][0],48,213,397,14.5,leading=21,maxh=128);para(D['about'][1],48,357,397,14.5,leading=21,maxh=123)
rect(493,206,419,277,'#F1F1F1',16);label('EXPERIENCE',516,227)
yy=253
for v in D['experience']:text(v['title'],516,yy,15,'Medium');text(v['detail'],516,yy+22,11.5);yy+=58
label('EDUCATION',516,374);para('M.Tech · Robotics and Automation\nB.Tech · Electrical and Electronics Engineering\nUX/UI Design certification · Intellipaat',516,397,370,12.5,leading=21,maxh=73)
end()
# 03–07 — RepUp
p=P[0];cover(p,'#0C392A','repup')
start('01 / REPUP / RESEARCH');heading('Clarity is part of the workout.',size=45)
para(p['problem'],48,145,590,16,maxh=104)
for i,m in enumerate(p['research']):
    x=48+i*221;line(x,279,x+194,279);text(m['value'],x,296,55,'Medium');para(m['label'],x,359,184,13)
rect(48,405,864,77,BLUE,13);para('“'+p['quote']+'”',70,420,811,16,PAPER,leading=22,maxh=56)
para(p['researchNote'],673,147,237,11.5,leading=17,maxh=120);end()
start('01 / REPUP / STRUCTURE');heading('Map the loop before the screens.',size=42)
for i,s in enumerate(p['process']):
    y=164+i*109;label('0'+str(i+1),48,y);text(s['title'],82,y-2,19,'Medium');para(s['text'],82,y+28,310,12.5,leading=17,maxh=68)
rect(422,157,490,305,'#F1F1F1',15);photo('repup/board-ia.webp',435,177,464,265)
label('SIX SECTIONS / THREE CORE JOURNEYS',438,474);end()
start('01 / REPUP / KEY DECISIONS');heading('A shorter path to action.',size=43)
for i,(decision,file) in enumerate(zip(p['decisions'],['home.png','insights.webp','fitness-level.webp'])):
    x=48+i*295;phone('repup/'+file,x,165,237);label('0'+str(i+1),x+128,170);para(decision['title'],x+128,197,143,18,INK,'Medium',21,maxh=84);para(decision['text'],x,424,264,11.5,leading=16,maxh=66)
end()
start('01 / REPUP / FINAL SCREENS');heading('One visual system. A daily rhythm.',size=41)
for i,file in enumerate(['home.png','todays-workout.webp','progress.webp','profile.webp','upgrade.webp']):phone('repup/'+file,52+i*134,164,255)
rect(736,160,176,312,ACID,14);label('WHAT I’D DO NEXT',752,179);para(p['next'],752,209,143,12.5,INK,leading=18,maxh=226)
label('POPPINS / ICONIFY / 4 PX SPACING SCALE',48,444);link('Explore all 23 screens online', 'https://abhijith2198.github.io/repup.html',48,470,300);end()
# 08–11 — Meridian
p=P[1];cover(p,'#E6EBE2','meridian')
start('02 / MERIDIAN / INTENT & PROCESS');heading('A service, not a catalogue.',size=44)
para(p['problem'],48,147,395,15,leading=22,maxh=119)
for i,s in enumerate(p['process']):
    y=272+i*75;label('0'+str(i+1),48,y);text(s['title'],78,y-2,16,'Medium');para(s['text'],78,y+23,358,11.5,leading=16,maxh=48)
rect(482,146,430,324,'#F1F1F1',14);photo('meridian/home-routes.webp',494,160,406,285);label('SIGNATURE ROUTES / AFTER MENTOR REVIEW',499,453);end()
start('02 / MERIDIAN / KEY DECISIONS');heading('Let the brand guide the interface.',size=41)
photo('meridian/home-hero.webp',48,151,527,310,9)
for i,s in enumerate(p['decisions']):
    y=157+i*113;label('0'+str(i+1),614,y);para(s['title'],645,y-2,259,18,INK,'Medium',21,maxh=45);para(s['text'],614,y+47,298,11.5,leading=16,maxh=64)
label('1200 PX INQUIRY BAR / HAND-DRAWN ROUTE / COORDINATES',48,477);end()
start('02 / MERIDIAN / FINAL SCREENS');heading('An editorial world, across sizes.',size=42)
rect(48,156,408,293,'#F1F1F1',3);photo('meridian/macbook.webp',54,161,395,282)
phone('meridian/mobile-hero.webp',490,164,283);phone('meridian/mobile-collection.webp',643,164,283)
para(p['next'],798,170,114,12,INK,leading=17,maxh=291)
label('JOURNAL / DESKTOP',48,465);label('HOMEPAGE / MOBILE',490,465);label('NEXT',798,145);end()
# 12–15 — Zomato
p=P[2];cover(p,'#F8EBEC','zomato')
start('03 / ZOMATO / AUDIT');heading('When everything is a destination.',size=42)
para(p['problem'],48,145,471,16,maxh=132)
issues=['Verticals compete for navigation','Content overload on Home','Promotions blur the hierarchy','Navigation changes across updates','Grocery redirects to a separate app']
for i,s in enumerate(issues):line(48,298+i*34,521,298+i*34);text('0'+str(i+1),48,308+i*34,10,'Medium','#BC233B');text(s,83,305+i*34,14)
rect(568,147,344,323,INK,18);label('DESIGN QUESTION',591,170,'#C6D2C0');para('What did you\ncome here to do?',591,218,270,38,PAPER,'Medium',42,maxh=145);para('Use intent to organize the experience before introducing more content.',591,370,274,16,'#C6D2C0',maxh=90);end()
start('03 / ZOMATO / PROPOSED ARCHITECTURE');heading('Four destinations. Clear responsibilities.',size=38)
for i,t in enumerate(p['tabs']):
    x=48+i*221;rect(x,175,201,223,'#FFFFFF',13,LINE);rect(x,175,201,55,'#F9E1E5',13);text(t['title'],x+19,192,22,'Medium');para('\n'.join(t['items']),x+19,251,160,13,leading=27,maxh=130)
rect(48,422,864,60,INK,12);para('Blinkit and District remain reachable through clearly signposted deep links, outside the core navigation.',70,438,807,15,PAPER,leading=21,maxh=43);end()
start('03 / ZOMATO / ORDERING FLOW');heading('Two ways in. One ordering journey.',size=40)
for i,s in enumerate(p['flow']):
    col=i%3;row=i//3;x=48+col*185;y=170+row*94;rect(x,y,167,76,'#F7ECEE',10);label(f'0{i+1}',x+15,y+13,'#BC233B');para(s,x+15,y+36,137,14,INK,'Medium',18,maxh=36)
rect(636,170,276,265,ACID,14);label('WHAT I’D DO NEXT',658,194);para(p['next'],658,226,230,14,INK,leading=21,maxh=192)
para('Card sorting, tree-testing methods and progressive disclosure informed the proposal. No quantitative validation results are recorded in the supplied case study.',48,461,856,10.5,leading=15,maxh=32);end()
# 16–18 — Verge
p=P[3];cover(p,'#E9E4F1','verge')
start('04 / VERGE / FOUR STEPS');heading('Make space for a more honest answer.',size=39)
names=['Name it','Prioritize','Reflect','Review']
for i,name in enumerate(names):
    x=49+i*221;phone(f'verge/step-{i+1}.webp',x+25,158,281);label('0'+str(i+1),x,459,'#796786');text(name,x+29,454,19,'Medium')
end()
start('04 / VERGE / DECISIONS & NEXT STEPS');heading('A reflection should leave room.',size=43)
para(p['problem'],48,146,852,17,maxh=80)
for i,s in enumerate(p['decisions']):
    x=48+i*294;line(x,234,x+270,234);label('0'+str(i+1),x,250);para(s['title'],x,276,257,21,INK,'Medium',24,maxh=53);para(s['text'],x,332,257,12,leading=17,maxh=91)
rect(48,436,864,57,ACID,10);label('NEXT',63,447);para(p['next'],118,447,776,11.5,INK,leading=16,maxh=38)
end()
# 19 — Shared editorial field notes
start('FIELD NOTES / EXPLORATIONS')
text('Behind',48,94,66,'Medium');text('the work.',48,163,66,'Medium')
label('DETAILS THAT CARRY AN IDEA',48,250)
rotated_photo('mockups/repup-home.png',49,275,99,169,-5)
rotated_photo('mockups/meridian-home.png',157,308,247,149,4)
label('REPUP / MERIDIAN',48,473)
for i,n in enumerate(D['fieldNotes']):
    y=98+i*204;line(465,y-14,912,y-14);text(n['number'],465,y+6,16,'Sans',MUTED)
    label(n['tag'],515,y+6)
    para(n['title'],515,y+35,391,23,INK,'Medium',26,maxh=56)
    para(n['text'],515,y+102,391,12.5,MUTED,leading=18,maxh=91)
end()
# 20 — Contact
start('CONTACT / LET’S TALK',BLUE,True,background_image='identity/sky-cover.webp')
text('Have something in mind?',48,91,18,'Sans','#FFFFFF')
text('Let’s talk.',40,150,144,'Medium','#FFFFFF')
para('I’m open to UI/UX designer and UI developer roles.',48,310,795,21,'#FFFFFF',maxh=60)
line(48,364,912,364,'#B5C9F4')
link(D['email'],'mailto:'+D['email'],48,388,380,'#FFFFFF')
link('Portfolio / abhijith2198.github.io','https://abhijith2198.github.io/',48,439,410,'#FFFFFF')
link('Behance / abhijithuvishnu','https://www.behance.net/abhijithuvishnu',493,439,400,'#FFFFFF')
link('GitHub / Abhijith2198','https://github.com/Abhijith2198',493,478,400,'#FFFFFF')
text(D['location'],48,478,12,'Sans','#FFFFFF');end()
assert num==20
c.save();shutil.copy2(OUT,ROOT/'assets/Abhijith-U-Portfolio.pdf')
print(f'Created {OUT} ({OUT.stat().st_size:,} bytes), {num} pages, 16:9.')
print('Text blocks near page boundary:',[q for q in checks if q['bottom']>499])
