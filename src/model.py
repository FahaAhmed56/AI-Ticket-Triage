"""Train and serve small, reproducible text classification pipelines."""
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from src.dataset import generate

ROOT=Path(__file__).resolve().parents[1]
MODEL_DIR=ROOT/'models'
ROUTES={
 'Access & Login':'Identity & Access Team',
 'Billing & Payments':'Billing Operations',
 'Technical Bug':'Engineering Support',
 'Feature Request':'Product Management',
 'Account & Subscription':'Customer Success',
}

def _pipeline():
 return Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),lowercase=True,strip_accents='unicode',max_features=6000)),('classifier',LogisticRegression(max_iter=1200,random_state=42))])

def train():
 data=ROOT/'data'/'sample_tickets.csv'
 if not data.exists(): generate(data)
 df=pd.read_csv(data)
 train_df,test_df=train_test_split(df,test_size=0.25,random_state=42,stratify=df['category']+'|'+df['priority'])
 MODEL_DIR.mkdir(parents=True,exist_ok=True)
 metrics={'dataset':'synthetic / demonstration only','rows':len(df),'train_rows':len(train_df),'test_rows':len(test_df),'models':{}}
 for target in ('category','priority'):
  model=_pipeline();model.fit(train_df['text'],train_df[target])
  pred=model.predict(test_df['text'])
  joblib.dump(model,MODEL_DIR/f'{target}_model.joblib')
  metrics['models'][target]={'accuracy':round(float(accuracy_score(test_df[target],pred)),4),'report':classification_report(test_df[target],pred,output_dict=True,zero_division=0)}
 (MODEL_DIR/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
 return metrics

class TicketTriage:
 def __init__(self,model_dir=MODEL_DIR):
  d=Path(model_dir)
  self.category=joblib.load(d/'category_model.joblib')
  self.priority=joblib.load(d/'priority_model.joblib')
 def predict(self,text):
  if not isinstance(text,str) or not text.strip():raise ValueError('Ticket description must not be empty')
  if len(text)>10000:raise ValueError('Ticket description must be 10,000 characters or fewer')
  c=self.category.predict_proba([text])[0]; q=self.priority.predict_proba([text])[0]
  ci=int(c.argmax()); qi=int(q.argmax());label=str(self.category.classes_[ci]);urgency=str(self.priority.classes_[qi])
  return {'category':label,'category_confidence':round(float(c[ci]),4),'priority':urgency,'priority_confidence':round(float(q[qi]),4),'route_to':ROUTES[label], 'needs_human_review':bool(float(c[ci])<0.60 or float(q[qi])<0.60)}

if __name__=='__main__':
 result=train()
 for name,details in result['models'].items():print(f"{name} held-out accuracy: {details['accuracy']:.1%}")
