
#pragma once

#include <yvals_core.h>
#include <exception>
#include <typeinfo>
#include <xmemory>
#include <xstddef>

constexpr int _Small_object_num_ptrs = 6 + 16 / sizeof(void*);

template <class _Rx, class... _Types>
class __declspec(novtable) _Func_base { // abstract base for implementation types
public:
    virtual _Func_base* _Copy(void*) const = 0;
    virtual _Func_base* _Move(void*) noexcept = 0;
    virtual _Rx _Do_call(_Types&&...) = 0;
    virtual const type_info& _Target_type() const noexcept = 0;
    virtual void _Delete_this(bool) noexcept = 0;

#if _HAS_STATIC_RTTI
    const void* _Target(const type_info& _Info) const noexcept {
        return _Target_type() == _Info ? _Get() : nullptr;
    }
#endif // _HAS_STATIC_RTTI

    _Func_base() = default;
    _Func_base(const _Func_base&) = delete;
    _Func_base& operator=(const _Func_base&) = delete;
    // dtor non-virtual due to _Delete_this()

private:
    virtual const void* _Get() const noexcept = 0;
};

template <bool _Test, class _Ty = void>
struct enable_if {}; // no member "type" when !_Test

template <class _Ty>
struct enable_if<true, _Ty> { // type is _Ty for _Test
    using type = _Ty;
};

template <class _Callable, class _Rx, class... _Types>
class _Func_impl_no_alloc final : public _Func_base<_Rx, _Types...> {
    // derived class for specific implementation types that don't use allocators
//public:
//    using _Mybase = _Func_base<_Rx, _Types...>;
//    using _Nothrow_move = is_nothrow_move_constructible<_Callable>;
//
//    template <class _Other, enable_if_t<!is_same_v<_Func_impl_no_alloc, decay_t<_Other>>, int> = 0>
//    explicit _Func_impl_no_alloc(_Other&& _Val) : _Callee(_STD forward<_Other>(_Val)) {}
//
//    // dtor non-virtual due to _Delete_this()
//
//private:
//    virtual _Mybase* _Copy(void* _Where) const override {
//        if constexpr (_Is_large<_Func_impl_no_alloc>) {
//            (void)_Where; // TRANSITION, DevCom-1004719
//            return _Global_new<_Func_impl_no_alloc>(_Callee);
//        }
//        else {
//            return ::new (_Where) _Func_impl_no_alloc(_Callee);
//        }
//    }
//
//    virtual _Mybase* _Move(void* _Where) noexcept override {
//        if constexpr (_Is_large<_Func_impl_no_alloc>) {
//            (void)_Where; // TRANSITION, DevCom-1004719
//            return nullptr;
//        }
//        else {
//            return ::new (_Where) _Func_impl_no_alloc(_STD move(_Callee));
//        }
//    }
//
//    virtual _Rx _Do_call(_Types&&... _Args) override { // call wrapped function
//        return _Invoker_ret<_Rx>::_Call(_Callee, _STD forward<_Types>(_Args)...);
//    }
//
//    virtual const type_info& _Target_type() const noexcept override {
//#if _HAS_STATIC_RTTI
//        return typeid(_Callable);
//#else // _HAS_STATIC_RTTI
//        _CSTD abort();
//#endif // _HAS_STATIC_RTTI
//    }
//
//    virtual const void* _Get() const noexcept override {
//        return _STD addressof(_Callee);
//    }
//
//    virtual void _Delete_this(bool _Dealloc) noexcept override { // destroy self
//        this->~_Func_impl_no_alloc();
//        if (_Dealloc) {
//            _Deallocate<alignof(_Func_impl_no_alloc)>(this, sizeof(_Func_impl_no_alloc));
//        }
//    }
//
//    _Callable _Callee;
};
#include <tuple>
template <bool _Test, class _Ty = void>
using enable_if_t = typename enable_if<_Test, _Ty>::type;
[[noreturn]]  void __cdecl _Xbad_function_call();
constexpr size_t _Space_size = (_Small_object_num_ptrs - 1) * sizeof(void*);

