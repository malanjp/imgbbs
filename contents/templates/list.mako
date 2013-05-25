<%inherit file="layout.mako"/>
<%namespace name="widgets" file="widgets.mako"/>

<%def name="body()">

${widgets.uploadform('list', obj=upimage)}

${pagination()}
  <table class='image-list'>
    %for i in upimages:
    %if loop.index % 5 == 0:
    <tr class='media-list'>
    %endif
      <td class='media'>
        <div class='container'>
          <a href="${path_for('detail', id=i.id)}">
            %if i.reply_count is not None and i.reply_count > 0:
              <div class='title'>${i.title or '無題'}（${i.reply_count}）</div>
            %else:
              <div class='title'>${i.title or '無題'}</div>
            %endif
            <div class='thumbnail'>
              <img src="${path_for('img', path=i.thumb)}">
            </div>
          </a>
          <div class='author'>${i.author or '名無し'}</div>
        </div>
      </td>
    %if loop.index % 5 == 4:
    </tr>
    %endif
    %endfor
  </table>
${pagination()}
</%def>


<%def name="pagination()">
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
