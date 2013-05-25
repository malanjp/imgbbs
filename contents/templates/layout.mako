<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <%def name="title()">しょぼい画像うｐろだ・掲示板</%def>
    <title>${self.title()} - しょぼいろだ。</title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="description" content="「しょぼいろだ。」は、できたてホヤホヤの自由に使える画像アップローダです。">
    <meta name="keywords" content="うｐろだ,画像,掲示板,upload,アップローダ,しょぼいろだ,虹,二次,虹色,BBS">
    <meta name="robots" content="index,follow">
    <meta name="revisit_after" content="1 days">
    <meta name="google-site-verification" content="wx8SPjHiF7C07gVHbeAfeisfRMK9rzhyoLHGiORtxeI" />
    <link rel="home" href="http://shoboi.net/" title="しょぼいろだ。">
    <link rel="index" href="http://shoboi.net/" title="しょぼいろだ。">
    <link rel="shortcut icon" href="/favicon.ico">

    <!-- Loading Bootstrap -->
    <link href="${path_for('static', path='uiset/css/bootstrap.min.css')}" rel="stylesheet">
    <!-- Loading Flat UI -->
    <link href="${path_for('static', path='uiset/css/flat-ui.css')}" rel="stylesheet">
    <link href="${path_for('static', path='uiset/css/bootstrap-responsive.min.css')}" rel="stylesheet">
    <link href="${path_for('static', path='css/site.css')}" type="text/css" rel="stylesheet">
  </head>
  <body>
    <div class="container-fluid">
      <div class="navbar navbar-inverse">
        <div class="navbar-inner">
          <!-- Responsive Navbar Part 1: Button for triggering responsive navbar (not covered in tutorial). Include responsive CSS to utilize. -->
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="${path_for('list')}">しょぼいろだ。<span style="font-size:small" class="hidden-phone">エロも笑いも虹も惨事もしょぼいろだで共有してね</span></a>
          <!-- Responsive Navbar Part 2: Place all navbar contents you want collapsed withing .navbar-collapse.collapse. -->
          <div class="nav-collapse collapse  pull-right">
            <ul class="nav">
            <li><a href="${path_for('software')}">Software</a></li>
            <li><a href="${path_for('about')}">About</a></li>
            <li><a href="${path_for('contact')}">Contact</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!-- /.navbar-inner -->
      </div><!-- /.navbar -->

      <div class="row-fluid">
        <div class="span12">
          ${self.body()}
        </div>
      </div>

      <div class="row-fluid">
        ## <SCRIPT TYPE="text/javascript" SRC="http://rranking13.ziyu.net/js/shoboi.js" charset=utf-8></SCRIPT>
        ## <SCRIPT TYPE="text/javascript" SRC="http://rranking13.ziyu.net/rank.php?shoboi"></SCRIPT><A href="http://www.ziyu.net/" target=_blank><IMG SRC="http://rranking13.ziyu.net/rranking.gif" alt="アクセスランキング" border=0 width=35 height=11></A><NOSCRIPT><A href="http://www.ziyu.net/" target=_blank>アクセスランキング</A></NOSCRIPT>
        <footer>
        ## TODO: footer
        </footer>
      </div>
    </div>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
    <script type="text/javascript" src="${path_for('static', path='uiset/js/bootstrap-modal.js')}"></script>
    <script type="text/javascript" src="${path_for('static', path='js/site.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-transition.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-alert.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-modal.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-dropdown.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-scrollspy.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-tab.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-tooltip.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-popover.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-button.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-collapse.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-carousel.js')}"></script>
    <script src="${path_for('static', path='uiset/js/bootstrap-typeahead.js')}"></script>
    <!-- HTML5 shim, for IE6-8 support of HTML5 elements. All other JS at the end of file. -->
    <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
    <![endif]-->

    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
    
      ga('create', 'UA-40862442-1', 'shoboi.net');
      ga('send', 'pageview');
    </script>
  </body>
</html>
