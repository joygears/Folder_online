#include <stdio.h>
#include "AVL.h"
#define N 6


int main() {
	bstree t = NULL;
	int h = 0;
	datatype xs[] = { 120,80,30,90,45,60 };
	for (int i = 0; i < 6; i++)
		insertAvlTree(xs[i], &t, &h);

	return 0;
}