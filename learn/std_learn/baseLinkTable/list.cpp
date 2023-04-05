#include <iostream>
#include <stdexcept>

using namespace std;

template<class T>class list{


public:
	list():m_header(nullptr),m_tail(nullptr){}
	list(list<T> const& that):m_header(nullptr),m_tail(nullptr){

		for(node * pnode = that.m_header;pnode;pnode=pnode->m-next){
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

		if(empty())
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

	node * m_header;
	node * m_tail;
	friend ostream& operator<<(ostream& os,list<int>& l);
};

ostream& operator<<(ostream& os,list<int>& l){

	for(list<int>::node * pnode = l.m_header;pnode;pnode=pnode->m_next){
		os << pnode->m_data << " ";
	}
	return os;
}
int main(){
	list<int> m;
	m.push_back(1);
	m.push_back(2);
	m.push_back(3);
	
	cout << m;

	return 0;
}