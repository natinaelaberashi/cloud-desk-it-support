const tickets=[
{id:"INC-1042",issue:"VPN connection failure",priority:"High",team:"Network",status:"Resolved",hours:3.2,sla:true},
{id:"INC-1041",issue:"Password reset / MFA",priority:"Medium",team:"Access",status:"Resolved",hours:0.8,sla:true},
{id:"INC-1040",issue:"Checkout application error",priority:"Critical",team:"Applications",status:"Pending",hours:6.4,sla:false},
{id:"INC-1039",issue:"Laptop performance",priority:"Low",team:"Service Desk",status:"Resolved",hours:4.1,sla:true},
{id:"INC-1038",issue:"User account locked",priority:"High",team:"Access",status:"Open",hours:2.1,sla:true},
{id:"INC-1037",issue:"Network latency",priority:"High",team:"Network",status:"Resolved",hours:5.3,sla:false},
{id:"INC-1036",issue:"CRM application issue",priority:"Medium",team:"Applications",status:"Resolved",hours:2.7,sla:true},
{id:"INC-1035",issue:"Software installation",priority:"Low",team:"Service Desk",status:"Resolved",hours:1.4,sla:true},
{id:"INC-1034",issue:"Payment timeout",priority:"Critical",team:"Applications",status:"Resolved",hours:4.8,sla:true},
{id:"INC-1033",issue:"Email access",priority:"Medium",team:"Access",status:"Pending",hours:7.2,sla:false}
];
const $=id=>document.getElementById(id);
function render(){const p=$("priority").value,s=$("status").value,t=$("team").value;const data=tickets.filter(x=>(p==="All"||x.priority===p)&&(s==="All"||x.status===s)&&(t==="All"||x.team===t));
$("total").textContent=data.length;const compliance=data.length?Math.round(data.filter(x=>x.sla).length/data.length*100):0;$("sla").textContent=compliance+"%";$("avg").textContent=(data.length?data.reduce((a,x)=>a+x.hours,0)/data.length:0).toFixed(1)+"h";$("open").textContent=data.filter(x=>x.status!=="Resolved").length;$("count").textContent=data.length+" incidents";
const counts=["Critical","High","Medium","Low"].map(k=>[k,data.filter(x=>x.priority===k).length]);const max=Math.max(...counts.map(x=>x[1]),1);$("bars").innerHTML=counts.map(([k,v])=>`<div class="bar-group"><div class="bar-value">${v}</div><div class="bar" style="height:${Math.max(v/max*145,8)}px"></div><div class="bar-label">${k}</div></div>`).join("");
const team=data.reduce((a,x)=>(a[x.team]=(a[x.team]||0)+1,a),{});const top=Object.entries(team).sort((a,b)=>b[1]-a[1])[0];$("insights").innerHTML=`<div class="insight"><b>Highest volume</b><span>${top?top[0]+" • "+top[1]+" tickets":"No matching tickets"}</span></div><div class="insight"><b>SLA attention</b><span>${data.filter(x=>!x.sla).length} incident(s) outside target</span></div><div class="insight"><b>Priority focus</b><span>${data.filter(x=>x.priority==="Critical").length} critical incident(s) require escalation</span></div>`;
$("rows").innerHTML=data.map(x=>`<tr><td><b>${x.id}</b></td><td>${x.issue}</td><td><span class="pill ${x.priority==="Critical"?"bad":x.priority==="High"?"warn":""}">${x.priority}</span></td><td>${x.team}</td><td>${x.status}</td><td>${x.hours}h</td><td><span class="pill ${x.sla?"good":"bad"}">${x.sla?"Within":"Breached"}</span></td></tr>`).join("")}
["priority","status","team"].forEach(id=>$(id).addEventListener("change",render));$("resetBtn").onclick=()=>{["priority","status","team"].forEach(id=>$(id).value="All");render()};render();