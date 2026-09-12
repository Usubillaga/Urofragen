// Isolated DOM model: no browser storage or real approvals are modified.
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(require('path').join(__dirname,'../pruefung.html'),'utf8');
const bank=JSON.parse(html.match(/<script id="bank" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const source=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements={};let saved=null,failStorage=false,downloads=[];
class El{
 constructor(tag='div',text='',value=''){this.tag=tag;this.textContent=text;this.value=value;this.children=[];this.events={};this.files=[];}
 set id(id){this._id=id;elements[id]=this;}get id(){return this._id;}
 append(...nodes){this.children.push(...nodes);}replaceChildren(...nodes){this.children=nodes;this.value=nodes[0]?.value||'';}
 add(n){this.children.push(n);if(this.children.length===1)this.value=n.value;}
 addEventListener(k,fn){this.events[k]=fn;}setAttribute(){}focus(){}scrollIntoView(){}remove(){}click(){return this.events.click?.();}
}
for(const [,id] of html.matchAll(/id="([^"]+)"/g))elements[id]=new El();
elements.bank.textContent=JSON.stringify(bank);
const sandbox={console,Date,JSON,Object,Array,String,Number,Set,Error,Blob,Option:class extends El{constructor(text,value){super('option',text,value);}},localStorage:{getItem:()=>null,setItem:(k,v)=>{if(failStorage)throw Error();saved=v;}},document:{getElementById:id=>elements[id],createElement:tag=>new El(tag),documentElement:{},body:new El()},window:{confirm:()=>true,addEventListener(){}},URL:{createObjectURL:b=>{downloads.push(b);return 'blob:test';},revokeObjectURL(){}},setTimeout:fn=>fn()};
vm.createContext(sandbox);vm.runInContext(source,sandbox);const run=s=>vm.runInContext(s,sandbox);
(async()=>{
 assert.match(elements.summary.textContent,/214 offen/);
 run("save('approved')");assert.match(elements.feedback.textContent,/Prüfernamen/);assert.equal(saved,null);
 elements.name.value='TEST ONLY';run("save('changes_requested')");assert.match(elements.feedback.textContent,/beschreibe/);
 elements.note.value='Test correction';run("save('changes_requested')");assert.equal(Object.values(JSON.parse(saved).decisions)[0].decision,'changes_requested');
 elements.expiry.value='2000-01-01';run("save('approved')");assert.match(elements.feedback.textContent,/Ablaufdatum/);
 elements.expiry.value='2099-12-31';run("save('approved')");assert.equal(Object.values(JSON.parse(saved).decisions)[0].decision,'approved');
 run("lang='es';configure();selectList()");assert.match(elements.summary.textContent,/214 pendientes/);assert.equal(run('decision(list[0])'),null);
 run("lang='de';configure();selectList()");assert.equal(run('decision(list[0]).decision'),'approved');
 run("save('withdrawn')");assert.equal(run('decision(list[0])'),null);assert.equal(Object.values(JSON.parse(saved).decisions)[0].history.length,2);
 elements.expiry.value='2099-12-31';failStorage=true;run("save('approved')");assert.match(elements.feedback.textContent,/fehlgeschlagen/);assert.equal(run('decision(list[0]).decision'),'approved');failStorage=false;
 await elements.export.click();assert.equal(downloads.length,1);const exported=JSON.parse(await downloads[0].text());assert.equal(exported.schema,'urofragen-clinical-review-v1');
 run('state.decisions={}');elements.restore.files=[{text:async()=>JSON.stringify(exported)}];await elements.restore.events.change();assert.equal(run('decision(list[0]).decision'),'approved');
 run('list[0].version++');assert.equal(run('decision(list[0])'),null);
 assert.equal(bank.questions.length,214);assert.equal(bank.questions.filter(q=>q.taxonomy.domain==='mibc').length,10);
 console.log('Review UI: validation, correction, approval, expiry, language isolation, withdrawal/history, storage failure, export, restore and changed-version checks passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});
