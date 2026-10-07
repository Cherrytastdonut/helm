import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out=path.resolve(process.argv[2]);
const read=async n=>JSON.parse(await fs.readFile(path.join(out,'DATA',n+'.json'),'utf8'));
const [parts,measures,critical,field,nodes]=await Promise.all(['parts-numbered','measurement-register','critical-checks','field-adjustment','cad-node-map'].map(read));
const wb=Workbook.create(); const ink='#173041',teal='#087E83';
const specs=[
 ['전체번호','HELM 부품번호와 CAD 적용','1차 29개 + 2차 64개 = 93개 구매 항목. 칩은 상위 보드에 귀속하며 미사용 재고도 보존했습니다. 재단 승인 전 검토본입니다.',
 ['번호','구매 ID','차수·원본 행','부품','모델','구매 수량 원문','치수표 번호','근거','치수 mm','판단','필요 작업','CAD 적용','노드 수','대표 노드','상품 링크'],
 parts.map(p=>[p.number,p.purchase_id,`${p.round} / ${p.source_row}`,p.item,p.model,p.quantity_source,p.measurement_number,p.evidence_type,p.dimensions_mm,p.decision,p.action,p.cad_usage,p.cad_nodes,p.node_examples,p.source_url]),
 [9,16,18,28,64,21,14,35,48,25,74,36,12,66,72]],
 ['실측기록','치수표 원문과 CAD 반영','원본 번호 10은 없습니다. C920 구매 행 22는 모델명으로 대조해 P1-003 / 원본 7행에 연결했습니다. 중형 25m는 25mm 오기로 정규화했습니다.',
 ['치수표 번호','구매 ID','부품','근거','치수 mm','CAD 반영','확인·조정','원문 치수','원문 상태','출처'],
 measures.map(p=>[p.number,p.purchase_id,p.item,p.evidence_type,p.normalized_mm,p.cad_action,p.required_action,p.raw_measurement,p.source_note,p.source]),
 [13,16,28,24,60,70,78,65,65,45]],
 ['필수확인','재단 전에 꼭 필요한 확인','G1~G4는 기준 홀·회전축·장착부·범퍼 기능에 영향을 줍니다. C 항목은 시험 끼움 또는 해당 부품 채택 때만 확인합니다. 작은 칩 개별 측정은 불필요합니다.',
 ['구분','구매 ID','대상','판단','필요한 확인','이유','완료 기준','실물 확인 결과'],
 critical.map(p=>[p.id,p.purchase_id,p.item,p.decision,p.need,p.reason,p.accept,'']),
 [10,30,35,25,72,72,82,55]],
 ['현장조정','현장 상황에 따라 조정할 항목','고정된 부품의 홀은 실제 부품을 놓고 전사합니다. 회전축·기준 홀·큰 관통 홀의 미확정 치수는 먼저 해결합니다.',
 ['대상','조정 방법','제한'],field.map(p=>[p.item,p.method,p.limit]),[40,100,105]],
 ['CAD노드','3,888개 CAD 노드와 구매품 연결','제조사 모델의 작은 형상은 상위 구매품에 연결했습니다. 제작품·가상 체결품과 구매품 본체는 관계 열로 구분합니다.',
 ['노드','구매 ID 또는 재료 후보','관계','주석','그룹','원래 형상 상태','이동','제작 후보'],
 nodes.map(p=>[p.node,p.purchase_id,p.relation,p.note,p.group,p.geometry_status,p.moving,p.fabricate]),[65,35,38,78,30,35,16,16]],
 ['출처','치수 근거와 적용 범위','실측, 공식 본체 자료, 상품명 표기는 서로 다른 근거입니다. 상세 홀·재고·힌지 위치까지 확인됐다는 뜻으로 확대하지 않습니다.',
 ['자료','적용 범위','출처·링크'],[
 ['사용자 부품 치수.xlsx','13개 기록 중 실측·근사 실측 10개. 원본 문구·사진 보존.','EVIDENCE/source-measurements.xlsx'],
 ['SER0063 공식 CAD·공식 페이지','55 × 20.5 × 47.38 mm 몸체 유지. 혼 별도.','https://www.dfrobot.com/product-2787.html'],
 ['ROCKET 공식 배터리 표','ES7-12 케이스 151 × 65 × 94, 단자 포함 98 mm.','https://www.gbattery.com/files/product/fea63c67182c5e5e5c72b8f6e1532027.pdf'],
 ['MG995 판매자 사진','외관 확인. 정밀 홀 피치·내측 폭·두께 미확정.','https://m.intopion.com/goods/view?no=3831971'],
 ['소형 꺽쇠','사용자 기록 20 × 24 × 24. 실물 보유 불확실. 독립적인 공식 확인으로 표시하지 않음.','부품 치수.xlsx / 시트1 / 7행'],
 ['고정 부품 홀','현장 실물 전사 허용. 작은 칩 개별 측정 불필요.','DATA/field-adjustment.json'],
 ['같은 리비전 적용','MEASURED_LAYOUT_20261006. 과거 FINAL/PASS는 당시 검사 범위.','DATA/REVISION.json']
 ],[42,100,105]]
];
for(const [name,title,note,heads,rows,widths] of specs){
 const sh=wb.worksheets.add(name);sh.showGridLines=false;sh.tabColor=teal;
 const width=heads.length, height=rows.length+5;
 const all=sh.getRangeByIndexes(0,0,height,width);all.format.font={name:'NanumGothic',size:10,color:ink};all.format.wrapText=true;all.format.verticalAlignment='center';all.format.rowHeight=60;
 const titleRange=sh.getRangeByIndexes(0,0,2,Math.min(width,6));titleRange.merge();sh.getRange('A1').values=[[title]];titleRange.format={fill:ink,font:{name:'NanumGothic',size:19,bold:true,color:'#FFFFFF'}};sh.getRange('1:2').format.rowHeight=23;
 const noteRange=sh.getRangeByIndexes(2,0,2,Math.min(width,6));noteRange.merge();sh.getRange('A3').values=[[note]];noteRange.format.font={name:'NanumGothic',size:10,color:ink};sh.getRange('3:4').format.rowHeight=25;
 sh.getRangeByIndexes(4,0,1,width).values=[heads];sh.getRangeByIndexes(5,0,rows.length,width).values=rows.map(r=>r.map(v=>v??''));
 const table=sh.tables.add(sh.getRangeByIndexes(4,0,rows.length+1,width),true,'HelmTable'+specs.findIndex(x=>x[0]===name));table.showFilterButton=true;
 sh.getRangeByIndexes(4,0,1,width).format={fill:teal,font:{name:'NanumGothic',bold:true,color:'#FFFFFF'},rowHeight:30};
 widths.forEach((w,i)=>sh.getRangeByIndexes(0,i,height,1).format.columnWidth=w);
 if(name==='전체번호')sh.getRangeByIndexes(5,0,rows.length,1).setNumberFormat('000');
 if(name==='필수확인')sh.getRange('H6:H12').format.fill='#FFF1CB';
 if(name==='CAD노드')sh.getRangeByIndexes(5,0,rows.length,width).format.rowHeight=45;
 sh.freezePanes.freezeRows(5);
}
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'전체번호!A5:D9',include:'values',tableMaxRows:5,tableMaxCols:4,maxChars:2000})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1500})).ndjson);
await fs.mkdir(path.join(out,'PREVIEWS'),{recursive:true});
for(const [name,,,,rows] of specs){const blob=await wb.render({sheetName:name,range:`A1:${name==='현장조정'||name==='출처'?'C':'G'}${Math.min(rows.length+5,9)}`,scale:1,format:'png'});await fs.writeFile(path.join(out,'PREVIEWS',`sheet-${name}.png`),new Uint8Array(await blob.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,'HELM_부품번호_실측적용표.xlsx'));
console.log('XLSX complete',parts.length,measures.length,nodes.length);
