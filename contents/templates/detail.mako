<%inherit file="layout.mako"/>
<%namespace name="widgets" file="widgets.mako"/>

<%def name="sidebar()">
</%def>

<%def name="body()">
${widgets.uploadform(pathname='reply', id=upimage.id)}
<div class='span4'></div>
<div class='span4'>
   <div class='detail'>
    <div class='title'>${upimage.title or '&nbsp;'}</div>
    <a href="${path_for('static', path='upload/' + upimage.img)}">
      <img src="${path_for('static', path='upload/' + upimage.img)}">
    </a>
    <div class='author'>${upimage.author or 'anonymous'}</div>
    <blockquote class='message'>${upimage.message or 'コメント無し'}</blockquote>
    <form action='${path_for('delete', id=upimage.id)}' method='post'>
      <input type='hidden' name='id' value='${upimage.id}'>
      <input type='hidden' name='img' value='${upimage.img}'>
      ${xsrf()}
      ${upimage.delkey.label('削除キー')}
      ${upimage.delkey.textbox()}
      ${upimage.delkey.error()}
      <input type='submit' value='削除' class="btn btn-primary">
    </form>
  </div>

  %for r in replies:
    <div class='detail'>
      <div class='title'>${r.title or '&nbsp;'}</div>
      <a href="${path_for('static', path='upload/' + r.img)}">
        <img src="${path_for('static', path='upload/' + r.img)}">
      </a>
      <div class='author'>${r.author or 'anonymous'}</div>
      <blockquote class='message'>${r.message or 'コメント無し'}</blockquote>
      <form action='${path_for('delete_reply', id=r.id)}' method='post'>
        <input type='hidden' name='id' value='${r.id}'>
        <input type='hidden' name='parent_id' value='${upimage.id}'>
        ${xsrf()}
        ${r.delkey.label('削除キー')}
        ${r.delkey.textbox()}
        ${r.delkey.error()}
        <input type='submit' value='削除' class="btn btn-primary">
      </form>
    </div>
  %endfor
</div>
<div class='span4'></div>
</%def>


