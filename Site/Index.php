<?php include "head.php"?>
<?php include "navigation.php";?>

	<div class="container">
		<div id="carousel-example-generic" class="dia carousel slide" data-ride="carousel">
		  <!-- Indicators -->
		  <ol class="carousel-indicators">
			<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
			<li data-target="#carousel-example-generic" data-slide-to="1"></li>
			<li data-target="#carousel-example-generic" data-slide-to="2"></li>
			<li data-target="#carousel-example-generic" data-slide-to="3"></li>
		  </ol>

		  <!-- Wrapper for slides -->
		  <div class="carousel-inner" role="listbox">
			<div class="item active">
			  <img src="foto's/sheet1.png" alt="foto">
			  <div class="carousel-caption">
				<h3>Altium schema sheet 1</h3>
			  </div>
			</div>
			<div class="item">
			  <img src="foto's/sheet2.png" alt="foto">
			  <div class="carousel-caption">
				<h3>Altium schema sheet 2</h3>
			  </div>
			</div>
			<div class="item">
			  <img src="foto's/PCBlayout.png" alt="foto">
			  <div class="carousel-caption">
				<h3>Altium PCB lay-out</h3>
			  </div>
			</div>
			<div class="item">
			  <img src="foto's/placeholder.png" alt="foto">
			  <div class="carousel-caption">
				<h3>foto4</h3>
			  </div>
			</div>
		  </div>

		  <!-- Controls -->
		  <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
			<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
			<span class="sr-only">Previous</span>
		  </a>
		  <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
			<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
			<span class="sr-only">Next</span>
		  </a>
		</div>
			<div class="paragraph container">
		<div class="custompan panel panel-primary">
		  <div class="panel-heading">
			<h3 class="panel-title">Voorwoord</h3>
		  </div>
		  <div class="panel-body">
			<p>Het idee van de SmartAlarmClock ontstond uit de frustratie tijdens het zetten van de wekker. Je moet namelijk eerst op je kalender kijken of je de volgende dag afspraken hebt en zoja om welk uur om te weten wanneer je de wekker moet zetten. Dit proces elke dag herhalen is niet echt efficiënt. 
			De SmartAlarmClock probeert hiervoor een oplossing te bieden door de klok en de kalender op een slimme manier te combineren.</p>
			<p>De SmartAlarmClock zal afhankelijk van informatie uit de Google kalender en de instellingen zelf het alarm instellen. Op deze manier kan de gebruiker zorgeloos slapen zonder ongerust te moeten zijn over het missen van een afspraak.</p>
		  </div>
		</div>
	</div>
	</div>
	
<?php include "footer.php";?>