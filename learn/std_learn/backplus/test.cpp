#include <iostream>

class Counter {
public:
  Counter(int count = 0) : m_count(count) {}
  int GetCount() const { return m_count; }

  // 前置递增运算符重载
  Counter& operator++() {
    ++m_count;
    return *this;
  }

  // 后置递增运算符重载
  Counter operator++(int) {
    Counter temp(*this);
    ++m_count;
    return temp;
  }

private:
  int m_count;
};

int main() {
  Counter c1(1);
  std::cout << "Initial count: " << c1.GetCount() << std::endl;

  // 使用后缀++递增计数器对象，并打印使用前缀++递增计数器对象
  std::cout << "After post-increment: " << (c1++).GetCount() << std::endl;
  std::cout << "After pre-increment: " << (++c1).GetCount() << std::endl;

  return 0;
}
