#include<stdio.h>
#include<conio.h>
FILE * pFile;
// Program by Thawatchai Chomsiri and Wiwat Sriphum
void xputch(char ch)
{
	/*
	if(ch==('A'^'1')) {
		putch('E');
	} else {
		if(ch==('M'^'5')) {
			putch('F');
		} else {
			if(ch==('Z'^'9')) {
				putch('G');
			} else {
				putch(ch);
			}
		}
	}
	*/
	if(ch==('A'^'1')) {
		//putch('7');
		fprintf(pFile, "C0 ");
	} else {
		if(ch==('M'^'5')) {
			//putch('8');
			fprintf(pFile, "C1 ");
		} else {
			if(ch==('Z'^'9')) {
				//putch('9');
				fprintf(pFile, "C2 ");
			} else {
				if(ch=='A') fprintf(pFile, "A0 "); //putch('1');
				if(ch=='M') fprintf(pFile, "A1 "); //putch('2');
				if(ch=='Z') fprintf(pFile, "A2 "); //putch('3');
				if(ch=='1') fprintf(pFile, "B0 "); //putch('4');
				if(ch=='5') fprintf(pFile, "B1 "); //putch('5');
				if(ch=='9') fprintf(pFile, "B2 "); //putch('6');

			}
		}
	}


	return;
}

int in_row(char c) {
  if((c=='A')||(c=='1')||(c==('A'^'1'))) return 0;
  if((c=='M')||(c=='5')||(c==('M'^'5'))) return 1;
  if((c=='Z')||(c=='9')||(c==('Z'^'9'))) return 2;

  return 0;
}

int three_char_not_repeat(char c1, char c2, char c3) {
  int row_count[3];
  row_count[0] = 0;
  row_count[1] = 0;
  row_count[2] = 0;

  row_count[in_row(c1)]++;
  row_count[in_row(c2)]++;
  row_count[in_row(c3)]++;

  if((row_count[0]>1)||(row_count[1]>1)||(row_count[2]>1)) {
    return 0; // repeat
  } else {
    return 1; // 1 = TRUE = not repaet
  }
}

