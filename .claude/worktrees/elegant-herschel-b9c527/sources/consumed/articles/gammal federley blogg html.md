---
title: "gammal federley blogg html"
kind: article
party: third
source: evernote
source_id: "Privat:599"
evernote_notebook: "Privat"
provenance: extracted
ingested: 2026-05-13
created: 2014-03-16
updated: 2014-03-16
tags: []
status: reference
register: consumed
reclassified: 2026-05-18
---

<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "[http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd](http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd)">

<html expr:dir='data:blog.languageDirection' xmlns='[http://www.w3.org/1999/xhtml](http://www.w3.org/1999/xhtml)' xmlns:b='[http://www.google.com/2005/gml/b](http://www.google.com/2005/gml/b)' xmlns:data='[http://www.google.com/2005/gml/data](http://www.google.com/2005/gml/data)' xmlns:expr='[http://www.google.com/2005/gml/expr](http://www.google.com/2005/gml/expr)'>

  <head>

    <b:include data='blog' name='all-head-content'/>

    <title><data:blog.pageTitle/></title>

    <b:skin><![CDATA[/*

 * Blogger Template Style

 *

 * Sand Dollar

 * by Jason Sutter

 * Updated by Blogger Team

 */

/* Variable definitions

   ====================

   <Variable name="textcolor" description="Text Color"

             type="color" default="#000" value="#000000">

   <Variable name="bgcolor" description="Page Background Color"

             type="color" default="#f6f6f6" value="#f6f6f6">

   <Variable name="pagetitlecolor" description="Blog Title Color"

             type="color" default="#F5DEB3" value="#F5DEB3">

   <Variable name="pagetitlebgcolor" description="Blog Title Background Color"

             type="color" default="#DE7008" value="#DE7008">

  <Variable name="descriptionColor" description="Blog Description Color"

            type="color" default="#9E5205"  value="#9E5205"/>

   <Variable name="descbgcolor" description="Description Background Color"

             type="color" default="#F5E39e" value="#F5E39e">

   <Variable name="titlecolor" description="Post Title Color"

             type="color" default="#9E5205" value="#9E5205">

   <Variable name="datecolor" description="Date Header Color"

             type="color" default="#777777" value="#777777">

   <Variable name="footercolor" description="Post Footer Color"

             type="color" default="#444444" value="#444444">

   <Variable name="linkcolor" description="Link Color"

             type="color" default="#DE7008" value="#DE7008">

   <Variable name="footerlinkcolor" description="Post Footer Link Color"

             type="color" default="#968a0a" value="#968a0a">

   <Variable name="visitedlinkcolor" description="Visited Link Color"

             type="color" default="#DE7008" value="#DE7008">

   <Variable name="sidebarcolor" description="Sidebar Title Color"

             type="color" default="#B8A80D" value="#B8A80D">

   <Variable name="sidebarlinkcolor" description="Sidebar Link Color"

             type="color" default="#999999" value="#999999">

   <Variable name="bordercolor" description="Border Color"

             type="color" default="#e0ad12" value="#e0ad12">

   <Variable name="bodyfont" description="Text Font"

             type="font"

             default="normal normal 100% 'Trebuchet MS',Trebuchet,Verdana,Sans-Serif" value="normal normal 100% 'Trebuchet MS',Trebuchet,Verdana,Sans-Serif">

   <Variable name="headerfont" description="Sidebar Title Font"

             type="font"

             default="normal bold 150% Verdana,Sans-serif" value="normal bold 150% Verdana,Sans-serif">

   <Variable name="dateHeaderFont" description="Date Header Font"

             type="font"

             default="normal bold 105% 'Trebuchet MS',Trebuchet,Verdana,Sans-serif" value="normal bold 105% 'Trebuchet MS',Trebuchet,Verdana,Sans-serif">

   <Variable name="pagetitlefont" description="Blog Title Font"

             type="font" default="normal bold 300% Verdana,Sans-Serif" value="normal bold 300% Verdana,Sans-Serif">

   <Variable name="titlefont" description="Post Title Font"

             type="font" default="normal bold 160% Verdana,Sans-Serif" value="normal bold 160% Verdana,Sans-Serif">

   <Variable name="startSide" description="Start side in blog language"

             type="automatic" default="left" value="left">

   <Variable name="endSide" description="End side in blog language"

             type="automatic" default="right" value="right">

*/

body {

  margin:0px;

  padding:0px;

  background:$bgcolor;

  color:$textcolor;

  font-size: small;

}

#outer-wrapper {

  font:$bodyfont;

}

              

a {

 color:$linkcolor;

}

              

a:hover {

 color:$titlecolor;

}

a img {

  border-width: 0;

}

                       

#content-wrapper {

  padding-top: 0;

  padding-$endSide: 1em;

  padding-bottom: 0;

  padding-$startSide: 1em;

}

@media all  {

  div#main {

    float:$endSide;

    width:66%;

    padding-top:30px;

    padding-$endSide:0;

    padding-bottom:10px;

    padding-$startSide:1em;

    border-$startSide:dotted 1px $bordercolor;

    word-wrap: break-word; /* fix for long text breaking sidebar float in IE */

    overflow: hidden;     /* fix for long non-text content breaking IE sidebar float */

  }                 

  div#sidebar {

    margin-top:20px;

    margin-$endSide:0px;

    margin-bottom:0px;

    margin-$startSide:0;

    padding:0px;

    text-align:$startSide;

    float: $startSide;

    width: 31%;

    word-wrap: break-word; /* fix for long text breaking sidebar float in IE */

    overflow: hidden;     /* fix for long non-text content breaking IE sidebar float */

  }

}

                       

@media handheld  {

  div#main {

   float:none;

   width:90%;

 }

 

  div#sidebar {

    padding-top:30px;

    padding-$endSide:7%;

    padding-bottom:10px;

    padding-$startSide:3%;

  }                         

}

                       

#header {

  padding-top:0px;

  padding-$endSide:0px;

  padding-bottom:0px;

  padding-$startSide:0px;

  margin-top:0px;

  margin-$endSide:0px;

  margin-bottom:0px;

  margin-$startSide:0px;

  border-bottom:dotted 1px $bordercolor;

  background:$descbgcolor;

}

                             

h1 a:link  {

 text-decoration:none;

 color:$pagetitlecolor

}

              

h1 a:visited  {

  text-decoration:none;

  color:$pagetitlecolor

}

h1,h2,h3 {

  margin: 0;

}

h1 {

  padding-top:25px;

  padding-$endSide:0px;

  padding-bottom:10px;

  padding-$startSide:5%;

  color:$pagetitlecolor;

  background:$pagetitlebgcolor;

  font:$pagetitlefont;

  letter-spacing:-2px;

}

              

h3.post-title {

  color:$titlecolor;

  font:$titlefont;

  letter-spacing:-1px;

}

h3.post-title a,

h3.post-title a:visited {

  color: $titlecolor;

}

               

h2.date-header  {

  margin-top:10px;

  margin-$endSide:0px;

  margin-bottom:0px;

  margin-$startSide:0px;

  color:$datecolor;

  font: $dateHeaderFont;

}

              

h4 {

 color:#aa0033;

}

                             

#sidebar h2 {

  color:$sidebarcolor;

  margin:0px;

  padding:0px;

  font:$headerfont;

}

#sidebar .widget {

  margin-top:0px;

  margin-$endSide:0px;

  margin-bottom:33px;

  margin-$startSide:0px;

  padding-top:0px;

  padding-$endSide:0px;

  padding-bottom:0px;

  padding-$startSide:0px;

  font-size:95%;

}

#sidebar ul {

  list-style-type:none;

  padding-$startSide: 0;

  margin-top: 0;

}

#sidebar li {

  margin-top:0px;

  margin-$endSide:0px;

  margin-bottom:0px;

  margin-$startSide:0px;

  padding-top:0px;

  padding-$endSide:0px;

  padding-bottom:0px;

  padding-$startSide:0px;

  list-style-type:none;

  font-size:95%;

}

.description {

  padding:0px;

  margin-top:7px;

  margin-$endSide:12%;

  margin-bottom:7px;

  margin-$startSide:5%;

  color:$descriptionColor;

  background:transparent;

  font:bold 100% Verdana,Sans-Serif;

}

 .post {

  margin-top:0px;

  margin-$endSide:0px;

  margin-bottom:30px;

  margin-$startSide:0px;

}

              

.post strong {

  color:$textcolor;

  font-weight:bold;

}

pre,code {

 color:$sidebarlinkcolor;

}

strike {

 color:$sidebarlinkcolor;

}

.post-footer  {

  padding:0px;

  margin:0px;

  color:$footercolor;

  font-size:80%;

}

.post-footer a {

  border:none;

  color:$footerlinkcolor;

  text-decoration:none;

}

.post-footer a:hover {

  text-decoration:underline;

}

#comments {

  padding:0px;

  font-size:110%;

  font-weight:bold;

}

.comment-author {

  margin-top: 10px;

 }

.comment-body {

  font-size:100%;

  font-weight:normal;

  color:black;

}

