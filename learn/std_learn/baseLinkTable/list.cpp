#include <iostream>
#include <stdexcept>

using namespace std;

template<class T>class list{


public:
	list():m_header(nullptr),m_tail(nullptr){}
	list(list<T> const& that):m_header(nullptr),m_tail(nullptr){

		for(node * pnode = that.m_header;pnode;pnode=pnode->m_next){
			this->push_back(pnode->m_data);
		}

	}
	~list(){
		clear(); 
	}
	//
	//	链表判空
	//
	bool empty(){
		return m_header == nullptr &&  m_tail == nullptr;
	}
	//
	//	添加头节点
	//
	void push_front(T const& data){
		m_header = new node(nullptr,data,m_header);
		if(m_header->m_next)
			m_header->m_next->m_prev = m_head;
		else
			m_tail = m_header 
	}
	//
	//	删除 头节点
	//
	void pop_front(){
			if(empty()){
				return;
			}
			node * temp = m_header;
			m_header = m_header->m_next;
			delete temp;
			if(!m_header){
				m_tail = m_header;
				return;
			}

			m_header->m_prev = nullptr;

	}
	//
	//	获取头节点的元素
	//
	T& front(){
		if(empty())
			throw underflow_error("null node");
		return m_header->m_data;
	}
	T const& front() const{
		return const_cast<list *>(this)->front();
	}
	//
	// 添加尾节点
	//
	void push_back(T const& data){
	
		m_tail  = new node(m_tail,data,nullptr);

		if(!m_tail->m_prev)
			m_header=m_tail;
		else
			m_tail->m_prev->m_next = m_tail;


	}
	//
	//	删除 尾节点
	//
	void pop_back(){
		if(empty()){
			return;
		}
		
		if(m_tail->m_prev){
				//两个节点及以上
			m_tail = m_tail->m_prev;
			delete m_tail->m_next;
			m_tail->m_next = nullptr;
		}
		else{
				// 只有一个节点
				delete m_tail;
				m_header = m_tail = nullptr;
		}
		
	}
	//
	//	获取尾节点的元素
	//
	T& back(){
		if(empty())
			throw underflow_error("null node");
		return m_tail->m_data;
	}
	T const& back() const{
			return const_cast<list *>(this)->back();
	}


	//
	//	清空列表
	//
	void clear(){
		// if(empty())
		// 	return;

		// while(m_header != nullptr){
		// 	node * pnode = m_header;
		// 	m_header = m_header->m_next;
		// 	delete pnode;
		// }
		// m_tail = nullptr;
		while(!empty())
			pop_front();
	}
	//
	//	获取链表的大小
	//
	size_t size(){
		size_t count = 0;
		node * pnode = m_header;
		while(pnode != nullptr){
			
			pnode = pnode->m_next;
			count++;
		}
		return count;
	}


private:
	class node{
	public:
		node(node * prev,T const& data,node * next):m_prev(prev),m_data(data),m_next(next){}
		public:
			node * m_prev;
			T m_data;
			node * m_next;
	};
public:
	//
	//	迭代类
	//
	class iterator{
	public:
		iterator(node * start,node * cur,node * end):m_start(start),m_cur(cur),m_end(end){}
		T& operator*(){
			if(m_cur == nullptr)
				throw underflow_error("null node");
			return m_cur->m_data;
		}

		iterator& operator++(){
			if(m_cur)
				m_cur=m_cur->m_next;
			else
				m_cur = m_start;
			return *this;
		}

		iterator operator++(int){
			iterator temp(*this);
			if(m_cur)
				m_cur=m_cur->m_next;
			else
				m_cur = m_start;
			return temp;
		}

		iterator& operator--(){
			if(m_cur)
				m_cur=m_cur->m_prev;
			else
				m_cur = m_end;
			return *this;
		}
		bool operator==(iterator & that) {

				return m_start==that.m_start && m_cur == that.m_cur && m_end == that.m_end;
		}

		bool operator!=(iterator & that){

			return !(*this == that);
		}
	private:
		node * m_start;
		node * m_cur;
		node * m_end;
		// friend void list<T>::insert(iterator &it,const T& data);
		// friend void list<T>::erase(iterator& it);
		friend class list<T>;
	};

	iterator begin(){

		return iterator(m_header,m_header,m_tail);
	}

	iterator end(){
		return iterator(m_header,nullptr,m_tail);
	}

	void insert(iterator &it,const T& data){
			if(it == end()){
				push_back(data);
			}
			else{
				node * pnode = new node(it.m_cur->m_prev,data,it.m_cur);
				
				it.m_cur->m_prev = pnode;
				if(pnode->m_prev)
					pnode->m_prev->m_next = pnode;
				else
					m_header = pnode;
			}

	}
	void erase(iterator& it){
		if(it == end()){
			return;
		}
		if(it.m_cur->m_prev)
			it.m_cur->m_prev->m_next = it.m_cur->m_next;
		else
			m_header = it.m_cur->m_next;
		if(it.m_cur->m_next)
			it.m_cur->m_next->m_prev = it.m_cur->m_prev;
		else
			m_tail = it.m_cur->m_prev;

		delete it.m_cur;
	}

public:
	class const_iterator{
	public:
		const_iterator(iterator &it):m_it(it){}
		T operator*(){
			return *m_it;
		}
		const_iterator& operator--(){
			--m_it;
			return *this;
		}
		const_iterator& operator++(){
			++m_it;
			return *this;
		}
		bool operator==(const_iterator & that){

			return m_it==that.m_it;
		}
		bool operator!=(const_iterator & that){

			return m_it!=that.m_it;
		}
	private:
		iterator m_it;
	};

	const_iterator begin() const{

			return const_iterator(const_cast<list *>(this)->begin());
		}

	const_iterator end() const{
		return const_iterator(const_cast<list *>(this)->end());
	}


private:
	node * m_header;
	node * m_tail;
	//friend ostream& operator<<(ostream& os,list<int>& l);
};

