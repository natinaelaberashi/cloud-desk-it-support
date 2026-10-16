"use strict";
const $=id=>document.getElementById(id);
const escapeHtml=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const parseCSV=text=>{const lines=text.trim().split(/\r?\n/);const cols=lines.shift().split(",");return lines.map(line=>{const values=line.split(",");return Object.fromEntries(cols.map((c,i)=>[c,values[i]??""]))})};
let tickets=[];
function render(){
 const p=$("priority").value,s=$("status").value,t=$("team").value;
 const data=tickets.filter(x=>(p==="All"||x.priority===p)&&(s==="All"||x.status===s)&&(t==="All"||x.team===t));
 const resolved=data.filter(x=>x.status==="Resolved");
 const compliance=resolved.length?100*resolved.filter(x=>x.sla_met==="true").length/resolved.length:null;
 const avg=resolved.length?resolved.reduce((n,x)=>n+Number(x.resolution_hours),0)/resolved.length:null;
 $("total").textContent=data.length.toLocaleString();
 $("sla").textContent=compliance===null?"N/A":compliance.toFixed(1)+"%";
 $("avg").textContent=avg===null?"N/A":avg.toFixed(1)+"h";
 $("open").textContent=data.filter(x=>x.status!=="Resolved").length;
 $("count").textContent=data.length+" incidents";
 const counts=["Critical","High","Medium","Low"].map(k=>[k,data.filter(x=>x.priority===k).length]);
 const max=Math.max(1,...counts.map(x=>x[1]));
 $("bars").innerHTML=counts.map(([k,v])=>`<div class="bar-group"><div class="bar-value">${v}</div><div class="bar" style="height:${Math.max(4,v/max*145)}px"></div><div class="bar-label">${k}</div></div>`).join("");
 const groups={};for(const x of data){groups[x.team]??={total:0,resolved:0,met:0};groups[x.team].total++;if(x.status==="Resolved"){groups[x.team].resolved++;if(x.sla_met==="true")groups[x.team].met++}}
 $("teams").innerHTML=Object.entries(groups).sort((a,b)=>b[1].total-a[1].total).map(([team,v])=>`<div class="team-row"><b>${escapeHtml(team)}</b><span>${v.total} tickets · SLA ${v.resolved?(100*v.met/v.resolved).toFixed(1)+"%":"N/A"}</span></div>`).join("")||"<p>No matching teams</p>";
 const months={};for(const x of data){const month=x.created_at.slice(0,7);months[month]=(months[month]||0)+1}
 const series=Object.entries(months).sort((a,b)=>a[0].localeCompare(b[0]));const top=Math.max(1,...series.map(x=>x[1]));
 $("trends").innerHTML=series.map(([month,v])=>`<div class="trend-col" title="${month}: ${v} tickets"><span>${v}</span><div class="trend-bar" style="height:${Math.max(3,110*v/top)}px"></div><small>${month.slice(5)}</small></div>`).join("")||"<p>No matching dates</p>";
 $("insights").innerHTML=`<div class="insight"><b>Resolved incidents</b><span>${resolved.length} of ${data.length} selected tickets</span></div><div class="insight"><b>Resolved SLA misses</b><span>${resolved.filter(x=>x.sla_met==="false").length} incidents</span></div><div class="insight"><b>Critical backlog</b><span>${data.filter(x=>x.priority==="Critical"&&x.status!=="Resolved").length} unresolved critical tickets</span></div>`;
 $("rows").innerHTML=data.slice().sort((a,b)=>b.created_at.localeCompare(a.created_at)).slice(0,50).map(x=>`<tr><td><b>${escapeHtml(x.id)}</b></td><td>${escapeHtml(x.issue)}</td><td>${escapeHtml(x.priority)}</td><td>${escapeHtml(x.team)}</td><td>${escapeHtml(x.status)}</td><td>${x.resolution_hours?escapeHtml(x.resolution_hours)+"h":"—"}</td><td>${x.sla_met===""?"Pending":x.sla_met==="true"?"Within":"Breached"}</td></tr>`).join("");
}
async function init(){try{const response=await fetch("data/incidents_extended.csv",{cache:"no-store"});if(!response.ok)throw new Error("HTTP "+response.status);tickets=parseCSV(await response.text());if(!tickets.length)throw new Error("Dataset is empty");$("load-status").textContent="600 synthetic incidents · illustrative sample";render()}catch(e){$("load-status").textContent="Could not load data: "+e.message;console.error(e)}}
["priority","status","team"].forEach(id=>$(id).addEventListener("change",render));
$("resetBtn").addEventListener("click",()=>{["priority","status","team"].forEach(id=>$(id).value="All");render()});
init();
