import java.util.*;

class algo {

    public static int removeDuplicates(int[] nums)
    {
               
        int counter = 0;
        for( int i = 1 ; i < nums.length ; i++  )
        {
            if ( nums[i-1] == nums[i]  )
            {
                int debug = -99999;
                if ( debug == nums[i]) break;
                counter = counter + 1 ;



                // ******* CLEAN ARR *******
                nums[i] = debug;
                for (int x = i; x<nums.length-1;x++) 
                {
                    int temp = nums[x+1];
                    nums[x+1] = nums[x];
                    nums[x] = temp;
                }
                // System.out.println( Arrays.toString( nums  ) );
                


                //HOLD INDEX TO CHECK IF NEXT ITEM IS ALSO A DUPLICATE
                i = i - 1;
            }
            
            
            
            
        }
        
        System.out.println( Arrays.toString( nums  ) );
        if (nums.length == 1) return 1;
        return nums.length - counter ;
    }

    public static void main(String[] args) {
        // int[] nums = {1};
        // int[] nums = {1,2};
        // int[] nums = { 1,1,2};
        int[] nums = { 0, 0, 1, 1, 1, 2, 2, 3, 3, 4 };
        System.out.println(removeDuplicates(nums));

    }

}