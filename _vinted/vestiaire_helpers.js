// Vestiaire Collective — dépôt d'annonce via Claude in Chrome (Chrome du HP, compte connecté via Google).
// 1) Page https://fr.vestiairecollective.com/sell-clothes-online/ : find refs -> clic radio "Mode homme/femme",
//    form_input sur le select Catégorie (valeurs : 39 Vestes & Blousons, 37 Pulls Gilets & Sweats, 512 Manteaux, 525 Tee shirts, 524 Polos, 38 Chemises, 34 Jeans, 35 Pantalons, 48 Sacs),
//    clic champ Marque + type, puis clic JS sur le bouton dont innerText === marque exacte, puis "Continuer" (navigation -> réinjecter ce fichier).
// 2) Page détails : injecter ce fichier, puis await vcDetails({cat,etat,mat,col,imp,norm,size,vintage}).
//    L'ÉTAT ne s'ouvre PAS en JS : faire find "État button" -> left_click sur le ref, puis clickText('Très bon état').
//    Vérifier avec vcCheck().
// 3) await vcRest(dossier, ['01','02',...], description) : photos (fetch GitHub raw -> input file multiple), description, adresse, arrive sur #/price.
// 4) Prix : find "Prix textbox" -> triple_click, ctrl+a, type "79". Lire "Pour vous" et le prix recommandé.
// 5) Clic JS bouton "Vérifiez l'annonce", relire le récap, puis bouton "Déposer mon article". product_id dans l'URL de confirmation.
// Frais vendeur : < ~75 € : 15 € fixes ; au-delà ~20 %. Prix entiers seulement. Photos min 900x900.
const W=ms=>new Promise(r=>setTimeout(r,ms));
window.opts=()=>[...document.querySelectorAll('[role=option],li')].filter(e=>e.offsetParent).map(e=>e.innerText.trim()).filter(Boolean).filter(t=>!/^\d\n/.test(t));
window.pick=(t)=>{const e=[...document.querySelectorAll('[role=option],li')].filter(e=>e.offsetParent&&e.innerText.trim()===t)[0]; if(!e) return 'NF '+t; e.click(); return 'ok '+t};
window.openCombo=(name)=>{const i=document.querySelector(`input[name="${name}"]`); const btn=i.parentElement.parentElement.querySelector('button')||i.parentElement.querySelector('button'); (btn||i).click(); i.click(); i.focus();};
window.clickText=(t)=>{const els=[...document.querySelectorAll('*')].filter(e=>e.offsetParent&&e.childElementCount===0&&e.innerText&&e.innerText.trim()===t);const e=els[els.length-1];if(!e)return 'NF '+t;(e.closest('label,button,li,[role=option],[role=radio]')||e).click();return 'ok '+t};
window.setSel=(el,v)=>{const p=Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set;p.call(el,v);el.dispatchEvent(new Event('change',{bubbles:true}))};
window.vcCheck=()=>{const lab=[...document.querySelectorAll('*')].find(e=>e.childElementCount===0&&e.innerText&&e.innerText.trim()==='État'&&e.offsetParent);let q=lab;for(let i=0;i<4;i++)q=q.parentElement;return q.innerText.slice(0,80)};
window.vcDetails=async(d)=>{const log=[];openCombo('Catégorie');await W(700);log.push(pick(d.cat));await W(600);
 for(const [n,v] of [['Matière',d.mat],['Couleur',d.col],['Imprimé',d.imp]]){openCombo(n);await W(700);log.push(pick(v));await W(500)}
 let s=document.querySelectorAll('select');setSel(s[0],String(d.norm));await W(800);s=document.querySelectorAll('select');const o=[...s[1].options].find(o=>o.text.trim()===d.size);if(o){setSel(s[1],o.value);log.push('size '+o.text)}else log.push('size NF '+[...s[1].options].map(o=>o.text).join(','));
 if(d.vintage){const v=document.querySelector('input[name=vintage]');if(!v.checked)(v.closest('label')||v).click()}
 return log};
const cont=()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='Continuer').pop().click();
window.vcRest=async(ref,files,desc)=>{const log=[];cont();await W(3000);log.push(location.hash);
 const dt=new DataTransfer();for(const n of files){const b=await (await fetch(`https://raw.githubusercontent.com/cncrtdrop/Cncrt-photos/main/${ref}/${n}.jpg`)).blob();dt.items.add(new File([b],`${ref}_${n}.jpg`,{type:'image/jpeg'}))}
 const inp=document.querySelector('input[type=file][multiple]');inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));
 for(let i=0;i<30;i++){await W(1000);const n=[...document.querySelectorAll('main img')].filter(i=>i.offsetParent).length;if(n>=files.length)break}
 log.push('imgs '+[...document.querySelectorAll('main img')].filter(i=>i.offsetParent).length);
 cont();await W(3000);log.push(location.hash);
 const ta=document.querySelector('main textarea');const p=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set;p.call(ta,desc);ta.dispatchEvent(new Event('input',{bubbles:true}));
 await W(500);cont();await W(3000);log.push(location.hash);cont();await W(3500);log.push(location.hash);
 const t=document.querySelector('main').innerText;log.push(t.slice(t.indexOf('Pour vous'),t.indexOf('Pour vous')+200));return log};
'helpers ok';
