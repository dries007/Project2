<?php include "head.php"; ?>
<?php include "navigation.php"; ?>
    <div class="container">
        <h2 class="paragraph contrasttext">Hardware</h2>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Raspberry Pi Zero Essentials kit</h3>
                </div>
                <div class="panel-body">
                    <p>Het platform dat wordt gebruikt in dit project is de Raspberry Pi Zero. Dit is gekozen om een
                        aantal verschillende redenen. Ten eerste biedt de Zero een zeer goede ondersteuning voor
                        verschillende communicatie interfaces zoals SPI, I2S en I2C maar ook voor het opzetten van
                        draadloze netwerken of webservers. Ten tweede is de kostprijs ook zeer aantrekkelijk aangezien
                        de Raspberry Pi Zero Essentials kit slechts € 8 kost en alle basis benodigdheden bevat.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Rotary encoder</h3>
                </div>
                <div class="panel-body">
                    <p>Als input voor bv. het volume van het geluid of de helderheid van het scherm, wordt gebruik
                        gemaakt van een rotary encoder. De gebruikte rotary encoder heeft naast een rotatie functie ook
                        een drukknop functie.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">I2C RTC (3.3 V DS3231)</h3>
                </div>
                <div class="panel-body">
                    <p>Een andere component van de SmartAlarmClock is de DS3231 Real Time Clock. Deze chip werd gekozen
                        voor zijn hoge nauwkeurigheid en zijn instelbaarheid via de I2C interface die ook wordt
                        ondersteund in de Linux kernel. Zijn hoge nauwkeurigheid dankt de chip aan de ingebouwde
                        temperatuur gecompenseerde kristal oscillator. </p>
                    <p>Een extra reden voor de keuze van deze chip is de mogelijkheid om een batterij toe te voegen als
                        back-up voeding. Het overschakelen naar de batterijspanning gebeurt automatisch wanneer de chip
                        detecteert dat zijn voedingspanning wegvalt. Dit is handig om te kunnen garanderen dat een
                        backup alarm toch nog minstens 1 keer kan afgaan nadat de hoofdvoeding is uitgevallen. Naast de
                        tijd in uren, minuten en seconden (24 uurs of 12 uurs met AM/PM) wordt ook de datum bijgehouden.
                        Deze datum wordt automatisch aangepast, rekening houdend met het aantal dagen in elke maand en
                        ook correctie voor schrikkeljaren.</p>
                    <p>De klok geeft toegang tot 2 alarmen die bij een alarmconditie de INT pin gaan aansturen (actief
                        laag).</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Spanningsregelaar (MCP1703)</h3>
                </div>
                <div class="panel-body">
                    <p>Aangezien onze voeding 5V bedraagt en een deel van onze componenten zoals de lcd op 3.3 V werken
                        moeten we de spanning naar 3.3 V kunnen regelen. De MCP1703 is een CMOS low drop-out (max 650mV)
                        spanningsregelaar die 250 mA kan leveren en zelf slechts 2 µA verbruiken.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">2.4” 240x320 spi tft LCD (3.3 V)</h3>
                </div>
                <div class="panel-body">
                    <p>Om de klok en eventueel andere informatie te kunnen tonen aan de gebruiker hebben we een 2.4”
                        240x320 SPI tft scherm gebruikt. Correcte datasheets voor deze module zijn moeilijk te vinden.
                        Hierdoor moesten we ons baseren op de weinige informatie die we wel konden vinden en voor de
                        rest wachten tot de displays toekwamen.</p>
                    <p>De SD kaartlezer is in dit project overbodig, en dus ook niet aangesloten.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Buzzer</h3>
                </div>
                <div class="panel-body">
                    <p>De buzzer dient hoofdzakelijk als back-up alarm. Indien de voedingspanning wegvalt, zal door de
                        back-up voeding van de RTC deze toch nog blijven werken. Tijdens normale werking wordt het alarm
                        in de RTC afgezet vooraleer het zijn interrupt kan geven en zullen de speakers voor het alarm
                        zorgen. Indien de Raspberry pi niet gevoed wordt, zal dit niet gebeuren waardoor de interrupt
                        wel wordt gegeven en er een set plaats vindt van de flipflop. Dit zorgt er op zijn beurt voor
                        dat de buzzer zal afgaan tot de gebruiker de flipflop reset via een aparte knop. De Raspberry pi
                        kan de buzzer ook setten en resetten indien nodig.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Levelshifter (AN10441)</h3>
                </div>
                <div class="panel-body">
                    <p>De Raspberry Pi gebruikt 0 V en 3.3 V als GPIO level. Om te kunnen communiceren met de andere
                        componenten op 5 V zoals de RTC hebben we levelshifters nodig. Aangezien de communicatie over
                        bv. I2C bi-directioneel is, moeten de levelshifters ook bi-directioneel zijn en bovendien snel
                        kunnen werken. De makkelijkste manier is om MOSFET’s op elke lijn te plaatsen. </p>
                    <p>De AN10441’s werken bi-directioneel door zijn 3 mogelijke states:</p>
                    <p>State 1 is wanneer het 3.3 V gedeelte hoog wordt/is. In dit geval is de MOSFET niet in geleiding
                        aangezien de drempelspanning tussen de gate en de source niet is bereikt. Doordat de MOSFET niet
                        in geleiding is wordt de 5 V kant op zijn beurt ook hoog getrokken door zijn eigen pull-up
                        weerstand. Beide kanten zijn dus hoog maar op een ander spanningsniveau. </p>
                    <p>De tweede state is wanneer de 3.3 V kant wordt laag getrokken. In dit geval wordt de
                        drempelspanning tussen de gate en de source wel overschreden waardoor de MOSFET in geleiding
                        gaat. Hierdoor wordt het 5 V gedeelte ook laag getrokken. </p>
                    <p>De derde state is wanneer de 5 V kant laag wordt getrokken. In dit geval zal de diode, ingebouwd
                        in de MOSFET ervoor zorgen dat de 3.3 V kant laag wordt getrokken tot een level waarbij de
                        drempelspanning wordt overschreden. Wanneer dit gebeurt, zal de MOSFET in geleiding gaan
                        waardoor het 3.3 V gedeelte nog verder wordt laag getrokken. </p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Audio stereo DAC (PCM 5102A 3.3 V)</h3>
                </div>
                <div class="panel-body">
                    <p>Om ook muziek te kunnen spelen wanneer de wekker afgaat, hebben we een DAC (digital to analog
                        converter) nodig. Deze chip ondersteunt de I2S serial bus interface standaard die dient voor
                        digitale audio (zie intermezzo I2S). Dit is handig aangezien de Raspberry Pi Zero deze standaard
                        ondersteunt. De PCM 5102A chip heeft een stereo output, wat wil zeggen dat er een L (links) en R
                        (rechts) kanaal is voor de audio. </p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">I2S</h3>
                </div>
                <div class="panel-body">
                    <p>I2S staat voor Inter-IC Sound en is een seriële bus interface standaard die wordt gebruikt om
                        verschillende digitale audio devices te verbinden. De bus heeft minimum 3 lijnen: bit clock
                        lijn, word clock lijn (WS of LRCLK) en een data lijn. De bit clock wordt gepulst voor elke bit
                        op de datalijnen. De word clock laat het device weten voor welk kanaal (1 of 2 ) de huidige data
                        is bedoeld. Wanneer de word clock laag is, is de data bedoeld voor het linker kanaal, anders
                        voor het rechter kanaal.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Audio amplifier (TPA2016D2 5V)</h3>
                </div>
                <div class="panel-body">
                    <p>De TPA2016D2 is een stereo audio versterker die tot 2.8 W/kanaal kan leveren afhankelijk van de
                        weerstand van de speakers en de voedingsspanning. De chip bevat ook een Dynamic Range
                        Compression (DRC) en Automatic Gain Control (AGC) functie. </p>
                    <p>De DRC functie gaat dynamisch de range van het geluid beperken. Dit wil zeggen dat de harde
                        geluiden boven een bepaalde waarde worden afgezwakt terwijl de waardes onder deze drempel
                        ongewijzigd blijven. De belangrijkste functie van de DRC is het opvangen van te grote
                        niveauverschillen in het geluid.</p>
                    <p>De AGC gaat op zijn beurt ervoor zorgen dat de versterking automatisch wordt aangepast aan het
                        ingangssignaal. Zwakkere signalen zullen dus harder worden versterk als de sterkere signalen. De
                        versterker kan tussen -28dB en 30dB versterken op beide kanalen van het stereo signaal. </p>
                    <p>Het instellen van de versterker kan door via I2C, 7 registers in te stellen. In deze registers
                        kan bv. De versterking en de versterkingssnelheid worden ingesteld.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">Supercap</h3>
                </div>
                <div class="panel-body">
                    <p>Als back-up voeding voor de basisfunctionaliteit van de klok wordt een condensator van 1.5 farad
                        (“supercap”) gebruikt. De RTC schakelt over naar de voeding van de condensator indien de
                        voedingsspanning wegvalt. Aangezien de RTC en flipflop slechts enkele µA gebruiken zou de backup
                        functionaliteit zeer lang moeten meegaan, tenzij het alarm afgaat. Dan was de backup succesvol
                        en is het dus niet erg is als de wekker uitvalt.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">WS2812 LED’s</h3>
                </div>
                <div class="panel-body">
                    <p>De WS2812 led’s werken als een lange serie schakeling, waarbij elke led de eerste 24 bits
                        gebruikt om zijn kleur in te stellen. De andere bits worden doorgegeven, zie onderstaande
                        figuren. De volgorde van de bits is niet RGB, maar GRB, met hoogste bit eerst.</p>
                    <p>Wegens het niet tijdig arriveren van de PCB's werd de PWM pin voor deze LED's opgeofferd voor de
                        muziek.</p>
                </div>
            </div>
        </div>
        <div class="paragraph">
            <div class="panel panel-primary">
                <div class="panel-heading">
                    <h3 class="panel-title">PCB's</h3>
                </div>
                <div class="panel-body">
                    <p>Voor de PCB schema's en PCB lay-out wordt verwezen naar de foto pagina.</p>
                </div>
            </div>
        </div>
    </div>

<?php include "footer.php"; ?>