# do-not-forget-me
Tech4Good Hackathon Project. 

For fundraising!




## Setup and Run!

### Install Dependencies

`pip install -r requirements.txt`


### Install Redis Server

`sudo apt install redis-server`

### Run Redis

#### On macOS with Homebrew

`brew services start redis`

#### On Ubuntu

`sudo systemctl start redis-server`

#### Using Docker

`docker run -d -p 6379:6379 redis:latest`


### Seed Sample Data

`python scripts/seed_data.py`

### Start the Application

`python app.py`

### Test the API

#### Health check
`curl http://localhost:5000/health`

#### Get all individuals
`curl http://localhost:5000/individuals`

#### Get wealth ranking
`curl http://localhost:5000/individuals/ranking`

#### Get statistics
`curl http://localhost:5000/stats`