.comment-footer {

  padding-bottom:20px;

  color:$footercolor;

  font-size:80%;

  font-weight:normal;

  display:inline;

  margin-$endSide:10px

}

.deleted-comment  {

  font-style:italic;

  color:gray;

}

.comment-link  {

  margin-$startSide:.6em;

}

.profile-textblock {

  clear: both;

  margin-$startSide: 0;

}

.profile-img {

  float: $startSide;

  margin-top: 0;

  margin-$endSide: 5px;

  margin-bottom: 5px;

  margin-$startSide: 0;

  border: 2px solid $pagetitlebgcolor;

}

#sidebar a:link  {

  color:$sidebarlinkcolor;

  text-decoration:none;

}   

#sidebar a:active  {

  color:#ff0000;

  text-decoration:none;

}    

#sidebar a:visited  {

  color:sidebarlinkcolor;

  text-decoration:none;

}

#sidebar a:hover {

  color:$sidebarcolor;

  text-decoration:none;

}

.feed-links {

  clear: both;

  line-height: 2.5em;

}

#blog-pager-newer-link {

  float: $startSide;

 }

 

#blog-pager-older-link {

  float: $endSide;

}

 

#blog-pager {  

  text-align: center;

}

.clear {

  clear: both;

}

.widget-content {

  margin-top: 0.5em;

}

/** Tweaks for layout editor preview */

body#layout #outer-wrapper {

  margin-top: 0;

}

body#layout #main,

