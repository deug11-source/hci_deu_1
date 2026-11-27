# 제1인문관 층별 평면도 (건물 층별 안내도 사진 기준). 방 순서와 종류만 따르고, 크기는 비율로 맞춘 그림이에요.
import re
C={'L':'#ddc9f0','P':'#f8cdd3','R':'#f7d98b','A':'#f2ea9c','G':'#cdeedd','WC':'#ffffff','ST':'#eef3f1','O':'#ffffff'}
F={
 6:(['WC1','612 L2','611 L2.5','610 L2.5','609 R1','WC1','608 R1','607 R1'],['ST1','601 P2.5','602 L2','603 L2','ST1','604 R1','605 R1','606 R1']),
 5:(['WC1','515 P1','514 P2','513 P1','512 A2','511 R1','510 R1','WC1','509 R1','508 R1'],['ST1','501 L2','502 L1','503 P2','504 L2','ST1','505 R1','506 R1','507 R1']),
 4:(['WC1','415 L3','414 L2.5','413 R1','412 R1','411 R1.2','WC1','410 R1','409 R1.2'],['ST1','401 P3','402 G1','403 R1','404 R1','405 R1','ST1.2','406 R1','407 R1','408 R1']),
 3:(['WC1','316 P1','315 P1','314 L2','313 A1','312 P1','310 P2','WC1','309 R1','308 R1'],['ST1','301 P0.8','301-1 P1.3','- P0.5','302 L2.5','303 P2.3','ST1','305 R1','306 R1','307 R1']),
 2:(['WC1','211-1 G1','211 G1','210-1 G1','210 G1','209 G1','208 L3','WC1','207 R1','206 R1'],['ST1','201 P2.5','202 L2.5','OPEN O2','ST1','203 P2','204 P1']),
 1:(['- O1'],['ST1','101 G4','입구 O1.6','ST1','103 G2','104 G0.8']),
}
X0,X1=10,590; TOP=(14,154); COR=(154,200); BOT=(200,340)
def parse(t):
    m=re.match(r'(\S+)\s+(\S+?)([\d.]+)$',t)
    if m: return m.group(1),m.group(2),float(m.group(3))
    k=re.match(r'([A-Z]+)([\d.]+)$',t); return k.group(1),k.group(1),float(k.group(2))
