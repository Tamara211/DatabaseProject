import requests
res = requests.post('http://localhost:40444/api/send', json={"command1":["lalala", "bababa"], "a":"b"})
