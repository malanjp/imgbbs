<%inherit file="layout.mako"/>

<%def name="sidebar()">
</%def>

<%def name="body()">
<div class='span4'></div>
<div class='span4'>
   <div class='detail'>
    <div class='title'>${upimage.title or '&nbsp;'}</div>
    <a href="${path_for('static', path='upload/' + upimage.img)}">
      <img src="${path_for('static', path='upload/' + upimage.img)}">
    </a>
    <div class='author'>${upimage.author or 'anonymous'}</div>
    <blockquote class='message'>${upimage.message or 'コメント無し'}</blockquote>
    <form action='${path_for('delete')}' method='post'>
      <input type='hidden' name='id' value='${upimage.id}'>
      <input type='hidden' name='img' value='${upimage.img}'>
      ${xsrf()}
      ${upimage.delkey.label('削除キー')}
      ${upimage.delkey.textbox()}
      ${upimage.delkey.error()}
      <input type='submit' value='削除' class="btn btn-primary">
    </form>
  </div>
</div>
<div class='span4'></div>
</%def>


