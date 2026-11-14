import json,re,random
root='/mnt/data/study-playbook/src/';docs=json.load(open(root+'content.json'));bank=[]
for d in docs:
 for t in d['topics']:
  body=re.sub(r'\s+',' ',t['body']).strip();sent=re.split(r'(?<=[.!?])\s+',body)
  good=[s for s in sent if 45<len(s)<330 and not re.search(r'\b(?:Learning Objectives|Lecture Notes on|Student Notes)\b',s,re.I)]
  if not good:continue
  correct=good[0];other=[x for x in d['topics'] if x['id']!=t['id'] and len(x['body'])>70]
  alternatives=[]
  for o in other:
   s=re.split(r'(?<=[.!?])\s+',re.sub(r'\s+',' ',o['body']))[0]
   if 45<len(s)<330 and s!=correct:alternatives.append((s,o['title']))
  if len(alternatives)<3:continue
  random.Random(t['id']).shuffle(alternatives);opts=[correct]+[a[0] for a in alternatives[:3]]
  why=['This statement is the source-grounded description of the selected topic.']+[f'This describes “{a[1]}”, a different section in the same uploaded document.' for a in alternatives[:3]]
  for k,(kind,diff) in enumerate([('single','Easy'),('single','Medium'),('multiple','Hard'),('tf','Easy')]):
   if kind=='tf':
    statement=correct if (int(t['id'].split('-')[-1])%2==0) else alternatives[0][0]
    opts2=['True','False'];ans=[0] if statement==correct else [1];reason=f'The uploaded section “{t["title"]}” states: {correct}'
    bank.append(dict(id=f'{t["id"]}-{k}',sourceId=d['id'],topicId=t['id'],week=d['week'],course=d['course'],prompt=f'According to the source section “{t["title"]}”, is this statement accurate? {statement}',options=opts2,correct=ans,type='tf',difficulty=diff,explanation=reason,whyWrong=['The statement is supported by this section.' if ans==[0] else 'This statement belongs to a different source section.','The statement does not match this section.' if ans==[0] else 'This statement is not the description of the named section.'],page=t['page'],origin='Generated from uploaded source',hint='Compare the statement to the meaning of the named section.'))
   elif kind=='multiple':
    second=good[1] if len(good)>1 and good[1]!=correct else None
    if not second:continue
    os=[correct,second,alternatives[0][0],alternatives[1][0]]
    bank.append(dict(id=f'{t["id"]}-{k}',sourceId=d['id'],topicId=t['id'],week=d['week'],course=d['course'],prompt=f'Which TWO statements appear in the uploaded section “{t["title"]}”?',options=os,correct=[0,1],type='multiple',difficulty=diff,explanation=f'The source states: {correct} {second}',whyWrong=['Supported by the cited section.','Supported by the cited section.',f'Describes “{alternatives[0][1]}” instead.',f'Describes “{alternatives[1][1]}” instead.'],page=t['page'],origin='Generated from uploaded source',hint='Two options come from the same named section; the others come from different sections.'))
   else:
    prompt=f'Which statement best matches the lecture section “{t["title"]}”?' if k==0 else f'While revising “{t["title"]}”, which explanation is directly supported by the uploaded notes?'
    bank.append(dict(id=f'{t["id"]}-{k}',sourceId=d['id'],topicId=t['id'],week=d['week'],course=d['course'],prompt=prompt,options=opts,correct=[0],type='single',difficulty=diff,explanation=correct,whyWrong=why,page=t['page'],origin='Generated from uploaded source',hint='Focus on the exact definition or explanation in the named lecture section.'))
json.dump(bank,open(root+'questions.json','w'),ensure_ascii=False)
print('questions:',len(bank),'topics:',len(set(x['topicId'] for x in bank)))