template <class... _Types>
struct _Arg_types {}; // provide argument_type, etc. when sizeof...(_Types) is 1 or 2

template <class _Ret, class... _Types>
class _Func_class : public _Arg_types<_Types...>  {
public:
       using result_type = _Ret;

      using _Ptrt = _Func_base<_Ret, _Types...>;
    _Func_class() noexcept {
       _Set(nullptr);
    }

    _Ret operator()(_Types... _Args) const {
        if (_Empty()) {
            _Xbad_function_call();
        }
       const auto _Impl = _Getimpl();
        return _Impl->_Do_call(_STD forward<_Types>(_Args)...);
    }

    ~_Func_class() noexcept {
        _Tidy();
    }

protected:
   /* template <class _Fx, class _Function>
    using _Enable_if_callable_t =
        enable_if_t<conjunction_v<negation<is_same<decay_t<_Fx>, _Function>>, _Is_invocable_r<_Ret, _Fx, _Types...>>,
        int>;*/

    bool _Empty() const noexcept {
        return !_Getimpl();
    }

    void _Reset_copy(const _Func_class& _Right) { // copy _Right's stored object
        if (!_Right._Empty()) {
            _Set(_Right._Getimpl()->_Copy(&_Mystorage));
        }
    }

    void _Reset_move(_Func_class&& _Right) noexcept { // move _Right's stored object
        if (!_Right._Empty()) {
            if (_Right._Local()) { // move and tidy
                _Set(_Right._Getimpl()->_Move(&_Mystorage));
                _Right._Tidy();
            }
            else { // steal from _Right
                _Set(_Right._Getimpl());
                _Right._Set(nullptr);
            }
        }
    }

    template <class _Fx>
    void _Reset(_Fx&& _Val) { // store copy of _Val
        if (!_Test_callable(_Val)) { // null member pointer/function pointer/std::function
            return; // already empty
        }
        
        using _Impl = _Func_impl_no_alloc<decay_t<_Fx>, _Ret, _Types...>;
    //    if constexpr (_Is_large<_Impl>) {
    //        // dynamically allocate _Val
    //        _Set(_Global_new<_Impl>(_STD forward<_Fx>(_Val)));
    //    }
    //    else {
    //        // store _Val in-situ
    //        _Set(::new (static_cast<void*>(&_Mystorage)) _Impl(_STD forward<_Fx>(_Val)));
    //    }
    }

//#if _HAS_FUNCTION_ALLOCATOR_SUPPORT
//    template <class _Fx, class _Alloc>
//    void _Reset_alloc(_Fx&& _Val, const _Alloc& _Ax) { // store copy of _Val with allocator
//        if (!_Test_callable(_Val)) { // null member pointer/function pointer/std::function
//            return; // already empty
//        }
//
//        using _Myimpl = _Func_impl<decay_t<_Fx>, _Alloc, _Ret, _Types...>;
//        if constexpr (_Is_large<_Myimpl>) {
//            // dynamically allocate _Val
//            using _Alimpl = _Rebind_alloc_t<_Alloc, _Myimpl>;
//            _Alimpl _Al(_Ax);
//            _Alloc_construct_ptr<_Alimpl> _Constructor{ _Al };
//            _Constructor._Allocate();
//            _Construct_in_place(*_Constructor._Ptr, _STD forward<_Fx>(_Val), _Ax);
//            _Set(_Unfancy(_Constructor._Release()));
//        }
//        else {
//            // store _Val in-situ
//            const auto _Ptr = reinterpret_cast<_Myimpl*>(&_Mystorage);
//            _Construct_in_place(*_Ptr, _STD forward<_Fx>(_Val), _Ax);
//            _Set(_Ptr);
//        }
//    }
//#endif // _HAS_FUNCTION_ALLOCATOR_SUPPORT
//
    void _Tidy() noexcept {
        if (!_Empty()) { // destroy callable object and maybe delete it
            _Getimpl()->_Delete_this(!_Local());
            _Set(nullptr);
        }
    }
//
    void _Swap(_Func_class& _Right) noexcept { // swap contents with contents of _Right
        if (!_Local() && !_Right._Local()) { // just swap pointers
            _Ptrt* _Temp = _Getimpl();
            _Set(_Right._Getimpl());
            _Right._Set(_Temp);
        }
        else { // do three-way move
            _Func_class _Temp;
            _Temp._Reset_move(_STD move(*this));
            _Reset_move(_STD move(_Right));
            _Right._Reset_move(_STD move(_Temp));
        }
    }

#if _HAS_STATIC_RTTI
    const type_info& _Target_type() const noexcept {
        return _Getimpl() ? _Getimpl()->_Target_type() : typeid(void);
    }

