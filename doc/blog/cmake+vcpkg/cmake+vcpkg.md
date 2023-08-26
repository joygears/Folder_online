## cmake+vcpkg 实在是泰裤辣

### 使用vcpkg

#### 项目集成vcpkg

`vcpkg`执行

~~~bat
D:\Downloads\tset> vcpkg integrate install
Applied user-wide integration for this vcpkg root.
CMake projects should use: "-DCMAKE_TOOLCHAIN_FILE=C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake"

All MSBuild C++ projects can now #include any installed libraries. Linking will be handled automatically. Installing new libraries will make them instantly available.
~~~

然后我们只要把`-DCMAKE_TOOLCHAIN_FILE`这句代码加入到cmake构建语句中，即可完成集成vcpkg，如下所示

~~~bat
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake
~~~

> 最好每次执行cmake构建语句时将原来生成的build文件夹删掉，避免因使用原来的缓存文件而没有刷新环境变量导致找不到库

#### 导入目标库

在`vcpkg` 安装，在最后会给出`cmake`的用法，如下所示

~~~bat
D:\Downloads\tset>vcpkg install fmt:x86-windows fmt:x64-windows
Computing installation plan...
The following packages are already installed:
    fmt[core]:x64-windows -> 10.0.0
    fmt[core]:x86-windows -> 10.0.0
fmt:x64-windows is already installed
fmt:x86-windows is already installed
Restored 0 package(s) from C:\Users\czl\AppData\Local\vcpkg\archives in 100 us. Use --debug to see more details.
Total install time: 1.14 ms
The package fmt provides CMake targets:

    find_package(fmt CONFIG REQUIRED)  
    target_link_libraries(main PRIVATE fmt::fmt)

    # Or use the header-only version
    find_package(fmt CONFIG REQUIRED)
    target_link_libraries(main PRIVATE fmt::fmt-header-only)
~~~

我们把`find_package`、`target_link_libraries`加入`CMakeLists.txt`就行了,到这里就可以编译了，只是依赖了本地的`vcpkg`而已

### 导出目标库

之前那样会依赖本地的`vcpkg`，我们可以将我们想要的库都导出来，放到我们的项目目录中，这样就不会依赖本地环境

#### vcpkg导出命令

~~~bat
vcpkg export fmt:x86-windows fmt:x64-windows jsoncpp:x86-windows jsoncpp:x64-windows  --raw --output-dir .  --output vcpkg
~~~

+ `vcpkg export` 是导出命令
+ `fmt:x86-windows fmt:x64-windows jsoncpp:x86-windows jsoncpp:x64-windows` 表示32位和64位都要打包，且同时可以导出多个库
+  `--raw` 以原始方式导出，写死的没什么好说的
+ `--output-dir <path>` 要导出在哪个目录
+    `--output vcpkg`  这个是要生成的包名  我这里用vcpkg

> 包里生成vcpkg.exe可以删掉

#### 修改`-DCMAKE_TOOLCHAIN_FILE`

下面是`导出语句`的命令行输出

~~~bat
D:\Downloads\tset>vcpkg export fmt:x86-windows fmt:x64-windows jsoncpp:x86-windows jsoncpp:x64-windows  --raw --output-dir .  --output vcpkg
The following packages are already built and will be exported:
    fmt:x86-windows
    fmt:x64-windows
    jsoncpp:x86-windows
    jsoncpp:x64-windows
  * vcpkg-cmake:x64-windows
  * vcpkg-cmake-config:x64-windows
Additional packages (*) need to be exported to complete this operation.
Exporting vcpkg-cmake:x64-windows...
Exporting vcpkg-cmake-config:x64-windows...
Exporting fmt:x86-windows...
Exporting fmt:x64-windows...
Exporting jsoncpp:x86-windows...
Exporting jsoncpp:x64-windows...
Files exported at: D:\Downloads\tset\.\vcpkg
To use exported libraries in CMake projects, add -DCMAKE_TOOLCHAIN_FILE=D:/Downloads/tset/./vcpkg/scripts/buildsystems/vcpkg.cmake to your CMake command line.
~~~

接下来包生成的包复制到项目目录中，并将`cmake构建语句`中的`-DCMAKE_TOOLCHAIN_FILE`的值修改为`<包所在目录>/<包名>/scripts/buildsystems/vcpkg.cmake`即可

### 例子

下面通过一个使用了`fmt`、`jsoncpp`的项目，来演示如何在`cmake`中使用`vcpkg`

#### 项目结构

~~~bat
│  CMakeLists.txt
│  compile.bat
│  main.cpp
│
└─sdk
    └─win
        └─vcpkg
~~~



#### 源代码

**main.cpp**

~~~c++
#include <iostream>
#include <fmt/core.h>
#include <json/json.h>

int main() {
    int num = 42;
    std::string text = "Hello, fmt!";
    
    // 使用 fmt 库进行格式化输出
    std::string formatted = fmt::format("Number: {}, Text: {}", num, text);
    
    std::cout << formatted << std::endl;
    
        // 创建 JSON 对象
    Json::Value root;
    root["name"] = "John";
    root["age"] = 30;
    root["city"] = "New York";

    // 将 JSON 对象转换为 JSON 字符串
    Json::StreamWriterBuilder writer;
    std::string json_str = Json::writeString(writer, root);

    std::cout << "JSON String: " << json_str << std::endl;
    return 0;
}
~~~

#### vcpkg安装需要的库

~~~bat
vcpkg install fmt:x86-windows fmt:x64-windows jsoncpp:x86-windows jsoncpp:x64-windows
~~~

#### vcpkg导出需要的库

~~~~bat
vcpkg export fmt:x86-windows fmt:x64-windows jsoncpp:x86-windows jsoncpp:x64-windows  --raw --output-dir .  --output vcpkg
~~~~

删掉包里`vcpkg.exe`,将导出的包复制到项目目录的`sdk/win`中

#### 构建项目

**CMakeLists.txt**

~~~cmake
# 指定编译的最小版本
cmake_minimum_required(VERSION 3.0.0) 

# 指定解决方案的名字 和版本
project(test VERSION 0.1.0)

# 添加可执行项目
add_executable(test main.cpp)


# 链接第三方库

find_package(jsoncpp CONFIG REQUIRED)
find_package(fmt CONFIG REQUIRED)

target_link_libraries(test PRIVATE JsonCpp::JsonCpp fmt::fmt)

~~~

#### 编译脚本

**compile.bat**

~~~bat
SET WORKSPACE=%~dp0

SET BUILD_DIR=%WORKSPACE%\build

cmake -S %WORKSPACE% -B %BUILD_DIR% -DCMAKE_TOOLCHAIN_FILE=%WORKSPACE%sdk/win/vcpkg/scripts/buildsystems/vcpkg.cmake
cmake --build %BUILD_DIR% 
~~~

到这里就结束了，`vcpkg`是跨平台的，`macos`的用法应该是一样的

这是这个例子的[仓库地址](https://github.com/2963663242/cmake-vcpkg-demo)，感兴趣的朋友可以尝试一下 