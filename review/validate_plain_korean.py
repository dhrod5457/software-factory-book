"""Validate scope-preserving prose edits against fixed baseline, from repository root."""
from pathlib import Path
import re, subprocess, collections, json, hashlib
BASELINE='a812a23bf03c85f94ae109414e43df8ced795d78'
EDITED_SOURCES='9efe5bf'
def original(ref,p): return subprocess.check_output(['git','show',ref+':'+str(p)],text=True)
def code(s): return re.findall(r'(?ms)^(```|~~~)([^\n]*)\n(.*?)^\1\s*$',s)
def urls(s): return re.findall(r'https?://[^\s)]+',s)
def heads(s): return re.findall(r'^#+ .+',s,re.M)
def nums(s): return collections.Counter(re.findall(r'(?<![A-Za-z])\d+(?:[,.]\d+)*',s))
paths=sorted(Path('chapters').glob('*/draft.md'))+[Path('manuscript')/x for x in ['preface.md','glossary.md','case-study-boxes.md','figure-captions.md','book.md']]
report={'baseline':BASELINE,'scope':'Existing publication scope preserved; no canonical RC2 synchronization.','files':[]}
for p in paths:
 a=original(BASELINE,p);b=p.read_text()
 checks={'code_blocks_exact':code(a)==code(b),'headings_exact':heads(a)==heads(b),'url_order_exact':urls(a)==urls(b),'number_counts_exact':nums(a)==nums(b)}
 if p.name!='book.md':checks['prior_edited_source_exact']=b==original(EDITED_SOURCES,p)
 assert all(checks.values()),(str(p),checks)
 report['files'].append({'path':str(p),'checks':checks,'sha256':hashlib.sha256(b.encode()).hexdigest()})
p=Path('manuscript/book.md');a=original(BASELINE,p);b=p.read_text()
report['book']={'heading_count':len(heads(b)),'references_exact':a[a.index('# References'):]==b[b.index('# References'):],'figure_ids_exact':re.findall(r'<!-- FIGURE (F\d+):',a)==re.findall(r'<!-- FIGURE (F\d+):',b),'case_ids_exact':re.findall(r'<!-- CASE (C\d+):',a)==re.findall(r'<!-- CASE (C\d+):',b)}
assert report['book']['heading_count']==465 and all(v for k,v in report['book'].items() if k!='heading_count')
Path('review/plain-korean-validation-2026-10-03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: 30 files; 29 edited sources unchanged; book 465 headings, original code, number counts, URL order, references and publication IDs preserved.')