template<class IT,class T> 
IT myfind(IT& a,IT& b,T data){
	for(IT t=a;t!=b;t++){
		if(*t==data)
			return t;
	}
	return b;
}
template<class IT>
void sort(IT &begin,IT &end){
	IT p=begin,i=begin,j=--end;
	while(i!=j){
		if(*p==*i){
			if(*p < *j)
				--j;
			else{
				swap(*p,*j);
				p = j;
				++i;
			}
		}
		else{
			if(*i< *p)
				++i;
			else{
				swap(*p,*i);
				p = i;
				--j;
			}

		}

	}
	IT it=begin;
	++it;
	if(p!=begin && p!=it)
		sort(begin,p);
	it = p;
	++it;
	if(it!=--end && it!=end)
		sort(it,end);
}

// ostream& operator<<(ostream& os,list<int>& l){

// 	for(list<int>::node * pnode = l.m_header;pnode;pnode=pnode->m_next){
// 		os << pnode->m_data << " ";
// 	}
// 	return os;
// }

int main(){
	list<int> m;
	m.push_back(22);
	m.push_back(1);
	m.push_back(3);
	// list<int>::iterator it_ = m.begin();
	// m.insert(it_,0);
	// list<int>::iterator target =  m.begin();

	// for(list<int>::iterator it = m.begin();it != m.end();  ){
	// 		 target = it++;
	// }
	// m.erase(target);
	// list<int>::iterator it = myfind(m.begin(),m.end(),2);
	// m.erase(it);
	sort(m.begin(),m.end());
	for(list<int>::iterator it = m.begin();it != m.end(); it++ ){

		cout << *it << endl;
	}
	// const list<int> n = m;

	// for(list<int>::const_iterator it = n.begin();it != n.end(); ++it){
	// 	cout << *it << endl;
	// }
	

	return 0;
}