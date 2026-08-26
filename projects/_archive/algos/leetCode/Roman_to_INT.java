package finishedAlgos;
import java.util.*;

class Roman_to_INT {

    public static int romanToInt(String s) {

        // data set
        Character[] symbols = { 'I', 'V', 'X', 'L', 'C', 'D', 'M', };
        int[] values = { 1, 5, 10, 50, 100, 500, 1000 };
        HashMap<Character, Integer> map = new HashMap<>();
        for (int i = 0; i < symbols.length; i++) {
            map.put(symbols[i], values[i]);
        }

        // run through string.... if previous is less than current... minus the previous

        int output = 0;
        for (int i = 0; i < s.length() ; i++) {
            int current = map.get(s.charAt(i));
            output = output + current;

            if (i > 0)
            {
                int previous = map.get(s.charAt(i-1));
                if (previous < current)
                {
                    output = output - (previous * 2);
                }
            }
        }

        return output;

    }

    public static void main(String[] args) {
        
        System.out.println(romanToInt("MCMXCIV")); /// 1994
        // System.out.println(romanToInt("LVIII")); /// 58
        // System.out.println(romanToInt("XLI")); /// 41
        // System.out.println(romanToInt("IV")); /// 4
        // System.out.println(romanToInt("III")); /// 3
    }

}