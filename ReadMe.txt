TICKETLYV2 - Himadri Dixit, 21F1006310

A.) For starting up the Flask application: 
1. Ensure you are in the backend directory (cd backend).
2. Start up the virtual environment (cd evn/Scripts then activate.bat).
3. Run the app.py file from backend folder(python.exe app.py).

B.) For starting the VueJS system: 
1. Ensure you are in the frontend directory (cd frontend)
2. Run the command npm run serve
3. For the PWA version, use the following commands in the terminal -  npm run build;npx http-server dist

C.) For starting the Redis server: 
1. in wsl, run the command - sudo service redis-server start
2. run command - redis-cli

D.) For starting the Celery beat
1. Navigate to backend directory (cd backend)
2. Run the celery -A app.celery beat --max-interval 1 -l info

E.) For starting Celery worker:
1. Navigate to the backend directory (cd backend)
2. Run the command celery -A app.celery worker -l info -P solo


(Each of the 5 features/tasks has to be performed in separate, concurrently running terminals in Linux/WSL)