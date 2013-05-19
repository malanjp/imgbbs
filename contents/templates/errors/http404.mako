<%inherit file="../layout.mako"/>

<%def name="sidebar()">
</%def>

<%def name="body()">
<div class='span4'></div>
<div class='span4'>
<h1>HTTP 404 ERROR</h1>
<p>ファイルとかページが存在しないっぽいです。</p>
<a href="${path_for('list')}">TOPへ戻る</a>
</div>
<div class='span4'></div>
</%def>





