




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




template <class>
constexpr bool _Always_false = false;

template <class _Tx>
struct _Get_function_impl {
    static_assert(_Always_false<_Tx>, "std::function does not accept non-function types as template arguments.");
};

//#define _GET_FUNCTION_IMPL(CALL_OPT, X1, X2, X3)                                                 \
    template <class _Ret, class... _Types>                                                        \
    struct _Get_function_impl<_Ret CALL_OPT(_Types...)> { /* determine type from argument list */ \
        using type = _Func_class<_Ret, _Types...>;                                                \
    };
template <class _Fty>
class functional : public _Get_function_impl<_Fty>::type
{

public:
	function() noexcept {}
};

