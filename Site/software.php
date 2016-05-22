<?php include "head.php"; ?>
<?php include "navigation.php"; ?>
    <div class="container">
        <h2 class="paragraph contrasttext">Software</h2>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">De nodige drivers en initialisatiecode</h3>
                </div>
                <div class="panel-body">
                    <p>Wij gebruiken voor dit project een Linux distributie genaamd “Arch Linux ARM” omdat deze weinig
                        onnodige “features” heeft. Er is echter wel een zeer ruime aanbieding software en help
                        beschikbaar.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Kernel-parameters en –modules</h3>
                </div>
                <div class="panel-body">
                    <p>De Linux kernel heeft de mogelijkheid om via “serial console” te worden bestuurd, hiervoor moeten
                        in “/boot/cmdline.txt” het loglevel naar 5 worden veranderd. Om dan ook een login console te
                        krijgen en niet enkel kernel debug informatie wordt de “getty@ttyAMA0” service geactiveerd (met
                        automatische root login, zie “.bash_profile”).</p>
                    <p>Om I²C, SPI en I²S kernel modules te kunnen gebruiken moeten deze worden geactiveerd in
                        “/boot/config.txt” en “/etc/modules-load.d/raspberrypi.conf”.</p>
                    <p>Om de LCD aan te sturen via een framebuffer, in plaats van rechtstreeks SPI te gebruiken, laden
                        we via “/etc/modules-load.d/raspberrypi.conf” de “fbtft_device” kernel module. Deze module heeft
                        parameters nodig aangezien er meerdere LCD modules worden ondersteund. De parameters worden in
                        “/etc/modprobe.d/fbtft.conf” beschreven (op één regel):</p>
                    <p>“options fbtft_device custom name=fb_ili9341 gpios=reset:23,dc:22 fps=23 speed=42000000
                        rotate=90”</p>
                    <ul>
                        <li>“name=fb_ili9341” is de naam van de gebruikte LCD chip.Dit is nodig voor de initialisatie
                            code en de SPI data frames.
                        </li>
                        <li>“gpios= reset:23,dc:22” laat de driver weten waar de relevante pinnen zijn aangesloten. De
                            SPI pinnen moeten niet worden beschreven.
                        </li>
                        <li>“fps=23” bepaald de maximale vernieuwingsfrequentie.</li>
                        <li>“speed=42000000” legt de snelheid van de SPI bus vast op 42MHz.(Experimenteel bepaalde
                            maximale frequentie voor foutloze communicatie)
                        </li>
                        <li>“rotate=90” draait de framebuffer 90° zodat de LCD in landschap modus kan worden gebruikt
                            zonder extra werk in de applicatiecode.
                        </li>
                    </ul>
                    <p>De achtergrondverlichting wordt niet via deze module geregeld omdat die geen ondersteuning bied
                        voor dimmen. Later meer hierover.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">“.bash_profile”</h3>
                </div>
                <div class="panel-body">
                    <p>Door een bug in pygame is het niet mogelijk het hoofdprogramma uit te voeren als service. Om rond
                        deze beperking te werken wordt gebruik gemaakt van een automatische login op de serial console.
                        Deze voert dan “.bash_profile” uit.</p>
                    <p>Dit script print een kleine hoeveelheid debug informatie, zet enkele omgevingsvariabelen juist,
                        registreert de RTC en start het hoofdprogramma.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Nginx</h3>
                </div>
                <div class="panel-body">
                    <p>Om het Python programma niet onnodig te belasten met de web interface, worden alle statische
                        files (HTML, CSS, JavaScript, Lettertypes) via het webserverprogramma Nginx naar de gebruiker
                        gestuurd. Nginx luistert naar poort 80 (de standaard HTTP poort) en stuurt, indien het verkeer
                        voor Python bestemd is, intern het verkeer door naar poort 5000. Dit is de poort waarop normaal
                        Flask draait (zie verder). Nginx kan die onderscheiding makkelijk maken omdat al onze API calls
                        naar python via een virtuele sub-directory “/api/” gaan.</p>
                    <p>Deze manier van werken heeft nog als voordeel dat Nginx veel sneller start dan Flask, en dus is
                        de web-interface altijd klaar voor dat de gebruiker naar het IP adres surft. Als dit voorkomt
                        falen natuurlijk wel de API calls vanuit JavaScript maar dit kan worden opgevangen met een
                        boodschap (“Even geduld a.u.b., het programma is nog aan het opstarten”) waarna na korte tijd
                        opnieuw word geprobeerd.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Het hoofdprogramma (app.py)</h3>
                </div>
                <div class="panel-body">
                    <p>Voor dit programma is Python 3 gebruikt aangezien er veel ondersteuning is voor Python op de
                        Raspberry Pi. Ook omdat python in ons lessenpakket zit en omdat er (bijna) alle delen van het
                        project in gemaakt kunnen worden zonder al te ingewikkelde constructies.</p>
                    <p>Omdat CPython (de standaard Python implementatie) een “Global Interpreter Lock” gebruikt is het
                        eenvoudig om veilig globale variabelen te gebruiken als gedeelde status tussen het aansturen van
                        de LCD, de web interface en het alarm.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">LCD aansturen</h3>
                </div>
                <div class="panel-body">
                    <p>Om tekst op het scherm te krijgen wordt gebruik gemaakt van de Python module pygame. Deze module
                        is bedoelt om via Python spelletjes te ontwikkelen en is veruit de makkelijkste manier on vanuit
                        Python een framebuffer aan te sturen. Om aan te geven welke framebuffer SDL (de achterliggende
                        grafische bibliotheek van pygame) moet gebruiken is in “.bash_profile” de omgevingsvariabele
                        “SDL_FBDEV” op “/dev/fb1” gezet.</p>
                    <p>De achtergrondverlichting van de LCD module is niet verbonden via een van de kernel module
                        opties, maar met PWM0 (pin 12). Het “gpio” commando wordt gebruikt om deze pin aan te sturen
                        omdat dit minder CPU gebruikt dan de Python GPIO module.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">RTC aansturen</h3>
                </div>
                <div class="panel-body">
                    <p>Door het toevoegen van de nodige modules in de kernel parameters en het instellen van de RTC in
                        “.bash_profile” kunnen de basisfuncties van de RTC worden aangesproken zonder manueel I²C
                        commando’s uit te voeren. Het ingebouwde commando “hwclock” kan nu worden opgeroepen via een
                        “subprocess.call” met parameters </p>
                    <ul>
                        <li>“-w“ (write) voor schrijven van de systeemklok naar de RTC klok</li>
                        <li>“-r” (read) voor het weergeven van de RTC klok (handig voor debug)</li>
                        <li>“-s” (sync) voor het synchroniseren van de systeemklok naar de RTC klok</li>
                    </ul>
                    <p>Om de alarmfuncties van de RTC te gebruiken zijn is wel kennis van de registers en adressen
                        nodig, aangezien die niet zijn ondersteund door de kernel. Hiervoor worden de volgende
                        commando’s van het pakket “i2c-tools” gebruikt.</p>
                    <ul>
                        <li>i2cset [-f] [-y] [-m mask] [-r] i²cbus chip-address data-address [value] ... [mode]</li>
                        <li>i2cget [-f] [-y] i²cbus chip-address [data-address [mode]]</li>
                    </ul>
                    <p>Ook deze commando’s worden gebruikt via “subprocess.call”.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Google Calendar</h3>
                </div>
                <div class="panel-body">
                    <p>De SmartAlarmClock gebruikt de Google Calendar API om toegang te kunnen krijgen tot de kalender
                        van de gebruiker.</p>
                    <h4>Registreren van SmartAlarmClock </h4>
                    <p>Om als ontwikkelaar toegang te krijgen tot de Google APIs moet de toepassing worden geregistreerd
                        via de Google ontwikkelaarsconsole. Tijdens het registeren moet de ontwikkelaar aanduiden tot
                        welke onderdelen van Google de toepassing de toegang wilt. Na de registratie geeft Google de
                        ontwikkelaar een “client ID” en “client secret”, deze zijn zeer belangrijk verder in het
                        authenticatie proces. De “client ID” en “client secret” zijn hetzelfde voor alle
                        SmartAlarmClocks en dienen dus uitsluitend om de applicatie te onderscheiden.</p>
                    <h4>Toestemming krijgen van de gebruiken</h4>
                    <p>Dit is de eerste stap die moet worden uitgevoerd om de gebruiker om toestemming te vragen. Er
                        moet een HTTP POST request worden gestuurd naar Google met de “client ID” en een lijst van
                        “scopes”. De “scopes” geven weer tot wat de applicatie toegang wil in dit geval is het alleen
                        lezen toegang tot de kalender. Het antwoord van deze request is een JSON object dat 5 items
                        bevat. De “user code” en “verificatie URL” moeten aan de gebruiker worden getoond. Het
                        “interval”, “interval device code” en “expire time” zijn nodig voor de toepassing maar moeten
                        niet aan de gebruiker worden getoond.</p>
                    <p>De gebruiker moet naar de “verificatie URL” surfen en vervolgens zijn “user code” ingeven en op
                        volgende klikken. Nu zal een nieuwe pagina laden waarin staat beschreven welke toepassing tot
                        welke delen toegang vraagt. De laatste stap voor de gebruiker is het klikken op toestaan.</p>
                    <p>Tegelijkertijd met het tonen van de “user code” en de “verificatie URL”, kan de toepassing
                        beginnen met het pollen van het Google API OAuth endpoint voor een “access” en “refresh token”.
                        Het pollen bestaat uit een POST request die de “device code”, “client ID” en “client secret”
                        bevat. De tijd tussen requests wordt gespecifieerd door het “interval” uit het eerste request.
                        Zolang de gebruiker geen toegang heeft verleend zal het antwoord op de request een JSON object
                        zijn dat een error bevat “authorization_pending”. Deze error kan ook informatie bevatten zoals
                        “slow down” indien de requests te snel op elkaar volgen. Indien de gebruiker wel toegang heeft
                        verleend zal het antwoord een JSON object zijn dat een “access token”, “refresh token”, “token
                        type” en “expire” bevat. De “access token” wordt gebruikt tijdens het opvragen van informatie
                        uit de kalender. De “refresh token” is nodig bij het verkrijgen van een nieuwe access token na
                        het verlopen van de vorige en moet dus worden opgeslagen.</p>
                    <h4>Kalender afspraken opvragen</h4>
                    <p>De volgende stap is het opvragen van de informatie uit de Google Calendar. Hiervoor is een GET
                        request nodig naar het “/calendars/&gt;calendar id&lt;/events” endpoint met een geldige “access
                        token”. De “calendar id” is standaard “primary”, maar kan indien gewenst worden aangepast om
                        informatie uit een ander “kalenderbestand” te gebruiken. Dit is een eenvoudige manier om de
                        afspraken te filteren. Extra parameters kunnen worden toegevoegd aan de request om de
                        hoeveelheid nutteloze informatie te beperken. Zo zijn enkel de nabije toekomstige afspraken
                        nuttig en dus geven we als “timeMin” parameter de huidige tijd mee, en als “timeMax” de huidige
                        tijd plus 7 dagen. Het antwoord is een JSON object dat kan worden opgeslagen en gebruikt worden
                        in de rest van dit programma als “status[‘items’]”.
                    </p>
                    <h4>Een vervallen “Access token” vervangen</h4>
                    <p>Indien de access token is vervallen moet met de “refresh token” een nieuwe worden opgevraagd. Een
                        POST request met de “client ID”, “client secret” en “refresh token” zal als antwoord een nieuwe
                        access token geven.</p>
                    <p>De volledige handleiding over de Google OAuth 2.0 for devices API met voorbeelden is te vinden
                        op: <a href="https://developers.google.com/identity/protocols/OAuth2ForDevices">https://developers.google.com/identity/protocols/OAuth2ForDevices</a>
                    </p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Flask (Web interface API)</h3>
                </div>
                <div class="panel-body">
                    <p>Flask is een micro framework voor Python waarmee webpagina’s en Python code met elkaar kunnen
                        worden verweven. Eerst moet een instantie van de Flask klasse worden gemaakt. Dit object heeft
                        een “run” functie die met enkele parameters kan worden opgeroepen. De 2 belangrijke parameters
                        zijn “host” en “port”. De “host” parameter geeft weer op welk IP-adres Flask moet luisteren. De
                        “port” parameter geeft op zijn beurt weer op welke poort Flask moet luisteren. Met de “route”
                        annotatie wordt ingesteld op welke URL een bepaalde functie moet worden uitgevoerd. Op deze
                        manier kunnen AJAX calls vanuit de web interface een functie in Python oproepen. De opgeroepen
                        Python functie wordt uitgevoerd en de return waarde wordt als response teruggestuurd naar de web
                        interface. De response informatie kan dan worden opgenomen in de web interface. Op deze manier
                        worden bijvoorbeeld de huidige “settings” opgevraagd die in de “settings” tab van de web
                        interface kunnen worden weergegeven.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Netwerk en acces point</h3>
                </div>
                <div class="panel-body">
                    <p>De eerste stap in verband met het netwerk is het controleren van het bestaan van de “wlan0”
                        adapter. Dit kan door te controleren of het pad “/sys/class/net/wlan0” bestaat. Indien deze niet
                        bestaat wordt de errorboodschap “no wifi interface” op het scherm weergegeven. De tweede stap is
                        controleren of er al een geldig wifi profiel is ingesteld. Indien dit het geval is wordt de
                        functie “attempt_connect” opgeroepen.</p>
                    <p>Deze functie zal eerst alle actieve netwerkverbindingen op “wlan0” verbreken. Vervolgens wordt
                        via “subproces.call” het “netctl” commando uitgevoerd om naar het ingestelde wifi profiel te
                        wisselen. Indien dit lukt, zal de “status[‘network’]” op “True” worden gezet en zal het IP adres
                        op de display worden getoond. Nu de SmartAlarmClock een netwerk heeft wordt meteen ook via “ntp”
                        (network time protocol) de tijd juist gezet. Indien de synchronisatie met “ntp” mislukt wordt
                        dit via een foutboodschap op het scherm aan de gebruiker getoond. Indien de synchronisatie lukt
                        wordt de RTC tijd ook worden ge-update en wordt “status[‘draw’][‘clock’]” op “True” gezet zodat
                        de tijd op het scherm kan worden getoond. Indien het wisselen naar het netwerk profiel mislukt
                        wordt dit aan de gebruiker getoond.</p>
                    <p>Wanneer de “status[‘network’]” op “True” staat kunnen we er zeker van zijn dat we verbonden zijn
                        met een geldig netwerk. Indien er een “refresh token” is opgeslagen wordt die gebruikt om een
                        nieuwe “acces token” te vragen. Anders wordt de aanvraagprocedure gestart. Zolang er geen
                        netwerk verbinding is zal er een eigen access point worden gemaakt om de gebruiker in staat te
                        stellen om een netwerk te selecteren.</p>
                    <p>Het maken van een wifi profiel gebeurt via de tab “wifi settings” in de web interface. Een lijst
                        met beschikbare WiFi netwerken wordt geladen via JavaScript. Als het formulier is ingevuld en is
                        verzonden, wordt er een nieuw bestand aangemaakt in “/etc/netclt” met het juiste formaat en de
                        gegevens over het gekozen WiFi netwerk. Via een “attempt_connect” word er dan geprobeerd dit
                        profiel te laden.</p>
                    <p>Via het extern programma “iwlist” wordt de scan naar wifi netwerken uitgevoerd. De output van dit
                        programma is echter niet optimaal (het bevat veel overbodige info en onbruikbare netwerken) dus
                        wordt het eerst met RegEx omgezet naar een JSON vriendelijk formaat.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Rotary encoder</h3>
                </div>
                <div class="panel-body">
                    <p>Om de rotary encoder aan te sturen wordt gebruikt gemaakt van de “RPi.GPIO” module in Python.
                        Eerst wordt “GPIO” in de BCM mode gezet, dit wil zeggen dat de pinnen kunnen worden aangesproken
                        via de BCM pinnummering. Vervolgens worden pin A, pin B en pin S (switch) via “GPIO.setup” als
                        input gezet en worden de inwendige pull-up weerstanden geactiveerd. Als laatste wordt een
                        callback toegevoegd aan pin A en pin S. Deze callback functies reageren op een falling edge en
                        roepen respectievelijk de functie “int_rot” en “int_btn_ok” op. Voor pin A (rotatie) wordt een
                        bouncetime van 25ms toegevoegd en voor de pin S (switch) 250ms. De callback functies navigeren
                        door het menu aan de hand van het aantal klikken en/of rotaties door waardes in de “status”
                        dictionary te veranderen. De mogelijke waardes zijn none en elke waarde die in de enum Menu zit.
                        Elk element uit deze enum bevat een naam voor het menu veld en eventueel namen voor welke
                        settings het menu item kan aanpassen. De @unique annotatie wordt toegevoegd aan de enum om zeker
                        te zijn dat er geen waardes dubbel worden opgenomen. Dit vermijd domme typfoutjes en lang debug
                        werk.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Alarm/muziek</h3>
                </div>
                <div class="panel-body">
                    <p>Voor het afspelen van het geluid gingen we oorspronkelijk de I2S interface gebruiken. Aangezien
                        de printen echter niet tijdig werden geleverd moesten we een PWM pin opofferen om op deze manier
                        muziek af te spelen. Hierdoor kunnen we geen hardware PWM meer gebruiken voor de WS2812 led’s.
                        Zolang de muziek niet speelt wordt de software PWM gebruikt om de LCD te dimmen. Wanneer de
                        muziek speelt werkt dit echter niet meer aangezien de software en de muziek beide DMA nodig
                        hebben. Om dit op te lossen opteerde we om de helderheid van het scherm tijdens het spelen van
                        muziek op het maximum te zetten. Voor het spelen van muziek wordt gekozen uit een lijst van MP3
                        streams (VRT radiozenders). Deze worden afgespeeld via de commandline mp3 speler mpg123. </p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Web interface</h3>
                </div>
                <div class="panel-body">
                    <p>Voor de web interface is de HTML, CSS en javascript framework bootstrap gebruikt. Dit stelt ons
                        in staat om op een snelle en relatief simpele manier een mooie website te maken die schaalbaar
                        is voor verschillende toestellen. De web interface bestaat uit 1 webpagina met 4 verschillende
                        tabs. Het nut van elke tab wordt hieronder kort uitgelegd. De html en javascript met commentaar
                        is in de bijlage te vinden.</p>
                    <h4>Status tab</h4>
                    <p>De status tab geeft de gebruiker wat informatie over de status van het toestel. </p>
                    <h4>Wifi settings tab</h4>
                    <p>Deze tab geeft een lijst van alle beschikbare netwerken. De gebruiker kan hier zijn netwerk
                        kiezen en instellen.</p>
                    <h4>Clock settings tab </h4>
                    <p>De settings tab is de belangrijkste tab na het in gebruik nemen van het toestel. Hier kan de
                        gebruiker de SmartAlarmClock instellen naar zijn eigen wensen. Ten eerste kan het format en de
                        size van de tijd en de datum worden ingesteld. Ten tweede kan de gebruiker instellen hoelang
                        voor de eerste afspraak de wekker moet afgaan. Ten derde kan ook optioneel een minimum en
                        maximum wek tijd worden ingesteld. Deze waarden willen zeggen dat de wekker nooit vroeger dan
                        het minimum en later dan het maximum mag afgaan. Een vierde instelling bepaalt of de wekker
                        enkel in de week, weekend of elke dag mag afgaan. Ten vijfde kan de gebruiker kiezen of de dag
                        wordt weergegeven of niet en indien deze wordt getoond in welke size dit moet. De laatste
                        instelling bepaalt welk type van alarm er moet worden gebruikt tijdens het wekken. De gebruiker
                        heeft hierbij de keuze uit een muziekfile, muziekstream of 1 van de ingebouwde geluiden.</p>
                    <h4>Google Calendar tab</h4>
                    <p>In de Google Calendar tab kan de gebruiker kiezen welke kalender moet worden gebruikt. Ook het
                        resetten van de Google Calendar link indien deze is vervallen kan in deze tab. Op deze pagina
                        kan ook de user code en de verification URL worden getoond wanneer de gebruiker toegang moet
                        geven aan de SmartAlarmClock .</p>
                </div>
            </div>
        </div>
    </div>
<?php include "footer.php"; ?>