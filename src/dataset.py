"""Generate labeled demonstration tickets. Not production training data."""
import csv
import random
from pathlib import Path

ISSUES = {
 "Access & Login": ["cannot log in to my account", "password reset link is failing", "my account is locked", "single sign on authentication fails", "multi factor code is not arriving", "permission denied when opening the portal"],
 "Billing & Payments": ["charged twice for my subscription", "invoice total is incorrect", "payment declined on checkout", "need a refund for an order", "credit card was billed unexpectedly", "receipt is missing from my billing history"],
 "Technical Bug": ["dashboard crashes after saving", "application shows an error 500", "page loads blank after update", "integration webhook stops working", "export button does not respond", "mobile app freezes during startup"],
 "Feature Request": ["please add dark mode", "can you support CSV bulk import", "need an option to schedule reports", "would love a custom dashboard widget", "please add team activity notifications", "request integration with our calendar"],
 "Account & Subscription": ["cancel my subscription next month", "upgrade our plan to enterprise", "change the organization owner", "update my account profile details", "switch subscription from monthly to annual", "delete my account and data"],
}
PREFIX = ["Hello team,", "Hi support,", "Please help:", "Customer message:", "Request:", ""]
SUFFIX = [" Thanks.", " Please advise.", " Can someone help?", " Awaiting an update.", "", " This affects our workflow."]
URGENCY = {
 "Low": ["No rush, whenever you have time.", "This is a suggestion for a future release.", "Not blocking work; just checking."],
 "Medium": ["Please resolve this within a few days.", "This is impacting my usual workflow.", "I need an update soon."],
 "High": ["URGENT: our team cannot work until this is fixed.", "Critical business impact; please help immediately.", "Production is blocked right now. ASAP!"],
}
def generate(path='data/sample_tickets.csv', seed=42):
 rng=random.Random(seed)
 rows=[]
 for category, issues in ISSUES.items():
  for issue in issues:
   for priority, urgency_phrases in URGENCY.items():
    for j in range(8):
     msg=' '.join(x for x in [rng.choice(PREFIX), issue.capitalize()+'.', rng.choice(urgency_phrases), rng.choice(SUFFIX)] if x).strip()
     rows.append({'ticket_id':f'TKT-{len(rows)+1:04d}','text':msg,'category':category,'priority':priority})
 rng.shuffle(rows)
 out=Path(path); out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='',encoding='utf-8') as f:
  writer=csv.DictWriter(f,fieldnames=['ticket_id','text','category','priority']);writer.writeheader();writer.writerows(rows)
 return rows
if __name__=='__main__':
 print(f'Generated {len(generate())} synthetic tickets')
