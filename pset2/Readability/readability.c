#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

//Variables definition
string text;
int letters = 0;
int words = 1;
int sentences = 0;

int main(void)
{
    text = get_string("Text:  "); //User input
    //Count how many letter
    for (int i = 0; i < strlen(text); i++)
    {
        if isalpha(text[i])
        {
            letters ++;
        }
    }
    //Count how many words
    for (int j = 0; j < strlen(text); j++)
    {
        if isspace(text[j])
        {
            words++;
        }
    }
    //Count how many sentences
    for (int k = 0; k < strlen(text); k++)
    {
        if (text[k] == '.' || text[k] == '?' || text[k] == '!')
        {
            sentences++;
        }
    }
    //Do Coleman-Liau index
    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;
    float index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index >= 16)
    {
        printf(" Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int) index);
    }
}