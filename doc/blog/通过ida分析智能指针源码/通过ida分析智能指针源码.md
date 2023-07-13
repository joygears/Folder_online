## 通过`IDA`分析智能指针源码

首先我们看一看智能指针的内存结构

### `std::shard_ptr<T *>`

```c++
std::shard_ptr{
	T * ptr;
	std::_Ref_count<T> * Rep;
}
```

**`ptr`**
对象的指针
**`Rep`**
引用计数对象的指针

```c++
std::_Ref_count{
	void * vtf;
	int refCount;
	int weak;
	T * ptr;
}
```

**`vtf`**
虚表
**`refCount`**
引用计数
**`weak`**
这个标志很有意思，当`refCount`为0时，`weak`减1，当有`weak_ptr`指向`Rep`时，`weak`加1，当`weak_ptr`析构时，`weak`减一，当`weak`为0时，`Rep`被销毁
也就是说当没有智能指针指向对象时，`Rep`被销毁
**`ptr`**
对象的指针

然后我们看一个智能指针构造函数的IDA反编译例子

~~~c++
void **__thiscall shard_ptr_video_decoder_config_ctor(void **this, void *ptr)
{
  _DWORD *v3; // eax
  _DWORD *v4; // esi
  volatile signed __int32 *Rep; // edi
  void **result; // eax
  int v7; // [esp+0h] [ebp-28h] BYREF
  void **this_1; // [esp+14h] [ebp-14h]
  int *v9; // [esp+18h] [ebp-10h]
  int v10; // [esp+24h] [ebp-4h]

  v9 = &v7;
  this_1 = this;
  v10 = 0;
  v3 = (_DWORD *)operator new(16);              // --------------------------------
  v4 = v3;
  if ( v3 )
  {
    v3[1] = 1; // refCount
    v3[2] = 1; // weak
    *v3 = &std::_Ref_count_del<cdm::VideoDecoderConfig_2,_lambda_e48d69f8f8c691b46ec86555318d101c_>::`vftable'; //vtf
    v3[3] = ptr; // ptr
  }
  else                                          // 创建std::_Ref_count<T>对象，构造函数里，refCount和weak都设置为1，并将ptr保存
  {
    v4 = 0;
  }                                             // --------------------------------
  Rep = (volatile signed __int32 *)this[1];
  if ( Rep )
  {
    if ( !_InterlockedExchangeAdd(Rep + 1, 0xFFFFFFFF) )
    {
      (**(void (__thiscall ***)(volatile signed __int32 *))Rep)(Rep);// 析构目标对象（析构目标对象的函数在Ref虚表的第0个位置）
      if ( !_InterlockedExchangeAdd(Rep + 2, 0xFFFFFFFF) )
        (*(void (**)(void))(*Rep + 4))();       // 析构Ref对象（析构Ref对象的函数在Ref虚表的第1个位置）
    }
  }
  result = this_1;
  this_1[1] = v4;
  *result = ptr;
  return result;
}
~~~

~~~c++
  v3 = (_DWORD *)operator new(16);              // --------------------------------
  v4 = v3;
  if ( v3 )
  {
    v3[1] = 1; // refCount
    v3[2] = 1; // weak
    *v3 = &std::_Ref_count_del<cdm::VideoDecoderConfig_2,_lambda_e48d69f8f8c691b46ec86555318d101c_>::`vftable'; //vtf
    v3[3] = ptr; // ptr
  }
  else                                          // 创建std::_Ref_count<T>对象，构造函数里，refCount和weak都设置为1，并将ptr保存
  {
    v4 = 0;
  } 
~~~

上面这一段主要是创建`std::_Ref_count<T>`对象，构造函数里，`refCount`和`weak`都设置为1，并将智能指针指向的目标对象指针`ptr`保存

~~~c++
  Rep = (volatile signed __int32 *)this[1];
  if ( Rep ) ////判断原来的智能指针是不是还存在(通过判断Ref指针是否为0，来判断原来的智能指针是否存在)
  {
    if ( !_InterlockedExchangeAdd(Rep + 1, 0xFFFFFFFF) )
    {
      (**(void (__thiscall ***)(volatile signed __int32 *))Rep)(Rep);// 析构目标对象（析构目标对象的函数在Ref虚表的第0个位置）
      if ( !_InterlockedExchangeAdd(Rep + 2, 0xFFFFFFFF) )
        (*(void (**)(void))(*Rep + 4))();       // 析构Ref对象（析构Ref对象的函数在Ref虚表的第1个位置）
    }
  }
~~~

上面主要是看这个对象智能指针是不是已经存在智能指针，如果存在，则将原来智能指针的`refCount`-1，若`refCount`为0，则析构原来智能指针指向的对象，然后再`weak`-1，若`weak`为0，则析构原来智能指针的`std::_Ref_count`对象



下面再看一个智能指针发生赋值的时候`IDA`的`c++`反编译例子

~~~c++
shard_ptr_video_decoder_config_ctor(&v23, v10);
    Ref = *(_DWORD *)(v11 + 0xBC);  //获取原来智能指针的Ref
    *(_DWORD *)(v11 + 0xBC) = v24;  //这里智能指针发生了赋值
    *(_DWORD *)(v11 + 0xB8) = v23; //这里智能指针发生了赋值
    Ref_1 = (volatile signed __int32 *)Ref;
    v26[0] = Ref;
    if ( Ref )//判断原来的智能指针是不是还存在(通过判断Ref指针是否为0，来判断原来的智能指针是否存在)
    {
      if ( !_InterlockedExchangeAdd((volatile signed __int32 *)(Ref + 4), 0xFFFFFFFF) ) //如果存在，则将该智能指针的refCount-1，若refCount为0，
      {
        (**(void (__thiscall ***)(int))Ref)(Ref); // 则析构原来智能指针指向的对象
        if ( !_InterlockedExchangeAdd(Ref_1 + 2, 0xFFFFFFFF) ) //将weak-1，若weak为0
          (*(void (__thiscall **)(volatile signed __int32 *))(*Ref_1 + 4))(Ref_1); //则析构原来智能指针的std::_Ref_count对象
      }
    }
~~~

上面主要是当智能指针发生赋值时，会先判断原来的智能指针是不是还存在，如果存在，则将该智能指针的`refCount`-1，若`refCount`为0，则析构原来智能指针指向的对象，将`weak`-1，若`weak`为0，则析构原来智能指针的`std::_Ref_count`对象

> 析构智能指针指向的目标对象的函数在Ref虚表的第0个位置
>
> 析构Ref对象的函数在Ref虚表的第1个位置