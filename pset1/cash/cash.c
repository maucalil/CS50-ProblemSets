#include <cs50.h>
#include <stdio.h>
#include <math.h>

float change;
int cents;
int coins = 0;
//Calculate how many coins are needed for a change prompted by the user
//Coins avaiables are quarters (25¢); dimes (10¢); nickels (5¢) and pennies (1¢)


int main(void)
{
    //Get the user input for change owed
    do
    {
        change = get_float("Change owed:");
        cents = round(change * 100);
    }
    while (cents < 0);

    //Calculate how many quartes fits
    while (cents / 25 > 0)
    {
        coins++;
        cents = cents - 25;
    }

    //Calculate how many dimes fits
    while (cents / 10 > 0)
    {
        coins++;
        cents = cents - 10;
    }

    //Calculate how many dimes fits
    while (cents / 5 > 0)
    {
        coins++;
        cents = cents - 5;
    }

    //Calculate how many pennies fits
    while (cents / 1 > 0)
    {
        coins++;
        cents = cents - 1;
    }
    printf("%i\n", coins);

}
