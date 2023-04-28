#include "func.h"

void Function(std::function<void()> fun) {
	fun();
}