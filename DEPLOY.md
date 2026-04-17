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

1. Deploy in cloud

Recomandat cand aplicatia trebuie folosita de colegi din afara biroului. Codul sta pe GitHub, iar aplicatia ruleaza pe un serviciu cloud. Comanda de pornire este:

```text
python web_app.py
```

Aplicatia citeste automat variabila `PORT`, daca platforma cloud o seteaza.

2. VPN sau Tailscale

Bun pentru folosire interna, fara a publica aplicatia pe internet. Calculatorul din birou ramane gazda, iar colegii intra prin reteaua privata/VPN.

3. Tunel temporar

Bun pentru test rapid sau demo. Un tunel face calculatorul local accesibil printr-un URL public temporar. Nu este varianta preferata pentru folosire zilnica fara reguli clare de securitate.

## Recomandarea pentru birou

Pentru folosire serioasa in afara biroului: GitHub + deploy cloud cu HTTPS.

Pentru folosire doar de echipa interna: calculator dedicat in birou + VPN/Tailscale.
