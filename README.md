# Calculator CBAM

Aplicatie Python cu backend local si frontend responsive pentru calculul:

- greutatii totale a importului;
- emisiilor implicite;
- costului CBAM estimat.

## Pornire pe laptop sau PC

Din folderul proiectului:

```powershell
python web_app.py
```

Apoi deschideti in browser:

```text
http://localhost:8000
```

Sau dublu-click pe:

```text
start_cbam.bat
```

## Folosire de catre colegii din birou

Aplicatia trebuie sa ruleze pe un calculator pornit din reteaua biroului. Colegii intra din browser folosind IP-ul acelui calculator si portul `8000`.

Exemplu pentru reteaua curenta:

```text
http://192.168.0.104:8000
```

Daca pagina nu se deschide de pe calculatorul unui coleg:

- verificati ca aplicatia ruleaza in continuare pe calculatorul gazda;
- verificati ca ambele calculatoare sunt in aceeasi retea;
- permiteti Python in Windows Firewall pentru reteaua privata/de birou;
- daca firma are reguli IT mai stricte, cereti deschiderea portului `8000` in reteaua interna.

## Folosire pe telefon

Telefonul trebuie sa fie in aceeasi retea Wi-Fi cu laptopul sau PC-ul pe care ruleaza aplicatia.

Pe acest calculator, aplicatia poate fi accesata la:

```text
http://192.168.0.104:8000
```

Daca IP-ul calculatorului se schimba, il puteti afla cu:

```powershell
Get-NetIPAddress -AddressFamily IPv4
```

## Teste

```powershell
python -m unittest -v
```

## Important

Valorile din `valori_CBAM` sunt valorile implicite furnizate pentru codurile NC 7308 si 7210. Cheia `implicit` reprezinta valoarea directa, iar cheia `2026` reprezinta valoarea cu mark-up.

Lista de tari din aplicatie include tari terte uzuale pentru importuri CBAM. Nu include statele membre UE si tarile exceptate prin Anexa III CBAM: Islanda, Liechtenstein, Norvegia si Elvetia. Teritoriile Busingen, Heligoland, Livigno, Ceuta si Melilla sunt de asemenea in afara domeniului CBAM.

In aplicatie, tabelul "Valori default pe tari" arata valorile Direct si valorile 2026 cu mark-up pentru codurile NC 7210 si 7308. Daca sursa este "specifica tarii", exista o valoare separata pentru tara respectiva. Daca sursa este "default cod NC", aplicatia foloseste valoarea "_Other Countries and Territories".

Pentru panouri sandwich, greutatea se calculeaza din grosimea panoului plus grosimea tablei exterior si interior. Tabelul initial de panouri ramane baza pentru greutatea miezului, iar partea de otel se recalculeaza dupa formula `grosime tabla mm / 1000 * 7850`. Grosimile implicite sunt 0.5 mm exterior si 0.5 mm interior. Pentru panourile de acoperis, tabla exterioara foloseste coeficientul de profilare `1.08`, iar pentru panourile de perete coeficientul este `1.00`.

Rezultatele includ si costul CBAM pe metru patrat, calculat ca `cost CBAM total / suprafata`.
