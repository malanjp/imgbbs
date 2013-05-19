<%def name="uploadform(pathname='list', obj=None, parent_id=None)">
<div class='span12'>
  <div class='span4'></div>
  <div class='span4'>
    <p class='center bold'>法に触れなければなんでもどうぞ。</p>
    <form action='${path_for(pathname)}' method='post' enctype='multipart/form-data' class="newinput">
      ${xsrf()}
      %if parent_id:
        <input type='hidden' name='parent_id' value='${parent_id}'>
      %endif
      <fieldset>
        <table>
          <tr>
            <td>
              ${obj.author.label('名前')}
            </td>
            <td>
              ${obj.author.textbox('名前', class='input-xlarge')}
              ${obj.author.error()}
            </td>
          </tr>
          %if hasattr(obj, 'title'):
          <tr>
            <td>
              ${obj.title.label('タイトル')}
            </td>
            <td>
              ${obj.title.textbox('', '', class='input-xlarge')}
              ${obj.title.error()}
            </td>
          </tr>
          %endif
          <tr>
            <td>
              ${obj.message.label('コメント')}
            </td>
            <td>
              ${obj.message.textarea('', '', class='input-xlarge', rows=3)}
              ${obj.message.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${obj.img.label('画像', class='required')} 
            </td>
            <td>
              <input type='file' id='img' name='img'>
              ${obj.img.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${obj.delkey.label('削除キー')}
            </td>
            <td>
              ${obj.delkey.textbox()}
              ${obj.delkey.error()}
            </td>
          </tr>
          <tr>
            <td>
              ${obj.deltime.label('自動削除')}
            </td>
            <td>
              <input type='datetime-local' id='deltime' name='deltime' placeholder='ex. 2013/05/01 12:30'>
              ${obj.deltime.error()}
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
    ${obj.error()}
    <p class='center'>* JPEG, PNG, GIF で 10MBまで</p>
  </div>
  <div class='span4'></div>
</div>
</%def>
