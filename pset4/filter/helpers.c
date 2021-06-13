#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Get each cor values
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;

            //Find average and round it
            float avg = (round(red) + round(green) + round(blue)) / 3;
            avg = round(avg);

            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = (sepiaRed > 255) ? 255 : sepiaRed;
            image[i][j].rgbtGreen = (sepiaGreen > 255) ? 255 : sepiaGreen;
            image[i][j].rgbtBlue = (sepiaBlue > 255) ? 255 : sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Make a new image identical to the original image to work on it
    RGBTRIPLE newimage[height][width];

    //Goes over each row and column of the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            newimage[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Defines the sum of each color and sorround pixels count
            float sr = 0;
            float sg = 0;
            float sb = 0;
            int spc = 0;

            for (int k = -1; k < 2; k++) // checks each pixel within -1 to + 1 of each [i] left-right
            {
                for (int l = -1; l < 2; l++) // checks each pixel within -1 to + 1 of each [j] up-down
                {
                    if (i + k >= 0 && j + l >= 0 && i + k < height && j + l < width) //Make sure that the pixel are not going out of the image
                    {
                        //Sum each color to make it totals on the 2D array
                        sr = newimage[i + k][j + l].rgbtRed + sr;
                        sg = newimage[i + k][j + l].rgbtGreen + sg;
                        sb = newimage[i + k][j + l].rgbtBlue + sb;
                        spc++;
                    }
                }
            }
            //Copy the blurred pixel into the orignal image
            image[i][j].rgbtRed = round(sr / spc);
            image[i][j].rgbtGreen = round(sg / spc);
            image[i][j].rgbtBlue = round(sb / spc);
        }
    }
    return;
}
