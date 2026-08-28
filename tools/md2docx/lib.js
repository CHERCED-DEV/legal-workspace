const d = require('docx');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,BorderStyle,PageOrientation} = d;

const LETTER = {width:12240,height:15840};
const MARGIN = {top:1080,right:1080,bottom:1080,left:1080};
const CONTENT = 12240-2160; // 10080

function p(text,opt={}){
  return new Paragraph({
    alignment: opt.align||AlignmentType.JUSTIFIED,
    spacing:{after:opt.after===undefined?140:opt.after, line:280},
    indent: opt.indent?{left:opt.indent}:undefined,
    border: opt.rule?{bottom:{style:BorderStyle.SINGLE,size:6,color:"999999",space:6}}:undefined,
    children: runs(text,opt)
  });
}
// **bold** y *cursiva* dentro del texto
function runs(text,opt={}){
  const out=[]; const re=/(\*\*[^*]+\*\*|\*[^*]+\*)/g; let last=0,m;
  while((m=re.exec(text))!==null){
    if(m.index>last) out.push(new TextRun({text:text.slice(last,m.index),size:opt.size||21,font:"Calibri",color:opt.color}));
    const t=m[0];
    if(t.startsWith('**')) out.push(new TextRun({text:t.slice(2,-2),bold:true,size:opt.size||21,font:"Calibri",color:opt.color}));
    else out.push(new TextRun({text:t.slice(1,-1),italics:true,size:opt.size||21,font:"Calibri",color:opt.color}));
    last=re.lastIndex;
  }
  if(last<text.length) out.push(new TextRun({text:text.slice(last),size:opt.size||21,font:"Calibri",color:opt.color}));
  return out;
}
function h(text,level){
  return new Paragraph({heading:level,spacing:{before:260,after:130},
    children:[new TextRun({text,bold:true,font:"Calibri",size:level===HeadingLevel.HEADING_1?30:(level===HeadingLevel.HEADING_2?25:22),color:"1F3864"})]});
}
function bullet(text){
  return new Paragraph({bullet:{level:0},spacing:{after:70,line:280},children:runs(text)});
}
function box(lines,color){
  return new Table({
    columnWidths:[CONTENT],width:{size:CONTENT,type:WidthType.DXA},
    rows:[new TableRow({children:[new TableCell({
      width:{size:CONTENT,type:WidthType.DXA},
      shading:{type:ShadingType.CLEAR,fill:color||"FFF2CC"},
      margins:{top:120,bottom:120,left:150,right:150},
      children:lines.map(l=>p(l,{after:60}))
    })]})]});
}
function table(headers,rows,widths){
  const total=widths.reduce((a,b)=>a+b,0);
  const cols=widths.map(w=>Math.round(CONTENT*w/total));
  const diff=CONTENT-cols.reduce((a,b)=>a+b,0); cols[cols.length-1]+=diff;
  const head=new TableRow({tableHeader:true,children:headers.map((t,i)=>new TableCell({
    width:{size:cols[i],type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,fill:"1F3864"},
    margins:{top:80,bottom:80,left:110,right:110},
    children:[new Paragraph({alignment:AlignmentType.LEFT,spacing:{after:0},
      children:[new TextRun({text:t,bold:true,color:"FFFFFF",size:19,font:"Calibri"})]})]
  }))});
  const body=rows.map((r,ri)=>new TableRow({children:r.map((t,i)=>new TableCell({
    width:{size:cols[i],type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,fill:ri%2?"F2F2F2":"FFFFFF"},
    margins:{top:80,bottom:80,left:110,right:110},
    children:[new Paragraph({alignment:AlignmentType.LEFT,spacing:{after:0,line:250},children:runs(String(t),{size:19})})]
  }))}));
  return new Table({columnWidths:cols,width:{size:CONTENT,type:WidthType.DXA},rows:[head,...body]});
}
function doc(title,subtitle,children){
  return new Document({
    styles:{default:{document:{run:{font:"Calibri",size:21}}}},
    sections:[{
      properties:{page:{size:LETTER,margin:MARGIN}},
      children:[
        new Paragraph({spacing:{after:60},children:[new TextRun({text:title,bold:true,size:34,font:"Calibri",color:"1F3864"})]}),
        new Paragraph({spacing:{after:200},border:{bottom:{style:BorderStyle.SINGLE,size:12,color:"1F3864",space:8}},
          children:[new TextRun({text:subtitle,size:20,font:"Calibri",color:"595959"})]}),
        ...children
      ]}]});
}
module.exports={d,p,h,bullet,box,table,doc,Packer,HeadingLevel,AlignmentType};
