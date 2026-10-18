from fastapi.testclient import TestClient
from api.main import app
client=TestClient(app)
def test_health():
 assert client.get('/health').json()=={'status':'ok'}
def test_predict():
 response=client.post('/predict',json={'text':'I was charged twice for my subscription. Please help.'})
 assert response.status_code==200
 assert 'category' in response.json()
def test_validation():
 assert client.post('/predict',json={'text':''}).status_code==422