void main()
{
	unsigned long count=0, count_not_repeat=0;
	int x, y, i, j, r0, r1, r2, r3, r4, r5, r6, r7, r8;
	char cube[3][3];
	char line_org[9], line[9];
	int can_recov=0;
	char three_char[3];
	pFile = fopen("DR_Code.txt","w");


	line_org[0] = cube[0][0] = 'A';
	line_org[1] = cube[0][1] = 'M';
	line_org[2] = cube[0][2] = 'Z';
	line_org[3] = cube[1][0] = '1';
	line_org[4] = cube[1][1] = '5';
	line_org[5] = cube[1][2] = '9';
	line_org[6] = cube[2][0] = cube[0][0] ^ cube[1][0];
	line_org[7] = cube[2][1] = cube[0][1] ^ cube[1][1];
	line_org[8] = cube[2][2] = cube[0][2] ^ cube[1][2];

	for(i=0; i<9; i++) {
		line[i]=line_org[i];
	}



	clrscr();
	//printf("Hello\n");
	//xputch(cube[0][0]); xputch(cube[1][0]); xputch(cube[2][0]); printf("\n");
	//xputch(cube[0][1]); xputch(cube[1][1]); xputch(cube[2][1]); printf("\n");
	//xputch(cube[0][2]); xputch(cube[1][2]); xputch(cube[2][2]); printf("\n");

	count=1;
	count_not_repeat=1;
	for(r0=0; r0<9; r0++) {
	 for(r1=0; r1<9; r1++) {
	  if(r1!=r0) {
	   for(r2=0; r2<9; r2++) {
	    if((r2!=r1)&&(r2!=r0)) {
	      for(r3=0; r3<9; r3++) {
	       if((r3!=r2)&&(r3!=r1)&&(r3!=r0)) {
		for(r4=0; r4<9; r4++) {
		 if((r4!=r3)&&(r4!=r2)&&(r4!=r1)&&(r4!=r0)) {
		  for(r5=0; r5<9; r5++) {
		   if((r5!=r4)&&(r5!=r3)&&(r5!=r2)&&(r5!=r1)&&(r5!=r0)) {
		    for(r6=0; r6<9; r6++) {
		     if((r6!=r5)&&(r6!=r4)&&(r6!=r3)&&(r6!=r2)&&(r6!=r1)&&(r6!=r0)) {
		      for(r7=0; r7<9; r7++) {
		       if((r7!=r6)&&(r7!=r5)&&(r7!=r4)&&(r7!=r3)&&(r7!=r2)&&(r7!=r1)&&(r7!=r0)) {
			for(r8=0; r8<9; r8++) {
			 if((r8!=r7)&&(r8!=r6)&&(r8!=r5)&&(r8!=r4)&&(r8!=r3)&&(r8!=r2)&&(r8!=r1)&&(r8!=r0)) {

		//================
		//printf("r0=%d,r1=%d,r2=%d,r3=%d,r4=%d,r5=%d,r6=%d,r7=%d,r8=%d, ", r0, r1, r2, r3, r4, r5, r6, r7, r8);
		//printf("count=%lu, count_nr=%lu \n", count, count_not_repeat);

		line[0] = line_org[r0]; line[1] = line_org[r1]; line[2] = line_org[r2];
		line[3] = line_org[r3]; line[4] = line_org[r4]; line[5] = line_org[r5];
		line[6] = line_org[r6]; line[7] = line_org[r7]; line[8] = line_org[r8];
		can_recov=0;
		//check row1
		three_char[0] = line[0]; three_char[1] = line[3]; three_char[2] = line[6];
		can_recov=three_char_not_repeat(three_char[0], three_char[1], three_char[2]);
		if(can_recov==1) {
		  //check row2
		  three_char[0] = line[1]; three_char[1] = line[4]; three_char[2] = line[7];
		  can_recov=three_char_not_repeat(three_char[0], three_char[1], three_char[2]);
		  if(can_recov==1) {
		    //check row3
		    three_char[0] = line[2]; three_char[1] = line[5]; three_char[2] = line[8];
		    can_recov=three_char_not_repeat(three_char[0], three_char[1], three_char[2]);
		    if(can_recov) {
		      //check col1
		      three_char[0] = line[0]; three_char[1] = line[1]; three_char[2] = line[2];
		      can_recov=three_char_not_repeat(three_char[0], three_char[1], three_char[2]);
		      if(can_recov==1) {
			//check col2
			three_char[0] = line[3]; three_char[1] = line[4]; three_char[2] = line[5];
			can_recov=three_char_not_repeat(three_char[0], three_char[1], three_char[2]);
			if(can_recov==1) {
			  //check col3
			  three_char[0] = line[6]; three_char[1] = line[7]; three_char[2] = line[8];
			  can_recov=three_char_not_repeat(three_char[0], three_char[1], three_char[2]);

		//------------
		if(can_recov==1) {// not repeat
		  xputch(line[0]); xputch(line[3]); xputch(line[6]); fprintf(pFile, "\n");
		  xputch(line[1]); xputch(line[4]); xputch(line[7]); fprintf(pFile, "\n");
		  xputch(line[2]); xputch(line[5]); xputch(line[8]); fprintf(pFile, "\n");


		  fprintf(pFile, "r0=%d,r1=%d,r2=%d,r3=%d,r4=%d,r5=%d,r6=%d,r7=%d,r8=%d, ", r0, r1, r2, r3, r4, r5, r6, r7, r8);
		  fprintf(pFile, "count=%lu, count_nr=%lu \n", count, count_not_repeat);
		  //printf("Press any key .....(ESC=exit)...\n");
		  //if(getch()==27) return;
		  count++;
		}
		//-------------

		  }
		}
		count_not_repeat++;
		//================



			   }
			  }
			 }
			}
		       }
	     //printf("Press any key .....(ESC=exit)...\n");
	     //if(getch()==27) return;

		      }
		     }
	     //printf("Press any key .....(ESC=exit)...\n");
	     //if(getch()==27) return;

		    }
		   }
	     //printf("Press any key .....(ESC=exit)...\n");
	     //if(getch()==27) return;

		  }
		 }
	     //printf("Press any key .....(ESC=exit)...\n");
	     //if(getch()==27) return;

		}
	       }
	     //printf("Press any key .....(ESC=exit)...\n");
	     //if(getch()==27) return;

	      }
	     }
	     //printf("Press any key .....(ESC=exit)...\n");
	     //if(getch()==27) return;

	    }
	   }
	   //printf("Press any key .....(ESC=exit)...\n");
	   //if(getch()==27) return;
	  }
	 }
	 //printf("Press any key .....(ESC=exit)...\n");
	 //if(getch()==27) return;
	}
	fclose(pFile);
	printf("## OK ## -- Press any key .....(ESC=exit)...\n");
	getch();
	return;


}