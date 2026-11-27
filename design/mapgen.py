import re
p='design/prototype.html';s=open(p).read()
# official names/numbers (deu.ac.kr campus map). Positions: Naver Map labels; * = placed from the school guide map (estimate)
B=[('23','정보공학관',803,127),('21','건윤관',695,232),('20','산학협력관',682,322),('22','공학관',760,403),('17','음악관',425,363),
   ('19','지천관',610,438),('18','창의관',610,518),('16','생활과학관',330,517),('15','의료보건관',330,646),('12','중앙도서관',560,722),
   ('11','효민체육관',760,690),('13','성파글로벌관',330,775),('14','제2효민생활관',245,705),('25','학생군사교육단',800,790),
   ('8','수덕전',525,860),('10','제2인문관',680,870),('9','제1인문관',660,975),('26','행복기숙사',245,860),
   ('5','국제관',205,950),('7','상영관',470,1015),('6','동의스포츠센터',470,1085),('','효민원',300,1055),
   ('3','상경관',205,1150),('1','대학본관',360,1180),('2','법정관',520,1205),('24','제1효민생활관',905,575)]
FS=22
def wd(n,nm): return (len(nm)+(len(n)*0.6+0.5 if n else 0))*FS*0.98+28
roads=['M490 -40 L490 240 L492 450','M492 450 L470 600 L458 760 L455 860 L440 990 L418 1120 L408 1215',
       'M430 420 L360 420 L330 620 L320 900 L290 1110 L180 1100','M180 1100 L540 1140 L545 1250 L500 1300 L360 1265 L180 1265',
       'M330 1205 L520 1235','M440 990 L490 1035 L572 985 L640 900 L720 640 L765 640','M765 640 L820 600 L880 520 L890 320',
       'M492 450 L670 455 L720 370 L770 250 L800 90','M490 240 L510 330 L640 345 L655 250','M320 900 L455 880']
def campus(gid,rot=0):
    g=[f'<g id="{gid}">','<rect x="-600" y="-600" width="2300" height="2700" fill="#e2f7e6"/>',
       '<path d="M190 70 L470 0 L500 250 L520 330 L640 120 L780 30 L860 80 L900 300 L1010 560 L900 800 L760 900 L640 1050 L560 1320 L300 1460 L170 1300 L160 900 L210 620 L380 300 Z" fill="#d6f0dc"/>']
    def lab(x,y,txt,fs,col):
        t=f' transform="rotate({rot} {x} {y})"' if rot else ''
        return f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="{col}"{t}>{txt}</text>'
    g.append('<ellipse cx="928" cy="685" rx="80" ry="62" fill="#bfe8c6" stroke="#fff" stroke-width="3"/>'+lab(928,685,'효민축구장',16,'#3d6b4a'))
    g.append('<ellipse cx="350" cy="1350" rx="80" ry="58" fill="#bfe8c6" stroke="#fff" stroke-width="3"/>'+lab(350,1350,'효민야구장',16,'#3d6b4a'))
    g.append('<ellipse cx="380" cy="935" rx="40" ry="16" fill="#bfe3f7"/>'+lab(378,960,'혜안지',14,'#3d5b6b'))
    g.append('<rect x="560" y="1020" width="50" height="58" rx="12" fill="#bfe3f7" transform="rotate(25 585 1049)"/>'+lab(585,1090,'정심정',14,'#3d5b6b'))
    for d in roads: g.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append('<circle cx="485" cy="490" r="26" fill="#fff"/><circle cx="485" cy="490" r="12" fill="#bfe8c6"/><circle cx="408" cy="1215" r="16" fill="#fff"/>')
    for n,nm,x,y in B:
        w=wd(n,nm); t=f' transform="rotate({rot} {x} {y})"' if rot else ''
        g.append(f'<g class="bld"{t}><rect x="{x-w/2:.0f}" y="{y-22}" width="{w:.0f}" height="44" rx="16" fill="#c9f0d4" stroke="#fff" stroke-width="3"/>'
                 f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="{FS}" font-weight="800" fill="#1d2b28">'+(f'<tspan font-weight="900" fill="#0e7f6c">{n}</tspan> ' if n else '')+f'{nm}</text></g>')
    for x,y in [(510,470),(453,858),(432,926),(417,1093)]:
        t=f' rotate({rot})' if rot else ''
        g.append(f'<g transform="translate({x} {y}){t}"><rect x="-11" y="-11" width="22" height="22" rx="6" fill="#fff" stroke="#4a90d9" stroke-width="2.5"/><text y="5" text-anchor="middle" font-size="12">🚌</text></g>')
    g.append(lab(430,34,'정문 방향 ↑' if not rot else '정문 방향',15,'#5b6b67'))
    g.append('</g>')
    return ''.join(g)
# overlap check
bx=[(x-wd(n,nm)/2,y-22,x+wd(n,nm)/2,y+22,nm) for n,nm,x,y in B]
ov=[(a[4],b[4]) for i,a in enumerate(bx) for b in bx[i+1:] if a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]]
print('overlaps',ov)
H=184  # heading on 2.0 (travel direction, degrees clockwise from north)
a=s.index('<defs>');b=s.index('</defs>',a)
s=s[:a]+'<defs>'+campus('campus')+campus('campusR',H)+s[b:]
# ---- overlays ----
DEST=lambda rot=0: (f'<g{f" transform=\"rotate({rot} 660 975)\"" if rot else ""}><rect x="574" y="947" width="172" height="56" rx="20" fill="#ff9f6e" stroke="#fff" stroke-width="5"/><text x="660" y="984" text-anchor="middle" font-size="26" font-weight="900" fill="#1d2b28">9 제1인문관</text>'
                     '<rect x="612" y="902" width="96" height="38" rx="19" fill="#1d2b28"/><text x="660" y="928" text-anchor="middle" font-size="19" font-weight="800" fill="#fff">목적지</text></g>')
