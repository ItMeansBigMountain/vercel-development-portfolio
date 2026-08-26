package genspark.assignments.section5;

import genspark.assignments.Assignment;

import java.util.ArrayList;

public class NthRowPascal implements Assignment {
    public ArrayList<Integer> solution(int nth) {


        //WHEN PLACED IN SEQUENCE, THE TRIANGLE IS ACTUALLY A PATTERN OF DOUBLE ONES....
        //ADD TWO "1" INTEGERS TO EACH ITERATION OF ROWS.
        // EACH ROW GENERATES THE "NTH-1" AMOUNT OF NUMBERS
        //EACH NEW NUMBER IS A PATTERN FALLING BACK TWO & THREE INDICES



        //INIT OUTPUT LIST
        ArrayList<Integer> row = new ArrayList<Integer>();


        //EDGE CASE MANAGEMENT
        if (nth <= 1) {
            if (nth == 1) {
                row.add(1);
                row.add(1);
                return row;
            }
            row.add(1);
            return row;
        }


        //OUTPUT STRETCH INIT
        row.add(1);
        row.add(1);
        row.add(1);
        row.add(1);


        //PATTERN INIT
        int repeat = 1;
        int go_back1 = 2;
        int go_back2 = 3;


        //FOR EVERY nth ITERATION
        for (int i = 0; i < nth - 1; i++) {

            //GENERATE ROW OBJECTS
            for (int x = 0; x < repeat; x++) {
                int sum_lol = (row.get(row.size() - go_back1)) + (row.get(row.size() - go_back2));
                row.add(sum_lol);
            }

            //ADD SECTION
            row.add(1);
            row.add(1);

            //FALL BACK PATTERN
            go_back1++;
            go_back2++;


            //NUMBER GENERATION PATTERN
            repeat++;
            System.out.println("------");
            System.out.println(  row.subList(row.size()-go_back2-1, row.size() )  );
        }


        //DEBUG
        // System.out.println(  row  );
        // System.out.println( nth  );


        //CONVERT FALLBACK SUBLIST INTO ARRAY
        ArrayList<Integer> output = new ArrayList<Integer>(row.subList(row.size() - go_back2, row.size() - 1));


        //OUTPUT
        System.out.println("__________________________");
        return output;
    }
}
