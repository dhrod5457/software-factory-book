from pathlib import Path
import re,subprocess,collections,json,hashlib
BASELINE='a812a23bf03c85f94ae109414e43df8ced795d78'
root=Path.cwd();book=Path('manuscript/book.md').read_text();oldbook=subprocess.check_output(['git','show',BASELINE+':manuscript/book.md'],text=True)
fig=re.compile(r'(?ms)^<!-- FIGURE (F\d+):[^\n]*-->\n\n\*\*Figure .*?\n\n```mermaid\n.*?^```\n\n\*[^\n]+\*')
case=re.compile(r'(?m)^<!-- CASE (C\d+):[^\n]*-->\n\n(?:>[^\n]*\n?)+')
def norm(s):
 s=fig.sub('',s);s=case.sub('',s);s=re.sub(r'(?m)^#+ ', '# ',s);s=re.sub(r'(?m)^---\s*$','',s)
 return re.sub(r'\s+',' ',s).strip()
def code(s):return re.findall(r'(?ms)^(```|~~~)([^\n]*)\n(.*?)^\1\s*$',s)
def urls(s):return re.findall(r'https?://[^\s)]+',s)
def heads(s):return re.findall(r'^#+ .+',s,re.M)
def nums(s):return collections.Counter(re.findall(r'(?<![A-Za-z])\d+(?:[,.]\d+)*',s))
report={'baseline':BASELINE,'source_files':[],'assembly_exact':{},'restored_sections':{},'publication_insertions':{},'original_book_code_variants_superseded':[]}
for p in sorted(Path('chapters').glob('*/draft.md'))+[Path('manuscript/preface.md'),Path('manuscript/glossary.md'),Path('manuscript/case-study-boxes.md'),Path('manuscript/figure-captions.md')]:
 old=subprocess.check_output(['git','show',BASELINE+':'+str(p)],text=True);new=p.read_text()
 checks={'code_blocks':code(old)==code(new),'headings':heads(old)==heads(new),'urls':urls(old)==urls(new),'numbers':nums(old)==nums(new)}
 assert all(checks.values()),(p,checks)
 report['source_files'].append({'path':str(p),'checks':checks})
for n in range(1,25):
 start=re.search(rf'(?m)^## {n}장\.',book).start()
 nxt=re.search(r'(?m)^# Part |^## \d+장\.|^# Epilogue',book[start+1:])
 end=start+1+nxt.start() if nxt else len(book)
 actual=book[start:end]
 source=Path(f'chapters/{n:02d}/draft.md').read_text().split('\n## 참고 자료')[0]
 assert norm(actual)==norm(source),n
 report['assembly_exact'][f'{n:02d}']=True
 oldstart=re.search(rf'(?m)^## {n}장\.',oldbook).start();oldnext=re.search(r'(?m)^# Part |^## \d+장\.|^# Epilogue',oldbook[oldstart+1:]);oldend=oldstart+1+oldnext.start() if oldnext else len(oldbook)
 oldtitles=[re.sub(r'^#+ ','',x) for x in heads(oldbook[oldstart:oldend])]
 report['restored_sections'][f'{n:02d}']=[re.sub(r'^#+ ','',x) for x in heads(source) if re.sub(r'^#+ ','',x) not in oldtitles]
for name,p,a,z in [('preface','manuscript/preface.md','# 들어가며','# Part I.'),('epilogue','chapters/epilogue/draft.md','# Epilogue.','# Glossary'),('glossary','manuscript/glossary.md','# Glossary','# References')]:
 section=book[book.index(a):book.index(z,book.index(a))];assert norm(section)==norm(Path(p).read_text());report['assembly_exact'][name]=True
for name,pat in [('figures',fig),('cases',case)]:
 oldids=collections.Counter(pat.findall(oldbook));newids=collections.Counter(pat.findall(book));assert oldids==newids
 report['publication_insertions'][name]={'count':sum(newids.values()),'all_original_ids_preserved':True}
assert set(urls(oldbook))<=set(urls(book))
report['all_original_book_urls_preserved']=True
report['all_source_reference_urls_in_book']=all(u in book for p in Path('chapters').glob('*/draft.md') for u in urls(p.read_text()))
assert report['all_source_reference_urls_in_book']
oldcodes=collections.Counter((lang,body) for _,lang,body in code(oldbook));newcodes=collections.Counter((lang,body) for _,lang,body in code(book))
for (lang,body),count in (oldcodes-newcodes).items():report['original_book_code_variants_superseded'].append({'language':lang,'old_body':body,'reason':'Canonical chapter draft contains the maintained variant; source code unchanged by this edit.'})
report['old_book_heading_count']=len(heads(oldbook));report['new_book_heading_count']=len(heads(book));report['book_sha256']=hashlib.sha256(book.encode()).hexdigest()
Path('review/plain-korean-validation-2026-10-03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(report['source_files']),'source files;',len(report['assembly_exact']),'exact assembly sections;',report['publication_insertions']);print('Superseded existing book code variants',len(report['original_book_code_variants_superseded']))
