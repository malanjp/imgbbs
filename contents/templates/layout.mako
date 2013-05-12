<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>ろだたそ〜</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="/static/img/favicon.ico">
    <!-- Loading Bootstrap -->
    <link href="/static/uiset/css/bootstrap.min.css" rel="stylesheet">
    <!-- Loading Flat UI -->
    <link href="/static/uiset/css/flat-ui.css" rel="stylesheet">
    <link href="${path_for('static', path='css/site.css')}" type="text/css" rel="stylesheet" />
    <link href="/static/uiset/css/bootstrap-responsive.min.css" rel="stylesheet">
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    <script type="text/javascript" src="${path_for('static', path='js/site.js')}"></script>
    <!-- HTML5 shim, for IE6-8 support of HTML5 elements. All other JS at the end of file. -->
    <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container-fluid">
      <div class="navbar navbar-inverse">
        <div class="navbar-inner">
          <div class="container">
            <a class="brand" href="${path_for('list')}">ろだたそ〜</a>
            <ul class="nav nav-pills pull-right">
              <li><a href="${path_for('about')}">About</a></li>
              <li><a href="${path_for('contact')}">Contact</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="row-fluid">
##        <div class="span2">
##          ${self.sidebar()}
##        </div>
##        <div class="span10 pull-right">
        <div class="span12">
          ${self.body()}
        </div>
      </div>
    </div>
  </body>
</html>
