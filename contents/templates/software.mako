<%inherit file="layout.mako"/>

<%def name="sidebar()">
</%def>

<%def name="body()">
<style>
p, h2, h3 {
    font-size:small;
}
a {
    font-size:large;
}
</style>

<div class='span4'></div>
<div class='span4'>
<h1>Software</h1>
<hr>
<h2>* P2Proxy</h2>

<p>規制うぜーと思って P2 使ってたんですが、
一部の Mac 用 2ch クライアントで P2 経由での書き込みができない場合があったのでとりあえずの対策として実装しました。</p>

<p>正直いってバグだらけだったり未実装だらけだったりしますがとりあえず書き込めます。<br/>
BathyScaphe で書き込んでみたら 「ＥＲＲＯＲ：アクセス規制中です！！」と表示されますが書き込めてますのでスレをリロードしてみてください。</p>

<h2>* 注意</h2>

<p>BBSPINK などは P2 経由でも書き込めないので諦めてください。</p>

<p>あとエラー処理など無視してますので全然書き込めないときは現状どうしようもないです。<br/>
そのうち改善していきたいと思っています。</p>

<h2>* 環境</h2>

<p>Mac 用です。<br/>
Linux や BSDな どをお使いの方でも使えるとは思いますが設定などは自力でなんとかしてください。</p>

<h2>* 必要なもの</h2>

<ul>
<li>Python 2.7.4<br/>
2.7.x ならなんでもいいかもしれませんが未確認</li>
</ul>


<h2>* 使い方</h2>

<h3>** なにはともあれ</h3>

<blockquote><p>pip install &lt; requirement.txt<br/>
python p2proxy.py</p></blockquote>

<h3>* Mac (MountainLion) の設定</h3>

<ol>
<li>システム環境設定 > ネットワーク > お使いのネットワークを選択 > 詳細 > プロキシ</li>
<li>Web プロキシ（HTTP）にチェック</li>
<li>Web プロキシサーバに「127.0.0.1」:「8081」を入力</li>
<li>プロキシ設定を使用しないホストとドメイン に「p2.2ch.net」を追加</li>
<li>OK の後、適用</li>
</ol>

<p>4 については safari 6.x のバグの存在ゆえに設定しなければならないところです。</p>
<p>そのうち直ってくれるといいですね。。。</p>

<h3>* ダウンロード</h3>
<a href="${path_for('static', path='p2proxy-0.1.zip')}">こちら</a>
</div>
<div class='span4'></div>
</%def>




