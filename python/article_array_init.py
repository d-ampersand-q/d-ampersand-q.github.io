from util import process_code as process_code
from util import generate_html as generate_html

title = '编译时初始化数组'
comment_id = '1'
summary = '在编译时决定一个数组的初始值，而非运行时。'
topics = ['C++']

background_str = """\
今天面试实习生时，发现对方答题时写了如下的代码：
<pre><code>int something[10] = {0};</code></pre>
询问之后，果然是想把一个数组的所有元素初始化为0。C码农应该很容易看到问题在哪里。但是现在大学里似乎有很多人是直接学C++，所以会有这样的误解。<br />
看到这段代码后，想到了另一个不同但有点关系的问题：怎么样得到一个编译时的常量数组，并且每个元素都是0？如果需要初始化成任意指定的值又该怎么做？

<h4>目标</h4>
<ul class="alt">
  <li>基础目标：把一个数组的所有元素初始化为0</li>
  <li>进阶目标：把一个数组的所有元素初始化为1，2，3，4 ...</li>
  <li>终极目标：把一个数组的所有元素初始化为一个函数<i>f(n)</i>的输出结果，其中n代表数组中的第n个元素</li>
</ul>

以上都希望是一个编译时的数组。"""

topic_str = '相关主题：'
for topic in topics:
  topic_str = topic_str + '<a href="../index.html#topics">' + topic + '</a>'

code_snippet = []
sections = []

# code snippets
code_snippet.append("""\
template <typename T, std::size_t... Ints>
struct compile_time_array_1
{
  static constexpr T array[] = { (Ints, 0)... };
};

// Note
// template <typename T, std::size_t... Ints>
// constexpr T compile_time_array_1<T, Ints...>::array[];

template <typename T, std::size_t... Ints>
constexpr compile_time_array_1<T, Ints...> get_compile_time_array_1(std::index_sequence<Ints...>)
{
  return compile_time_array_1<T, Ints...>{};
}""")

code_snippet.append("""\
auto numbers_1 = get_compile_time_array_1<int>(std::make_index_sequence<10>()).array;
std::cout << numbers_1[2];""")

code_snippet.append("""\
template <typename T, std::size_t... Ints>
struct compile_time_array_2
{
  static constexpr T array[] = { Ints... };
};

// Note
// template <typename T, std::size_t... Ints>
// constexpr T compile_time_array_2<T, Ints...>::array[];

template <typename T, std::size_t... Ints>
constexpr compile_time_array_2<T, Ints...> get_compile_time_array_2(std::index_sequence<Ints...>)
{
  return compile_time_array_2<T, Ints...>{};
}""")

code_snippet.append("""\
auto numbers_2 = get_compile_time_array_2<int>(std::make_index_sequence<10>()).array;
std::cout << numbers_2[2];""")

code_snippet.append("""\
template <typename T, typename F, std::size_t... Ints>
struct compile_time_array_3
{
  static constexpr T array[] = { F{}(Ints)... };
};

// Note
// template <typename T, typename F, std::size_t... Ints>
// constexpr T compile_time_array_3<T, F, Ints...>::array[];

template <typename T, typename F, std::size_t... Ints>
constexpr compile_time_array_3<T, F, Ints...> get_compile_time_array_3(std::index_sequence<Ints...>)
{
  return compile_time_array_3<T, F, Ints...>{};
}""")

code_snippet.append("""\
struct f
{
  constexpr std::size_t operator() (std::size_t index)
  {
    return 2 * index;
  }
};

auto numbers_3 = get_compile_time_array_3<int, f>(std::make_index_sequence<10>()).array;
std::cout << numbers_3[2];""")

# section 1
sections.append(('基础目标', ((0, process_code(code_snippet[0])),
                              (18, '\n下面这段代码输出的是0。<br />'), 
                              (0, process_code(code_snippet[1])), 
                              (18, """\n注意前一段代码中注释的部分：link没有报错，说明最终的程序的确没有用到array的地址。如果把下面的代码改成一个输出数组所有元素的循环，link就会报错，因为我用的编译器不能在编译时遍历一个数组。即使这个数组是一个编译时常量也不行。<br />\n顺便提一下，如果编译器优化没有打开，link也可能报错，因为编译器没有把这个数组转化成常量。"""))))

# section 2
sections.append(('进阶目标', ((0, process_code(code_snippet[2])),
                              (18, '下面这段代码输出的是2。前一段代码中注释的部分的含义与前一节相同。'),
                              (0, process_code(code_snippet[3])))))

# section 3
sections.append(('终极目标', ((0, process_code(code_snippet[4])),
                              (18, '下面这段代码输出的是4。前一段代码中注释的部分的含义与前一节相同。'),
                              (0, process_code(code_snippet[5])))))

# generate
generate_html(title, comment_id, summary, background_str, topic_str, sections)
