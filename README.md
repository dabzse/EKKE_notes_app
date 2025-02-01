# Simple Notes APP

## usage on Linux

- create a "WORKSPACE" directory
- open a terminal in the "WORKSPACE" directory
- clone the repository into it using the following command:
```bash
git clone https://github.com/dabzse/EKKE_notes_app.git
```
- change directory to the cloned repository
```bash
cd EKKE_notes_app
```
- run the following command to install the required packages
```bash
pip install -r requirements.txt
```
- run the following command to start the server
```bash
uvicorn app.main:app --reload
```
- open a browser and navigate to the following address
```bash
http://localhost:8000
```

- for the Swagger UI (OpenAPI) navigate to the following address
```bash
http://localhost:8000/docs
```

- for the ReDoc UI navigate to the following address
```bash
http://localhost:8000/redoc
```

- and you can see the endpoints, and can test them using the Swagger UI or the ReDoc UI


## users

> user_id: **1** \
> username: **dabzse** \
> password: **localhost**

the other users are created with the `Faker` library, and saved in the `fake_data.txt` file
