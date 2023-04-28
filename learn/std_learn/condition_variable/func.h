#include <functional>

using namespace std;

__declspec(dllexport) void Function(std::function<void()> fun);