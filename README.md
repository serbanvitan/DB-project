# ReadMe - Apigee API Project

## Partea 1: Configurarea în Google Cloud Platform (GCP)

Pentru a pune în aplicare proiectul nostru care interacționează cu Apigee, am început prin configurarea corespunzătoare a platformei Google Cloud. Primul pas a fost crearea unui **proiect în GCP**. După ce am creat proiectul, am activat **Apigee API**, un serviciu esențial care permite crearea, gestionarea și monitorizarea aplicațiilor API.

După activarea Apigee API, am trecut la configurarea unui **Service Account** în GCP, un pas esențial pentru a interacționa cu API-urile Apigee. Acesta este contul care ne permite să autentificăm aplicațiile care vor utiliza API-ul Apigee. Pentru crearea unui service account am navigat în **IAM & Admin** → **Service Accounts**, am creat un cont cu permisiunile necesare (roluri precum `Apigee Admin` sau `Apigee Viewer`), în funcție de scopul nostru.

După crearea service account-ului, am generat un **fisier de cheie JSON** pentru contul respectiv. Acest fișier conține toate informațiile necesare (precum cheia API și datele contului de service) pentru a autentifica aplicațiile noastre când se conectează la Apigee.

În continuare, am descărcat acest fișier JSON și l-am utilizat pentru a asigura accesul la Apigee prin API. De asemenea, am implementat scripturi în Python pentru a lista aplicațiile, a căuta aplicațiile după dezvoltator și a crea noi aplicații, toate având ca fundament autentificarea prin acest fișier JSON.

## Partea 2: Securizarea Credentialelor API

Pentru a asigura un mediu cât mai sigur și cât mai apropiat de producție, am decis să **securizăm credentialele API**. Într-o aplicație reală de producție, securizarea credentialelor este esențială pentru protejarea datelor sensibile. În acest proiect, am folosit două metode de securizare a acestora:

### Securizarea credentialelor în aplicația Python:
Am folosit **GitHub Secrets** pentru a securiza fișierul JSON al contului de service și informațiile necesare pentru Apigee. În GitHub, am creat două secrete:
- **SERVICE_ACCOUNT_FILE**: conține fișierul JSON cu credentialele contului de service.
- **APIGEE_ORG**: conține ID-ul organizației Apigee.

În cadrul pipeline-ului nostru CI/CD, am descărcat aceste secrete din GitHub și le-am folosit pentru a crea fișierul `service-account.json`, care este necesar pentru autentificarea în GCP. Apoi, am utilizat acest fișier pentru a interacționa cu Apigee API și a realiza operațiile de listare și creare aplicații.

### Secundarea credentialelor în Docker:
În ceea ce privește implementarea în **Docker**, am folosit o metodă de securizare a credentialelor prin **mounting** fișierului JSON al contului de service ca volum. Astfel, am montat fișierul `service-account.json` într-un container Docker și l-am setat în variabila de mediu `GOOGLE_APPLICATION_CREDENTIALS`, pentru a-l utiliza în aplicație. În acest fel, am asigurat că credentialele sunt protejate și că nu au fost expuse în codul sursă sau Dockerfile.

Aceste metode de securizare au fost esențiale pentru a crea un mediu similar cu cel de producție, unde accesul la datele sensibile trebuie să fie limitat și protejat.

## Partea 3: Provocări și Soluții

În ciuda faptului că majoritatea pașilor au fost implementați fără probleme mari, am întâmpinat câteva **provocări** pe parcursul proiectului:

1. **Configurarea Apigee în GCP**: La început, nu eram siguri ce permisiuni exacte trebuiau acordate contului de service pentru a accesa corect Apigee API. După consultarea documentației oficiale a GCP și Apigee, am reușit să configurăm corect contul de service cu rolurile adecvate, ceea ce a permis aplicației să acceseze Apigee API fără erori.

2. **Problema cu `EOFError` în Python (CI/CD)**: În timpul rulării scriptului Python în cadrul pipeline-ului CI/CD, am întâmpinat o eroare legată de input-ul din linia de comandă. Eroarea a apărut deoarece aplicația a încercat să citească de la tastatură într-un mediu în care nu exista o interacțiune directă (CI/CD). Mesajul de eroare a fost:
   ```
   File "/app/apigee_manager.py", line 129, in <module>
       main()
   File "/app/apigee_manager.py", line 101, in main
       choice = input("\nEnter your choice: ")
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   EOFError: EOF when reading a line
   ```
   Pentru a rezolva această problemă, am adăugat o verificare în scriptul Python care să detecteze dacă aplicația rulează în mediu CI/CD și să seteze automat o alegere predefinită:
   ```python
   if os.getenv('CI') == 'true':
       choice = '1'
   ```
   Aceasta a permis aplicației să continue rularea fără a necesita input manual, simțind mediul automatizat al CI/CD.

În ciuda acestor provocări, am reușit să găsim soluțiile necesare și să implementăm corect funcționalitățile aplicației, bazându-ne pe documentația detaliată a GCP și Apigee. Astfel, am finalizat cu succes implementarea și testarea aplicației.

### Concluzie:
Acest proiect ne-a ajutat să înțelegem cum să integrăm Apigee API într-o aplicație reală, să lucrăm cu Google Cloud Platform și să implementăm un mediu de producție simulat folosind Docker și CI/CD. De asemenea, am învățat importanța securizării credentialelor și cum să configurăm corect permisiunile și accesul în cloud. Cu ajutorul documentației și al soluțiilor implementate, am reușit să depășim provocările întâmpinate și să livrăm un proiect complet funcțional.
