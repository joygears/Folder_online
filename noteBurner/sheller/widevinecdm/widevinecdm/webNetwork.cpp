#include "webNetwork.h"
#include <condition_variable>
#include <mutex>
#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>

using namespace websocketpp;

// 创建WebSocket客户端类型
typedef client<config::asio_client> client_t;
using websocketpp::lib::placeholders::_1;
using websocketpp::lib::placeholders::_2;
using websocketpp::lib::bind;

// 定义条件变量和互斥锁用于同步等待服务器回复
std::condition_variable cv;
std::mutex mutex;
std::string server_response;
bool got_response = false;
client_t cli;
client_t::connection_ptr con;

// 定义处理接收消息的回调函数
void on_message(client_t* c, websocketpp::connection_hdl hdl, client_t::message_ptr msg) {
    std::cout << "接收到消息：" << msg->get_payload() << std::endl;

    // 在这里处理接收到的消息，您可以根据需要进行逻辑处理
    // ...

    // 设置服务器回复，并通知等待的线程
    std::unique_lock<std::mutex> lock(mutex);
    server_response = msg->get_payload();
    got_response = true;
    cv.notify_all();
}

// 函数：连接服务器，返回是否连接成功
bool connectToServer(const std::string& serverAddress, uint16_t port) {

    try {
        // 连接前设置访问通道
        cli.clear_access_channels(websocketpp::log::alevel::all);
        cli.set_access_channels(websocketpp::log::alevel::connect);
        cli.set_access_channels(websocketpp::log::alevel::disconnect);
        cli.set_access_channels(websocketpp::log::alevel::app);

        // 初始化客户端并绑定消息回调函数
        cli.init_asio();
        cli.set_message_handler(bind(&on_message, &cli, ::_1, ::_2));

        // 连接到服务器
        websocketpp::lib::error_code ec;
        con = cli.get_connection("ws://" + serverAddress + ":" + std::to_string(port), ec);
        if (ec) {
            std::cout << "无法创建连接：" << ec.message() << std::endl;
            return false;
        }

        // 连接到服务器
        cli.connect(con);

        // 等待连接完成
        cli.run();

    }
    catch (websocketpp::exception const& e) {
        std::cout << "错误：" << e.what() << std::endl;
        return false;
    }

    return true;
}

// 函数：发送消息并等待返回消息
std::string sendMessageAndWaitForResponse(const std::string& message) {
    std::unique_lock<std::mutex> lock(mutex);
    server_response = "";
    got_response = false;

    // 向服务器发送消息
    // 这里需要根据具体的WebSocket客户端库来发送消息，示例中省略此部分代码
    cli.send(con, message, websocketpp::frame::opcode::text);
    // 等待回复
    cv.wait(lock, [] { return got_response; });

    return server_response;
}

// 函数：发送消息并等待返回消息
void sendMessage(const std::string& message) {
    std::unique_lock<std::mutex> lock(mutex);
    // 向服务器发送消息
    // 这里需要根据具体的WebSocket客户端库来发送消息，示例中省略此部分代码
    cli.send(con, message, websocketpp::frame::opcode::text);
  

}

void closeClient() {
    cli.close(con, websocketpp::close::status::normal, "Client shutting down");
}