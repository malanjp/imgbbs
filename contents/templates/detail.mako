<%inherit file="layout.mako"/>
<%namespace name="widgets" file="widgets.mako"/>

<%def name="sidebar()">
</%def>

<%def name="body()">
${widgets.uploadform(pathname='reply', obj=reply, parent_id=reply.parent_id)}

<div class='span4'></div>
<div class='span4'>
   <div class='detail'>
    <a href="${path_for('img', path=upimage.img)}">
      <img src="${path_for('img', path=upimage.img)}">
    </a>
    <div class='author'>
        <span class='title'>${upimage.title or '無題'}</span>
        名前：<span class='name'>${upimage.author or '名無し'}</span>
        ${upimage.created_on}&nbsp;&nbsp;<a id="pop_modal_${upimage.id}"
          data-toggle="modal"
          data-target="modal_${upimage.id}"
          href="#" onclick="$('#modal_${upimage.id}').modal();">削除</a>
    </div>
    <blockquote class='message'>${upimage.message or 'コメント無し'}<div class='del_schedule'>${upimage.deltime}&nbsp;ごろ削除予定</div></blockquote>
  </div>

  ## 削除モーダル
  <div id="modal_${upimage.id}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="投稿を削除" aria-hidden="true">
    <form action='${path_for('delete', id=upimage.id)}' method='post'>
      <input type='hidden' name='id' value='${upimage.id}'>
      <input type='hidden' name='img' value='${upimage.img}'>
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
        <h3 id="myModalLabel">Modal header</h3>
      </div>
      <div class="modal-body">
        ${xsrf()}
        ${upimage.delkey.textbox(placeholder='削除キー', class='input-xxlarge')}
        ${upimage.delkey.error()}
      </div>
      <div class="modal-footer">
        <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
        <input type='submit' value='削除' class="btn btn-primary">
      </div>
    </form>
  </div>
  <hr>

  %for r in replies:
    <div class='detail'>
      %if r.img:
      <a href="${path_for('img', path=r.img)}">
        <img src="${path_for('img', path=r.img)}">
      </a>
      %endif
      <div class='author'>
        名前：<span class='name'>${r.author or '名無し'}</span>
        ${r.created_on}&nbsp;&nbsp;<a id="pop_modal_${r.id}"
          data-toggle="modal"
          data-target="modal_${r.id}"
          href="#" onclick="$('#modal_${r.id}').modal();">削除</a>
      </div>
      <blockquote class='message'>${r.message or 'コメント無し'}
        %if r.deltime:
          <div class='del_schedule'>${r.deltime}&nbsp;ごろ削除予定</div>
        %endif
    </blockquote>

    </div>
    </script>

    ## 削除モーダル
    <div id="modal_${r.id}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="投稿を削除" aria-hidden="true">
      <form action='${path_for('delete_reply', id=r.id)}' method='post'>
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
          <h3 id="myModalLabel">Modal header</h3>
        </div>
        <div class="modal-body">
          <input type='hidden' name='id' value='${r.id}'>
          <input type='hidden' name='parent_id' value='${upimage.id}'>
          ${xsrf()}
          ${r.delkey.textbox(placeholder='削除キー', class='input-xxlarge')}
          ${r.delkey.error()}
        </div>
        <div class="modal-footer">
          <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
          <input type='submit' value='削除' class="btn btn-primary">
        </div>
      </form>
    </div>
    <hr>
  %endfor
</div>
<div class='span4'></div>
</%def>


