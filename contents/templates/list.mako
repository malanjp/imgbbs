<%inherit file="layout.mako"/>
<%namespace name="widgets" file="widgets.mako"/>

<%def name="sidebar()">
</%def>

<%def name="body()">

${widgets.uploadform('list', obj=upimage)}

<div class='span12'>
  <div class='image-list'>
    %for i in upimages:
    <ul class='media-list'>
      <li class='media'>
        <div class='container'>
          <a href="${path_for('detail', id=i.id)}">
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

