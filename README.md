# postgresql-microservice
a small micro service that stores data in the tables either by invoking its API, or by the Cron cycle

## clone it

- `git clone https://github.com/blumareks/postgresql-microservice.git`
- or simply download it as zip

Then change the directory to
```sh
cd postgresql-microservice
```


## build it

* If you have a mac, then run commands :

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

for win OS in powershell run
```sh
.\.venv\bin\activate
```

### run it

  * in the terminal write `flask --app app run`
  * In a browser, load the url: http://127.0.0.1:5000/

### deploy it in a cloud as a microservice using RHOS

You need to setup the env variable in RHOS for the access to the postgresql:
```
URL=postgresql://ibm_cloud_ user:pass@the.address.databases.appdomain.cloud:port/ibmclouddb
```


# testing - easy path

call http://127.0.0.1:5000/alertspager
to check the response:
```json
{"alerts":[],"next_page":null,"total_pages":0}
```