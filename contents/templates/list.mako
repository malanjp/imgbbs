<%inherit file="layout.mako"/>

<%def name="sidebar()">
</%def>
<%def name="rightbar()">
</%def>

<%def name="body()">

<form action='/' method='post' enctype='multipart/form-data' class="newinput">
  <fieldset>
    ${xsrf()}
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
          ${upimage.message.textarea('', '', class='input-xlarge', rows=5)}
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
          ${upimage.message.label('削除キー')}
        </td>
        <td>
          ${upimage.message.textbox()}
          ${upimage.message.error()}
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

  <div class="image-list">
    %for i in upimages:
    <ul class='media-list'>
      <li class='media'>
        <div class='container'>
          <a href='/static/upload/${i.img}'>
            <div class='title'>${i.title or '&nbsp;'}</div>
            <div class='thumbnail'><a href='/static/upload/${i.img}'><img src="/static/upload/${i.thumb}"></a></div>
          </a>
          <div class='author'>${i.author or 'anonymous'}</div>
        </div>
      </li>
    </ul>
  %endfor
  </div>

</%def>

