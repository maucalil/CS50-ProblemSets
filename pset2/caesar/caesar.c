#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

bool vk(string s);

int main(int argc, string argv[])
{
    //Forcing user to colaborate
    if (argc != 2 || !vk(argv[1]))
    {
        printf("Usage: ./caesar key");
        return 1;
    }
    //Transforming the key argument into a interger
    int key = atoi(argv[1]);

    //Gettin user input for plaintext
    string pt = get_string("plaintext:  ");

    printf("ciphertext: ");

//Loop for lower and upercase letters
    for (int i = 0, len = strlen(pt); i < len; i++)
    {
        char c = pt[i];
        if (isalpha(c))
        {
            char m = 'A';
            if (islower(c))
            {
                m = 'a';
            }
            //Using Caesar's algorithm
            printf("%c", (c - m + key) % 26 + m);
        }
        else
        {
            //Printing other characters besides letters
            printf("%c", c);
        }
    }
    printf("\n");
    return 0;
}

//Verify key loop
bool vk(string s)
{
    for (int i = 0, len = strlen(s); i < len; i++)

        if (!isdigit(s[i]))
        {
            return false;
        }
    return true;
}