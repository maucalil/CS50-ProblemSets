//Get user name and say hello to the user.
#include <stdio.h>
#include <cs50.h>
int main(void)
{
    string n = get_string("What's your name?");
    printf("Hello, %s\n", n) ;
}