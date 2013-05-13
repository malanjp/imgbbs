<%inherit file="layout.mako"/>

<%def name="sidebar()">
aaa
</%def>

<%def name="body()">

<div class='span12'>
  <div class='span4'></div>
  <div class='span4'>
    <p class='center bold'>法に触れなければなんでもどうぞ。</p>
    <form action='${path_for('list')}' method='post' enctype='multipart/form-data' class="newinput">
      ${xsrf()}
      <fieldset>
        <table>
          <tr>
            <td>
              ${upimage.author.label('名前')}
            </td>
            <td>
              ${upimage.author.textbox('名前', class='input-xlarge')}
              ${upimage.author.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${upimage.title.label('タイトル')}
            </td>
            <td>
              ${upimage.title.textbox('', '', class='input-xlarge')}
              ${upimage.title.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${upimage.message.label('コメント')}
            </td>
            <td>
              ${upimage.message.textarea('', '', class='input-xlarge', rows=3)}
              ${upimage.message.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${upimage.img.label('画像', class='required')} 
            </td>
            <td>
              <input type='file' id='img' name='img'>
              ${upimage.img.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${upimage.delkey.label('削除キー')}
            </td>
            <td>
              ${upimage.delkey.textbox()}
              ${upimage.delkey.error()}
            </td>
          </tr>
          <tr>
            <td></td>
            <td>
              <input type='submit' value='送信' class="btn btn-block btn-primary">
            </td>
        </table>
      </fieldset>
    </form>
  ${upimage.error()}
  <p class='center'>* JPEG, PNG, GIF で 10MBまで</p>
  </div>
  <div class='span4'></div>
</div>

<div class='span12'>
  <div class='image-list'>
    %for i in upimages:
    <ul class='media-list'>
      <li class='media'>
        <div class='container'>
          <a href="${path_for('detail', filename=i.img)}">
            <div class='title'>${i.title or '&nbsp;'}</div>
            <div class='thumbnail'>
              <img src="${path_for('static', path='upload/' + i.thumb)}">
            </div>
          </a>
          <div class='author'>${i.author or 'anonymous'}</div>
        </div>
      </li>
    </ul>
    %endfor
  </div>
</div>

<div>
  <div class="pagination">
    <ul>
    %if int(page) > 1:
      <li class='previous'><a href="${int(page) - 1}">
            <img src="${path_for('static', path='uiset/images/pager/previous.png')}"></a></li>
    %else:
      <li class='previous desabled'><a href="">
            <img src="${path_for('static', path='uiset/images/pager/previous.png')}"></a></li>
    %endif

    %for p in range(pages):
      %if int(page) == loop.index + 1:
        <li class='active'><a href="${path_for('page', page=loop.index + 1)}">${loop.index + 1}</a></li>
      %else:
        <li><a href="${path_for('page', page=loop.index + 1)}">${loop.index + 1}</a></li>
      %endif
    %endfor

    %if int(page) < pages:
      <li class='next'><a href="${path_for('page', page=int(page) + 1)}">
            <img src="${path_for('static', path='uiset/images/pager/next.png')}"></a></li>
    %else:
      <li class='next desabled'><a href="">
            <img src="${path_for('static', path='uiset/images/pager/next.png')}"></a></li>
    %endif
    </ul>
  </div>
</div>


</%def>

