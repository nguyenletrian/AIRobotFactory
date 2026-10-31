const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
test('offline viewer HTML has parseable inline UI script',()=>{
  const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
  const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(s=>s.trim());
  assert.equal(scripts.length,1,'one inline app script expected');
  assert.doesNotThrow(()=>new Function(scripts[0]));
  for(const key of ['view','a','b','l1','l2','x','y','go','reset','demo','status']) {
    assert.match(html,new RegExp('id="'+key+'"'));
  }
  assert.equal(/<script[^>]+src="https?:/.test(html),false);
});
