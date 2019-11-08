from util import process_code as process_code
from util import generate_html as generate_html

title = '手动备份小米路由器硬盘'
comment_id = '2'
summary = '当小米路由器硬盘损坏后，恢复损坏的硬盘或者切换到另一块硬盘'
topics = ['IT']

background_str = """\
我的路由器是第一代的R1D，所以本文的内容可能<strong>不适合其它型号的小米路由器</strong>。<br /><br />
不知道是不是设计问题，小米路由器的硬盘特别容易损坏。才几年，我这个已经搞坏了两块硬盘了。当然，第二块硬盘是叠瓦磁的，所以可能不能怪小米。硬盘坏了之后，比较头疼的问题有几个：
<br /><br />
<ul class="alt">
  <li>找一块硬盘再重新刷机比较费时</li>
  <li>刷机完后，还要重新调各种设置</li>
  <li>不知道是不是人品问题，路由器自带的设置备份在我这里不能正常工作</li>
</ul>
<h4>目标</h4>
正好家里有好几块废旧硬盘，如果可以废物利用，就解决以上的问题了。希望把一两块旧硬盘预先刷成小米的路由器硬盘。这样出问题了就可以直接替换。而且设置跟刷硬盘时候的设置完全一样。虽然原装的硬盘是1T的，但因为废旧硬盘都比较小，所以希望几十G、一百来G的旧硬盘也可以工作。
<br />
这样还有一个好处：1T的新硬盘可以当优盘在需要时连接到路由器上。不需要一直在线。兼顾存储空间和硬盘寿命。"""

code_snippet = []
sections = []

# code snippets
code_snippet.append("""\
sudo dd if=/dev/sdd1 of=~/xiaomi_disk_part1.bak
d2 of=~/xiaomi_disk_part2.bak
d3 of=~/xiaomi_disk_part3.bak""")

code_snippet.append("""\
sudo dd if=~/xiaomi_disk_part1.bak of=/dev/sdd1
sudo dd if=~/xiaomi_disk_part2.bak of=/dev/sdd2
sudo dd if=~/xiaomi_disk_part3.bak of=/dev/sdd3""")

# section 1
temp = """\n\
<ul>
  <li>2.5寸的移动硬盘盒</li>
    <ul>
      <li>注意：<strong>其它型号的小米路由器可能用台式机硬盘，不是2.5寸</strong></li>
    </ul>
  <li>装了linux系统的机器，并安装分区工具gparted</li>
    <ul>
      <li>或者能连接物理优盘的虚拟机上安装linux和分区工具</li>
    </ul>
  <li>小米路由器的硬盘能够拆下。注意：<strong>拆硬盘后，保修会出问题。所以操作之前先确认可以接受</strong></li>
  <li>废旧硬盘。几十G以上就完全没有问题</li>
</ul>"""

sections.append(('前提条件', ((18, temp), )))

# section 2
temp = """\n\
把旧硬盘装进移动硬盘盒后，连接到电脑上。连接完成后，查看/dev/下该硬盘对应的文件名。比如，在我的系统上，加载后，旧硬盘的文件名是/dev/sdd。以后都假设硬盘文件名是sdd。<br />
在gparted中，将sdd按照以下方式分区。分区前最好检查一下现有路由器硬盘的分区结构是否和下表一致。<br />
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>分区号</th>
        <th>大小</th>
        <th>文件系统格式</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>一</td>
        <td>132M</td>
        <td>ext4</td>
      </tr>
      <tr>
        <td>二</td>
        <td>132M</td>
        <td>ext4</td>
      </tr>
      <tr>
        <td>三</td>
        <td>264M</td>
        <td>ext4</td>
      </tr>
      <tr>
        <td>四</td>
        <td>剩下的所有磁盘空间</td>
        <td>ext4</td>
      </tr>
    </tbody>
  </table>
</div>"""

sections.append(('小米路由器硬盘的分区结构', ((18, temp), )))

# section 3
temp = """\n\
卸载旧硬盘，将路由器硬盘装进硬盘盒，并加载到计算机上。假设对应文件名还是sdd。这时可以用如下几条命令备份前三个分区。第四个分区的大小不固定，而且不是系统盘，所以可以直接cp来备份到一个目录。"""

sections.append(('备份', ((18, temp), (0, process_code(code_snippet[0])))))

# section 4
temp = """\n\
卸载路由器硬盘，将之前分好区的旧硬盘装进硬盘盒，并加载到计算机上。假设对应文件名还是sdd。这时可以用如下几条命令刷前三个分区。第四个分区可以直接cp拷贝之前备份的内容即可。"""

temp2 = '以上备份的内容可以继续用来刷下一块旧硬盘。所以可以保留下来，以后继续使用。'

sections.append(('刷硬盘', ((18, temp), (0, process_code(code_snippet[1])), (18, temp2))))

# section 5
temp = """\n\
断电状态下，用刷好的旧硬盘代替原先的路由器硬盘，插入路由器。通电后，路由器初始化完成，亮蓝灯。网络共享的硬盘第四分区一切正常，只是显示的空余空间比之前要小很多。因为替换的硬盘只有几十G。一切正常。"""

sections.append(('测试', ((18, temp), )))

# generate
generate_html(title, comment_id, summary, topics, background_str, sections)