def row(items,y0,y1,dest):
    ps=[parse(t) for t in items]; tot=sum(w for _,_,w in ps); x=X0; out=[]; pos={}
    for name,typ,w in ps:
        ww=(X1-X0)*w/tot; fill=C.get(typ,'#fff')
        if name==dest: fill='#ff9f6e'
        if typ=='ST':
            out.append(f'<rect x="{x:.0f}" y="{y0}" width="{ww:.0f}" height="{y1-y0}" fill="{fill}" stroke="#9fb3ad" stroke-width="2"/>'+''.join(f'<line x1="{x+6:.0f}" x2="{x+ww-6:.0f}" y1="{y0+12+i*11}" y2="{y0+12+i*11}" stroke="#9fb3ad" stroke-width="2"/>' for i in range((y1-y0-14)//11)))
        elif typ=='WC':
            out.append(f'<rect x="{x:.0f}" y="{y0}" width="{ww:.0f}" height="{y1-y0}" fill="#fff" stroke="#9fb3ad" stroke-width="2"/><text x="{x+ww/2:.0f}" y="{(y0+y1)/2+6:.0f}" text-anchor="middle" font-size="16">🚻</text>')
        elif name=='-':
            out.append(f'<rect x="{x:.0f}" y="{y0}" width="{ww:.0f}" height="{y1-y0}" fill="{fill}" stroke="#9fb3ad" stroke-width="2"/>')
        else:
            sw=4 if name==dest else 2
            out.append(f'<rect x="{x:.0f}" y="{y0}" width="{ww:.0f}" height="{y1-y0}" fill="{fill}" stroke="{"#fff" if name==dest else "#9fb3ad"}" stroke-width="{sw}"/>')
            if typ=='O' and name=='OPEN': out.append(f'<line x1="{x:.0f}" y1="{y0}" x2="{x+ww:.0f}" y2="{y1}" stroke="#9fb3ad" stroke-width="2"/><line x1="{x+ww:.0f}" y1="{y0}" x2="{x:.0f}" y2="{y1}" stroke="#9fb3ad" stroke-width="2"/>')
            elif ww>=len(name)*15+8: out.append(f'<text x="{x+ww/2:.0f}" y="{(y0+y1)/2+9:.0f}" text-anchor="middle" font-size="26" font-weight="900" fill="#1d2b28">{name}</text>')
            else:
                cx,cy=x+ww/2,(y0+y1)/2
                out.append(f'<text x="{cx:.0f}" y="{cy+8:.0f}" text-anchor="middle" font-size="24" font-weight="900" fill="#1d2b28" transform="rotate(-90 {cx:.0f} {cy:.0f})">{name}</text>')
        pos[name]=(x,ww); x+=ww
    return ''.join(out),pos
def plan(n,dest=None,me=None,route=False):
    top,bot=F[n]
    t,tp=row(top,*TOP,dest); b,bp=row(bot,*BOT,dest)
    s=[f'<svg viewBox="0 0 600 380" role="img" aria-label="제1인문관 {n}층 평면도">',
       f'<rect x="{X0}" y="{TOP[0]}" width="{X1-X0}" height="{BOT[1]-TOP[0]}" rx="10" fill="#F0FFF0" stroke="#5b6b67" stroke-width="3"/>',t,b,
       f'<rect x="{X0}" y="{COR[0]}" width="{X1-X0}" height="{COR[1]-COR[0]}" fill="#fff"/><text x="{X0+10}" y="{COR[0]+25}" font-size="16" fill="#5b6b67">복도</text>']
    # stairs+elevator in the middle of the bottom row
    sts=[k for k in bp if k=='ST']
    mids=[(x,w) for (k,(x,w)) in [(k,v) for k,v in bp.items()]]
    cx=[x for x,w in [bp_val for kk,bp_val in []]]
    midx=None
    xs=[]; x=X0
    for name,typ,w in [parse(i) for i in bot]:
        ww=(X1-X0)*w/sum(parse(i)[2] for i in bot)
        if typ=='ST': xs.append(x+ww/2)
        x+=ww
    if len(xs)>1: midx=xs[1]
    elif xs: midx=xs[-1]
    if midx: s.append(f'<g transform="translate({midx:.0f} {BOT[1]+24})"><rect x="-36" y="-17" width="72" height="34" rx="12" fill="#fff" stroke="#0e7f6c" stroke-width="2.5"/><text y="7" text-anchor="middle" font-size="19" font-weight="900" fill="#0e7f6c">🛗 EV</text></g>')
    if n==1: s.append(f'<text x="{bp["입구"][0]+bp["입구"][1]/2-30:.0f}" y="{BOT[1]+30}" text-anchor="middle" font-size="19" font-weight="800" fill="#0e7f6c">▲ 정문 출입구</text>')
    if route and dest in bp and midx:
        dx,dw=bp[dest]
        s.append(f'<path d="M{midx:.0f} {BOT[0]} L{midx:.0f} {COR[0]+20} L{dx+dw/2:.0f} {COR[0]+20} L{dx+dw/2:.0f} {BOT[0]+6}" fill="none" stroke="#0e7f6c" stroke-width="7" stroke-dasharray="2 12" stroke-linecap="round" stroke-linejoin="round"/>')
    if dest in bp:
        dx,dw=bp[dest]; s.append(f'<rect x="{dx+dw/2-46:.0f}" y="{BOT[0]+86}" width="92" height="32" rx="16" fill="#1d2b28"/><text x="{dx+dw/2:.0f}" y="{BOT[0]+108}" text-anchor="middle" font-size="18" font-weight="800" fill="#fff">목적지</text>')
    if me:
        mx={'mid':midx,'dest':(bp[dest][0]+bp[dest][1]/2) if dest in bp else midx}[me]
        s.append(f'<circle cx="{mx:.0f}" cy="{COR[0]+20}" r="11" fill="#2f6fe4" stroke="#fff" stroke-width="4"/>')
    s.append('</svg>')
    return ''.join(s)
if __name__=='__main__':
    p='design/prototype.html';h=open(p).read()
    a=h.index('<section class="screen" id="2.2"');b=h.index('</section>',a)
    sec=h[a:b]
    floors='\n'.join(f'      <button class="tap{" on" if n==4 else ""}" onclick="floorPick(this,\'{n}\',\'{n}F\')">{n}F'+('<span class="now" data-v="now1">지금</span>' if n==1 else '<span class="now" data-v="now4">지금</span>' if n==4 else '')+'</button>' for n in range(1,7))
    sec=re.sub(r'(<div class="floors" role="tablist" aria-label="층 고르기">\n).*?(\n    </div>)',lambda m:m.group(1)+floors+m.group(2),sec,flags=re.S)
    plans=''.join(f'\n    <div data-plan="{n}" style="position:absolute;inset:0;{"" if n==4 else "display:none"}">{plan(n,"401" if n==4 else None,None,route=(n==4))}</div>' for n in range(1,7))
    sec=re.sub(r'(<span class="fl">4F 평면도</span>).*?(\n    <span class="maplabel")',lambda m:m.group(1)+plans+m.group(2),sec,flags=re.S)
    sec=sec.replace('평면도 자리 (예시)','제1인문관 층별 안내도 참고')
    sec=sec.replace('<div class="warnc" data-v="w4">⚠️ 4층에는 연결다리가 없어요. <b>3층에서 연결다리로 건너간 뒤</b> 계단으로 올라가세요.</div>',
                    '<div class="warnc" data-v="w4">🛗 가운데 <b>계단·엘리베이터로 4층</b>에 올라가 복도를 따라 <b>왼쪽 끝</b>으로 가세요. 401호는 왼쪽 계단 바로 옆이에요.</div>')
    sec=sec.replace('지금 있는 <b>제2인문관 3층 연결다리</b>로 건너가세요.','지금 있는 <b>제2인문관에서 이어진 통로</b>로 건너오세요.')
    sec=sec.replace('<b>401호 · 4층 · 오른쪽 동 끝</b><small>정보 확인일 2026. 11 · 운영진 검수</small>','<b>401호 · 4층 · 왼쪽 끝 계단 옆</b><small>광고홍보학과 멀티미디어 BTL 광고실습실 · 층별 안내도 기준</small>')
    sec=sec.replace("floorPick(this.closest('.screen').querySelectorAll('.floors button')[3],'3','3F')","floorPick(this.closest('.screen').querySelectorAll('.floors button')[0],'1','1F')")
    h=h[:a]+sec+h[b:]
    h=h.replace('"2.2":{normal:["w4","now1"],neighbor:["nb","now3"],arrive:["w4","now4","arr"]}','"2.2":{normal:["w4","now1"],neighbor:["nb","now1"],arrive:["w4","now4","arr"]}')
    h=h.replace('d.style.display=d.dataset.plan===k?(k==="x"?"flex":"block"):"none"','d.style.display=d.dataset.plan===k?"block":"none"')
    h=h.replace('<span>4층 · 오른쪽 동 끝, 여기가 찾던 강의실이에요</span>','<span>4층 왼쪽 끝 · 광고홍보학과 BTL 광고실습실이에요</span>')
    h=h.replace('를 찾았어요. 지하 강의실(B401)을 찾으셨다면 ‘아니에요’를 눌러 주세요.','를 찾았어요. 제1인문관에는 지하층이 없어요. 다른 건물의 B401을 찾으셨다면 ‘아니에요’를 눌러 주세요.')
    h=h.replace('<span class="src">학교 도면</span><b>제1인문관 4층 평면도</b><span>마지막 확인 2026. 11. 05</span>','<span class="src">건물 층별 안내도</span><b>제1인문관 4층 평면도</b><span>마지막 확인 2026. 11. 27</span>')
    open(p,'w').write(h)
    print('ok', h.count('data-plan='), h.count('B401을 찾으셨다면'))
