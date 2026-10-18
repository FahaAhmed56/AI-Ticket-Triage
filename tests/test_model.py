import pytest
from src.dataset import generate
from src.model import TicketTriage,MODEL_DIR,ROUTES

def test_data_generation(tmp_path):
 rows=generate(tmp_path/'tickets.csv')
 assert len(rows)==720
 assert len({r['category'] for r in rows})==5
 assert len({r['priority'] for r in rows})==3

def test_models_exist():
 assert (MODEL_DIR/'category_model.joblib').exists()
 assert (MODEL_DIR/'priority_model.joblib').exists()

def test_predict_output():
 output=TicketTriage().predict('My invoice total is incorrect. Please resolve this within a few days.')
 assert output['category'] in ROUTES
 assert output['priority'] in {'Low','Medium','High'}
 assert 0<=output['category_confidence']<=1
 assert output['route_to']==ROUTES[output['category']]

def test_empty_description():
 with pytest.raises(ValueError):TicketTriage().predict('   ')
