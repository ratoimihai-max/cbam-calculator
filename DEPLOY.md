# Publicare si acces din afara biroului

## GitHub

GitHub este bun pentru stocarea codului si colaborare. GitHub Pages nu este suficient pentru aceasta aplicatie, deoarece avem backend Python.

Pasii generali:

```powershell
cd C:\CBAM-Latest
git init
git add .
git commit -m "Initial CBAM calculator"
git branch -M main
git remote add origin https://github.com/USER/REPO.git
git push -u origin main
```

Inlocuiti `USER/REPO` cu repository-ul creat in GitHub.

## Acces din afara retelei Wi-Fi

Aveti trei variante practice:

1. Deploy in cloud pe Render

Recomandat cand aplicatia trebuie folosita de colegi din afara biroului. Codul sta pe GitHub, iar aplicatia ruleaza pe un serviciu cloud. Comanda de pornire este:

```text
python web_app.py
```

Aplicatia citeste automat variabila `PORT`, daca platforma cloud o seteaza.

### Render

Aplicatia include `render.yaml`, deci Render poate citi automat configuratia:

- service type: Web Service
- runtime: Python
- plan: Free
- build command: `pip install -r requirements.txt`
- start command: `python web_app.py`
- health check: `/`

Pasi:

1. Urcati codul in GitHub.
2. In Render: New > Blueprint sau New > Web Service.
3. Conectati repository-ul GitHub.
4. Alegeti branch-ul `main`.
5. Porniti deploy-ul.

La final, Render va afisa un URL public de forma:

```text
https://cbam-calculator.onrender.com
```

### Daca repository-ul nu apare in Render

De obicei inseamna ca Render nu are permisiune pe repository-ul GitHub.

Verificati in Render:

1. Account Settings.
2. Git Providers.
3. GitHub.
4. Configure sau Reconnect.
5. La acces repository-uri, alegeti una dintre variante:
   - All repositories; sau
   - Only select repositories si bifati `ratoimihai-max/cbam-calculator`.
6. Reveniti la New > Blueprint sau New > Web Service si dati Refresh la lista de repository-uri.

Daca repository-ul este privat, Render trebuie sa aiba explicit acces la el.

Varianta rapida:

1. In GitHub, intrati in repository.
2. Settings > General.
3. Change repository visibility.
4. Faceti temporar repository-ul Public.
5. In Render, folositi New > Web Service si cautati repository-ul din nou.

Dupa deploy, repository-ul poate ramane privat daca Render a primit permisiunile corecte.

2. VPN sau Tailscale

Bun pentru folosire interna, fara a publica aplicatia pe internet. Calculatorul din birou ramane gazda, iar colegii intra prin reteaua privata/VPN.

3. Tunel temporar

Bun pentru test rapid sau demo. Un tunel face calculatorul local accesibil printr-un URL public temporar. Nu este varianta preferata pentru folosire zilnica fara reguli clare de securitate.

## Recomandarea pentru birou

Pentru folosire serioasa in afara biroului: GitHub + deploy cloud cu HTTPS.

Pentru folosire doar de echipa interna: calculator dedicat in birou + VPN/Tailscale.
