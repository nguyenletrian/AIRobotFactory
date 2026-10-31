const test = require('node:test');
const assert = require('node:assert/strict');
const {forward,inverse,intersectsCircle}=require('./kinematics.js');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,a+' != '+b);
test('forward matches analytic sample',()=>{near(forward(0,0).tip.x,210);near(forward(0,90).tip.x,120);near(forward(0,90).tip.y,90);});
test('both inverse branches reproduce target',()=>{for(const [a,b] of [[35,-60],[-80,40],[0,0],[30,90]]){const t=forward(a,b).tip;for(const up of [true,false]){const q=inverse(t.x,t.y,120,90,up);const r=forward(q.a,q.b).tip;near(r.x,t.x);near(r.y,t.y);}}});
test('IK rejects unreachable or invalid data',()=>{assert.throws(()=>inverse(300,0),RangeError);assert.throws(()=>inverse(0,0),RangeError);assert.throws(()=>inverse(NaN,0),RangeError);assert.throws(()=>forward(0,0,-1,90),RangeError);});
test('segment circle detection',()=>{const a={x:0,y:0},b={x:100,y:0};assert.equal(intersectsCircle(a,b,{x:50,y:10},11),true);assert.equal(intersectsCircle(a,b,{x:50,y:20},11),false);assert.equal(intersectsCircle(a,a,{x:0,y:0},0),true);assert.throws(()=>intersectsCircle(a,b,{x:0,y:0},-1),RangeError);});
