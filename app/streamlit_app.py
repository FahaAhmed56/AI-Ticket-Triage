"""Run: streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
from src.model import TicketTriage,MODEL_DIR

st.set_page_config(page_title='AI Ticket Triage',page_icon='🎫',layout='wide')
st.title('🎫 AI Customer Support Ticket Triage')
st.caption('Portfolio demo · Models are trained on generated examples, not real tickets.')
@st.cache_resource
def model():return TicketTriage()
with st.sidebar:
 st.header('How it works')
 st.write('TF-IDF converts ticket text into numeric features. Logistic Regression predicts ticket category and priority independently. The app suggests a team for routing.')
 st.warning('Always use human review for consequential or uncertain support decisions.')
tab1,tab2=st.tabs(['Single ticket','Batch CSV'])
with tab1:
 example='URGENT: The dashboard crashes after saving and our team is blocked. Please fix ASAP.'
 text=st.text_area('Ticket description',value=example,height=145)
 if st.button('Classify ticket',type='primary'):
  try:
   out=model().predict(text)
   a,b=st.columns(2)
   a.metric('Category',out['category']);b.metric('Priority',out['priority'])
   st.write('**Suggested queue:**',out['route_to'])
   st.write(f"Category confidence: {out['category_confidence']:.1%} | Priority confidence: {out['priority_confidence']:.1%}")
   if out['needs_human_review']:st.warning('Low model confidence: recommend human review.')
   else:st.info('Model confidence clears the demo threshold; human verification is still recommended.')
  except ValueError as e:st.error(str(e))
with tab2:
 st.write('Upload a CSV with a `text` column. Maximum 200 rows. Avoid personal or sensitive details.')
 file=st.file_uploader('CSV',type='csv')
 if file is not None:
  try:
   df=pd.read_csv(file)
   if 'text' not in df.columns:st.error('Missing required column: text')
   elif len(df)>200:st.error('Upload 200 rows or fewer.')
   else:
    outs=[model().predict(str(v)) if pd.notna(v) and str(v).strip() else {'error':'empty ticket'} for v in df['text']]
    result=pd.concat([df.reset_index(drop=True),pd.DataFrame(outs)],axis=1)
    st.dataframe(result,use_container_width=True)
    st.download_button('Download predictions CSV',result.to_csv(index=False).encode('utf-8'),'ticket_predictions.csv','text/csv')
  except Exception as e:st.error(f'Unable to process CSV: {e}')
st.divider()
st.caption('Synthetic training data makes the model a reproducible learning exercise, not a deployable production classifier.')
