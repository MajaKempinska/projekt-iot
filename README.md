# Projekt IoT – Konteneryzacja i wdrożenie aplikacji webowej w chmurze Azure

Wizytówka – aplikacja webowa we frameworku **Flask (Python)**, skonteneryzowana **Dockerem** i wdrożona w chmurze **Microsoft Azure** (Azure Container Registry + App Service) w modelu PaaS.
Projekt zrealizowany w ramach przedmiotu *IoT & Cloud Computing* (Collegium Da Vinci).

**Autor:** Maja Kempińska

🔗 **Aplikacja na żywo:** https://iot-maja-asia.azurewebsites.net

---

## Stack technologiczny

- **Backend:** Python, Flask, Gunicorn
- **Frontend:** HTML, CSS, szablony Jinja2 (responsywne, RWD)
- **Konteneryzacja:** Docker
- **Chmura:** Microsoft Azure – Container Registry (ACR), App Service (Linux, PaaS)
- **Baza danych:** Azure SQL Database (formularz kontaktowy zapisuje wiadomości)
- **Bezpieczeństwo:** Managed Identity (uwierzytelnianie ACR bez haseł)
- **CI/CD:** Continuous Deployment przez webhook ACR
- **IaC:** Terraform (infrastruktura jako kod)

---

## Struktura projektu

\`\`\`
projekt-iot/
├── app.py              # Aplikacja Flask (trasy, formularz kontaktowy, baza SQL)
├── requirements.txt    # Zależności Pythona
├── Dockerfile          # Definicja obrazu kontenera
├── templates/          # Szablony Jinja2 (base, strona główna, podstrony, formularz)
├── static/             # Pliki statyczne (zdjęcia, tło, favicon, logo)
└── terraform/          # Infrastruktura jako kod (main.tf)
\`\`\`

---

## Uruchomienie lokalne

### Bez Dockera
\`\`\`bash
pip install -r requirements.txt
python app.py
\`\`\`
Aplikacja dostępna pod \`http://localhost:5001\`.

### W kontenerze Docker
\`\`\`bash
docker build -t iot-app:v1 .
docker run -d -p 8080:80 --name iot-test iot-app:v1
\`\`\`
Aplikacja dostępna pod \`http://localhost:8080\`.

---

## Wdrożenie w chmurze Azure

Budowanie obrazu dla architektury zgodnej z Azure (x86) i wysłanie do rejestru:
\`\`\`bash
docker build --platform linux/amd64 -t iot-app:v1 .
docker tag iot-app:v1 iotcdv2026.azurecr.io/iot-app:v1
docker push iotcdv2026.azurecr.io/iot-app:v1
\`\`\`

> **Uwaga:** flaga \`--platform linux/amd64\` jest istotna przy budowaniu na komputerach z procesorem ARM (Apple Silicon) – Azure App Service działa na architekturze x86, więc obraz ARM nie uruchomi się w chmurze.

Dzięki skonfigurowanemu **Continuous Deployment** (webhook ACR) sam \`docker push\` automatycznie aktualizuje działającą aplikację – bez ręcznego restartu.

---

## Infrastruktura jako kod (Terraform)

Folder \`terraform/\` zawiera definicję infrastruktury. Wdrożenie:
\`\`\`bash
cd terraform
terraform init
terraform plan
terraform apply
\`\`\`

Usunięcie utworzonej infrastruktury:
\`\`\`bash
terraform destroy
\`\`\`

---

## Dobre praktyki FinOps

Wszystkie zasoby utworzono w ramach subskrypcji *Azure for Students*. Po zakończeniu projektu zasoby należy usunąć, aby nie zużywać kredytu:
\`\`\`bash
az group delete --name iot-rg --yes
\`\`\`