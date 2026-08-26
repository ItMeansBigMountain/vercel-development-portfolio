import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class mostFrequentINT {

    public static int most_frequent_int(int[] arr) {

        Map<Integer, Integer> dataMap = new HashMap<Integer, Integer>();

        for (int i = 0; i < arr.length; i++) {
            if (dataMap.containsKey(arr[i])) {
                dataMap.put(arr[i], dataMap.get(arr[i]) + 1);
            } else {
                dataMap.put(arr[i], 1);
            }
        }

        Object[] keyArr = dataMap.keySet().toArray();
        int maximum = dataMap.get(keyArr[0]);
        int output = (int) keyArr[0];
        for (var k : keyArr) {
            if (maximum < dataMap.get(k)) {
                maximum = dataMap.get(k);
                output = (int) k;
            }
        }

        System.out.println(dataMap);
        return output;
    }

    public static void main(String[] args) {

        System.out.println(most_frequent_int(new int[] { 5, 5, 2, 3, 44, 1, 4, 44, 44, 99, 1, 2 }));

    }
}
