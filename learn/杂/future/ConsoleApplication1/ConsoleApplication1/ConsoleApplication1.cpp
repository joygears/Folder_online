#include <thread>
#include <iostream>
#include <future>
#include <chrono>




struct MyData
{
    int value;
    float conf;
};

MyData data{ 0, 0.0f };

void InitializeCdmModule_4() {

    printf("helo");
};

int main()
{
    std::packaged_task<MyData()> produceTask(
       // [=]() { printf("helo"); }
        [&]() -> MyData {
            std::this_thread::sleep_for(std::chrono::seconds(1));
            return MyData{ 2, 1 };
        }
    );
   
    printf("1");
    auto dataFuture = produceTask.get_future();

    std::thread producer(
        [&](std::packaged_task<MyData()>& task) -> void {
            task();
        },
        std::ref(produceTask)
            );

    std::thread consumer(
        [&](std::future<MyData>& data) -> void {
            auto res = data.get();
            std::cout << res.value << "\t" << res.conf << std::endl;
        },
        std::ref(dataFuture)
            );

    producer.join();
    consumer.join();

    return 0;
}