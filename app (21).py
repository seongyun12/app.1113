"""토닥곰 — 우리집 먹고 싶은 음식 + 함께 할 일 뽑기
GitHub에 app.py / requirements.txt 업로드 후 Streamlit Community Cloud 배포.
배포 주소를 QR로 공유하면 접속 가능. 로컬: streamlit run app.py
한 기기를 돌려 쓰는 놀이 버전. 기기 간 동기화/로그인/서버 저장 없음.
취향 정답과 소원은 현재 화면 메모리에만 보관. 새로고침하면 초기화.
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="토닥곰 · 우리집 놀이", page_icon="🐻", layout="centered")
st.markdown('''<style>
[data-testid="stHeader"],[data-testid="stToolbar"],footer{display:none!important}
[data-testid="stAppViewContainer"]{background:#f3f7f1}
.block-container,[data-testid="stMainBlockContainer"]{padding:0!important;max-width:480px!important}
[data-testid="stVerticalBlock"]{gap:0!important}
iframe{width:100%;height:100svh!important;display:block;border:0}
</style>''', unsafe_allow_html=True)
PAGE = r'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
*{box-sizing:border-box}body{margin:0;padding:14px;background:#f3f7f1;color:#283f34;font-family:system-ui,-apple-system,'Malgun Gothic',sans-serif}main{max-width:448px;margin:auto}header{display:flex;align-items:center;justify-content:space-between;margin:0 4px 12px}h1{font-size:25px;margin:0;letter-spacing:-1px}header p{margin:3px 0 0;font-size:13px;color:#607265}.bear{font-size:45px}section{padding:17px;border-radius:26px;background:#fff;margin-bottom:11px}h2{font-size:19px;margin:0 0 12px;letter-spacing:-.5px}button,input{font:inherit}button{border:0;border-radius:17px;cursor:pointer;min-height:46px;font-weight:650;padding:10px 13px;color:#304c3b;background:#edf3eb;touch-action:manipulation}button:focus-visible,input:focus-visible{outline:3px solid #b47d23;outline-offset:2px}button:disabled{opacity:.5;cursor:default}.two{display:grid;grid-template-columns:1fr 1fr;gap:9px}.choice{font-size:17px;background:#f5f6ef;min-height:77px}.choice span{display:block;font-size:28px;margin-bottom:2px}.primary{background:#307759;color:white;width:100%;margin-top:10px}.small{font-size:13px;min-height:38px;padding:7px 12px}.question{font-size:17px;font-weight:650;margin:0 0 12px}.caption{font-size:13px;color:#607265;margin:8px 0;line-height:1.45}.result{background:#fff2d5;border-radius:17px;padding:12px;text-align:center;font-size:17px;font-weight:700;margin-top:10px}.row{display:flex;align-items:center;gap:8px}.row input{width:100%;min-width:0;border:1px solid #d4dfd0;border-radius:15px;padding:11px;font-size:16px;background:#fafcf8;color:#283f34}.chips{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}.chips button{font-size:13px;min-height:35px;padding:7px 10px}.wish-list{display:flex;gap:6px;flex-wrap:wrap;margin:7px 0}.wish-item{border:1px solid #d8e3d4;background:white;min-height:34px;font-size:13px;max-width:100%;overflow-wrap:anywhere}.wish-item span{margin-left:7px;color:#7d6657}footer{font-size:11px;text-align:center;color:#607265;line-height:1.5}dialog{border:0;border-radius:28px;width:calc(100% - 32px);max-width:360px;padding:23px;color:#283f34;max-height:90svh;overflow:auto}dialog::backdrop{background:#203e3266}.welcome{text-align:center}.welcome h2{font-size:23px}.steps{display:flex;justify-content:space-around;gap:8px;margin:20px 0}.steps div{flex:1;font-size:14px;font-weight:650}.steps span{font-size:35px;display:block;margin-bottom:8px}.welcome .caption{margin:10px 0}.hidden,[hidden]{display:none!important}
@media(max-height:730px){body{padding:9px 12px}header{margin-bottom:8px}section{padding:13px 15px;margin-bottom:8px}h2{margin-bottom:9px}.choice{min-height:66px}.chips{margin:7px 0}.primary{margin-top:8px}.bear{font-size:38px}.caption{margin:6px 0}}
</style></head><body><main>
<header><div><h1>토닥곰</h1><p>다시 만나면, 함께 해요.</p></div><div class="bear" role="img" aria-label="웃는 곰">🐻</div></header>
<section><h2>🪖 형들 돌아오는 날</h2><div class="two"><div>⚓ 첫째 · 해군<p class="caption">입대 3월 4일</p><strong id="navy">입대 연도 확인 필요</strong></div><div>🪖 둘째 · 육군<p class="caption">입대 6월 20일</p><strong id="army">입대 연도 확인 필요</strong></div></div><div class="row" style="margin-top:10px"><input id="year" type="number" min="2000" max="2100" placeholder="두 형의 입대 연도" aria-label="두 형의 입대 연도"><button id="yearSet">확인</button></div><p class="caption">병 복무 기준 예상일 · 실제 전역일과 다를 수 있어요</p></section>
<section><h2>🍽️ 우리 가족이 먹고 싶은 음식</h2><div class="row"><select id="person" aria-label="가족 선택" style="font:inherit;min-height:44px;border-radius:14px;max-width:110px"><option>엄마</option><option>첫째형</option><option>둘째형</option><option>나</option><option>아빠</option></select><input id="food" maxlength="24" placeholder="먹고 싶은 음식" aria-label="음식"><button id="foodAdd" aria-label="음식 추가">＋</button></div><div id="foods" class="wish-list"></div><p id="foodStatus" class="caption" aria-live="polite">누가 무엇을 먹고 싶은지 적어요.</p></section>
<section aria-labelledby="wishTitle"><h2 id="wishTitle">🎁 다 같이 만나면 하고 싶은 일</h2>
<div class="row"><input id="wishInput" maxlength="24" placeholder="함께 하고 싶은 일" aria-label="가족 소원 입력"><button id="add" aria-label="소원 추가">＋</button></div>
<div class="chips" aria-label="소원 빠른 추가"><button data-wish="치킨 먹기">🍗 치킨</button><button data-wish="함께 산책하기">🌳 산책</button><button data-wish="가족사진 찍기">📸 가족사진</button></div>
<div class="wish-list" id="wishes"></div><p class="caption" id="wishStatus" aria-live="polite">소원을 넣고 하나 뽑아봐요.</p>
<button class="primary" id="draw" disabled>소원 뽑기 🎲</button><div class="result hidden" id="wishResult" role="status"></div>
</section><footer>한 기기로 함께 놀아요 · 새로고침하면 초기화돼요</footer>
</main>
<dialog id="welcome" class="welcome" aria-labelledby="introTitle"><div class="bear">🐻</div><h2 id="introTitle">우리집 놀이 시작!</h2><div class="steps"><div><span>🍽️</span>음식 적고</div><div><span>🌳</span>할 일 담고</div><div><span>🎁</span>소원 뽑아요</div></div><p class="caption">한 기기를 번갈아 사용해요.<br>멀리 있는 가족과 자동 연결되지는 않아요.</p><button class="primary" id="start">같이 해볼까요?</button></dialog>
<script>
'use strict';
const $=id=>document.getElementById(id);
function updateDates(){const y=Number($('year').value);if(!Number.isInteger(y)||y<2000||y>2100){$('navy').textContent='연도를 확인해 주세요';$('army').textContent='연도를 확인해 주세요';return;}for(const [id,m,d,months] of [['navy',2,4,20],['army',5,20,18]]){const date=new Date(y,m+months,d-1);$(id).textContent='예상 '+date.getFullYear()+'.'+(date.getMonth()+1)+'.'+date.getDate();}}
$('yearSet').addEventListener('click',updateDates);
let foods=[];
function renderFoods(){ $('foods').replaceChildren();foods.forEach((f,i)=>{const b=document.createElement('button');b.className='wish-item';b.textContent=f.person+' · '+f.food+' ×';b.setAttribute('aria-label',f.person+' '+f.food+' 삭제');b.addEventListener('click',()=>{foods.splice(i,1);renderFoods();});$('foods').append(b);});}
$('foodAdd').addEventListener('click',()=>{const food=$('food').value.trim(),person=$('person').value;if(!food){$('foodStatus').textContent='음식을 적어 주세요.';return;}if(foods.length>=8){$('foodStatus').textContent='8개까지 담을 수 있어요. 누르면 삭제돼요.';return;}if(foods.some(f=>f.person===person&&f.food===food))return;foods.push({person,food});$('food').value='';renderFoods();$('foodStatus').textContent='담았어요 · 누르면 삭제';});
$('food').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.isComposing)$('foodAdd').click();});
let wishes=[];
function renderWishes(message){$('wishes').replaceChildren();wishes.forEach((wish,i)=>{const b=document.createElement('button');b.className='wish-item';b.type='button';b.textContent=wish;const cross=document.createElement('span');cross.textContent='×';cross.setAttribute('aria-hidden','true');b.append(cross);b.setAttribute('aria-label',wish+' 삭제');b.addEventListener('click',()=>{wishes.splice(i,1);$('wishResult').classList.add('hidden');renderWishes('소원을 지웠어요.');});$('wishes').append(b);});$('draw').disabled=wishes.length===0;$('wishStatus').textContent=message||(wishes.length?wishes.length+'개 준비됐어요 · 누르면 삭제':'소원을 넣고 하나 뽑아봐요.');}
function addWish(value){const v=value.trim();if(!v){$('wishStatus').textContent='소원을 한 가지 적어 주세요.';return;}if(wishes.includes(v)){$('wishStatus').textContent='이미 넣은 소원이에요.';return;}if(wishes.length>=6){$('wishStatus').textContent='6개까지 넣을 수 있어요. 하나를 눌러 지워주세요.';return;}wishes.push(v);$('wishInput').value='';$('wishResult').classList.add('hidden');renderWishes();}
$('add').addEventListener('click',()=>addWish($('wishInput').value));$('wishInput').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.isComposing)addWish($('wishInput').value);});document.querySelectorAll('[data-wish]').forEach(b=>b.addEventListener('click',()=>addWish(b.dataset.wish)));
$('draw').addEventListener('click',()=>{if(!wishes.length)return;$('wishResult').textContent='🎁 '+wishes[Math.floor(Math.random()*wishes.length)];$('wishResult').classList.remove('hidden');$('wishStatus').textContent='가족 모두 괜찮다면, 함께 해봐요!';});
$('start').addEventListener('click',()=>{$('welcome').close();$('food').focus();});renderWishes();$('welcome').showModal();
</script></body></html>'''
components.html(PAGE, height=850, scrolling=True)
