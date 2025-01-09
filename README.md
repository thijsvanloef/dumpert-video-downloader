# Dumpert Video Downloader

Dumpert Downloader is een webapplicatie waarmee je video's van Dumpert kunt downloaden. De applicatie is gebouwd met Flask en maakt gebruik van Selenium en BeautifulSoup om de video's te scrapen en te downloaden.

## Inhoudsopgave

- [Dumpert Video Downloader](#dumpert-video-downloader)
  - [Inhoudsopgave](#inhoudsopgave)
  - [Installatie](#installatie)
  - [Gebruik](#gebruik)
  - [Docker](#docker)
  - [Bijdragen](#bijdragen)

## Installatie

Volg deze stappen om de applicatie lokaal te installeren en uit te voeren:

1. Clone de repository:

    ```sh
    git clone https://github.com/thijsvanloef/dumpert_downloader.git
    cd dumpert_downloader
    ```

2. Maak een virtuele omgeving aan en activeer deze:

    ```sh
    python -m venv venv
    source venv/bin/activate  # Voor Windows: venv\Scripts\activate
    ```

3. Installeer de vereiste pakketten:

    ```sh
    pip install -r requirements.txt
    ```

4. Start de applicatie:

    ```sh
    python web.py
    ```

De applicatie is nu toegankelijk op `http://127.0.0.1:8080`.

## Gebruik

1. Open de webapplicatie in je browser.
2. Voer de URL van de Dumpert-video in die je wilt downloaden.
3. Klik op "Submit".
4. De video wordt gedownload en je krijgt een downloadlink aangeboden.

## Docker

Je kunt de applicatie ook uitvoeren met Docker. Volg deze stappen:

1. Bouw de Docker-image:

    ```sh
    docker build -t dumpert_downloader .
    ```

2. Start een container:

    ```sh
    docker run -p 8080:8080 dumpert_downloader
    ```

De applicatie is nu toegankelijk op `http://localhost:8080`.

## Bijdragen

Bijdragen zijn welkom! Volg deze stappen om bij te dragen:

1. Fork de repository.
2. Maak een nieuwe branch aan (`git checkout -b feature/naam-van-feature`).
3. Commit je wijzigingen (`git commit -am 'Voeg nieuwe feature toe'`).
4. Push naar de branch (`git push origin feature/naam-van-feature`).
5. Open een Pull Request.
