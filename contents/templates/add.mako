<%inherit file="layout.mako"/>

<h1>Sign Guestbook</h1>
${greeting.error()}
<form action="${path_for('add')}" method='post' enctype='multipart/form-data'>
    ${xsrf()}
    <p>
        ${greeting.author.label('Author:')}
        ${greeting.author.textbox()}
        ${greeting.author.error()}
    </p>
    <p>
        ${greeting.message.textarea()}
        ${greeting.message.error()}
    </p>
    <p>
        <input type='file' name='img'>
    </p>
    <p>
    <input type='submit' value='Leave Message'>
    </p>
</form>
<a href="${path_for('list')}">Back</a>
