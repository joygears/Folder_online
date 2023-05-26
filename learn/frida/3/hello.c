#include <stdio.h>
#include <Windows.h>

void
f (int n)
{
  printf ("Number: %d\n", n);
}

int
main (int argc,
      char * argv[])
{
  int i = 0;

  printf ("f() is at %p\n", f);

  while (1)
  {
    f (i++);
    Sleep (1000);
  }
}