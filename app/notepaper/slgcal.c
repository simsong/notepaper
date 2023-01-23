/*
 * This program prints the calendar for the current month.
 * Although there are a lot of calendar programs out there, they are all
 * incredibly gross. This one is designed to have a simple implementation
 * that's based on the localtime() function. 
 *
 * It's written in C, but designed to be easily portable to other languages.
 */

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

const char *months[]={"January","February","March","April","May","June","July",
		     "August","September","October","November","December"};

const char width=21;			/* width of each line */

void cal(int year,int month,char lines[8][30])
{
    int i;
    struct tm tm;
    int current_line = 0;

    for(i=0;i<8;i++){
	memset(lines[i],' ',width);
	lines[i][width] = 0;
    }
    if(month<1 || month>12) return;
    memset(&tm,0,sizeof(tm));

    tm.tm_year = year-1900;
    tm.tm_mon = month-1;
    tm.tm_mday = 1;			/* start on the first */

    strcpy(lines[0]+(width-strlen(months[tm.tm_mon]))/2,months[tm.tm_mon]);
    strcpy(lines[1]," S  M Tu  W Th  F  S");

    /* Now fill in each day into the calendar */
    current_line = 2;			/* where we start */
    do {
	char buf[4];			/* date buffer */

	time_t t = mktime(&tm);		/* get the time_t for now */
	tm = *(localtime(&t));		/* this will fill in the fields */
	sprintf(buf,"%2d",tm.tm_mday);	/* gets a printable representation */
	memcpy(lines[current_line]+3*tm.tm_wday,buf,2); /* copy in the number */
	
	if(tm.tm_wday==6) current_line++; /* we just did sat, go to sun */
	t+=60*60*24;			/* go to the next day */
	tm = *(localtime(&t));		/* get it back out */
    } while(tm.tm_mon == month-1);	/* until we advance to the next month */
}

main(int argc,char **argv)
{
    int i;
    char lines[8][30];

    cal(2004,5,lines);
    for(i=0;i<8;i++){
	puts(lines[i]);
    }
}
