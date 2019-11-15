import re

def print_with_indent(indent, str):
  prefix = ''
  for i in range(indent):
    prefix = prefix + ' ' 
  strs = str.split('\n')
  for line in strs:
    if re.match('^\s*$', line):
      print(prefix + '<br />')
    else:
      print(prefix + line)

def process_code(str):
  result = '<pre><code>\n'
  result = result + str.replace('<', '&lt;').replace('>', '&gt;')
  result = result + '\n</code></pre>'
  return result

def generate_html(title, comment_id, summary, topics, background_str, sections):
  topic_str = '相关主题：'
  for topic in topics:
    topic_str = topic_str + '<a href="../index.html#topics">' + topic + '</a>'

  print_with_indent(0, """\
<!DOCTYPE HTML>
<html>
  <head>
    <title>""" + title + """</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../assets/css/main.css" />
    <noscript><link rel="stylesheet" href="../assets/css/noscript.css" /></noscript>
  </head>
  <body class="is-preload">
    <!-- Wrapper -->
      <div id="wrapper">
        <!-- Header -->
          <header id="header">
            <div class="logo">
              <span class="icon fa-gem"></span>
            </div>
            <div class="content">
              <div class="inner">""")

  # summary and topics
  print_with_indent(16,   '<h1>' + title + '</h1>')
  print_with_indent(16,   '<p>' + summary + '<br /></p>')
  print_with_indent(16,   '<p>' + topic_str + '</p>')

  print_with_indent(0, """\
              </div>
            </div>
            <nav>
              <ul>""")

  print_with_indent(16,   '<li><a href="#content">' + title + '</a></li>')

  print_with_indent(0, """\
                <li><a href="../index.html">回到主页</a></li>
                <li><a href="../index.html#intro">回到主页：简介</a></li>
                <li><a href="../index.html#blogs">回到主页：博客</a></li>
                <li><a href="../index.html#topics">回到主页：主题</a></li>
                <li><a href="../index.html#about">回到主页：关于</a></li>
              </ul>
            </nav>
          </header>
        <!-- Main -->
          <div id="main">
            <!-- Content -->
              <article id="content">""")

  # title
  print_with_indent(16,   '<h2 class="major">' + title + '</h2>')

  # image
  print_with_indent(16, """<span class="image main"><img src="../images/pic02.jpg" alt="" /></span>""")

  # motivation and background
  print_with_indent(16, '<section>')
  print_with_indent(18,   '<h3 class="major">背景</h3>')
  print_with_indent(18,    background_str)
  print_with_indent(16, '</section>')

  # sections
  for section in sections:
    print_with_indent(16, '<hr />\n<section>')
    print_with_indent(16, '  <h3 class="major">' + section[0] + '</h3>')
    for sub_section in section[1]:
      print_with_indent(sub_section[0], sub_section[1])
    print_with_indent(16, '</section>')

  print_with_indent(0, """\
                <hr />
                <div class="gh-comments"></div>
              </article>
          </div>
        <!-- Footer -->
          <footer id="footer">
            <p class="copyright">&copy; D &amp; Q 出品</p>
          </footer>
      </div>
    <!-- BG -->
      <div id="bg"></div>
    <!-- Scripts -->
      <script src="../assets/js/jquery.min.js"></script>
      <script src="../assets/js/browser.min.js"></script>
      <script src="../assets/js/breakpoints.min.js"></script>
      <script src="../assets/js/util.js"></script>
      <script src="../assets/js/main.js"></script>
      <script type="text/javascript">
        (function (gh_issue_id){
          var gh_comments = document.getElementsByClassName('gh-comments')[0];
          var gh_api = 'https://api.github.com/repos/d-ampersand-q/d-ampersand-q.github.io/issues';
          var gh_issue_url = 'https://github.com/d-ampersand-q/d-ampersand-q.github.io/issues/' + gh_issue_id;
          var gh_comments_url = gh_api + '/' + gh_issue_id + '/comments';
          fetch(gh_comments_url, {
            headers: new Headers({
              'Accept': 'application/vnd.github.v3.html+json',
              'Content-Type': 'application/json'
            }),
            method: 'GET'
          }).then((res) => {
            if (res.status == 200) return res.json();
            let error = new Error('HTTP Exception[GET]');
            error.status = res.status;
            error.statusText = res.statusText;
            error.url = res.url;
            throw error;
          }).then((json) => {
              gh_comments.insertAdjacentHTML('afterbegin', `<h2 class="major">GitHub评论</h3>
                <p>请访问<a href="${gh_issue_url}">GitHub Issue</a>评论此文.</p>`);
              for (let comment of json) {
                let date = new Date(comment.created_at);
                let c = '<div class="gh-comment">' +
                    `<h3 class="major"><img src="${comment.user.avatar_url}" width="24px"> ` +
                    `<a href="${comment.user.html_url}">${comment.user.login}</a>` +
                    '发表于' +
                    `${date.toLocaleDateString()}` + ' ' + `${date.toLocaleTimeString()}</h3>` +
                    comment.body_html +
                    '</div>' + 
                    '<hr>';
                gh_comments.insertAdjacentHTML('beforeend', c);
              }
          }).catch((err) => {
            gh_comments.insertAdjacentHTML('afterbegin', '<h3>GitHub Comments</h3><p>Comments are not open for this post yet</p>');
          });})(""")
  print_with_indent(0, comment_id + """);
      </script>
  </body>
</html>""")
