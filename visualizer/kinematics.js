/* Analytic 2-link planar kinematics; millimeters and degrees. Never controls hardware. */
(function (root) {
  "use strict";
  function valid(a,b) {
    if (![a,b].every(x=>Number.isFinite(x)&&x>0)) throw new RangeError("Links must be positive finite lengths");
  }
  function forward(a,b,l1=120,l2=90) {
    valid(l1,l2);
    if (![a,b].every(Number.isFinite)) throw new RangeError("Angles must be finite");
    const p=Math.PI/180;
    const elbow={x:l1*Math.cos(a*p),y:l1*Math.sin(a*p)};
    const tip={x:elbow.x+l2*Math.cos((a+b)*p),y:elbow.y+l2*Math.sin((a+b)*p)};
    return {elbow,tip};
  }
  function inverse(x,y,l1=120,l2=90,elbowUp=false) {
    valid(l1,l2);
    if (![x,y].every(Number.isFinite)) throw new RangeError("Target must be finite");
    let c=(x*x+y*y-l1*l1-l2*l2)/(2*l1*l2);
    if(c < -1-1e-10 || c > 1+1e-10) throw new RangeError("Target outside reachable workspace");
    c=Math.min(1,Math.max(-1,c));
    const b=(elbowUp?-1:1)*Math.acos(c);
    const a=Math.atan2(y,x)-Math.atan2(l2*Math.sin(b),l1+l2*Math.cos(b));
    return {a:a*180/Math.PI,b:b*180/Math.PI};
  }
  function intersectsCircle(a,b,c,r) {
    if(![a.x,a.y,b.x,b.y,c.x,c.y,r].every(Number.isFinite)||r<0) throw new RangeError("Invalid collision geometry");
    const dx=b.x-a.x,dy=b.y-a.y,d2=dx*dx+dy*dy;
    const t=d2===0?0:Math.max(0,Math.min(1,((c.x-a.x)*dx+(c.y-a.y)*dy)/d2));
    const ex=a.x+t*dx-c.x,ey=a.y+t*dy-c.y;
    return ex*ex+ey*ey<=r*r;
  }
  const api=Object.freeze({forward,inverse,intersectsCircle});
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
  root.AIRobotKinematics=api;
})(typeof window!=="undefined"?window:globalThis);
