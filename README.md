# Python WA Website

## Installing / Running - Frontend

``` sh
# install node (tested on version 16)... then
cd frontend
npm install
npm run dev
# go to http://localhost:3000 in your browser
```

## QR Code Generation

Here's a bash helper function to give all the Segno <https://segno.readthedocs.io/> settings for building our QR Codes for slides.
You can just use the segno line and replace the filename and content values if you wish.

```bash
function pythonwaqr() {
    local filename="$1"
    local content="$2"
    segno --scale=10 --border=1 --dark "#295377" --data-light "#ffe15f" --light "#ffffff" --output=${filename} "${content}"
}
```

## Deployment (AWS Manual)

```bash
cd frontend
npm run build
git add dist
cd ..
cd infrastructure
cdk synth && cdk deploy --all

```


[//]: # ()
[//]: # (## Installing / Running - Backend)

[//]: # ()
[//]: # (``` sh)

[//]: # (# if you don't already have it)

[//]: # (# pip install pipenv)

[//]: # (pipenv install)

[//]: # (pipenv run uvicorn main:app --reload)

[//]: # (```)

[//]: # ()
[//]: # (## Deploying)

[//]: # ()
[//]: # (#### Deployment will run automatically on commit to main branch.)

[//]: # ()
[//]: # (### Manual deployment steps)

[//]: # ()
[//]: # (``` sh)

[//]: # (cd frontend)

[//]: # (npm run build)

[//]: # (git add dist)

[//]: # (git commit -m 'my awesome change')

[//]: # (git push heroku master)

[//]: # (```)
