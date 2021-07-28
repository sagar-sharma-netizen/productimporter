# How to setup project locally

### Manual

1. Clone the repo
   `git clone <repo>>`
   
2. create virtualenv
    `virtualenv -p python3 ~/env/<project_name>/`
   
3. activate virtualenv
    `source ~/env/<project_name>/bin/activate`
   
4. Install requirements
    `pip install -r requirements.txt`
   
5. copy env file .env.example to .env and set env variables
    `cp .env.example .env`
   
6. Run migrations
    `python manage.py migrate`
   
7. Initialise the server
    `python manage.py runserver 8004`
   

### Using Docker

1. Clone the repo
   `git clone <repo>>`
   
2. Build docker containers
    `sudo docker-compose up -d --build`