MAIN='M498 478 L470 600 L458 760 L455 860 L440 990 L490 1035 L600 990'
SC_LIB=('M470 600 L470 690 L530 712','M530 712 L590 735','M590 735 L640 830 L655 945')   # outdoor, indoor(EV 5F), outdoor
SC_SUD=('M458 760 L470 848 L500 858','M500 858 L555 866','M555 866 L630 900 L650 945')
def tag(x,y,txt,rot=0):
    t=f' transform="rotate({rot} {x} {y})"' if rot else ''
    w=len(txt)*15+20
    return f'<g{t}><rect x="{x-w/2}" y="{y-16}" width="{w}" height="32" rx="16" fill="#fff" stroke="#ff9f6e" stroke-width="2.5"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="16" font-weight="800" fill="#9a4a1c">{txt}</text></g>'
def sc_paths(sc,w=9,hl=False):
    o,i,o2=sc; col='#14a38b' if hl else '#ff9f6e'
    return (f'<path d="{o}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {"" if hl else "stroke-dasharray=\"2 12\""}/>'
            f'<path d="{i}" fill="none" stroke="#ff9f6e" stroke-width="{w+2}" stroke-dasharray="3 11" stroke-linecap="round"/>'
            f'<path d="{o2}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {"" if hl else "stroke-dasharray=\"2 12\""}/>')
ME_UP='<path d="M0 0 L-26 -64 A68 68 0 0 1 26 -64 Z" fill="#2f6fe4" fill-opacity=".3"/><circle r="32" fill="#2f6fe4" fill-opacity=".16"/><circle r="13" fill="#2f6fe4" stroke="#fff" stroke-width="5"/>'
ME=lambda x,y,ang: f'<g transform="translate({x} {y}) rotate({ang})">{ME_UP}</g>'
# 2.1 amenity pins follow building list
AMB={'대학본관':['🏦'],'국제관':['🏪'],'공학관':['🏪','☕'],'제2인문관':['🏪','☕'],'수덕전':['🏪','☕'],'상경관':['🏪']}
pins=''
for n,nm,x,y in B:
    for k,e in enumerate(AMB.get(nm,[])):
        pins+=f'<g transform="translate({x+wd(n,nm)/2-4+k*34} {y-26})"><circle r="16" fill="#fff" stroke="#ff9f6e" stroke-width="3"/><text y="6" text-anchor="middle" font-size="17">{e}</text></g>'
svg21=('<svg viewBox="200 330 640 560" preserveAspectRatio="xMidYMid slice" role="img" aria-label="동의대 가야캠퍼스 지도와 내 위치">'
       f'<use href="#campus"/><g class="ampins">{pins}</g>'
       f'<g data-v-svg="me">{ME(498,478,180)}<rect x="522" y="470" width="88" height="32" rx="16" fill="#fff"/><text x="566" y="492" text-anchor="middle" font-size="16" font-weight="800" fill="#1d2b28">내 위치</text></g></svg>')
svg11=('<svg viewBox="250 450 560 680" preserveAspectRatio="xMidYMid meet" role="img" aria-label="목적지 제1인문관, 바깥길과 엘리베이터 지름길 두 개">'
       '<use href="#campus"/>'
       f'<path d="{MAIN}" fill="none" stroke="#0e7f6c" stroke-width="7" stroke-dasharray="2 14" stroke-linecap="round" stroke-linejoin="round"/>'
       +sc_paths(SC_LIB,7)+sc_paths(SC_SUD,7)+tag(650,690,'도서관 EV 5층')+tag(600,820,'수덕전 EV 5층')
       +DEST()+ME(498,478,180)+'</svg>')
# 2.0 heading-up: me fixed at bottom-centre, map rotated so travel direction points up
mx,my=470,600; VW,VH=560,470
rot=f'rotate({-H} {mx} {my})'
svg20=(f'<svg viewBox="{mx-VW/2} {my-VH*0.70:.0f} {VW} {VH}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="경로 안내 지도, 바라보는 방향이 위쪽">'
       f'<g transform="{rot}"><use href="#campusR"/>'
       '<path d="M498 478 L470 600" fill="none" stroke="#b9c9c4" stroke-width="12" stroke-linecap="round"/>'
       '<g data-v-svg="m1"><path d="M470 600 L458 760 L455 860 L440 990 L490 1035 L600 990" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/><path d="M470 600 L458 760 L455 860 L440 990 L490 1035 L600 990" fill="none" stroke="#14a38b" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
       +sc_paths(SC_LIB,7)+sc_paths(SC_SUD,7)+tag(660,700,'지름길 도서관 EV 5층',H)+tag(610,830,'지름길 수덕전 EV 5층',H)+'</g>'
       '<g data-v-svg="m2">'+sc_paths(SC_LIB,11,True)+tag(660,700,'엘리베이터 5층',H)+'</g>'
       '<g data-v-svg="m3"><path d="M470 600 L458 760" fill="none" stroke="#14a38b" stroke-width="11" stroke-linecap="round"/>'+sc_paths(SC_SUD,11,True)+tag(610,830,'엘리베이터 5층',H)+'</g>'
       +DEST(H)+'</g>'
       f'<g transform="translate({mx} {my})">{ME_UP}</g></svg>')
def rep(s,mark,new):
    i=s.index(mark);a=s.index('<svg',i);b=s.index('</svg>',a)+6;return s[:a]+new+s[b:]
s=rep(s,'id="2.1"',svg21);s=rep(s,'id="1.1"',svg11);s=rep(s,'id="2.0"',svg20)
open(p,'w').write(s)