    const void* _Target(const type_info& _Info) const noexcept {
        return _Getimpl() ? _Getimpl()->_Target(_Info) : nullptr;
    }
#endif // _HAS_STATIC_RTTI[[noreturn]]

private:
    bool _Local() const noexcept { // test for locally stored copy of object
        return _Getimpl() == static_cast<const void*>(&_Mystorage);
    }

    union _Storage { // storage for small objects (basic_string is small)
        max_align_t _Dummy1; // for maximum alignment
        char _Dummy2[_Space_size]; // to permit aliasing
        _Ptrt* _Ptrs[_Small_object_num_ptrs]; // _Ptrs[_Small_object_num_ptrs - 1] is reserved
    };

    _Storage _Mystorage;
//    enum { _EEN_IMPL = _Small_object_num_ptrs - 1 }; // helper for expression evaluator
    _Ptrt* _Getimpl() const noexcept { // get pointer to object
        return _Mystorage._Ptrs[_Small_object_num_ptrs - 1];
    }

    void _Set(_Ptrt* _Ptr) noexcept { // store pointer to object
        _Mystorage._Ptrs[_Small_object_num_ptrs - 1] = _Ptr;
    }
};

template <class _Tx>
struct _Get_function_impl {
   // static_assert(_Always_false<_Tx>, "std::function does not accept non-function types as template arguments.");
};



#define _EMIT_CDECL(FUNC, OPT1, OPT2, OPT3) FUNC(__cdecl, OPT1, OPT2, OPT3)
#define _EMIT_CLRCALL(FUNC, OPT1, OPT2, OPT3)
#define _EMIT_FASTCALL(FUNC, OPT1, OPT2, OPT3) FUNC(__fastcall, OPT1, OPT2, OPT3)
#define _EMIT_STDCALL(FUNC, OPT1, OPT2, OPT3)  FUNC(__stdcall, OPT1, OPT2, OPT3)
#define _EMIT_THISCALL(FUNC, OPT1, OPT2, OPT3) FUNC(__thiscall, OPT1, OPT2, OPT3)
#define _EMIT_VECTORCALL(FUNC, OPT1, OPT2, OPT3) FUNC(__vectorcall, OPT1, OPT2, OPT3)

#define _NON_MEMBER_CALL(FUNC, CV_OPT, REF_OPT, NOEXCEPT_OPT) \
    _EMIT_CDECL(FUNC, CV_OPT, REF_OPT, NOEXCEPT_OPT)          \
    _EMIT_CLRCALL(FUNC, CV_OPT, REF_OPT, NOEXCEPT_OPT)        \
    _EMIT_FASTCALL(FUNC, CV_OPT, REF_OPT, NOEXCEPT_OPT)       \
    _EMIT_STDCALL(FUNC, CV_OPT, REF_OPT, NOEXCEPT_OPT)        \
    _EMIT_VECTORCALL(FUNC, CV_OPT, REF_OPT, NOEXCEPT_OPT)


#define _GET_FUNCTION_IMPL(CALL_OPT, X1, X2, X3)                                                  \
    template <class _Ret, class... _Types>                                                        \
    struct _Get_function_impl<_Ret CALL_OPT(_Types...)> { /* determine type from argument list */ \
        using type = _Func_class<_Ret, _Types...>;                                                \
    };

_NON_MEMBER_CALL(_GET_FUNCTION_IMPL, X1, X2, X3)
#undef _GET_FUNCTION_IMPL


template <class _Fty>
class function : public _Get_function_impl<_Fty>::type
{

public:
	function() noexcept {}
};

