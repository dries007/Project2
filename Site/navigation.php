<?php $basename=basename($_SERVER['REQUEST_URI'], '.php'); $index= $basename == 'index' ?>
<nav class="navbar navbar-default">
    <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="index.php"><img class="logo" src="fotos/logo.jpg" alt="Smartclock logo"></a>
        </div>
        <div class="collapse navbar-collapse" id="navbar">
            <ul class="nav navbar-nav">
                <li class="<?php if ($index) echo 'active'  ?>"><a href="index.php">Home<span class="sr-only">(current)</span></a></li>
                <li class="dropdown <?php if (!$index) echo 'active' ?>">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true"
                       aria-expanded="false">Navigeren<span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <li class="<?php if ($basename == 'software') echo 'active' ?>"><a href="software.php">Software</a></li>
                        <li class="<?php if ($basename == 'hardware') echo 'active' ?>"><a href="hardware.php">Hardware</a></li>
                        <li class="<?php if ($basename == 'pictures') echo 'active' ?>"><a href="pictures.php">Foto's</a></li>
                        <li role="separator" class="divider"></li>
                        <li class="<?php if ($basename == 'about') echo 'active' ?>"><a href="about.php">Over ons</a></li>
                    </ul>
                </li>
            </ul>
            <div class="title">
                <h1>SmartAlarmClock</h1>
            </div>
        </div><!-- /.navbar-collapse -->
    </div><!-- /.container-fluid -->
</nav>