body#layout #sidebar {

  margin-top: 10px;

  padding-top: 0;

}

]]
>
</b:skin>

  </head>

  <body>

  <b:section class='navbar' id='navbar' maxwidgets='1' showaddelement='no'>

    <b:widget id='Navbar1' locked='true' title='Navbar' type='Navbar'>

      <b:includable id='main'>&lt;script type=&quot;text/javascript&quot;&gt;

    function setAttributeOnload(object, attribute, val) {

      if(window.addEventListener) {

        window.addEventListener(&#39;load&#39;,

          function(){ object[attribute] = val; }, false);

      } else {

        window.attachEvent(&#39;onload&#39;, function(){ object[attribute] = val; });

      }

    }

  &lt;/script&gt;

&lt;div id=&quot;navbar-iframe-container&quot;&gt;&lt;/div&gt;

&lt;script type=&quot;text/javascript&quot; src=&quot;https://apis.google.com/js/plusone.js&quot;&gt;&lt;/script&gt;

&lt;script type=&quot;text/javascript&quot;&gt;

        gapi.load(&quot;gapi.iframes:gapi.iframes.style.bubble&quot;, function() {

          if (gapi.iframes &amp;&amp; gapi.iframes.getContext) {

            gapi.iframes.getContext().openChild({

                url: &#39;https://www.blogger.com/navbar.g?targetBlogID\758350916\46blogName\75Federley\46publishMode\75PUBLISH_MODE_BLOGSPOT\46navbarType\75BLUE\46layoutType\75LAYOUTS\46searchRoot\75http://federley.blogspot.com/search\46blogLocale\75sv\46v\0752\46homepageUrl\75http://federley.blogspot.com/\46vt\0757572812111772135007&#39;,

                where: document.getElementById(&quot;navbar-iframe-container&quot;),

                id: &quot;navbar-iframe&quot;

            });

          }

        });

      &lt;/script&gt;&lt;script type=&quot;text/javascript&quot;&gt;

(function() {

var script = document.createElement(&#39;script&#39;);

script.type = &#39;text/javascript&#39;;

script.src = &#39;//pagead2.googlesyndication.com/pagead/js/google_top_exp.js&#39;;

var head = document.getElementsByTagName(&#39;head&#39;)[0];

if (head) {

head.appendChild(script);

}})();

&lt;/script&gt;

</b:includable>

    </b:widget>

  </b:section>

  <div id='outer-wrapper'><div id='wrap2'>

    <!-- skip links for text browsers -->

    <span id='skiplinks' style='display:none;'>

      <a href='#main'>skip to main </a> |

      <a href='#sidebar'>skip to sidebar</a>

    </span>

    <div id='header-wrapper'>

      <b:section class='header' id='header' maxwidgets='1' showaddelement='no'>

        <b:widget id='Header1' locked='true' title='Federley (rubrik)' type='Header'>

          <b:includable id='main'>

  <b:if cond='data:useImage'>

    <b:if cond='data:imagePlacement == &quot;BEHIND&quot;'>

      <!--

      Show image as background to text. You can't really calculate the width

      reliably in JS because margins are not taken into account by any of

      clientWidth, offsetWidth or scrollWidth, so we don't force a minimum

      width if the user is using shrink to fit.

      This results in a margin-width's worth of pixels being cropped. If the

      user is not using shrink to fit then we expand the header.

      -->

      <b:if cond='data:mobile'>

          <div id='header-inner'>

            <div class='titlewrapper' style='background: transparent'>

              <h1 class='title' style='background: transparent; border-width: 0px'>

                <b:include name='title'/>

              </h1>

            </div>

            <b:include name='description'/>

          </div>

        <b:else/>

          <div expr:style='&quot;background-image: url(\&quot;&quot; + data:sourceUrl + &quot;\&quot;); &quot;                        + &quot;background-position: &quot;                        + data:backgroundPositionStyleStr + &quot;; &quot;                        + data:widthStyleStr                        + &quot;min-height: &quot; + data:height                        + &quot;_height: &quot; + data:height                        + &quot;background-repeat: no-repeat; &quot;' id='header-inner'>

            <div class='titlewrapper' style='background: transparent'>

              <h1 class='title' style='background: transparent; border-width: 0px'>

                <b:include name='title'/>

              </h1>

            </div>

            <b:include name='description'/>

          </div>

        </b:if>

    <b:else/>

      <!--Show the image only-->

      <div id='header-inner'>

        <a expr:href='data:blog.homepageUrl' style='display: block'>

          <img expr:alt='data:title' expr:height='data:height' expr:id='data:widget.instanceId + &quot;_headerimg&quot;' expr:src='data:sourceUrl' expr:width='data:width' style='display: block'/>

        </a>

        <!--Show the description-->

        <b:if cond='data:imagePlacement == &quot;BEFORE_DESCRIPTION&quot;'>

          <b:include name='description'/>

        </b:if>

      </div>

    </b:if>

  <b:else/>

    <!--No header image -->

    <div id='header-inner'>

      <div class='titlewrapper'>

        <h1 class='title'>

          <b:include name='title'/>

        </h1>

      </div>

      <b:include name='description'/>

    </div>

  </b:if>

</b:includable>

          <b:includable id='description'>

  <div class='descriptionwrapper'>

    <p class='description'><span><data:description/></span></p>

  </div>

</b:includable>

          <b:includable id='title'>

  <b:if cond='data:blog.url == data:blog.homepageUrl'>

    <data:title/>

  <b:else/>

    <a expr:href='data:blog.homepageUrl'><data:title/></a>

  </b:if>

</b:includable>

        </b:widget>

      </b:section>

    </div>

 

    <div id='content-wrapper'>

      <div id='crosscol-wrapper' style='text-align:center'>

        <b:section class='crosscol' id='crosscol' showaddelement='no'/>

      </div>

      <div id='main-wrapper'>

        <b:section class='main' id='main' showaddelement='no'>

          <b:widget id='Blog1' locked='true' title='Blogginlägg' type='Blog'>

            <b:includable id='main' var='top'>

  <b:if cond='data:mobile == &quot;false&quot;'>

    <!-- posts -->

    <div class='blog-posts hfeed'>

      <b:include data='top' name='status-message'/>

      <data:defaultAdStart/>

      <b:loop values='data:posts' var='post'>

        <b:if cond='data:post.isDateStart'>

          <b:if cond='data:post.isFirstPost == &quot;false&quot;'>

            &lt;/div&gt;&lt;/div&gt;

          </b:if>

        </b:if>

        <b:if cond='data:post.isDateStart'>

          &lt;div class=&quot;date-outer&quot;&gt;

        </b:if>

        <b:if cond='data:post.dateHeader'>

          <h2 class='date-header'><span><data:post.dateHeader/></span></h2>

        </b:if>

        <b:if cond='data:post.isDateStart'>

          &lt;div class=&quot;date-posts&quot;&gt;

        </b:if>

        <div class='post-outer'>

        <b:include data='post' name='post'/>

        <b:if cond='data:blog.pageType == &quot;static_page&quot;'>

          <b:include data='post' name='comment_picker'/>

        </b:if>

        <b:if cond='data:blog.pageType == &quot;item&quot;'>

          <b:include data='post' name='comment_picker'/>

        </b:if>

        </div>

        <b:if cond='data:post.includeAd'>

          <b:if cond='data:post.isFirstPost'>

            <data:defaultAdEnd/>

          <b:else/>

            <data:adEnd/>

          </b:if>

          <div class='inline-ad'>

            <data:adCode/>

          </div>

          <data:adStart/>

        </b:if>

      </b:loop>

      <b:if cond='data:numPosts != 0'>

        &lt;/div&gt;&lt;/div&gt;

      </b:if>

      <data:adEnd/>

    </div>

    <!-- navigation -->

    <b:include name='nextprev'/>

    <!-- feed links -->

    <b:include name='feedLinks'/>

    <b:if cond='data:top.showStars'>

      <script src='//www.google.com/jsapi' type='text/javascript'/>

      <script type='text/javascript'>

        google.load(&quot;annotations&quot;, &quot;1&quot;, {&quot;locale&quot;: &quot;<data:top.languageCode/>&quot;});

        function initialize() {

          google.annotations.setApplicationId(<data:top.blogspotReviews/>);

          google.annotations.createAll();

          google.annotations.fetch();

        }

        google.setOnLoadCallback(initialize);

      </script>

    </b:if>

  <b:else/>

    <b:include name='mobile-main'/>

  </b:if>

  <b:if cond='data:top.showDummy'>

    <data:top.dummyBootstrap/>

  </b:if>

</b:includable>

            <b:includable id='backlinkDeleteIcon' var='backlink'>

  <span expr:class='&quot;item-control &quot; + data:backlink.adminClass'>

    <a expr:href='data:backlink.deleteUrl' expr:title='data:top.deleteBacklinkMsg'>

      <img src='//www.blogger.com/img/icon_delete13.gif'/>

    </a>

  </span>

</b:includable>

            <b:includable id='backlinks' var='post'>

  <a name='links'/><h4><data:post.backlinksLabel/></h4>

  <b:if cond='data:post.numBacklinks != 0'>

    <dl class='comments-block' id='comments-block'>

      <b:loop values='data:post.backlinks' var='backlink'>

        <div class='collapsed-backlink backlink-control'>

          <dt class='comment-title'>

            <span class='backlink-toggle-zippy'>&#160;</span>

            <a expr:href='data:backlink.url' rel='nofollow'><data:backlink.title/></a>

            <b:include data='backlink' name='backlinkDeleteIcon'/>

          </dt>

          <dd class='comment-body collapseable'>

            <data:backlink.snippet/>

          </dd>

          <dd class='comment-footer collapseable'>

            <span class='comment-author'><data:post.authorLabel/> <data:backlink.author/></span>

            <span class='comment-timestamp'><data:post.timestampLabel/> <data:backlink.timestamp/></span>

          </dd>

        </div>

      </b:loop>

    </dl>

  </b:if>

  <p class='comment-footer'>

    <a class='comment-link' expr:href='data:post.createLinkUrl' expr:id='data:widget.instanceId + &quot;_backlinks-create-link&quot;' target='_blank'><data:post.createLinkLabel/></a>

  </p>

</b:includable>

            <b:includable id='comment-form' var='post'>

  <div class='comment-form'>

    <a name='comment-form'/>

    <b:if cond='data:mobile'>

      <h4 id='comment-post-message'>

        <a expr:id='data:widget.instanceId + &quot;_comment-editor-toggle-link&quot;' href='javascript:void(0)'><data:postCommentMsg/></a></h4>

      <p><data:blogCommentMessage/></p>

      <data:blogTeamBlogMessage/>

      <a expr:href='data:post.commentFormIframeSrc' id='comment-editor-src'/>

      <iframe allowtransparency='true' class='blogger-iframe-colorize blogger-comment-from-post' frameborder='0' height='410' id='comment-editor' name='comment-editor' src='' style='display: none' width='100%'/>

    <b:else/>

      <h4 id='comment-post-message'><data:postCommentMsg/></h4>

      <p><data:blogCommentMessage/></p>

      <data:blogTeamBlogMessage/>

      <a expr:href='data:post.commentFormIframeSrc' id='comment-editor-src'/>

      <iframe allowtransparency='true' class='blogger-iframe-colorize blogger-comment-from-post' frameborder='0' height='410' id='comment-editor' name='comment-editor' src='' width='100%'/>

    </b:if>

    <data:post.friendConnectJs/>

    <data:post.cmtfpIframe/>

    <script type='text/javascript'>

      BLOG_CMT_createIframe(&#39;<data:post.appRpcRelayPath/>&#39;, &#39;<data:post.communityId/>&#39;);

    </script>

  </div>

</b:includable>

            <b:includable id='commentDeleteIcon' var='comment'>

  <span expr:class='&quot;item-control &quot; + data:comment.adminClass'>

    <b:if cond='data:showCmtPopup'>

      <div class='goog-toggle-button'>

        <div class='goog-inline-block comment-action-icon'/>

      </div>

    <b:else/>

      <a class='comment-delete' expr:href='data:comment.deleteUrl' expr:title='data:top.deleteCommentMsg'>

        <img src='//www.blogger.com/img/icon_delete13.gif'/>

      </a>

    </b:if>

  </span>

</b:includable>

            <b:includable id='comment_count_picker' var='post'>

  <b:if cond='data:post.commentSource == 1'>

    <span class='cmt_count_iframe_holder' expr:data-count='data:post.numComments' expr:data-onclick='data:post.addCommentOnclick' expr:data-post-url='data:post.url' expr:data-url='data:post.canonicalUrl'>

    </span>

  <b:else/>

    <a class='comment-link' expr:href='data:post.addCommentUrl' expr:onclick='data:post.addCommentOnclick'>

      <data:post.commentLabelFull/>:

    </a>

  </b:if>

</b:includable>

            <b:includable id='comment_picker' var='post'>

  <b:if cond='data:post.commentSource == 1'>

    <b:include data='post' name='iframe_comments'/>

  <b:else/>

    <b:if cond='data:post.showThreadedComments'>

      <b:include data='post' name='threaded_comments'/>

    <b:else/>

      <b:include data='post' name='comments'/>

    </b:if>

  </b:if>

</b:includable>

            <b:includable id='comments' var='post'>

  <div class='comments' id='comments'>

    <a name='comments'/>

    <b:if cond='data:post.allowComments'>

      <h4><data:post.commentLabelFull/>:</h4>

      <b:if cond='data:post.commentPagingRequired'>

        <span class='paging-control-container'>

          <b:if cond='data:post.hasOlderLinks'>

            <a expr:class='data:post.oldLinkClass' expr:href='data:post.oldestLinkUrl'><data:post.oldestLinkText/></a>

              &#160;

            <a expr:class='data:post.oldLinkClass' expr:href='data:post.olderLinkUrl'><data:post.olderLinkText/></a>

              &#160;

          </b:if>

          <data:post.commentRangeText/>

          <b:if cond='data:post.hasNewerLinks'>

            &#160;

            <a expr:class='data:post.newLinkClass' expr:href='data:post.newerLinkUrl'><data:post.newerLinkText/></a>

            &#160;

            <a expr:class='data:post.newLinkClass' expr:href='data:post.newestLinkUrl'><data:post.newestLinkText/></a>

          </b:if>

        </span>

      </b:if>

      <div expr:id='data:widget.instanceId + &quot;_comments-block-wrapper&quot;'>

        <dl expr:class='data:post.avatarIndentClass' id='comments-block'>

          <b:loop values='data:post.comments' var='comment'>

            <dt expr:class='&quot;comment-author &quot; + data:comment.authorClass' expr:id='data:comment.anchorName'>

              <b:if cond='data:comment.favicon'>

                <img expr:src='data:comment.favicon' height='16px' style='margin-bottom:-2px;' width='16px'/>

              </b:if>

              <a expr:name='data:comment.anchorName'/>

              <b:if cond='data:blog.enabledCommentProfileImages'>

                <data:comment.authorAvatarImage/>

              </b:if>

              <b:if cond='data:comment.authorUrl'>

                <a expr:href='data:comment.authorUrl' rel='nofollow'><data:comment.author/></a>

              <b:else/>

                <data:comment.author/>

              </b:if>

              <data:commentPostedByMsg/>

            </dt>

            <dd class='comment-body' expr:id='data:widget.instanceId + data:comment.cmtBodyIdPostfix'>

              <b:if cond='data:comment.isDeleted'>

                <span class='deleted-comment'><data:comment.body/></span>

              <b:else/>

                <p>

                  <data:comment.body/>

                </p>

              </b:if>

            </dd>

            <dd class='comment-footer'>

              <span class='comment-timestamp'>

                <a expr:href='data:comment.url' title='comment permalink'>

                  <data:comment.timestamp/>

                </a>

                <b:include data='comment' name='commentDeleteIcon'/>

              </span>

            </dd>

          </b:loop>

        </dl>

      </div>

      <b:if cond='data:post.commentPagingRequired'>

        <span class='paging-control-container'>

          <a expr:class='data:post.oldLinkClass' expr:href='data:post.oldestLinkUrl'>

            <data:post.oldestLinkText/>

          </a>

          <a expr:class='data:post.oldLinkClass' expr:href='data:post.olderLinkUrl'>

            <data:post.olderLinkText/>

          </a>

          &#160;

          <data:post.commentRangeText/>

          &#160;

          <a expr:class='data:post.newLinkClass' expr:href='data:post.newerLinkUrl'>

            <data:post.newerLinkText/>

          </a>

          <a expr:class='data:post.newLinkClass' expr:href='data:post.newestLinkUrl'>

            <data:post.newestLinkText/>

          </a>

        </span>

      </b:if>

      <p class='comment-footer'>

        <b:if cond='data:post.embedCommentForm'>

          <b:if cond='data:post.allowNewComments'>

            <b:include data='post' name='comment-form'/>

          <b:else/>

            <data:post.noNewCommentsText/>

          </b:if>

        <b:else/>

          <b:if cond='data:post.allowComments'>

            <a expr:href='data:post.addCommentUrl' expr:onclick='data:post.addCommentOnclick'><data:postCommentMsg/></a>

          </b:if>

        </b:if>

      </p>

    </b:if>

    <b:if cond='data:showCmtPopup'>

      <div id='comment-popup'>

        <iframe allowtransparency='true' frameborder='0' id='comment-actions' name='comment-actions' scrolling='no'>

        </iframe>

      </div>

    </b:if>

    <div id='backlinks-container'>

    <div expr:id='data:widget.instanceId + &quot;_backlinks-container&quot;'>

       <b:if cond='data:post.showBacklinks'>

         <b:include data='post' name='backlinks'/>

       </b:if>

    </div>

    </div>

  </div>

</b:includable>

            <b:includable id='feedLinks'>

  <b:if cond='data:blog.pageType != &quot;item&quot;'> <!-- Blog feed links -->

    <b:if cond='data:feedLinks'>

      <div class='blog-feeds'>

        <b:include data='feedLinks' name='feedLinksBody'/>

      </div>

    </b:if>

    <b:else/> <!--Post feed links -->

    <div class='post-feeds'>

      <b:loop values='data:posts' var='post'>

        <b:if cond='data:post.allowComments'>

          <b:if cond='data:post.feedLinks'>

            <b:include data='post.feedLinks' name='feedLinksBody'/>

          </b:if>

        </b:if>

      </b:loop>

    </div>

  </b:if>

</b:includable>

            <b:includable id='feedLinksBody' var='links'>

  <div class='feed-links'>

  <data:feedLinksMsg/>

  <b:loop values='data:links' var='f'>

     <a class='feed-link' expr:href='data:f.url' expr:type='data:f.mimeType' target='_blank'><data:f.name/> (<data:f.feedType/>)</a>

  </b:loop>

  </div>

</b:includable>

            <b:includable id='iframe_comments' var='post'>

  <b:if cond='data:post.allowIframeComments'>

    <script expr:src='data:post.iframeCommentSrc' type='text/javascript'/>

    <div class='cmt_iframe_holder' expr:data-href='data:post.canonicalUrl' expr:data-viewtype='data:post.viewType'/>

    <b:if cond='data:post.embedCommentForm == &quot;false&quot;'>

      <a expr:href='data:post.addCommentUrl' expr:onclick='data:post.addCommentOnclick'><data:postCommentMsg/></a>

    </b:if>

  </b:if>

</b:includable>

            <b:includable id='mobile-index-post' var='post'>

  <div class='mobile-date-outer date-outer'>

    <b:if cond='data:post.dateHeader'>

      <div class='date-header'>

        <span><data:post.dateHeader/></span>

      </div>

    </b:if>

    <div class='mobile-post-outer'>

      <a expr:href='data:post.url'>

        <h3 class='mobile-index-title entry-title' itemprop='name'>

          <data:post.title/>

        </h3>

        <div class='mobile-index-arrow'>&amp;rsaquo;</div>

        <div class='mobile-index-contents'>

          <b:if cond='data:post.thumbnailUrl'>

            <div class='mobile-index-thumbnail'>

              <div class='Image'>

                <img expr:src='data:post.thumbnailUrl'/>

              </div>

            </div>

          </b:if>

          <div class='post-body'>

            <b:if cond='data:post.snippet'><data:post.snippet/></b:if>

          </div>

        </div>

        <div style='clear: both;'/>

      </a>

      <div class='mobile-index-comment'>

        <b:if cond='data:blog.pageType != &quot;static_page&quot;'>

          <b:if cond='data:post.allowComments'>

            <b:if cond='data:post.numComments != 0'>

              <b:include data='post' name='comment_count_picker'/>

            </b:if>

          </b:if>

        </b:if>

      </div>

    </div>

  </div>

</b:includable>

            <b:includable id='mobile-main' var='top'>

    <!-- posts -->

    <div class='blog-posts hfeed'>

      <b:include data='top' name='status-message'/>

      <b:if cond='data:blog.pageType == &quot;index&quot;'>

        <b:loop values='data:posts' var='post'>

          <b:include data='post' name='mobile-index-post'/>

        </b:loop>

      <b:else/>

        <b:loop values='data:posts' var='post'>

          <b:include data='post' name='mobile-post'/>

        </b:loop>

      </b:if>

    </div>

   <b:include name='mobile-nextprev'/>

</b:includable>

            <b:includable id='mobile-nextprev'>

  <div class='blog-pager' id='blog-pager'>

    <b:if cond='data:newerPageUrl'>

      <div class='mobile-link-button' id='blog-pager-newer-link'>

      <a class='blog-pager-newer-link' expr:href='data:newerPageUrl' expr:id='data:widget.instanceId + &quot;_blog-pager-newer-link&quot;' expr:title='data:newerPageTitle'>&amp;lsaquo;</a>

      </div>

    </b:if>

    <b:if cond='data:olderPageUrl'>

      <div class='mobile-link-button' id='blog-pager-older-link'>

      <a class='blog-pager-older-link' expr:href='data:olderPageUrl' expr:id='data:widget.instanceId + &quot;_blog-pager-older-link&quot;' expr:title='data:olderPageTitle'>&amp;rsaquo;</a>

      </div>

    </b:if>

    <div class='mobile-link-button' id='blog-pager-home-link'>

    <a class='home-link' expr:href='data:blog.homepageUrl'><data:homeMsg/></a>

    </div>

    <div class='mobile-desktop-link'>

      <a class='home-link' expr:href='data:desktopLinkUrl'><data:desktopLinkMsg/></a>

    </div>

  </div>

  <div class='clear'/>

</b:includable>

            <b:includable id='mobile-post' var='post'>

  <div class='date-outer'>

    <b:if cond='data:post.dateHeader'>

      <h2 class='date-header'><span><data:post.dateHeader/></span></h2>

    </b:if>

    <div class='date-posts'>

      <div class='post-outer'>

        <div class='post hentry uncustomized-post-template' itemscope='itemscope' itemtype='http://schema.org/BlogPosting'>

          <b:if cond='data:post.thumbnailUrl'>

            <meta expr:content='data:post.thumbnailUrl' itemprop='image_url'/>

          </b:if>

          <meta expr:content='data:blog.blogId' itemprop='blogId'/>

          <meta expr:content='data:post.id' itemprop='postId'/>

          <a expr:name='data:post.id'/>

          <b:if cond='data:post.title'>

            <h3 class='post-title entry-title' itemprop='name'>

              <b:if cond='data:post.link'>

                <a expr:href='data:post.link'><data:post.title/></a>

              <b:else/>

                <b:if cond='data:post.url'>

                  <b:if cond='data:blog.url != data:post.url'>

                    <a expr:href='data:post.url'><data:post.title/></a>

                  <b:else/>

                    <data:post.title/>

                  </b:if>

                <b:else/>

                  <data:post.title/>

                </b:if>

              </b:if>

            </h3>

          </b:if>

          <div class='post-header'>

            <div class='post-header-line-1'/>

          </div>

          <div class='post-body entry-content' expr:id='&quot;post-body-&quot; + data:post.id' itemprop='articleBody'>

            <data:post.body/>

            <div style='clear: both;'/> <!-- clear for photos floats -->

          </div>

          <div class='post-footer'>

            <div class='post-footer-line post-footer-line-1'>

              <span class='post-author vcard'>

                <b:if cond='data:top.showAuthor'>

                  <b:if cond='data:post.authorProfileUrl'>

                    <span class='fn' itemprop='author' itemscope='itemscope' itemtype='http://schema.org/Person'>

                      <meta expr:content='data:post.authorProfileUrl' itemprop='url'/>

                      <a expr:href='data:post.authorProfileUrl' rel='author' title='author profile'>

                        <span itemprop='name'><data:post.author/></span>

                      </a>

                    </span>

                  <b:else/>

                    <span class='fn' itemprop='author' itemscope='itemscope' itemtype='http://schema.org/Person'>

                      <span itemprop='name'><data:post.author/></span>

                    </span>

                  </b:if>

                </b:if>

              </span>

              <span class='post-timestamp'>

                <b:if cond='data:top.showTimestamp'>

                  <data:top.timestampLabel/>

                  <b:if cond='data:post.url'>

                    <meta expr:content='data:post.canonicalUrl' itemprop='url'/>

                    <a class='timestamp-link' expr:href='data:post.url' rel='bookmark' title='permanent link'><abbr class='published' expr:title='data:post.timestampISO8601' itemprop='datePublished'><data:post.timestamp/></abbr></a>

                  </b:if>

                </b:if>

              </span>

              <span class='post-comment-link'>

                <b:if cond='data:blog.pageType != &quot;item&quot;'>

                  <b:if cond='data:blog.pageType != &quot;static_page&quot;'>

                    <b:if cond='data:post.allowComments'>

                      <b:include data='post' name='comment_count_picker'/>

                    </b:if>

                  </b:if>

                </b:if>

              </span>

            </div>

            <div class='post-footer-line post-footer-line-2'>

              <b:if cond='data:top.showMobileShare'>

                <div class='mobile-link-button goog-inline-block' id='mobile-share-button'>

                  <a href='javascript:void(0);'><data:shareMsg/></a>

                </div>

              </b:if>

              <b:if cond='data:top.showDummy'>

                <div class='goog-inline-block dummy-container'><data:post.dummyTag/></div>

              </b:if>

            </div>

          </div>

        </div>

        <b:if cond='data:blog.pageType == &quot;static_page&quot;'>

          <b:include data='post' name='comment_picker'/>

        </b:if>

        <b:if cond='data:blog.pageType == &quot;item&quot;'>

          <b:include data='post' name='comment_picker'/>

        </b:if>

      </div>

    </div>

  </div>

</b:includable>

            <b:includable id='nextprev'>

  <div class='blog-pager' id='blog-pager'>

    <b:if cond='data:newerPageUrl'>

      <span id='blog-pager-newer-link'>

      <a class='blog-pager-newer-link' expr:href='data:newerPageUrl' expr:id='data:widget.instanceId + &quot;_blog-pager-newer-link&quot;' expr:title='data:newerPageTitle'><data:newerPageTitle/></a>

      </span>

    </b:if>

    <b:if cond='data:olderPageUrl'>

      <span id='blog-pager-older-link'>

      <a class='blog-pager-older-link' expr:href='data:olderPageUrl' expr:id='data:widget.instanceId + &quot;_blog-pager-older-link&quot;' expr:title='data:olderPageTitle'><data:olderPageTitle/></a>

      </span>

    </b:if>

    <a class='home-link' expr:href='data:blog.homepageUrl'><data:homeMsg/></a>

    <b:if cond='data:mobileLinkUrl'>

      <div class='blog-mobile-link'>

        <a expr:href='data:mobileLinkUrl'><data:mobileLinkMsg/></a>

      </div>

    </b:if>

  </div>

  <div class='clear'/>

</b:includable>

            <b:includable id='post' var='post'>

  <div class='post hentry uncustomized-post-template' itemprop='blogPost' itemscope='itemscope' itemtype='http://schema.org/BlogPosting'>

    <b:if cond='data:post.firstImageUrl'>

      <meta expr:content='data:post.firstImageUrl' itemprop='image_url'/>

    </b:if>

    <meta expr:content='data:blog.blogId' itemprop='blogId'/>

    <meta expr:content='data:post.id' itemprop='postId'/>

    <a expr:name='data:post.id'/>

    <b:if cond='data:post.title'>

      <h3 class='post-title entry-title' itemprop='name'>

      <b:if cond='data:post.link'>

        <a expr:href='data:post.link'><data:post.title/></a>

      <b:else/>

        <b:if cond='data:post.url'>

          <b:if cond='data:blog.url != data:post.url'>

            <a expr:href='data:post.url'><data:post.title/></a>

          <b:else/>

            <data:post.title/>

          </b:if>

        <b:else/>

          <data:post.title/>

        </b:if>

      </b:if>

      </h3>

    </b:if>

    <div class='post-header'>

    <div class='post-header-line-1'/>

    </div>

    <b:if cond='data:blog.metaDescription == &quot;&quot;'>

      <!-- Then use the post body as the schema.org description,

          for good G+/FB snippeting. -->

      <div class='post-body entry-content' expr:id='&quot;post-body-&quot; + data:post.id' itemprop='description articleBody'>

        <data:post.body/>

        <div style='clear: both;'/> <!-- clear for photos floats -->

      </div>

    <b:else/>

      <div class='post-body entry-content' expr:id='&quot;post-body-&quot; + data:post.id' itemprop='articleBody'>

        <data:post.body/>

        <div style='clear: both;'/> <!-- clear for photos floats -->

      </div>

    </b:if>

    <b:if cond='data:post.hasJumpLink'>

      <div class='jump-link'>

        <a expr:href='data:post.url + &quot;#more&quot;' expr:title='data:post.title'><data:post.jumpText/></a>

      </div>

    </b:if>

    <div class='post-footer'>

    <div class='post-footer-line post-footer-line-1'>

      <span class='post-author vcard'>

        <b:if cond='data:top.showAuthor'>

          <data:top.authorLabel/>

            <b:if cond='data:post.authorProfileUrl'>

              <span class='fn' itemprop='author' itemscope='itemscope' itemtype='http://schema.org/Person'>

                <meta expr:content='data:post.authorProfileUrl' itemprop='url'/>

                <a class='g-profile' expr:href='data:post.authorProfileUrl' rel='author' title='author profile'>

                  <span itemprop='name'><data:post.author/></span>

                </a>

              </span>

            <b:else/>

              <span class='fn' itemprop='author' itemscope='itemscope' itemtype='http://schema.org/Person'>

                <span itemprop='name'><data:post.author/></span>

              </span>

            </b:if>

        </b:if>

      </span>

      <span class='post-timestamp'>

        <b:if cond='data:top.showTimestamp'>

          <data:top.timestampLabel/>

        <b:if cond='data:post.url'>

          <meta expr:content='data:post.canonicalUrl' itemprop='url'/>

          <a class='timestamp-link' expr:href='data:post.url' rel='bookmark' title='permanent link'><abbr class='published' expr:title='data:post.timestampISO8601' itemprop='datePublished'><data:post.timestamp/></abbr></a>

        </b:if>

        </b:if>

      </span>

      <span class='reaction-buttons'>

        <b:if cond='data:top.showReactions'>

          <table border='0' cellpadding='0' cellspacing='0' width='100%'><tr>

            <td class='reactions-label-cell' nowrap='nowrap' valign='top' width='1%'>

              <span class='reactions-label'>

              <data:top.reactionsLabel/></span>&#160;</td>

            <td><iframe allowtransparency='true' class='reactions-iframe' expr:src='data:post.reactionsUrl' frameborder='0' name='reactions' scrolling='no'/></td>

           </tr></table>

        </b:if>

      </span>

      <span class='star-ratings'>

        <b:if cond='data:top.showStars'>

           <div expr:g:background-color='data:backgroundColor' expr:g:text-color='data:textColor' expr:g:url='data:post.absoluteUrl' g:height='42' g:type='RatingPanel' g:width='280'/>

        </b:if>

      </span>

      <span class='post-comment-link'>

        <b:if cond='data:blog.pageType != &quot;item&quot;'>

          <b:if cond='data:blog.pageType != &quot;static_page&quot;'>

            <b:if cond='data:post.allowComments'>

              <b:include data='post' name='comment_count_picker'/>

            </b:if>

          </b:if>

        </b:if>

      </span>

       <!-- backlinks -->

       <span class='post-backlinks post-comment-link'>

         <b:if cond='data:blog.pageType != &quot;item&quot;'>

           <b:if cond='data:blog.pageType != &quot;static_page&quot;'>

             <b:if cond='data:post.showBacklinks'>

               <a class='comment-link' expr:href='data:post.url + &quot;#links&quot;'><data:top.backlinkLabel/></a>

             </b:if>

           </b:if>

         </b:if>

       </span>

      <span class='post-icons'>

        <!-- email post links -->

        <b:if cond='data:post.emailPostUrl'>

          <span class='item-action'>

          <a expr:href='data:post.emailPostUrl' expr:title='data:top.emailPostMsg'>

              <img alt='' class='icon-action' height='13' src='http://img1.blogblog.com/img/icon18_email.gif' width='18'/>

          </a>

          </span>

        </b:if>

        <!-- quickedit pencil -->

        <b:include data='post' name='postQuickEdit'/>

      </span>

      <!-- share buttons -->

      <div class='post-share-buttons goog-inline-block'>

        <b:if cond='data:post.sharePostUrl'>

          <b:include data='post' name='shareButtons'/>

        </b:if>

      </div>

      </div>

      <div class='post-footer-line post-footer-line-2'>

      <span class='post-labels'>

        <b:if cond='data:post.labels'>

          <data:postLabelsLabel/>

          <b:loop values='data:post.labels' var='label'>

            <a expr:href='data:label.url' rel='tag'><data:label.name/></a><b:if cond='data:label.isLast != &quot;true&quot;'>,</b:if>

          </b:loop>

        </b:if>

      </span>

      </div>

      <div class='post-footer-line post-footer-line-3'>

      <span class='post-location'>

        <b:if cond='data:top.showLocation'>

          <b:if cond='data:post.location'>

            <data:postLocationLabel/>

            <a expr:href='data:post.location.mapsUrl' target='_blank'><data:post.location.name/></a>

          </b:if>

        </b:if>

      </span>

      </div>

      <b:if cond='data:post.authorAboutMe'>

        <div class='author-profile' itemprop='author' itemscope='itemscope' itemtype='http://schema.org/Person'>

          <b:if cond='data:post.authorPhoto.url'>

            <img expr:src='data:post.authorPhoto.url' itemprop='image' width='50px'/>

          </b:if>

          <div>

            <a class='g-profile' expr:href='data:post.authorProfileUrl' itemprop='url' rel='author' title='author profile'>

              <span itemprop='name'><data:post.author/></span>

            </a>

          </div>

          <span itemprop='description'><data:post.authorAboutMe/></span>

        </div>

      </b:if>

    </div>

  </div>

</b:includable>

            <b:includable id='postQuickEdit' var='post'>

  <b:if cond='data:post.editUrl'>

    <span expr:class='&quot;item-control &quot; + data:post.adminClass'>

      <a expr:href='data:post.editUrl' expr:title='data:top.editPostMsg'>

        <img alt='' class='icon-action' height='18' src='http://img2.blogblog.com/img/icon18_edit_allbkg.gif' width='18'/>

      </a>

    </span>

  </b:if>

</b:includable>

            <b:includable id='shareButtons' var='post'>

  <b:if cond='data:top.showEmailButton'><a class='goog-inline-block share-button sb-email' expr:href='data:post.sharePostUrl + &quot;&amp;target=email&quot;' expr:title='data:top.emailThisMsg' target='_blank'><span class='share-button-link-text'><data:top.emailThisMsg/></span></a></b:if><b:if cond='data:top.showBlogThisButton'><a class='goog-inline-block share-button sb-blog' expr:href='data:post.sharePostUrl + &quot;&amp;target=blog&quot;' expr:onclick='&quot;window.open(this.href, \&quot;_blank\&quot;, \&quot;height=270,width=475\&quot;); return false;&quot;' expr:title='data:top.blogThisMsg' target='_blank'><span class='share-button-link-text'><data:top.blogThisMsg/></span></a></b:if><b:if cond='data:top.showTwitterButton'><a class='goog-inline-block share-button sb-twitter' expr:href='data:post.sharePostUrl + &quot;&amp;target=twitter&quot;' expr:title='data:top.shareToTwitterMsg' target='_blank'><span class='share-button-link-text'><data:top.shareToTwitterMsg/></span></a></b:if><b:if cond='data:top.showFacebookButton'><a class='goog-inline-block share-button sb-facebook' expr:href='data:post.sharePostUrl + &quot;&amp;target=facebook&quot;' expr:onclick='&quot;window.open(this.href, \&quot;_blank\&quot;, \&quot;height=430,width=640\&quot;); return false;&quot;' expr:title='data:top.shareToFacebookMsg' target='_blank'><span class='share-button-link-text'><data:top.shareToFacebookMsg/></span></a></b:if><b:if cond='data:top.showOrkutButton'><a class='goog-inline-block share-button sb-orkut' expr:href='data:post.sharePostUrl + &quot;&amp;target=orkut&quot;' expr:title='data:top.shareToOrkutMsg' target='_blank'><span class='share-button-link-text'><data:top.shareToOrkutMsg/></span></a></b:if><b:if cond='data:top.showPinterestButton'><a class='goog-inline-block share-button sb-pinterest' expr:href='data:post.sharePostUrl + &quot;&amp;target=pinterest&quot;' expr:title='data:top.shareToPinterestMsg' target='_blank'><span class='share-button-link-text'><data:top.shareToPinterestMsg/></span></a></b:if><b:if cond='data:top.showDummy'><div class='goog-inline-block dummy-container'><data:post.dummyTag/></div></b:if>

</b:includable>

            <b:includable id='status-message'>

  <b:if cond='data:navMessage'>

  <div class='status-msg-wrap'>

    <div class='status-msg-body'>

      <data:navMessage/>

    </div>

    <div class='status-msg-border'>

      <div class='status-msg-bg'>

        <div class='status-msg-hidden'><data:navMessage/></div>

      </div>

    </div>

  </div>

  <div style='clear: both;'/>

  </b:if>

</b:includable>

            <b:includable id='threaded-comment-form' var='post'>

  <div class='comment-form'>

    <a name='comment-form'/>

    <b:if cond='data:mobile'>

      <p><data:blogCommentMessage/></p>

      <data:blogTeamBlogMessage/>

      <a expr:href='data:post.commentFormIframeSrc' id='comment-editor-src'/>

      <iframe allowtransparency='true' class='blogger-iframe-colorize blogger-comment-from-post' frameborder='0' height='410' id='comment-editor' name='comment-editor' src='' style='display: none' width='100%'/>

    <b:else/>

      <p><data:blogCommentMessage/></p>

      <data:blogTeamBlogMessage/>

      <a expr:href='data:post.commentFormIframeSrc' id='comment-editor-src'/>

      <iframe allowtransparency='true' class='blogger-iframe-colorize blogger-comment-from-post' frameborder='0' height='410' id='comment-editor' name='comment-editor' src='' width='100%'/>

    </b:if>

    <data:post.friendConnectJs/>

    <data:post.cmtfpIframe/>

    <script type='text/javascript'>

      BLOG_CMT_createIframe(&#39;<data:post.appRpcRelayPath/>&#39;, &#39;<data:post.communityId/>&#39;);

    </script>

  </div>

</b:includable>

            <b:includable id='threaded_comment_js' var='post'>

  <script async='async' expr:src='data:post.commentSrc' type='text/javascript'/>

  <script type='text/javascript'>

    (function() {

      var items = <data:post.commentJso/>;

      var msgs = <data:post.commentMsgs/>;

      var config = <data:post.commentConfig/>;

// <![CDATA[

      var cursor = null;

      if (items && items.length > 0) {

        cursor = parseInt(items[items.length - 1].timestamp) + 1;

      }

      var bodyFromEntry = function(entry) {

        if (entry.gd$extendedProperty) {

          for (var k in entry.gd$extendedProperty) {

            if (entry.gd$extendedProperty[k].name == 'blogger.contentRemoved') {

              return '<span class="deleted-comment">' + entry.content.$t + '</span>';

            }

          }

        }

        return entry.content.$t;

      }

      var parse = function(data) {

        cursor = null;

        var comments = [];

        if (data && data.feed && data.feed.entry) {

          for (var i = 0, entry; entry = data.feed.entry[i]; i++) {

            var comment = {};

            // comment ID, parsed out of the original id format

            var id = /blog-(\d+).post-(\d+)/.exec(entry.id.$t);

            comment.id = id ? id[2] : null;

            comment.body = bodyFromEntry(entry);

            comment.timestamp = Date.parse(entry.published.$t) + '';

            if (entry.author && entry.author.constructor === Array) {

              var auth = entry.author[0];

              if (auth) {

                comment.author = {

                  name: (auth.name ? auth.name.$t : undefined),

                  profileUrl: (auth.uri ? auth.uri.$t : undefined),

                  avatarUrl: (auth.gd$image ? auth.gd$image.src : undefined)

                };

              }

            }

            if (entry.link) {

              if (entry.link[2]) {

                comment.link = comment.permalink = entry.link[2].href;

              }

              if (entry.link[3]) {

                var pid = /.*comments\/default\/(\d+)\?.*/.exec(entry.link[3].href);

                if (pid && pid[1]) {

                  comment.parentId = pid[1];

                }

              }

            }

            comment.deleteclass = 'item-control blog-admin';

            if (entry.gd$extendedProperty) {

              for (var k in entry.gd$extendedProperty) {

                if (entry.gd$extendedProperty[k].name == 'blogger.itemClass') {

                  comment.deleteclass += ' ' + entry.gd$extendedProperty[k].value;

                } else if (entry.gd$extendedProperty[k].name == 'blogger.displayTime') {

                  comment.displayTime = entry.gd$extendedProperty[k].value;

                }

              }

            }

            comments.push(comment);

          }

        }

        return comments;

      };

      var paginator = function(callback) {

        if (hasMore()) {

          var url = config.feed + '?alt=json&v=2&orderby=published&reverse=false&max-results=50';

          if (cursor) {

            url += '&published-min=' + new Date(cursor).toISOString();

          }

          window.bloggercomments = function(data) {

            var parsed = parse(data);

            cursor = parsed.length < 50 ? null

                : parseInt(parsed[parsed.length - 1].timestamp) + 1

            callback(parsed);

            window.bloggercomments = null;

          }

          url += '&callback=bloggercomments';

          var script = document.createElement('script');

          script.type = 'text/javascript';

          script.src = url;

          document.getElementsByTagName('head')[0].appendChild(script);

        }

      };

      var hasMore = function() {

        return !!cursor;

      };

      var getMeta = function(key, comment) {

        if ('iswriter' == key) {

          var matches = !!comment.author

              && comment.author.name == config.authorName

              && comment.author.profileUrl == config.authorUrl;

          return matches ? 'true' : '';

        } else if ('deletelink' == key) {

          return config.baseUri + '/delete-comment.g?blogID='

               + config.blogId + '&postID=' + comment.id;

        } else if ('deleteclass' == key) {

          return comment.deleteclass;

        }

        return '';

      };

      var replybox = null;

      var replyUrlParts = null;

      var replyParent = undefined;

      var onReply = function(commentId, domId) {

        if (replybox == null) {

          // lazily cache replybox, and adjust to suit this style:

          replybox = document.getElementById('comment-editor');

          if (replybox != null) {

            replybox.height = '250px';

            replybox.style.display = 'block';

            replyUrlParts = replybox.src.split('#');

          }

        }

        if (replybox && (commentId !== replyParent)) {

          document.getElementById(domId).insertBefore(replybox, null);

          replybox.src = replyUrlParts[0]

              + (commentId ? '&parentID=' + commentId : '')

              + '#' + replyUrlParts[1];

          replyParent = commentId;

        }

      };

      var hash = (window.location.hash || '#').substring(1);

      var startThread, targetComment;

      if (/^comment-form_/.test(hash)) {

        startThread = hash.substring('comment-form_'.length);

      } else if (/^c[0-9]+$/.test(hash)) {

        targetComment = hash.substring(1);

      }

      // Configure commenting API:

      var configJso = {

        'maxDepth': config.maxThreadDepth

      };

      var provider = {

        'id': config.postId,

        'data': items,

        'loadNext': paginator,

        'hasMore': hasMore,

        'getMeta': getMeta,

        'onReply': onReply,

        'rendered': true,

        'initComment': targetComment,

        'initReplyThread': startThread,

        'config': configJso,

        'messages': msgs

      };

      var render = function() {

        if (window.goog && window.goog.comments) {

          var holder = document.getElementById('comment-holder');

          window.goog.comments.render(holder, provider);

        }

      };

      // render now, or queue to render when library loads:

      if (window.goog && window.goog.comments) {

        render();

      } else {

        window.goog = window.goog || {};

        window.goog.comments = window.goog.comments || {};

        window.goog.comments.loadQueue = window.goog.comments.loadQueue || [];

        window.goog.comments.loadQueue.push(render);

      }

    })();

// ]]
>

  </script>

</b:includable>

            <b:includable id='threaded_comments' var='post'>

  <div class='comments' id='comments'>

    <a name='comments'/>

    <h4><data:post.commentLabelFull/>:</h4>

    <div class='comments-content'>

      <b:if cond='data:post.embedCommentForm'>

        <b:include data='post' name='threaded_comment_js'/>

      </b:if>

      <div id='comment-holder'>

         <data:post.commentHtml/>

      </div>

    </div>

    <p class='comment-footer'>

      <b:if cond='data:post.allowNewComments'>

        <b:include data='post' name='threaded-comment-form'/>

      <b:else/>

        <data:post.noNewCommentsText/>

      </b:if>

    </p>

    <b:if cond='data:showCmtPopup'>

      <div id='comment-popup'>

        <iframe allowtransparency='true' frameborder='0' id='comment-actions' name='comment-actions' scrolling='no'>

        </iframe>

      </div>

    </b:if>

    <div id='backlinks-container'>

    <div expr:id='data:widget.instanceId + &quot;_backlinks-container&quot;'>

       <b:if cond='data:post.showBacklinks'>

         <b:include data='post' name='backlinks'/>

       </b:if>

    </div>

    </div>

  </div>

</b:includable>

          </b:widget>

        </b:section>

      </div>

<a href='http://bloggping.com'><img alt='bloggping' border='0' src='http://image.bloggping.com/b.png'/></a>

      <div id='sidebar-wrapper'>

        <b:section class='sidebar' id='sidebar' preferred='yes'>

          <b:widget id='Profile1' locked='false' title='Om mig' type='Profile'>

            <b:includable id='main'>

    <b:if cond='data:title != &quot;&quot;'>

      <h2><data:title/></h2>

    </b:if>

    <div class='widget-content'>

    <b:if cond='data:team == &quot;true&quot;'> <!-- team blog profile -->

      <ul>

        <b:loop values='data:authors' var='i'>

          <li><a class='profile-name-link g-profile' expr:href='data:i.userUrl' expr:style='&quot;background-image: url(&quot; + data:i.profileLogo + &quot;);&quot;'><data:i.display-name/></a></li>

        </b:loop>

      </ul>

    <b:else/> <!-- normal blog profile -->

      <b:if cond='data:photo.url != &quot;&quot;'>

        <a expr:href='data:userUrl'><img class='profile-img' expr:alt='data:photo.alt' expr:height='data:photo.height' expr:src='data:photo.url' expr:width='data:photo.width'/></a>

      </b:if>

      <dl class='profile-datablock'>

        <dt class='profile-data'>

          <a class='profile-name-link g-profile' expr:href='data:userUrl' expr:style='&quot;background-image: url(&quot; + data:profileLogo + &quot;);&quot;' rel='author'>

            <data:displayname/>

          </a>

          <b:if cond='data:hasgoogleprofile'>

            <br/>

            <div class='g-follow' data-annotation='bubble' data-height='20' expr:data-href='data:userUrl'/>

          </b:if>

        </dt>

        <b:if cond='data:showlocation == &quot;true&quot;'>

          <dd class='profile-data'><data:location/></dd>

        </b:if>

        <b:if cond='data:aboutme != &quot;&quot;'><dd class='profile-textblock'><data:aboutme/></dd></b:if>

      </dl>

      <a class='profile-link' expr:href='data:userUrl' rel='author'><data:viewProfileMsg/></a>

    </b:if>

     <b:include name='quickedit'/>

    </div>

  </b:includable>

          </b:widget>

          <b:widget id='HTML1' locked='false' title='Twitter Updates' type='HTML'>

            <b:includable id='main'>

  <!-- only display title if it's non-empty -->

  <b:if cond='data:title != &quot;&quot;'>

    <h2 class='title'><data:title/></h2>

  </b:if>

  <div class='widget-content'>

    <data:content/>

  </div>

  <b:include name='quickedit'/>

</b:includable>

          </b:widget>

          <b:widget id='Feed1' locked='false' title='Jag i media' type='Feed'>

            <b:includable id='main'>

    <h2><data:title/></h2>

    <div class='widget-content' expr:id='data:widget.instanceId + &quot;_feedItemListDisplay&quot;'>

      <span style='filter: alpha(25); opacity: 0.25;'>

        <a expr:href='data:feedUrl'><data:loadingMsg/></a>

      </span>

    </div>

    <b:include name='quickedit'/>

  </b:includable>

          </b:widget>

          <b:widget id='Feed2' locked='false' title='Jag i bloggosfären' type='Feed'>

            <b:includable id='main'>

    <h2><data:title/></h2>

    <div class='widget-content' expr:id='data:widget.instanceId + &quot;_feedItemListDisplay&quot;'>

      <span style='filter: alpha(25); opacity: 0.25;'>

        <a expr:href='data:feedUrl'><data:loadingMsg/></a>

      </span>

    </div>

    <b:include name='quickedit'/>

  </b:includable>

          </b:widget>

          <b:widget id='Followers1' locked='false' title='Bloggintresserade' type='Followers'>

            <b:includable id='main'>

  <b:if cond='data:title != &quot;&quot;'>

    <b:if cond='data:codeSnippet != &quot;&quot;'>

      <h2 class='title'><data:title/></h2>

    <b:else/>

      <b:if cond='data:totalFollowerCount != &quot;&quot;'>

        <h2 class='title'><data:title/> (<data:totalFollowerCount/>)</h2>

      </b:if>

    </b:if> 

  </b:if>

  <div class='widget-content'>

    <div expr:id='data:widget.instanceId + &quot;-wrapper&quot;'>

      <b:if cond='data:codeSnippet != &quot;&quot;'>

        <div style='margin-right:2px;'>

          <data:codeSnippet/>

        </div>

      <b:else/>

        <b:if cond='data:totalFollowerCount == &quot;&quot;'>

          <span class='item-control following-not-admin'>

            <b><data:failureSnippet/></b>

          </span>

          <span class='item-control blog-admin'>

            <b><data:adminFailureSnippet/></b>

          </span>

        <b:else/>

          <b:if cond='data:followingLinkPresent'>

            <div class='follow-this profile-link item-control following-follow-this'>

              <a expr:href='&quot;javascript:_FollowersView._openPopup(\&quot;&quot; + data:followUri + &quot;\&quot;);&quot;'>

                <data:followThisMessage/>

              </a>

            </div>

            <div class='follow-this profile-link item-control following-stop-following-this'>

              <a expr:href='&quot;javascript:_FollowersView._openPopup(\&quot;&quot; + data:followUri + &quot;\&quot;);&quot;'>

                <data:stopFollowingMessage/>

              </a>

            </div>

          </b:if>

 

          <div class='followers-grid'>

            <b:if cond='data:totalFollowerCount == 0'>

              <div class='profile-link item-control following-follow-this'>

                <data:emptyFollowersMessage/>

              </div>

            </b:if>

            <!--

            Relies on the js written out in navbar.gxp

            -->

            <b:loop values='data:followers' var='follower'>

              <div class='follower'>

                <a expr:href='data:follower.profileUrl' expr:title='data:follower.displayName' rel='nofollow'>

                <img class='follower-img' expr:alt='data:follower.displayName' expr:height='data:follower.imageHeight' expr:onerror='&quot;this.onerror=null;this.src=\&quot;&quot; + data:anonFollowerImageUrl + &quot;\&quot;;&quot;' expr:onload='&quot;setAttributeOnload(this, \&quot;src\&quot;, \&quot;&quot; + data:follower.imageUrl + &quot;\&quot;)&quot;' expr:width='data:follower.imageWidth' src='http://img1.blogblog.com/img/blank.gif'/>

                </a>

              </div>

            </b:loop>

            <div class='clear'/>

          </div>

 

          <div class='followers-canvas profile-link'>

            <data:followersFooterMessage/>

            <span class='item-control following-not-admin'>

              <a expr:href='data:followersUri'>

                <data:viewAllMessage/>

              </a>

            </span>

            <span class='item-control blog-admin'>

              <a expr:href='data:manageFollowersUri'>

                <data:manageFollowersMessage/>

              </a>

            </span>

          </div>

          </b:if>

      </b:if>

    </div>

    <b:include name='quickedit'/>

  </div>

</b:includable>

          </b:widget>

          <b:widget id='LinkList1' locked='false' title='Bloggroll' type='LinkList'>

            <b:includable id='main'>

<b:if cond='data:title'><h2><data:title/></h2></b:if>

 <div class='widget-content'>

   <ul>

     <b:loop values='data:links' var='link'>

       <li><a expr:href='data:link.target'><data:link.name/></a></li>

     </b:loop>

   </ul>

   <b:include name='quickedit'/>

 </div>

</b:includable>

          </b:widget>

          <b:widget id='LinkList2' locked='false' title='Andra härliga länkar' type='LinkList'>

            <b:includable id='main'>

<b:if cond='data:title'><h2><data:title/></h2></b:if>

 <div class='widget-content'>

   <ul>

     <b:loop values='data:links' var='link'>

       <li><a expr:href='data:link.target'><data:link.name/></a></li>

     </b:loop>

   </ul>

   <b:include name='quickedit'/>

 </div>

</b:includable>

          </b:widget>

          <b:widget id='LinkList3' locked='false' title='Musik maestro' type='LinkList'>

            <b:includable id='main'>

<b:if cond='data:title'><h2><data:title/></h2></b:if>

 <div class='widget-content'>

   <ul>

     <b:loop values='data:links' var='link'>

       <li><a expr:href='data:link.target'><data:link.name/></a></li>

     </b:loop>

   </ul>

   <b:include name='quickedit'/>

 </div>

</b:includable>

          </b:widget>

          <b:widget id='BlogArchive1' locked='false' title='Bloggarkiv' type='BlogArchive'>

            <b:includable id='main'>

  <b:if cond='data:title'>

    <h2><data:title/></h2>

  </b:if>

  <div class='widget-content'>

  <div id='ArchiveList'>

  <div expr:id='data:widget.instanceId + &quot;_ArchiveList&quot;'>

    <b:if cond='data:style == &quot;HIERARCHY&quot;'>

     <b:include data='data' name='interval'/>

    </b:if>

    <b:if cond='data:style == &quot;FLAT&quot;'>

      <b:include data='data' name='flat'/>

    </b:if>

    <b:if cond='data:style == &quot;MENU&quot;'>

      <b:include data='data' name='menu'/>

    </b:if>

  </div>

  </div>

  <b:include name='quickedit'/>

  </div>

</b:includable>

            <b:includable id='flat' var='data'>

  <ul class='flat'>

    <b:loop values='data:data' var='i'>

      <li class='archivedate'>

        <a expr:href='data:i.url'><data:i.name/></a> (<data:i.post-count/>)

      </li>

    </b:loop>

  </ul>

</b:includable>

            <b:includable id='interval' var='intervalData'>

  <b:loop values='data:intervalData' var='i'>

      <ul class='hierarchy'>

        <li expr:class='&quot;archivedate &quot; + data:i.expclass'>

          <b:include data='i' name='toggle'/>

          <a class='post-count-link' expr:href='data:i.url'><data:i.name/></a>

            <span class='post-count' dir='ltr'>(<data:i.post-count/>)</span>

          <b:if cond='data:i.data'>

            <b:include data='i.data' name='interval'/>

          </b:if>

          <b:if cond='data:i.posts'>

            <b:include data='i.posts' name='posts'/>

          </b:if>

        </li>

      </ul>

  </b:loop>

</b:includable>

            <b:includable id='menu' var='data'>

  <select expr:id='data:widget.instanceId + &quot;_ArchiveMenu&quot;'>

    <option value=''><data:title/></option>

    <b:loop values='data:data' var='i'>

      <option expr:value='data:i.url'><data:i.name/> (<data:i.post-count/>)</option>

    </b:loop>

  </select>

</b:includable>

            <b:includable id='posts' var='posts'>

  <ul class='posts'>

    <b:loop values='data:posts' var='i'>

      <li><a expr:href='data:i.url'><data:i.title/></a></li>

    </b:loop>

  </ul>

</b:includable>

            <b:includable id='toggle' var='interval'>

  <b:if cond='data:interval.toggleId'>

  <b:if cond='data:interval.expclass == &quot;expanded&quot;'>

    <a class='toggle' href='javascript:void(0)'>

      <span class='zippy toggle-open'>&#9660;&#160;</span>

    </a>

  <b:else/>

    <a class='toggle' href='javascript:void(0)'>

      <span class='zippy'>

        <b:if cond='data:blog.languageDirection == &quot;rtl&quot;'>

          &#9668;&#160;

        <b:else/>

          &#9658;&#160;

        </b:if>

      </span>

    </a>

  </b:if>

 </b:if>

</b:includable>

          </b:widget>

          <b:widget id='CustomSearch1' locked='false' title='Leta i den här bloggen' type='CustomSearch'>

            <b:includable id='main'>

    <!-- only display title if it's non-empty -->

    <b:if cond='data:title != &quot;&quot;'>

      <h2 class='title'><data:title/></h2>

    </b:if>

    <div class='widget-content'>

      <div expr:id='data:widget.instanceId + &quot;_form&quot;'>

        <span class='cse-status'><data:loadingMsg/></span>

      </div>

    </div>

    <!-- override gsearch.css -->

    <style type='text/css'>

      #uds-searchControl .gs-result .gs-title,

      #uds-searchControl .gs-result .gs-title *,

      #uds-searchControl .gsc-results .gsc-trailing-more-results,

      #uds-searchControl .gsc-results .gsc-trailing-more-results * {

        color:<data:linkColor/>;

      }

      #uds-searchControl .gs-result .gs-title a:visited,

      #uds-searchControl .gs-result .gs-title a:visited * {

        color:<data:visitedLinkColor/>;

      }

      #uds-searchControl .gs-relativePublishedDate,

      #uds-searchControl .gs-publishedDate {

        color: <data:dateColor/>;

      }

      #uds-searchControl .gs-result a.gs-visibleUrl,

      #uds-searchControl .gs-result .gs-visibleUrl {

        color: <data:urlColor/>;

      }

      #uds-searchControl .gsc-results {

        border-color: <data:borderColor/>;

        background-color: <data:backgroundColor/>;

      }

      #uds-searchControl .gsc-tabhActive {

        border-color: <data:borderColor/>;

        border-top-color: <data:activeBorderColor/>;

        background-color: <data:backgroundColor/>;

        color: <data:textColor/>;

      }

      #uds-searchControl .gsc-tabhInactive {

        border-color: <data:borderColor/>;

        background-color: transparent;

        color: <data:linkColor/>;

      }

      #uds-searchClearResults {

        border-color: <data:borderColor/>;

      }

      #uds-searchClearResults:hover {

        border-color: <data:activeBorderColor/>;

      }

      #uds-searchControl .gsc-cursor-page {

        color: <data:linkColor/>;

      }

      #uds-searchControl .gsc-cursor-current-page {

        color: <data:textColor/>;

      }

    </style>

    <b:include name='quickedit'/>

  </b:includable>

          </b:widget>

          <b:widget id='Gadget1' locked='false' title='National Geographic Photos' type='Gadget'>

            <b:includable id='main'> 

  <!-- only display title if it's non-empty -->

  <b:if cond='data:renderingUrl != &quot;&quot;'>

    <b:if cond='data:title != &quot;&quot;'>

      <h2 class='title'><data:title/></h2>

    </b:if>

    <b:if cond='data:gadgetSnippet != &quot;&quot;'>

       <data:gadgetSnippet/>

    <b:else/>

      <div class='widget-content'>

        <b:if cond='data:nonSocialFragment != &quot;&quot;'>

          <data:nonSocialFragment/>

        </b:if>

      </div>

    </b:if>

  <b:else/>

    <data:errorMessage/>

  </b:if>

  <b:include name='quickedit'/>

</b:includable>

          </b:widget>

        </b:section>

      </div>

<a href='http://www.bloggtoppen.se/'><img alt='Bloggtoppen.se' border='0' src='http://www.bloggtoppen.se/tracker.php?do=in&amp;id=62'/></a>

<a href='http://www.gaybloggar.se/topplista/'><img alt='Gaybloggar.se' border='0' src='http://www.gaybloggar.se/topplista/button.php?u=federleyblogspot'/></a>

      <!-- spacer for skins that want sidebar and main to be the same height-->

      <div class='clear'>&#160;</div>

    </div> <!-- end content-wrapper -->

  </div></div> <!-- end outer-wrapper -->

</body>

</html>
