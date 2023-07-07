#include <iostream>
#include <future>

// 异步任务，计算给定数字的平方
int square(int num) {
    return num * num;
}

int main() {
 
    // 启动异步任务
    std::future<int> futureResult = std::async(square, 5);

    // 在主线程中执行其他操作...

    // 获取异步任务的结果
    int result = futureResult.get();

    // 打印结果
    std::cout << "平方结果: " << result << std::endl;

    return 0;
}

