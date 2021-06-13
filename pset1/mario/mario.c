#include <cs50.h>
#include <stdio.h>

int main(void)
{
//Define the pyramide height with the user input
    int h;
    do
    {
        h = get_int("Height:");
    }
    while (h < 1 || h > 8);
    for (int i = 1; i <= h; i++)
    {
        //Instruction for space to form right pyramid
        for (int s = 1; s <= h - i; s++)
        {
            printf(" ");
        }
        //Instruction for right pyramid - blocks
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        //Instruction for space between pyramids
        for (int sp = 1; sp < 2; sp++)
        {
            printf("  ");
        }
        //Instructions for the left pyramid
        for (int lp = 1; lp <= i; lp++)
        {
            printf("#");
        }
        printf("\n");
    }
}
