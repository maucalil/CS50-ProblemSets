// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"



// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //Hash a word
    int key = hash(word);

    //Set cursor to point the same as hashtable
    node *cursor = table[key];
    //Check if word exist in dictionary
    while(cursor != NULL)
    {
        if(strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int value = 0;

    for(int i = 0; word[i] != '\0'; i++)
    {
        value += tolower(word[i]);
    }
    return value % N;
}

//Initialize a counter to words in dictionary
int words = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //Open dictionary and checks if everything is ok
    FILE *dfile = fopen(dictionary, "r");
    if (dfile == NULL)
    {
        return false;
    }
    for(int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    //Defines word length
    char word[LENGTH+1];

    //Read the file
    while(fscanf(dfile, "%s", word) != EOF)
    {
        //Define each word the need of memory and check if malloc succeeded
        node *n = malloc(sizeof(node));
        if(n == NULL)
        {
            unload();
            return false;
        }
        //Copies word into new_node
        strcpy(n->word, word);

        //Hash word
        int index = hash(word);

        //Check if there's already a word in the hash
        if(table[index] == NULL)
        {
            n->next = NULL;
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        words++;
    }
    fclose(dfile);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}
// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //Iterate through hash
    for(int i = 0; i < N; i++)
    {
        //Set cursor to point the same as hashtable
        node *cursor = table[i];

        while(cursor != NULL)
        {
            node* tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }

        table[i] = NULL;
    }
    return true;
}