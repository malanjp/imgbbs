<%def name="uploadform(pathname='list', id=None)">
<div class='span12'>
  <div class='span4'></div>
  <div class='span4'>
    <p class='center bold'>法に触れなければなんでもどうぞ。</p>
    <form action='${path_for(pathname)}' method='post' enctype='multipart/form-data' class="newinput">
      ${xsrf()}
      %if id:
        <input type='hidden' name='parent_id' value='${id}'>
      %endif
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
</%def>
