#include <stdio.h>
#include <stdlib.h>

#include "AVL.h"

void lchange(bstree *t){
	bstree p1,p2;
	p1 = (*t)->lchild;
	if(p1->bal==1){

		(*t)->lchild=p1->rchild;
		p1->rchild=*t;
		(*t)->bal=0;
		(*t)=p1;
	}
	else{

		p2 = p1->rchild;
		p1->rchild=p2->lchild;
		p2->lchild = p1;
		(*t)->lchild = p2->rchild;
		p2->rchild = *t;
		if(p2->bal==1){(*t)->bal=-1; p1->bal=0;}
		else {(*t)->bal = 0; p1->bal=1;}
		(*t) = p2;
	}

	(*t)->bal = 0;


}

void rchange(bstree *t){
	bstree p1,p2;
	p1 = (*t)->rchild;
	if(p1->bal==-1){
		(*t)->rchild = p1->lchild;
		p1->lchild = *t;
		(*t)->bal = 0;
		(*t) = p1;
	}
	else{
		p2=p1->lchild;
		p1->lchild=p2->rchild;
		p2->rchild=p1;
		(*t)->rchild=p2->lchild;
		p2->lchild=(*t);
		if(p2->bal==-1)	{(*t)->bal=1;p1->bal=0;}
		else	{(*t)->bal=0;p1->bal=-1;}
		(*t) = p2;
	}
	(*t)->bal=0;
}

void insertAvlTree(datatype x,bstree *t,int * h){
	if(*t == NULL)
	{
		
		*t=(bstree)malloc(sizeof(bsnode));
		(*t)->key=x;
		(*t)->bal=0;
		*h = 1;
		(*t)->lchild=(*t)->rchild=NULL;
	}
	else{

		if(x<(*t)->key){
			insertAvlTree(x,&(*t)->lchild,h);
			if(*h)
				switch( (*t)->bal){
					case -1:{ (*t)->bal=0;*h=0; break;}
					case 0 :{(*t)->bal=1; break;}
					case 1:{
						lchange(t);
						*h=0;
						break;
					}
				}
		}
		else if(x >(*t)->key){
			insertAvlTree(x,&(*t)->rchild,h);
			if(*h)
				switch( (*t)->bal){
					case 1:{ (*t)->bal=0;*h=0; break;}
					case 0 :{(*t)->bal=-1; break;}
					case -1:{
						rchange(t);
						*h=0;
						break;
					}
				}
		}
		else
			*h = 0;
	}
	

}