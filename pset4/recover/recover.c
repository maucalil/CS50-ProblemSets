#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Open file
    FILE *file = fopen(argv[1], "r");

    //Chek if the user prompted correct
    if (argc != 2)
    {
        printf("Usage: ./recover ImageName");
        return 1;
        exit(1);
    }
    else if (!file)
    {
        printf("File not found\n");
        return 1;
        exit(1);
    }
    else
    {

        BYTE *buffer = malloc(512);
        //Jpeg counter
        int jpeg_count = 0;

        int writing = 0;
        //Jpeg names
        char *jpegName = malloc(8);
        //File for jpegs
        FILE *image = NULL;

        while (fread(buffer, 512, 1, file) && !feof(file))
        {
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                //Check if it's the first jpeg
                if (jpeg_count == 0)
                {
                    sprintf(jpegName, "%03i.jpg", jpeg_count);
                    image = fopen(jpegName, "w");
                    fwrite(buffer, 512, 1, image);
                    jpeg_count++;
                    writing = 1;
                }
                //Do the same for other jpegs
                else
                {
                    fclose(image);
                    sprintf(jpegName, "%03i.jpg", jpeg_count);
                    image = fopen(jpegName, "w");
                    fwrite(buffer, 512, 1, image);
                    jpeg_count++;
                }
            }
            //Continue writing in the previous file if the block isn't a jpeg
            else if (writing)
            {
                fwrite(buffer, 512, 1, image);
            }
        }
        //Closing remaining files
        fclose(file);
        fclose(image);
        free(buffer);
        free(jpegName);
        return 0;
    }
}
