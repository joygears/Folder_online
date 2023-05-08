typedef int datatype;
typedef struct node{
	datatype key;
	struct node * lchild,*rchild;
	int bal;
} bsnode;

typedef bsnode * bstree;


void lchange(bstree* t);
void rchange(bstree* t);
void insertAvlTree(datatype x, bstree* t, int* h);
