


namespace my {
	template<class Fx>
	class function {

	};
	template <class _Ret, class... _Types>
	class Func_base {
	public:
		virtual _Ret call(_Types... args) = 0;
	};
	template <class Fx,class _Ret, class... _Types>
	class Func_impl_no_alloc: public Func_base<_Ret, _Types...> {
	public:
		Func_impl_no_alloc(Fx fn) {
			caller = fn;
		}
		virtual _Ret call(_Types... args) {
			return caller(args...);
		}
		Fx caller;
	};
	template <class _Ret, class... _Types>
	class function<_Ret (_Types...)> {
	public:
		template<class Fx>
		void operator=(Fx fn) {
			storage[9]= new (static_cast<void*>(storage)) Func_impl_no_alloc<Fx, _Ret, _Types...>(fn);
		}
		_Ret operator()(_Types... args) {
			return storage[9]->call(args...);
		}
	public:
		Func_base<_Ret, _Types...> * storage[10];
	};

	
}