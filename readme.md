# Techquiz
#### Setup
> Create `.env` file to setup enviornment variables under `config` folder.
Inside `.env` file declare following variables. 
```
DB_URL=<mongodb url here> -- required
WEBHOOK_URL=<discord webhook url> -- optional
EMAIL_API_KEY=<mailgun api key> -- optional
```

#### Installation
>Create new virtual enviornment
```
python3 -m venv env_name
```
>Activate virtual enviornment

```
source env_name/bin/activate
```
>Install dependencies
```
pip install -r requirements.txt
```
___

#### Run Project
>Activate virtual enviornment

```
source env_name/bin/activate
```
>Start server
```
uvicorn application:app --reload
```