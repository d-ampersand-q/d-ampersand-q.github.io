#include <iostream>
#include <utility>
#include <array>

// First target
template <typename T, std::size_t... Ints>
struct compile_time_array_1
{
  static constexpr T array[] = { (Ints, 0)... };
};

//template <typename T, std::size_t... Ints>
//constexpr T compile_time_array_1<T, Ints...>::array[];

template <typename T, std::size_t... Ints>
constexpr compile_time_array_1<T, Ints...> get_compile_time_array_1(std::index_sequence<Ints...>)
{
  return compile_time_array_1<T, Ints...>{};
}

// Second target
template <typename T, std::size_t... Ints>
struct compile_time_array_2
{
  static constexpr T array[] = { Ints... };
};

//template <typename T, std::size_t... Ints>
//constexpr T compile_time_array_2<T, Ints...>::array[];

template <typename T, std::size_t... Ints>
constexpr compile_time_array_2<T, Ints...> get_compile_time_array_2(std::index_sequence<Ints...>)
{
  return compile_time_array_2<T, Ints...>{};
}

// Third target
template <typename T, typename F, std::size_t... Ints>
struct compile_time_array_3
{
  static constexpr T array[] = { F{}(Ints)... };
};

//template <typename T, typename F, std::size_t... Ints>
//constexpr T compile_time_array_3<T, F, Ints...>::array[];

template <typename T, typename F, std::size_t... Ints>
constexpr compile_time_array_3<T, F, Ints...> get_compile_time_array_3(std::index_sequence<Ints...>)
{
  return compile_time_array_3<T, F, Ints...>{};
}

int main()
{
  constexpr auto numbers_1 = get_compile_time_array_1<int>(std::make_index_sequence<10>()).array;
  constexpr auto numbers_2 = get_compile_time_array_2<int>(std::make_index_sequence<10>()).array;

  struct f
  {
    constexpr std::size_t operator() (std::size_t index)
    {
      return 2 * index;
    }
  };
  constexpr auto numbers_3 = get_compile_time_array_3<int, f>(std::make_index_sequence<10>()).array;

  std::cout << numbers_1[1] << '\n';
  std::cout << numbers_1[2] << '\n';
  std::cout << numbers_2[1] << '\n';
  std::cout << numbers_2[2] << '\n';
  std::cout << numbers_3[1] << '\n';
  std::cout << numbers_3[2] << '\n';
}
