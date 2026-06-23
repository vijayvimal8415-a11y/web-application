# Flask Docker Application

## Build Docker Image
docker build -t flask-app .

## Run Container
docker run -d --name flask-container -p 5000:5000 flask-app

## Verify Application
curl http://localhost:5000

Expected Output:
Hello from the DevOps Practical Interview app! Version: v1
