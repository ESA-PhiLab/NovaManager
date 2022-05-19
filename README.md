# NovaManager

## Setup Project with Pycharm

On Pycharm: Get from VCS > Follow menu to clone project (might need to add your github account if not done before)

After project cloned into Pycharm

copy .env.prod to .env and set the variables related to mysql
- DEBUG=1
- DATABASE=mysql
- MYSQL_ROOT_PASSWORD=rootpassword
- MYSQL_DATABASE=novadb
- MYSQL_USER=novauser
- MYSQL_PASSWORD=novapassword
- MYSQL_HOST=127.0.0.1
- MYSQL_PORT=3306

Launch DB, example with Docker:
```shell
cd <folder where the .env is located>
docker run --name nova-dev-mysql --env-file .env --network host -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

Allow Django to create DB, tables, ... :
```shell
export $(cat .env | xargs)
python manage.py migrate
python manage.py createsuperuser
```

Set in the .env file the OS_* with the info from creodias cloud dashboard > OpenStack RC File v3:
![Screenshot from 2022-05-18 18-50-08](https://user-images.githubusercontent.com/80842013/169098348-cc9d2618-9e8e-48e2-b41e-9a1c759fc5c2.png)

Remove from the .env all the empty variables

Add .env to PycharmConfiguration > Edit configurations
![Screenshot from 2022-05-18 18-36-46](https://user-images.githubusercontent.com/80842013/169098202-750b285a-0389-4de1-b386-834e5b057e9e.png)
![Screenshot from 2022-05-18 18-38-03](https://user-images.githubusercontent.com/80842013/169098248-b835dc58-41d8-4281-817d-899b71cf934c.png)

Launch NovaManager
![Screenshot from 2022-05-18 18-54-04](https://user-images.githubusercontent.com/80842013/169099088-b300d34f-3e37-4234-a03b-99d06bf98ca8.png)


Login in http://127.0.0.1:8000/ with the credentials created for superuser
